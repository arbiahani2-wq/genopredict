# GenoPredict - Alzheimer Risk Prediction

GenoPredict is a web application that evaluates the polygenic risk of Alzheimer's disease transmission to future offspring based on parental genomic data. It uses a Random Forest machine learning model and Mendelian genetic simulations to predict risk distributions.

## Features
- **Genomic Import**: Upload simulated parental genomic data (CSV format) containing key Alzheimer's markers (APOE, PICALM, etc.).
- **Mendelian Simulation**: Simulates 1,000 potential genomic combinations for offspring.
- **Machine Learning Analysis**: Evaluates each simulation using a pre-trained Random Forest model.
- **Risk Assessment**: Provides a comprehensive polygenic risk score, risk level (Low, Moderate, High), and detailed metrics with modern UI visualizations.

## Project Structure
- `backend/`: FastAPI server and inference logic.
- `frontend/`: Vanilla HTML/CSS/JS frontend application.
- `research/`: Research scripts, data generation, and model training files.
- `alzheimer_rf_model.pkl`: Pre-trained Random Forest model.

## Running Locally

1. **Install dependencies**:
   Ensure you have Python 3.9+ installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the application**:
   Run the FastAPI server with Uvicorn:
   ```bash
   python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000
   ```

3. **Access the application**:
   Open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Deployment (Free Hosting on Render)
This project is structured for easy deployment on [Render](https://render.com).
1. Push this repository to GitHub.
2. Create a new "Web Service" on Render and link your GitHub repository.
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn backend.api:app --host 0.0.0.0 --port $PORT`
5. Render will automatically detect the port and host the application for free.
