from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from .logic import run_simulation_and_prediction

app = FastAPI(title="GenoPredict API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            req.family_history
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount frontend static files
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
