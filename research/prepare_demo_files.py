import pandas as pd

# Load original trio data
df = pd.read_csv("trio_alzheimer_variants.csv")

# Split
father = df[df['Sample'] == 'HG003_Father']
mother = df[df['Sample'] == 'HG004_Mother']

# Save
father.to_csv("genopredict_app/father_genotype.csv", index=False)
mother.to_csv("genopredict_app/mother_genotype.csv", index=False)

print("Created father_genotype.csv and mother_genotype.csv in genopredict_app/")
