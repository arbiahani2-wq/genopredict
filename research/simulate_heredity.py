import pandas as pd
import random
import numpy as np

# Load the trio data
input_file = "trio_alzheimer_variants.csv"
output_file = "simulated_children.csv"

def parse_genotype(gt_str, ref, alt):
    """
    Parses a genotype string like '0/1' into a list of alleles [Ref, Alt]
    and a count of alt alleles (0, 1, or 2).
    """
    if pd.isna(gt_str):
        return [ref, ref], 0 # Assume Ref/Ref if missing
    
    # Handle phased pipe '|' or unphased slash '/'
    sep = '|' if '|' in gt_str else '/'
    try:
        alleles_idx = [int(x) for x in gt_str.split(sep)]
    except ValueError:
        return [ref, ref], 0
        
    alleles = []
    alt_count = 0
    for idx in alleles_idx:
        if idx == 0:
            alleles.append(ref)
        else:
            alleles.append(alt)
            alt_count += 1
            
    return alleles, alt_count

def simulate_child_genotype(father_alleles, mother_alleles):
    """
    Simulates a child's genotype by picking one allele from each parent.
    Returns: (Allele1, Allele2), Alt_Count
    """
    # Mendelian inheritance: random allele from each parent
    p_allele = random.choice(father_alleles)
    m_allele = random.choice(mother_alleles)
    
    # Check if they are Alt (we need to know which one is Alt to count)
    # This is tricky if we just pass strings. 
    # Let's pass indices instead for easier counting?
    # No, let's Stick to the logic: count how many are NOT Ref.
    # Actually, better to work with 0 and 1 indices directly.
    return None

def main():
    print("Loading data...")
    df = pd.read_csv(input_file)
    
    # Pivot to get Father and Mother side by side for each SNP
    # HG003 = Father, HG004 = Mother
    parents = df[df['Sample'].isin(['HG003_Father', 'HG004_Mother'])].copy()
    
    # We need to process each SNP
    snps = parents['rsID'].unique()
    
    # Dictionary to store simulation results
    # Structure: { 'Child_ID': [...], 'rsXYZ': [0, 1, 2...], ... }
    n_children = 1000
    sim_data = { 'Child_ID': [f'Child_{i+1}' for i in range(n_children)] }
    
    print(f"Simulating {n_children} children for {len(snps)} SNPs...")
    
    for rsid in snps:
        snp_data = parents[parents['rsID'] == rsid]
        
        # Get Ref/Alt (should be same for both)
        ref = snp_data.iloc[0]['Ref']
        alt = snp_data.iloc[0]['Alt']
        
        # Get Father alleles
        father_row = snp_data[snp_data['Sample'] == 'HG003_Father']
        if not father_row.empty:
            f_gt_str = father_row.iloc[0]['GT']
            # Parse indices: '0/1' -> [0, 1]
            sep = '|' if '|' in f_gt_str else '/'
            f_indices = [int(x) for x in f_gt_str.split(sep)]
        else:
            f_indices = [0, 0] # Default Ref/Ref
            
        # Get Mother alleles
        mother_row = snp_data[snp_data['Sample'] == 'HG004_Mother']
        if not mother_row.empty:
            m_gt_str = mother_row.iloc[0]['GT']
            sep = '|' if '|' in m_gt_str else '/'
            m_indices = [int(x) for x in m_gt_str.split(sep)]
        else:
            m_indices = [0, 0] # Default Ref/Ref

        # Simulate for all children
        child_genotypes = []
        for _ in range(n_children):
            # Pick one from father, one from mother
            f_a = random.choice(f_indices)
            m_a = random.choice(m_indices)
            
            # Sum of indices = number of Alt alleles (assuming 0=Ref, 1=Alt)
            # This works for biallelic SNPs which is our case.
            child_alt_count = f_a + m_a
            child_genotypes.append(child_alt_count)
            
        sim_data[rsid] = child_genotypes
        print(f"  Processed {rsid}: Father={f_indices}, Mother={m_indices}")

    # Create DataFrame
    sim_df = pd.DataFrame(sim_data)
    
    # Add some random metadata for the ML model later (Age, Sex, FamilyHistory)
    # Just generic columns to prepare for Step 4
    print("Adding metadata (Age, Sex)...")
    sim_df['Age'] = np.random.randint(50, 90, n_children)
    sim_df['Sex'] = np.random.choice([0, 1], n_children) # 0: Female, 1: Male
    sim_df['FamilyHistory'] = 1 # We know they are children of this specific trio, assume inheritance context
    
    # Save
    sim_df.to_csv(output_file, index=False)
    print(f"Simulation complete. Saved to {output_file}")
    print(sim_df.head())

if __name__ == "__main__":
    main()
