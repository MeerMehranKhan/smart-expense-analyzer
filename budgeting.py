import pandas as pd

def calculate_budget_utilization(df: pd.DataFrame, budgets: dict) -> list[dict]:
    """
    Calculates how much of the budget has been utilized in the current month.
    """
    if df.empty or not budgets:
        return []
        
    # Filter to current month's expenses
    expenses = df[df['type'] == 'Expense'].copy()
    if expenses.empty:
        return []
        
    current_month = expenses['date'].dt.to_period('M').max()
    curr_month_df = expenses[expenses['date'].dt.to_period('M') == current_month]
    
    spent_by_cat = curr_month_df.groupby('category')['amount'].sum().to_dict()
    
    results = []
    for cat, limit in budgets.items():
        spent = spent_by_cat.get(cat, 0.0)
        utilization = (spent / limit * 100) if limit > 0 else 0
        
        status = "On Track"
        if utilization >= 100:
            status = "Over Budget"
        elif utilization >= 85:
            status = "Warning"
            
        results.append({
            "category": cat,
            "budget": limit,
            "spent": spent,
            "remaining": max(0, limit - spent),
            "utilization_pct": utilization,
            "status": status
        })
        
    return results
