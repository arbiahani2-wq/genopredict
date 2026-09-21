<div align="center">

# 🧬 GenoPredict AD

### Polygenic Risk Prediction for Alzheimer's Disease

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**GenoPredict AD** is an AI-powered bioinformatics web application that estimates the polygenic risk of transmitting Alzheimer's disease to future offspring. It combines Mendelian inheritance simulation with a trained Random Forest model to deliver probabilistic risk assessments from parental genomic data.

[**Live Demo →**](https://genopredict.vercel.app) &nbsp;|&nbsp; [**API Docs →**](https://genopredict.vercel.app/docs) &nbsp;|&nbsp; [**Report an Issue →**](https://github.com/arbiahani2-wq/GenoPredict-/issues)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧬 **Genomic Import** | Upload parental VCF-style CSV files with key Alzheimer's SNP markers |
| 🎲 **Mendelian Simulation** | Simulates 1,000 offspring genotypes using probabilistic allele inheritance |
| 🤖 **ML Risk Scoring** | Random Forest model trained on synthetic genomic + clinical data |
| 📊 **Rich Visualizations** | Animated gauge, risk histogram, and per-SNP probability breakdowns |
| 🔒 **Privacy First** | All computation happens locally — no genomic data ever leaves your device |
| 📁 **Demo Mode** | One-click load of example parental genotype files to explore immediately |

---

## 🖼️ Interface Overview

The app is structured as a guided 4-step workflow:

```
Step 1: Welcome       →  Step 2: DNA Import      →  Step 3: Clinical Params  →  Step 4: Results
Intro & context          Upload father/mother CSV    Age, sex, family history    Charts & risk level
```

---

## 🔬 Scientific Background

GenoPredict AD analyzes three key SNPs associated with Alzheimer's disease risk:

| SNP | Gene | Role |
|-----|------|------|
| `rs429358` | **APOE** | Strongest genetic risk factor for late-onset AD |
| `rs7412` | **APOE** | Defines APOE ε2/ε3/ε4 haplotype in combination with rs429358 |
| `rs3851179` | **PICALM** | Affects amyloid precursor protein trafficking |

The model also incorporates clinical variables: **age**, **biological sex**, and **family history of AD**.

---

## 🏗️ Architecture

```
genopredict/
│
├── api/                        # Vercel serverless function
│   └── simulate.py             # FastAPI app (ASGI handler)
│
├── backend/                    # Local server module
│   ├── api.py                  # FastAPI app (serves static frontend)
│   └── logic.py                # Simulation & prediction logic
│
├── frontend/                   # Static web client
│   ├── index.html              # 4-step app UI (681 lines)
│   ├── styles.css              # Design system & animations
│   ├── app.js                  # State management & Chart.js charts
│   └── demo_data/              # Sample parental genotype CSVs
│       ├── father_genotype.csv
│       └── mother_genotype.csv
│
├── research/                   # Data generation & model training
│   ├── generate_training_data.py
│   ├── train_model.py
│   ├── simulate_heredity.py
│   ├── extract_snps.py
│   └── synthetic_training_data.csv
│
├── alzheimer_rf_model.pkl      # Pre-trained Random Forest model (~3MB)
├── vercel.json                 # Vercel deployment configuration
├── render.yaml                 # Render.com deployment configuration
├── Dockerfile                  # Docker / Hugging Face Spaces container
└── requirements.txt            # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/arbiahani2-wq/GenoPredict-.git
cd GenoPredict-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the development server
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload
```

Then open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

> **Windows users**: Double-click `start_app.bat` to launch automatically.

---

## 📂 Input File Format

GenoPredict expects CSV files with the following structure:

```csv
rsID,Chrom,Pos,REF,ALT,GT
rs429358,19,44908684,T,C,0/1
rs7412,19,44908822,C,T,0/0
rs3851179,11,85868640,A,C,0/1
```

| Column | Description |
|--------|-------------|
| `rsID` | SNP identifier (e.g. `rs429358`) |
| `Chrom` | Chromosome number |
| `Pos` | Genomic position (GRCh38) |
| `REF` | Reference allele |
| `ALT` | Alternate allele |
| `GT` | Genotype (`0/0`, `0/1`, or `1/1`) |

> Demo files are provided in `frontend/demo_data/` — click **"Utiliser les données de démonstration"** in the app.

---

## 🌐 Deployment

### Option 1 — Vercel (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/arbiahani2-wq/GenoPredict-)

Or manually:
1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import `arbiahani2-wq/GenoPredict-` from GitHub
3. Set **Framework Preset** → **Other**
4. Leave all build settings blank (handled by `vercel.json`)
5. Click **Deploy**

### Option 2 — Render.com

1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect `arbiahani2-wq/GenoPredict-` from GitHub
3. Render auto-detects `render.yaml` — no extra config needed
4. Click **Deploy**

### Option 3 — Docker

```bash
docker build -t genopredict .
docker run -p 7860:7860 genopredict
```

Open **[http://localhost:7860](http://localhost:7860)**

### Option 4 — Hugging Face Spaces

The app is also live on Hugging Face Spaces at:
`https://huggingface.co/spaces/haniy5/genopredict`

---

## 🧪 Model Details

| Property | Value |
|----------|-------|
| Algorithm | Random Forest Classifier |
| Training samples | 1,000 synthetic individuals |
| Features | Age, Sex, FamilyHistory, rs429358, rs7412, rs3851179 |
| Output | Probability of Alzheimer's risk (0–1) |
| Training script | `research/train_model.py` |
| Training data | `research/synthetic_training_data.csv` |

To retrain the model:
```bash
python research/generate_training_data.py
python research/train_model.py
```

---

## ⚠️ Disclaimer

> This application is intended **for educational and research purposes only**.
> It is **not a medical diagnostic tool** and should **not** be used to make clinical decisions.
> Genomic risk prediction is complex and depends on many factors beyond the SNPs analyzed here.
> Always consult a certified genetic counselor or medical professional for health-related decisions.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ · GenoPredict AD v2.0

</div>
