import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
model_file = "alzheimer_rf_model.pkl"
input_file = "simulated_children.csv"
output_file = "predicted_risk.csv"
plot_file = "risk_distribution.png"

def predict_risk():
    print("Loading model and data...")
    with open(model_file, 'rb') as f:
        iso_model = pickle.load(f)
        
    df = pd.read_csv(input_file)
    
    # Ensure columns match training features
    features = ['Age', 'Sex', 'FamilyHistory', 'rs429358', 'rs7412', 'rs3851179']
    
    # Check if all features exist
    for col in features:
        if col not in df.columns:
            print(f"Error: Missing column {col} in input data.")
            return

    print("Predicting risk...")
    # Predict probabilities (Risk Score)
    # class 1 = Alzheimer's
    probs = iso_model.predict_proba(df[features])
    
    # Basic RF returns [prob_0, prob_1]
    risk_scores = probs[:, 1]
    
    df['Risk_Score'] = risk_scores
    
    # Save results
    df.to_csv(output_file, index=False)
    print(f"Predictions saved to {output_file}")
    
    # Visualize
    print("Generating visualization...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Risk_Score'], bins=30, kde=True, color='skyblue')
    plt.title('Distribution of Alzheimer\'s Risk in Simulated Virtual Children')
    plt.xlabel('Predicted Risk Probability (0-1)')
    plt.ylabel('Count of Children')
    plt.axvline(x=0.5, color='red', linestyle='--', label='High Risk Threshold')
    plt.legend()
    plt.grid(axis='y', alpha=0.5)
    plt.savefig(plot_file)
    print(f"Plot saved to {plot_file}")
    
    # Summary stats
    print("\nRisk Summary:")
    print(df['Risk_Score'].describe())
    
    high_risk_count = (df['Risk_Score'] > 0.5).sum()
    print(f"\nNumber of children with Risk > 50%: {high_risk_count} / {len(df)}")

if __name__ == "__main__":
    predict_risk()
