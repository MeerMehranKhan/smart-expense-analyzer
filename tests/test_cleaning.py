import pandas as pd
from cleaning import clean_data

def test_clean_data_normal():
    data = pd.DataFrame({
        'Date': ['2024-03-01', '2024-03-02'],
        'Merchant Name': ['uber eats', 'target'],
        'Amount': [-15.50, 45.00]
    })
    
    cleaned = clean_data(data)
    
    assert len(cleaned) == 2
    assert 'date' in cleaned.columns
    assert 'merchant' in cleaned.columns
    assert 'amount' in cleaned.columns
    assert 'type' in cleaned.columns
    
    assert cleaned.iloc[1]['merchant'] == 'Uber Eats'
    assert cleaned.iloc[1]['amount'] == 15.50
    assert cleaned.iloc[1]['type'] == 'Expense' # inferred from negative amount

def test_clean_data_with_types():
    data = pd.DataFrame({
        'date': ['2024-03-01', '2024-03-02'],
        'merchant': ['salary', 'coffee'],
        'amount': [1000, 5],
        'type': ['Income', 'Expense']
    })
    
    cleaned = clean_data(data)
    
    assert cleaned.iloc[0]['type'] == 'Expense' # 2024-03-02 sorted desc
    assert cleaned.iloc[1]['type'] == 'Income'
