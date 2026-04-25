import pandas as pd
import numpy as np
import uuid

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and standardizes the ingested DataFrame.
    Expects columns similar to: Date, Description/Merchant, Amount.
    """
    if df.empty:
        return pd.DataFrame()

    # Create a copy to avoid SettingWithCopyWarning
    df = df.copy()

    # Column mapping heuristics
    col_map = {}
    lower_cols = {c: c.lower() for c in df.columns}
    
    for orig, lower in lower_cols.items():
        if 'date' in lower:
            col_map[orig] = 'date'
        elif 'desc' in lower or 'merchant' in lower or 'name' in lower or 'payee' in lower:
            col_map[orig] = 'merchant'
        elif 'amount' in lower or 'cost' in lower or 'price' in lower or 'value' in lower:
            col_map[orig] = 'amount'
        elif 'type' in lower:
            col_map[orig] = 'raw_type'
        elif 'category' in lower:
            col_map[orig] = 'category'

    df = df.rename(columns=col_map)
    
    # Ensure required columns exist
    required_cols = ['date', 'merchant', 'amount']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns. Could not identify: {', '.join(missing)}")

    # Clean date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Drop rows with invalid dates or missing amounts
    df = df.dropna(subset=['date', 'amount'])
    
    # Clean amount: Handle strings with currencies if necessary
    if df['amount'].dtype == 'O':
        df['amount'] = df['amount'].astype(str).str.replace(r'[^\d\.-]', '', regex=True)
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    df = df.dropna(subset=['amount'])
    
    # Determine type (Income / Expense)
    # If amounts are negative, they might be expenses. Let's standardize:
    # We will treat positive amounts as the absolute value, and use 'type' to distinguish.
    if 'raw_type' in df.columns:
        df['type'] = df.apply(
            lambda row: 'Income' if str(row['raw_type']).lower() in ['credit', 'income', 'deposit'] else 'Expense',
            axis=1
        )
        df['amount'] = df['amount'].abs()
    else:
        # Heuristic based on sign
        df['type'] = np.where(df['amount'] < 0, 'Expense', 'Income')
        # If all amounts are positive, assume Expense unless explicitly marked
        if (df['amount'] > 0).all():
            df['type'] = 'Expense'
        df['amount'] = df['amount'].abs()
        
    # Clean merchant name
    df['merchant'] = df['merchant'].astype(str).str.strip().str.title()
    
    # Add IDs if missing
    if 'id' not in df.columns:
        df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]
        
    # Add default columns if missing
    if 'category' not in df.columns:
        df['category'] = 'Uncategorized'
    if 'is_recurring' not in df.columns:
        df['is_recurring'] = False
    if 'is_anomaly' not in df.columns:
        df['is_anomaly'] = False
        
    # Return standardized columns
    cols = ['id', 'date', 'merchant', 'amount', 'category', 'is_recurring', 'is_anomaly', 'type']
    return df[cols].sort_values('date', ascending=False).reset_index(drop=True)
