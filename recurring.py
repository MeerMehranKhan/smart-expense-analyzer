import pandas as pd
import numpy as np

def detect_recurring(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detects likely recurring transactions (subscriptions, bills).
    A merchant is considered recurring if:
    - Appears >= 2 times
    - Amount is identical or very similar (std dev is low)
    - Time interval between transactions is roughly consistent (e.g. ~30 days, ~7 days)
    """
    if df.empty:
        return df

    df['is_recurring'] = False
    
    # Only analyze expenses
    expenses = df[df['type'] == 'Expense'].copy()
    if expenses.empty:
        return df
        
    # Group by merchant
    grouped = expenses.groupby('merchant')
    
    recurring_merchants = set()
    
    for merchant, group in grouped:
        if len(group) < 2:
            continue
            
        group = group.sort_values('date')
        
        # Check amount variance
        mean_amt = group['amount'].mean()
        std_amt = group['amount'].std()
        
        # If std dev is < 10% of mean, amount is very stable
        amount_stable = (pd.isna(std_amt)) or (std_amt / mean_amt < 0.15)
        
        # Check date intervals
        diffs = group['date'].diff().dt.days.dropna()
        if len(diffs) > 0:
            mean_diff = diffs.mean()
            std_diff = diffs.std()
            
            # Is it weekly (~7 days), monthly (~30 days), or yearly (~365 days)
            is_periodic = False
            for target_diff in [7, 14, 30, 90, 365]:
                if abs(mean_diff - target_diff) < 5 and (pd.isna(std_diff) or std_diff < 5):
                    is_periodic = True
                    break
                    
            if amount_stable and is_periodic:
                recurring_merchants.add(merchant)
                
    # Mark in original dataframe
    mask = (df['type'] == 'Expense') & (df['merchant'].isin(recurring_merchants))
    df.loc[mask, 'is_recurring'] = True
    
    return df
