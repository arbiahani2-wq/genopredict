<div align="center">

<img src="https://capsule-render.vercel.app/api?type=soft&color=0:0369A1,100:38BDF8&height=160&section=header&text=🧬%20GenoPredict%20AD&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=45&desc=Polygenic%20Risk%20Prediction%20for%20Alzheimer's%20Disease&descAlignY=70&descSize=16" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Gradio](https://img.shields.io/badge/Gradio-API-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)](https://gradio.app)
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![HuggingFace](https://img.shields.io/badge/Backend-HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/spaces/haniy5/genopredict)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

An **AI-powered bioinformatics** web application that estimates the **polygenic risk** of transmitting Alzheimer's disease to future offspring.  
It combines **Mendelian inheritance simulation** (1,000 offspring) with a trained **Random Forest** classifier to deliver probabilistic risk assessments from parental genomic data.

<br/>

<a href="https://genopredict.vercel.app"><img src="https://img.shields.io/badge/▶_Live_Demo-genopredict.vercel.app-0EA5E9?style=for-the-badge&logoColor=white"/></a>&nbsp;&nbsp;
<a href="https://huggingface.co/spaces/haniy5/genopredict"><img src="https://img.shields.io/badge/🤗_HuggingFace-ML_Backend-FFD21E?style=for-the-badge"/></a>&nbsp;&nbsp;
<a href="https://github.com/arbiahani2-wq/GenoPredict-/issues"><img src="https://img.shields.io/badge/🐛_Report-Issue-EF4444?style=for-the-badge"/></a>

</div>

<br/>

---

## ✨ Features

<table>
<tr>
<td>🧬</td><td><strong>Genomic Import</strong></td><td>Upload parental VCF-style CSV files with key Alzheimer's SNP markers (rs429358, rs7412, rs3851179)</td>
</tr>
<tr>
<td>🎲</td><td><strong>Mendelian Simulation</strong></td><td>Simulates <strong>1,000 offspring</strong> genotypes using probabilistic allele inheritance for each SNP</td>
</tr>
<tr>
<td>🤖</td><td><strong>ML Risk Scoring</strong></td><td>Random Forest classifier trained on synthetic genomic + clinical data (age, sex, family history)</td>
</tr>
<tr>
<td>📊</td><td><strong>Rich Visualizations</strong></td><td>Animated risk gauge, distribution histogram, and per-SNP probability breakdowns via Chart.js</td>
</tr>
<tr>
<td>🔒</td><td><strong>Privacy First</strong></td><td>All computation happens server-side on HuggingFace — <strong>no genomic data is stored</strong></td>
</tr>
<tr>
<td>📁</td><td><strong>Demo Mode</strong></td><td>One-click load of example parental genotype files to explore immediately</td>
</tr>
</table>

<br/>

---

## 🖼️ Application Workflow

The app guides users through a **4-step process**:

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

GenoPredict AD analyzes **three key SNPs** associated with Alzheimer's disease risk:

| SNP | Gene | Chr | Role | Reference |
|:---:|:----:|:---:|:-----|:----------|
| `rs429358` | **APOE** | 19 | Strongest genetic risk factor for late-onset Alzheimer's — defines the ε4 allele | [OMIM 107741](https://omim.org/entry/107741) |
| `rs7412` | **APOE** | 19 | Defines APOE ε2/ε3/ε4 haplotype in combination with rs429358 | [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) |
| `rs3851179` | **PICALM** | 11 | Affects amyloid precursor protein (APP) trafficking & Aβ clearance | [GWAS Catalog](https://www.ebi.ac.uk/gwas/) |

The model also incorporates **clinical covariates**: `Age`, `Biological Sex`, and `Family History of AD`.

<br/>

---

## 🏗️ Architecture

GenoPredict uses a **decoupled microservices architecture** — the frontend and ML backend are hosted on separate platforms to bypass serverless size limits while keeping everything **100% free**.

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

### Component Breakdown

| Component | Platform | Role |
|:----------|:---------|:-----|
| **Frontend** | Vercel | Static HTML/CSS/JS · PapaParse CSV parsing · Chart.js visualizations |
| **Backend** | HuggingFace Spaces | Headless Gradio app wrapping Python ML logic with `@spaces.GPU` |
| **ML Model** | `alzheimer_rf_model.pkl` | Pre-trained Random Forest (~3MB) · scikit-learn 1.9 |
| **Communication** | `@gradio/client` | JS library handling SSE queues for reliable long-running ML predictions |

<br/>

---

## 📁 Project Structure

```
genopredict/
│
├── 🌐 frontend/                    # Static web client (Vercel)
│   ├── index.html                  # 4-step guided UI
│   ├── styles.css                  # Design system & animations
│   ├── app.js                      # State management & Chart.js
│   └── demo_data/                  # Sample parental genotype CSVs
│       ├── father_genotype.csv
│       └── mother_genotype.csv
│
├── 🧠 backend/                     # ML processing module
│   ├── __init__.py
│   └── logic.py                    # Simulation engine & prediction logic
│
├── 🔬 research/                    # Data generation & model training
│   ├── generate_training_data.py   # Creates synthetic genomic dataset
│   ├── train_model.py              # Trains Random Forest classifier
│   ├── simulate_heredity.py        # Mendelian inheritance simulation
│   ├── extract_snps.py             # SNP extraction utilities
│   └── synthetic_training_data.csv # 1,000 synthetic individuals
│
├── 🤖 app.py                       # HuggingFace Gradio entrypoint
├── 📦 alzheimer_rf_model.pkl       # Pre-trained model (~3MB)
├── 🐳 Dockerfile                   # Container for HF Spaces
├── ⚙️ vercel.json                  # Vercel deployment config
├── ⚙️ render.yaml                  # Render.com deployment config
└── 📋 requirements.txt             # Python dependencies
```

<br/>

---

## 🚀 Getting Started

### Prerequisites

![Python](https://img.shields.io/badge/Python-≥3.9-3776AB?style=flat-square&logo=python&logoColor=white)
![pip](https://img.shields.io/badge/pip-latest-3776AB?style=flat-square&logo=pypi&logoColor=white)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/arbiahani2-wq/GenoPredict-.git
cd GenoPredict-

# Install dependencies
pip install -r requirements.txt

# Start the development server
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload
```

Then open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

> **🪟 Windows users** — Double-click `start_app.bat` to launch automatically.

<br/>

---

## 📂 Input File Format

GenoPredict expects **CSV files** with VCF-style genotype data:

```csv
rsID,Chrom,Pos,REF,ALT,GT
rs429358,19,44908684,T,C,0/1
rs7412,19,44908822,C,T,0/0
rs3851179,11,85868640,A,C,0/1
```

| Column | Type | Description |
|:-------|:-----|:------------|
| `rsID` | string | SNP identifier (e.g. `rs429358`) |
| `Chrom` | int | Chromosome number |
| `Pos` | int | Genomic position (GRCh38) |
| `REF` | string | Reference allele |
| `ALT` | string | Alternate allele |
| `GT` | string | Genotype: `0/0` (homozygous ref), `0/1` (heterozygous), `1/1` (homozygous alt) |

> 💡 Demo files are provided in `frontend/demo_data/` — click **"Utiliser les données de démonstration"** in the app.

<br/>

---

## 🧪 Model Details

<table>
<tr><td><strong>Algorithm</strong></td><td>Random Forest Classifier</td></tr>
<tr><td><strong>Library</strong></td><td>scikit-learn 1.9</td></tr>
<tr><td><strong>Training samples</strong></td><td>1,000 synthetic individuals</td></tr>
<tr><td><strong>Features</strong></td><td><code>Age</code> · <code>Sex</code> · <code>FamilyHistory</code> · <code>rs429358</code> · <code>rs7412</code> · <code>rs3851179</code></td></tr>
<tr><td><strong>Output</strong></td><td>Probability of Alzheimer's risk (0.0 – 1.0)</td></tr>
<tr><td><strong>Serialization</strong></td><td><code>alzheimer_rf_model.pkl</code> (~3 MB)</td></tr>
</table>

**Retrain the model:**

```bash
python research/generate_training_data.py   # Generate synthetic dataset
python research/train_model.py              # Train & export .pkl
```

<br/>

---

## 🌐 Deployment

> 🟢 **Already live** → [genopredict.vercel.app](https://genopredict.vercel.app) (frontend) + [huggingface.co/spaces/haniy5/genopredict](https://huggingface.co/spaces/haniy5/genopredict) (backend)

<details>
<summary><strong>Option 1 — Render.com</strong> ✅ Recommended for full-stack ML</summary>
<br/>

No serverless bundle size limits · Full Python runtime.

1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect `arbiahani2-wq/GenoPredict-` from GitHub
3. Render auto-detects `render.yaml` — no extra config needed
4. Click **Deploy**

</details>

<details>
<summary><strong>Option 2 — Vercel</strong> (frontend only)</summary>
<br/>

> ⚠️ Vercel serverless functions have a **250MB bundle limit**. ML dependencies exceed this — use Vercel for the frontend only.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/arbiahani2-wq/GenoPredict-)

Or manually:
1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import `arbiahani2-wq/GenoPredict-` from GitHub
3. Framework Preset → **Other** · Leave build settings blank
4. Click **Deploy**

</details>

<details>
<summary><strong>Option 3 — Docker</strong></summary>
<br/>

```bash
docker build -t genopredict .
docker run -p 7860:7860 genopredict
```

Open **[http://localhost:7860](http://localhost:7860)**

</details>

<details>
<summary><strong>Option 4 — Hugging Face Spaces</strong></summary>
<br/>

The ML backend is live on HuggingFace Spaces with ZeroGPU:  
`https://huggingface.co/spaces/haniy5/genopredict`

Synced to GitHub — push to `main` triggers automatic rebuild (2–4 min).

</details>

<br/>

---

## ⚠️ Disclaimer

> [!CAUTION]
> This application is intended **for educational and research purposes only**.  
> It is **not a medical diagnostic tool** and should **not** be used to make clinical decisions.  
> Genomic risk prediction is complex and depends on many factors beyond the SNPs analyzed here.  
> Always consult a **certified genetic counselor** or medical professional for health-related decisions.

<br/>

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

<br/>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=soft&color=0:0369A1,100:38BDF8&height=80&section=footer" width="100%"/>

<sub>Built by <a href="https://github.com/arbiahani2-wq"><strong>ARBIA Hani</strong></a> · GenoPredict AD v4.0</sub>

</div>
