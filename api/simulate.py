from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import numpy as np
import random
import pickle
import os

app = FastAPI(title="GenoPredict API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model path — relative to project root (where vercel deploys from)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "alzheimer_rf_model.pkl")

_model = None

def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(f"Model file not found at: {os.path.abspath(MODEL_PATH)}")
        try:
            with open(MODEL_PATH, "rb") as f:
                _model = pickle.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load model (possible version mismatch): {e}")
    return _model


def get_allele_indices(gt_str):
    """Returns list of indices like [0, 1]"""
    if pd.isna(gt_str):
        return [0, 0]
    gt_str = str(gt_str)
    sep = '|' if '|' in gt_str else '/'
    try:
        return [int(x) for x in gt_str.split(sep)]
    except Exception:
        return [0, 0]


def run_simulation_and_prediction(
    father_data: list,
    mother_data: list,
    age: int,
    sex_opts: list,
    family_history: int,
    n: int = 1000,
):
    father_df = pd.DataFrame(father_data)
    mother_df = pd.DataFrame(mother_data)

    snps = ['rs429358', 'rs7412', 'rs3851179']

    p_alleles = {}
    for rs in snps:
        f_row = father_df[father_df['rsID'] == rs] if 'rsID' in father_df.columns else pd.DataFrame()
        m_row = mother_df[mother_df['rsID'] == rs] if 'rsID' in mother_df.columns else pd.DataFrame()

        f_idx = [0, 0]
        if not f_row.empty:
            f_idx = get_allele_indices(f_row.iloc[0]['GT'])

        m_idx = [0, 0]
        if not m_row.empty:
            m_idx = get_allele_indices(m_row.iloc[0]['GT'])

        p_alleles[rs] = (f_idx, m_idx)

    sim_data = []
    for _ in range(n):
        child = {}
        for rs in snps:
            f_idx, m_idx = p_alleles[rs]
            f_a = random.choice(f_idx)
            m_a = random.choice(m_idx)
            child[rs] = f_a + m_a
        sim_data.append(child)

    sim_df = pd.DataFrame(sim_data)
    sim_df['Age'] = age
    sim_df['FamilyHistory'] = family_history
    sim_df['Sex'] = np.random.choice(sex_opts, size=len(sim_df))

    model = load_model()
    if not model:
        raise Exception("Model not found. Ensure alzheimer_rf_model.pkl is present.")

    feature_order = ['Age', 'Sex', 'FamilyHistory', 'rs429358', 'rs7412', 'rs3851179']
    X = sim_df[feature_order]

    probs = model.predict_proba(X)
    sim_df['Risk_Score'] = probs[:, 1]

    global_score = float(sim_df['Risk_Score'].mean() * 100)
    high_risk_count = int((sim_df['Risk_Score'] > 0.5).sum())
    p_apoe = float((sim_df['rs429358'] == 2).mean() * 100)
    p_picalm = float((sim_df['rs3851179'] == 2).mean() * 100)

    hist, bin_edges = np.histogram(sim_df['Risk_Score'], bins=30, range=(0, 1))

    return {
        "global_score": global_score,
        "high_risk_count": high_risk_count,
        "n_simulations": n,
        "p_apoe_cc": p_apoe,
        "p_picalm_cc": p_picalm,
        "histogram": {
            "counts": hist.tolist(),
            "bins": bin_edges[:-1].tolist(),
        },
    }


class SimulationRequest(BaseModel):
    father_data: List[Dict[str, Any]]
    mother_data: List[Dict[str, Any]]
    age: int
    sex_opts: List[int]
    family_history: int


@app.post("/api/simulate")
async def simulate(req: SimulationRequest):
    try:
        results = run_simulation_and_prediction(
            req.father_data,
            req.mother_data,
            req.age,
            req.sex_opts,
            req.family_history,
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Vercel handler — exposes the ASGI app
handler = app
