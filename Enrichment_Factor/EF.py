import numpy as np
import pandas as pd

df = pd.read_csv("external_validation_predictions.csv")

def compute_enrichment_factors(df, true_label_col='true_label', 
                               prob_col='prediction_probability', fractions=[0.01, 0.05, 0.1, 0.2]):
    
    df_sorted = df.sort_values(prob_col, ascending=False)
    total_positives = df_sorted[true_label_col].sum()
    total_samples = len(df_sorted)
    baseline = total_positives / total_samples
    
    results = {}
    for frac in fractions:
        n_top = max(1, int(frac * total_samples))
        top_subset = df_sorted.head(n_top)
        hits = top_subset[true_label_col].sum()
        
        ef = (hits / n_top) / baseline
        results[f'EF_{int(frac*100)}%'] = ef
    
    return results

ef_dict = compute_enrichment_factors(df)
ef_df = pd.DataFrame([ef_dict])
ef_df.to_csv("EF_CSV.csv")
ef_df
