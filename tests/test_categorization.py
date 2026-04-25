import pandas as pd
from categorization import categorize_transactions

def test_categorization():
    data = pd.DataFrame({
        'merchant': ['Uber Eats', 'Target', 'Netflix', 'Random Store'],
        'type': ['Expense', 'Expense', 'Expense', 'Expense'],
        'category': ['Uncategorized', 'Uncategorized', 'Uncategorized', 'Uncategorized']
    })
    
    cat = categorize_transactions(data)
    
    assert cat.iloc[0]['category'] == 'Food & Dining'
    assert cat.iloc[1]['category'] == 'Groceries'
    assert cat.iloc[2]['category'] == 'Subscriptions'
    assert cat.iloc[3]['category'] == 'Other'

def test_income_categorization():
    data = pd.DataFrame({
        'merchant': ['Stripe'],
        'type': ['Income'],
        'category': ['Uncategorized']
    })
    
    cat = categorize_transactions(data)
    assert cat.iloc[0]['category'] == 'Income'
