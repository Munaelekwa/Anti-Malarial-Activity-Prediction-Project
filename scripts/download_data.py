import requests
import pandas as pd
import time

# Base API URL
base_url = "https://www.ebi.ac.uk/chembl/api/data/activity.json"

# Parameters
params = {
    "target_organism": "Plasmodium falciparum",
    "limit": 1000,
    "offset": 0,
    "standard_type": "IC50",  # Only IC50 values
}

# Collect results
all_activities = []

while True:
    print(f"Fetching molecules {params['offset']} to {params['offset'] + params['limit'] - 1}...")
    response = requests.get(base_url, params=params)
    data = response.json()

    activities = data.get('activities', [])

    if not activities:
        print("No more data available.")
        break

    all_activities.extend(activities)

    params['offset'] += params['limit']
    time.sleep(1)  # Be polite!

# Convert to DataFrame
df = pd.DataFrame(all_activities)

# Only select the important columns
selected_columns = ['molecule_chembl_id', 'standard_value', 'canonical_smiles', 'ligand_efficiency', 'standard_units']

df_selected = df[selected_columns]

# Save the cleaned dataset
df_selected.to_csv("data/antimalarial_activities_selected.csv", index=False)

print(f"Downloaded and saved {len(df_selected)} selected activities!")



