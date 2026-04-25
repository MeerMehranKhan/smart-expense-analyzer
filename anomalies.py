import pandas as pd
import numpy as np

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detects anomalous transactions using IQR per category.
    """
    if df.empty:
        return df

    df['is_anomaly'] = False
    expenses = df[df['type'] == 'Expense'].copy()
    
    if expenses.empty:
        return df

    anomalous_indices = []

    # Group by category
    for category, group in expenses.groupby('category'):
        if len(group) < 4:
            continue # Not enough data to find statistically significant outliers
            
        Q1 = group['amount'].quantile(0.25)
        Q3 = group['amount'].quantile(0.75)
        IQR = Q3 - Q1
        
        # Upper bound only for anomalies (unusually high spending)
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = group[group['amount'] > upper_bound]
        anomalous_indices.extend(outliers.index.tolist())
        
    df.loc[anomalous_indices, 'is_anomaly'] = True
    
    return df
