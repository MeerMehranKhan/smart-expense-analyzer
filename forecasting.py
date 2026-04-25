import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from models import Forecast

def generate_forecast(df: pd.DataFrame) -> list[Forecast]:
    """
    Forecasts next month's spending per category using a simple moving average.
    """
    if df.empty:
        return []
        
    expenses = df[df['type'] == 'Expense'].copy()
    if expenses.empty:
        return []

    # Group by month and category
    expenses['month_year'] = expenses['date'].dt.to_period('M')
    monthly_cat = expenses.groupby(['month_year', 'category'])['amount'].sum().reset_index()
    
    forecasts = []
    
    for cat in monthly_cat['category'].unique():
        cat_data = monthly_cat[monthly_cat['category'] == cat].sort_values('month_year')
        
        if len(cat_data) < 2:
            # Not enough data, just use last month's as naive forecast
            pred = cat_data['amount'].iloc[-1] if not cat_data.empty else 0
            conf = "Low (Not enough history)"
        else:
            # Simple 3-month moving average
            recent = cat_data.tail(3)
            pred = recent['amount'].mean()
            conf = "Medium (Based on recent average)"
            
        if pred > 0:
            forecasts.append(Forecast(
                category=cat,
                predicted_amount=round(pred, 2),
                confidence=conf
            ))
            
    return forecasts
