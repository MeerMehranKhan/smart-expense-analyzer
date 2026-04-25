import pandas as pd
from datetime import datetime
from forecasting import generate_forecast

def test_forecast():
    # Create 3 months of data for 'Food'
    data = pd.DataFrame({
        'date': [
            datetime(2024, 1, 15),
            datetime(2024, 2, 15),
            datetime(2024, 3, 15)
        ],
        'amount': [100.0, 150.0, 200.0],
        'category': ['Food', 'Food', 'Food'],
        'type': ['Expense', 'Expense', 'Expense']
    })
    
    forecasts = generate_forecast(data)
    
    assert len(forecasts) == 1
    f = forecasts[0]
    assert f.category == 'Food'
    assert f.predicted_amount == 150.0 # (100 + 150 + 200) / 3
    assert f.confidence == "Medium (Based on recent average)"
