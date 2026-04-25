import pandas as pd

def format_currency(value: float) -> str:
    """Formats a float as USD currency."""
    if pd.isna(value):
        return "$0.00"
    return f"${value:,.2f}"

def format_pct(value: float) -> str:
    """Formats a float as a percentage."""
    if pd.isna(value):
        return "0%"
    return f"{value:.1f}%"

def get_summary_metrics(df: pd.DataFrame) -> dict:
    """Calculates top-level metrics for the dashboard."""
    if df.empty:
        return {
            "total_income": 0.0,
            "total_expense": 0.0,
            "net_savings": 0.0,
            "savings_rate": 0.0
        }
        
    inc = df[df['type'] == 'Income']['amount'].sum()
    exp = df[df['type'] == 'Expense']['amount'].sum()
    net = inc - exp
    rate = (net / inc * 100) if inc > 0 else 0.0
    
    return {
        "total_income": float(inc),
        "total_expense": float(exp),
        "net_savings": float(net),
        "savings_rate": float(rate)
    }
