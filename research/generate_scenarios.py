import pandas as pd
import os

# Define formatting to match BCFtools/Extract script output
columns = ["Sample", "rsID", "Chrom", "Pos", "Ref", "Alt", "GT"]

# Reference Data (GRCh38)
# rs429358: Ref=T, Alt=C (C is risk)
# rs7412: Ref=C, Alt=T (T is protective)
# rs3851179: Ref=T, Alt=C (C is risk)

# --- SCENARIO 1: HIGH RISK FAMILY (APOE e4/e4 Carriers) ---
# Both parents are 1/1 (Homozygous Alt) for rs429358
high_risk_data = [
    # Father
    ["Synthetic_Father_High", "rs429358", "19", 44908684, "T", "C", "1/1"], # High Risk
    ["Synthetic_Father_High", "rs7412", "19", 44908822, "C", "T", "0/0"],
    ["Synthetic_Father_High", "rs3851179", "11", 86157598, "T", "C", "0/1"],
    
    # Mother
    ["Synthetic_Mother_High", "rs429358", "19", 44908684, "T", "C", "1/1"], # High Risk
    ["Synthetic_Mother_High", "rs7412", "19", 44908822, "C", "T", "0/0"],
    ["Synthetic_Mother_High", "rs3851179", "11", 86157598, "T", "C", "1/1"]
]

# --- SCENARIO 2: LOW RISK FAMILY (No Genotypic Risk) ---
# Both parents are 0/0 (Ref) for risk variants
low_risk_data = [
    # Father
    ["Synthetic_Father_Low", "rs429358", "19", 44908684, "T", "C", "0/0"], # Normal
    ["Synthetic_Father_Low", "rs7412", "19", 44908822, "C", "T", "0/0"],
    ["Synthetic_Father_Low", "rs3851179", "11", 86157598, "T", "C", "0/0"],
    
    # Mother
    ["Synthetic_Mother_Low", "rs429358", "19", 44908684, "T", "C", "0/0"], # Normal
    ["Synthetic_Mother_Low", "rs7412", "19", 44908822, "C", "T", "1/1"],   # Protective? 
    ["Synthetic_Mother_Low", "rs3851179", "11", 86157598, "T", "C", "0/0"]
]

def save_csv(data_list, filename):
    df = pd.DataFrame(data_list, columns=columns)
    # Filter for Father/Mother inside the function is weird, let's just split manually
    
    # Split Father/Mother
    father = df[df['Sample'].str.contains("Father")]
    mother = df[df['Sample'].str.contains("Mother")]
    
    base_path = "genopredict_app/test_scenarios"
    f_name = f"{filename}_Father.csv"
    m_name = f"{filename}_Mother.csv"
    
    father.to_csv(os.path.join(base_path, f_name), index=False)
    mother.to_csv(os.path.join(base_path, m_name), index=False)
    print(f"Generated {f_name} and {m_name}")

if __name__ == "__main__":
    save_csv(high_risk_data, "Scenario_HighRisk")
    save_csv(low_risk_data, "Scenario_LowRisk")
