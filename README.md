<div align="center">

<img src="https://capsule-render.vercel.app/api?type=soft&color=0:0369A1,100:38BDF8&height=160&section=header&text=🧬%20GenoPredict&fontSize=46&fontColor=ffffff&animation=fadeIn&fontAlignY=45&desc=Polygenic%20Risk%20Prediction%20for%20Alzheimer's%20Disease&descAlignY=70&descSize=16" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Gradio](https://img.shields.io/badge/Gradio-API-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)](https://gradio.app)
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://genopredict.vercel.app)
[![HuggingFace](https://img.shields.io/badge/ML_Backend-HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/spaces/haniy5/genopredict)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

An **AI-powered bioinformatics** web application that estimates the **polygenic risk** of transmitting Alzheimer's disease to future offspring.  
Combines **Mendelian inheritance simulation** (1,000 offspring) with a trained **Random Forest** classifier  
to deliver probabilistic risk assessments from parental genomic data.

<br/>

<a href="https://genopredict.vercel.app"><img src="https://img.shields.io/badge/▶_Try_it_Live-genopredict.vercel.app-0EA5E9?style=for-the-badge&logoColor=white"/></a>&nbsp;&nbsp;
<a href="https://huggingface.co/spaces/haniy5/genopredict"><img src="https://img.shields.io/badge/🤗_ML_Backend-HuggingFace_Space-FFD21E?style=for-the-badge"/></a>

</div>

<br/>

---

## ✨ Features

<table>
<tr><td>🧬</td><td><strong>Genomic Import</strong></td><td>Upload parental VCF-style CSV files with key Alzheimer's SNP markers</td></tr>
<tr><td>🎲</td><td><strong>Mendelian Simulation</strong></td><td>Simulates <strong>1,000 offspring</strong> genotypes using probabilistic allele inheritance</td></tr>
<tr><td>🤖</td><td><strong>ML Risk Scoring</strong></td><td>Random Forest model trained on synthetic genomic + clinical data</td></tr>
<tr><td>📊</td><td><strong>Rich Visualizations</strong></td><td>Animated risk gauge, distribution histogram, per-SNP probability breakdowns</td></tr>
<tr><td>🔒</td><td><strong>Privacy First</strong></td><td>No genomic data is stored — all processing is ephemeral</td></tr>
<tr><td>📁</td><td><strong>Demo Mode</strong></td><td>One-click load of example parental genotype files to explore immediately</td></tr>
</table>

<br/>

---

## 🖼️ How It Works

```
   ┌──────────────┐     ┌──────────────────┐     ┌───────────────────┐     ┌──────────────────┐
   │  📋 Step 1   │     │   🧬 Step 2      │     │   🏥 Step 3       │     │   📊 Step 4      │
   │              │────▶│                  │────▶│                   │────▶│                  │
   │  Welcome &   │     │  DNA Import      │     │  Clinical Params  │     │  Results &       │
   │  Context     │     │  Father + Mother │     │  Age · Sex ·      │     │  Risk Charts     │
   │              │     │  CSV Upload      │     │  Family History   │     │  Gauge · Histo   │
   └──────────────┘     └──────────────────┘     └───────────────────┘     └──────────────────┘
```

<br/>

---

## 🔬 Scientific Background

GenoPredict analyzes **three key SNPs** associated with Alzheimer's disease:

| SNP | Gene | Chr | Role |
|:---:|:----:|:---:|:-----|
| `rs429358` | **APOE** | 19 | Strongest genetic risk factor for late-onset Alzheimer's — defines the ε4 allele |
| `rs7412` | **APOE** | 19 | Defines APOE ε2/ε3/ε4 haplotype in combination with rs429358 |
| `rs3851179` | **PICALM** | 11 | Affects amyloid precursor protein (APP) trafficking & Aβ clearance |

The model also incorporates **clinical covariates**: `Age`, `Biological Sex`, and `Family History`.

<br/>

---

## 🏗️ Architecture

A **decoupled microservices** design — frontend and ML backend are on separate platforms for performance and cost.

```mermaid
graph LR
    A["🧑‍💻 User Browser"] -->|"Upload CSV + Params"| B["⚡ Vercel Frontend"]
    B -->|"@gradio/client"| C["🤗 HuggingFace Space"]
    C -->|"ZeroGPU"| D["🧠 Random Forest Model"]
    D -->|"JSON Results"| C
    C -->|"Predictions"| B
    B -->|"Chart.js Rendering"| A

    style A fill:#0EA5E9,color:#fff,stroke:#0369A1
    style B fill:#000000,color:#fff,stroke:#333
    style C fill:#FFD21E,color:#000,stroke:#CC9900
    style D fill:#F97316,color:#fff,stroke:#C2410C
```

| Component | Platform | Role |
|:----------|:---------|:-----|
| **Frontend** | Vercel | HTML/CSS/JS · PapaParse CSV parsing · Chart.js visualizations |
| **Backend** | HuggingFace Spaces | Headless Gradio app with `@spaces.GPU` decorator |
| **Model** | `alzheimer_rf_model.pkl` | Pre-trained Random Forest (~3MB) · scikit-learn 1.9 |
| **Bridge** | `@gradio/client` | JS library handling SSE queues for ML predictions |

<br/>

---

## 🧪 Model Details

| Property | Value |
|:---------|:------|
| Algorithm | Random Forest Classifier |
| Library | scikit-learn 1.9 |
| Training samples | 1,000 synthetic individuals |
| Features | `Age` · `Sex` · `FamilyHistory` · `rs429358` · `rs7412` · `rs3851179` |
| Output | Probability of Alzheimer's risk (0.0 – 1.0) |

<details>
<summary><strong>🔄 Retrain the model</strong></summary>
<br/>

```bash
python research/generate_training_data.py   # Generate synthetic dataset
python research/train_model.py              # Train & export .pkl
```

</details>

<br/>

---

## 📂 Input Format

```csv
rsID,Chrom,Pos,REF,ALT,GT
rs429358,19,44908684,T,C,0/1
rs7412,19,44908822,C,T,0/0
rs3851179,11,85868640,A,C,0/1
```

| Column | Description |
|:-------|:------------|
| `rsID` | SNP identifier (e.g. `rs429358`) |
| `Chrom` | Chromosome number |
| `Pos` | Genomic position (GRCh38) |
| `REF` / `ALT` | Reference & alternate alleles |
| `GT` | Genotype: `0/0` · `0/1` · `1/1` |

> 💡 Demo files included in `frontend/demo_data/` — click **"Utiliser les données de démonstration"** in the app.

<br/>

---

## 🚀 Run Locally

```bash
git clone https://github.com/arbiahani2-wq/GenoPredict-.git
cd GenoPredict-
pip install -r requirements.txt
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload
```

Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** — or double-click `start_app.bat` on Windows.

<br/>

---

## ⚠️ Disclaimer

> [!CAUTION]
> This application is intended **for educational and research purposes only**.  
> It is **not a medical diagnostic tool** and should **not** be used for clinical decisions.  
> Always consult a **certified genetic counselor** or medical professional.

<br/>

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

<br/>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=soft&color=0:0369A1,100:38BDF8&height=80&section=footer" width="100%"/>

<sub>Built by <a href="https://github.com/arbiahani2-wq"><strong>ARBIA Hani</strong></a> · GenoPredict v4.0</sub>

</div>
