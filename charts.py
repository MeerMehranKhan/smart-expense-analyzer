import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_spending_over_time(df: pd.DataFrame):
    """Bar chart of income vs expenses over time (monthly)."""
    if df.empty:
        return go.Figure()
        
    monthly = df.copy()
    monthly['month'] = monthly['date'].dt.to_period('M').dt.strftime('%b %Y')
    
    # Keep the actual period for sorting, but use the string for display
    monthly['period'] = monthly['date'].dt.to_period('M')
    grouped = monthly.groupby(['period', 'month', 'type'])['amount'].sum().reset_index()
    grouped = grouped.sort_values('period')
    
    fig = px.bar(
        grouped, x='month', y='amount', color='type',
        barmode='group',
        color_discrete_map={'Income': '#10b981', 'Expense': '#ef4444'},
        title='Income vs Expenses Over Time',
        labels={'amount': 'Amount', 'month': 'Month', 'type': 'Transaction Type'}
    )
    
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{data.name}: $%{y:,.2f}<extra></extra>"
    )
    
    fig.update_layout(
        template='plotly_dark',
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(tickprefix="$"),
        hovermode="x unified",
        legend_title_text=''
    )
    return fig

def plot_category_pie(df: pd.DataFrame):
    """Donut chart of expense categories."""
    expenses = df[df['type'] == 'Expense']
    if expenses.empty:
        return go.Figure()
        
    cat_sum = expenses.groupby('category')['amount'].sum().reset_index()
    cat_sum = cat_sum.sort_values('amount', ascending=False)
    
    fig = px.pie(
        cat_sum, values='amount', names='category', 
        hole=0.5, title='Expenses Breakdown by Category',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Total: $%{value:,.2f}<br>Share: %{percent}<extra></extra>"
    )
    
    fig.update_layout(
        template='plotly_dark', 
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False
    )
    return fig

def plot_daily_trend(df: pd.DataFrame):
    """Line chart of cumulative spending over current month."""
    expenses = df[df['type'] == 'Expense'].copy()
    if expenses.empty:
        return go.Figure()
        
    current_month = expenses['date'].dt.to_period('M').max()
    curr_df = expenses[expenses['date'].dt.to_period('M') == current_month].copy()
    
    if curr_df.empty:
        return go.Figure()
        
    daily = curr_df.groupby('date')['amount'].sum().reset_index()
    daily = daily.sort_values('date')
    daily['cumulative'] = daily['amount'].cumsum()
    daily['date_str'] = daily['date'].dt.strftime('%b %d, %Y')
    
    fig = px.line(
        daily, x='date', y='cumulative', 
        title=f'Cumulative Spending ({current_month.strftime("%B %Y")})',
        markers=True,
        line_shape='spline'
    )
    
    fig.update_traces(
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8, color='#60a5fa'),
        hovertemplate="<b>%{customdata[0]}</b><br>Cumulative Spent: $%{y:,.2f}<extra></extra>",
        customdata=daily[['date_str']]
    )
    
    fig.update_layout(
        template='plotly_dark', 
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title='',
        yaxis_title='Total Spent',
        yaxis=dict(tickprefix="$"),
        hovermode="x unified"
    )
    return fig
