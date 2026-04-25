import pandas as pd
from typing import List
from models import Insight
from config import USE_LLM, OPENAI_API_KEY, OPENAI_MODEL
import openai

def generate_heuristic_insights(df: pd.DataFrame, budgets: dict) -> List[Insight]:
    """Generates rule-based insights."""
    insights = []
    if df.empty:
        return insights
        
    expenses = df[df['type'] == 'Expense']
    
    # Check top category
    if not expenses.empty:
        top_cat = expenses.groupby('category')['amount'].sum().idxmax()
        top_amt = expenses.groupby('category')['amount'].sum().max()
        total_exp = expenses['amount'].sum()
        pct = (top_amt / total_exp) * 100
        
        insights.append(Insight(
            title="Largest Spending Area",
            description=f"You spend {pct:.0f}% of your total expenses on {top_cat}.",
            type="info"
        ))
        
    # Check anomalies
    anomalies = df[df['is_anomaly'] == True]
    if not anomalies.empty:
        insights.append(Insight(
            title="Unusual Spending Detected",
            description=f"Found {len(anomalies)} unusually large transactions. Review your anomalies tab.",
            type="warning"
        ))
        
    # Check recurring
    recurring = df[df['is_recurring'] == True]
    if not recurring.empty:
        recurring_cost = recurring.groupby('merchant')['amount'].mean().sum()
        insights.append(Insight(
            title="Recurring Subscriptions",
            description=f"You have estimated recurring monthly costs of ${recurring_cost:.2f}. Consider auditing these.",
            type="opportunity"
        ))
        
    # Check budgets
    if budgets and not expenses.empty:
        current_month = expenses['date'].dt.to_period('M').max()
        curr_month_df = expenses[expenses['date'].dt.to_period('M') == current_month]
        spent_by_cat = curr_month_df.groupby('category')['amount'].sum().to_dict()
        
        over_budget = []
        for cat, limit in budgets.items():
            if spent_by_cat.get(cat, 0) > limit:
                over_budget.append(cat)
                
        if over_budget:
            insights.append(Insight(
                title="Over Budget",
                description=f"You are over budget in: {', '.join(over_budget)}.",
                type="warning"
            ))
        else:
            insights.append(Insight(
                title="Good Budgeting",
                description="You are within your budgets for all categories this month!",
                type="positive"
            ))
            
    return insights

def get_llm_financial_summary(df: pd.DataFrame) -> str:
    """Uses LLM to write a concise financial summary if enabled."""
    if not USE_LLM or not OPENAI_API_KEY or df.empty:
        return "LLM Analysis is disabled or no data available. Enable USE_LLM and provide API keys in .env."
        
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Prepare context
        expenses = df[df['type'] == 'Expense']
        income = df[df['type'] == 'Income']
        total_exp = expenses['amount'].sum()
        total_inc = income['amount'].sum()
        top_cats = expenses.groupby('category')['amount'].sum().nlargest(3).to_dict()
        
        prompt = f"""
        Act as an expert financial advisor. Review this monthly snapshot:
        Total Income: ${total_inc:.2f}
        Total Expenses: ${total_exp:.2f}
        Top Expense Categories: {top_cats}
        
        Provide a short (3-4 sentences), encouraging, but highly analytical assessment. 
        Point out one area to improve and one positive trend.
        """
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error connecting to AI service: {str(e)}"
