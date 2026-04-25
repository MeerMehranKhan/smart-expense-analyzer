import pandas as pd
import re

RULES = {
    'Food & Dining': ['uber eats', 'doordash', 'mcdonalds', 'starbucks', 'restaurant', 'cafe', 'grubhub', 'pizza'],
    'Groceries': ['walmart', 'target', 'kroger', 'safeway', 'whole foods', 'trader joe', 'aldi'],
    'Transportation': ['uber', 'lyft', 'shell', 'chevron', 'bp', 'transit', 'mta', 'gas'],
    'Utilities': ['pge', 'coned', 'water', 'electric', 'internet', 'comcast', 'verizon', 'att'],
    'Subscriptions': ['netflix', 'spotify', 'hulu', 'amazon prime', 'gym', 'planet fitness', 'apple'],
    'Shopping': ['amazon', 'best buy', 'home depot', 'mall', 'clothing'],
    'Housing': ['rent', 'mortgage', 'hoa'],
    'Income': ['payroll', 'salary', 'deposit', 'transfer from', 'venmo', 'zelle']
}

def categorize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies rule-based categorization to transactions.
    """
    if df.empty:
        return df

    def get_category(row):
        # Skip if already categorized manually
        if row['category'] != 'Uncategorized':
            return row['category']
            
        merchant = str(row['merchant']).lower()
        t_type = row['type']
        
        if t_type == 'Income':
            return 'Income'
            
        for category, keywords in RULES.items():
            if any(re.search(rf'\b{kw}\b', merchant) for kw in keywords):
                return category
                
        return 'Other'

    df['category'] = df.apply(get_category, axis=1)
    return df
