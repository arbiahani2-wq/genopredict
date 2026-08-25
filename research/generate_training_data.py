import pandas as pd
import numpy as np
import random

# Configuration
n_samples = 5000 # Increased sample size
output_file = "synthetic_training_data.csv"

def generate_data():
    data = []
    
    for _ in range(n_samples):
        # 1. Basic Demographics
        age = np.random.randint(60, 95)
        sex = np.random.choice([0, 1]) # 0: Female, 1: Male
        family_history = np.random.choice([0, 1], p=[0.7, 0.3])
        
        # 2. Genotypes 
        # rs429358 (APOE C is risk)
        rs429358 = np.random.choice([0, 1, 2], p=[0.72, 0.26, 0.02])
        # rs7412 (APOE T is protective)
        rs7412 = np.random.choice([0, 1, 2], p=[0.88, 0.11, 0.01])
        # rs3851179 (PICALM C is risk)
        rs3851179 = np.random.choice([0, 1, 2], p=[0.6, 0.3, 0.1])
        
        # 3. Calculate Risk Score (Sharper Logic)
        # Base score
        score = 0
        
        # Stronger Age effect (Exponential-ish)
        if age > 85: score += 40
        elif age > 75: score += 20
        elif age > 65: score += 10
        
        # Sex effect
        if sex == 0: score += 5
        
        # Family History
        if family_history == 1: score += 15
        
        # Genotype effects (Stronger penalties)
        # APOE e4 proxy (rs429358 C allele is bad)
        if rs429358 == 1: score += 25  # Heterozygous 
        elif rs429358 == 2: score += 60 # Homozygous (Very bad)
        
        # Protective APOE (rs7412 T)
        if rs7412 == 1: score -= 15
        elif rs7412 == 2: score -= 30
        
        # PICALM
        if rs3851179 == 1: score += 5
        elif rs3851179 == 2: score += 10
        
        # Add some random noise (-10 to +10) to prevent 100% deterministic rules
        noise = np.random.randint(-15, 15)
        total_score = score + noise
        
        # 4. Diagnosis Threshold
        # If score > 50, they have it. 
        # This makes the boundary distinct, allowing RF to find it easily.
        if total_score >= 50:
            diagnosis = 1
        else:
            diagnosis = 0
        
        record = {
            'Age': age,
            'Sex': sex,
            'FamilyHistory': family_history,
            'rs429358': rs429358,
            'rs7412': rs7412,
            'rs3851179': rs3851179,
            'Diagnosis': diagnosis
        }
        data.append(record)
        
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Generated {n_samples} training samples to {output_file}")
    print(df['Diagnosis'].value_counts(normalize=True))

if __name__ == "__main__":
    generate_data()
