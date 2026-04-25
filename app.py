import streamlit as st
import pandas as pd
from pathlib import Path
import os

from storage import load_transactions_df, save_transactions_df, load_budgets, save_budgets, clear_db
from ingestion import ingest_file, create_manual_transaction
from cleaning import clean_data
from categorization import categorize_transactions, RULES
from recurring import detect_recurring
from anomalies import detect_anomalies
from forecasting import generate_forecast
from budgeting import calculate_budget_utilization
from insights import generate_heuristic_insights, get_llm_financial_summary
from utils import get_summary_metrics, format_currency, format_pct
from charts import plot_spending_over_time, plot_category_pie, plot_daily_trend
from reporting import export_to_csv, export_to_json, export_to_pdf
from ui_helpers import apply_custom_css

# --- Page Config ---
st.set_page_config(page_title="Smart Expense Analyzer", page_icon="📈", layout="wide")
apply_custom_css()

# --- Load Data ---
df = load_transactions_df()
budgets = load_budgets()

# --- Sidebar: Data Management ---
with st.sidebar:
    st.header("⚙️ Data Management")
    
    # 1. Upload
    uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        if st.button("Process File"):
            with st.spinner("Processing..."):
                raw_df = ingest_file(uploaded_file, uploaded_file.name)
                cleaned_df = clean_data(raw_df)
                categorized_df = categorize_transactions(cleaned_df)
                df_with_rec = detect_recurring(categorized_df)
                final_df = detect_anomalies(df_with_rec)
                
                # Combine with existing data
                combined = pd.concat([df, final_df]).drop_duplicates(subset=['id'])
                save_transactions_df(combined)
                st.success("File processed and saved!")
                st.rerun()

    # 2. Sample Data
    if st.button("Load Sample Data"):
        sample_path = Path("data/sample_transactions.csv")
        if sample_path.exists():
            with open(sample_path, 'r') as f:
                raw_df = pd.read_csv(f)
            cleaned_df = clean_data(raw_df)
            categorized_df = categorize_transactions(cleaned_df)
            df_with_rec = detect_recurring(categorized_df)
            final_df = detect_anomalies(df_with_rec)
            save_transactions_df(final_df)
            st.success("Sample data loaded!")
            st.rerun()
        else:
            st.error("Sample data not found.")

    # 3. Clear Data
    if st.button("Clear All Data"):
        clear_db()
        st.success("Database cleared!")
        st.rerun()
        
    st.markdown("---")
    st.header("📝 Manual Entry")
    with st.form("manual_entry"):
        m_date = st.date_input("Date")
        m_merchant = st.text_input("Merchant")
        m_amount = st.number_input("Amount", min_value=0.01, format="%f")
        m_type = st.selectbox("Type", ["Expense", "Income"])
        m_cat = st.selectbox("Category", list(RULES.keys()) + ["Other", "Uncategorized"])
        if st.form_submit_button("Add Transaction"):
            new_tx = create_manual_transaction(str(m_date), m_merchant, m_amount, m_cat, m_type)
            combined = pd.concat([df, new_tx]).reset_index(drop=True)
            save_transactions_df(combined)
            st.success("Transaction added!")
            st.rerun()

# --- Main Content ---
st.title("📈 Smart Expense Analyzer")

if df.empty:
    st.info("👋 Welcome! Upload a CSV/Excel file or click 'Load Sample Data' in the sidebar to get started.")
    st.stop()

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Dashboard", "Transactions & Categories", "Anomalies & Recurring", "Budget & Forecast", "Insights & Export"
])

metrics = get_summary_metrics(df)

with tab1:
    st.header("Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Income", format_currency(metrics['total_income']))
    col2.metric("Total Expenses", format_currency(metrics['total_expense']))
    col3.metric("Net Savings", format_currency(metrics['net_savings']))
    col4.metric("Savings Rate", format_pct(metrics['savings_rate']))
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_spending_over_time(df))
    with c2:
        st.plotly_chart(plot_category_pie(df))
        
    st.plotly_chart(plot_daily_trend(df))

with tab2:
    st.header("Transactions")
    
    # Search & Filter
    c1, c2, c3 = st.columns(3)
    search = c1.text_input("Search Merchant")
    cat_filter = c2.selectbox("Filter Category", ["All"] + list(df['category'].unique()))
    type_filter = c3.selectbox("Filter Type", ["All", "Income", "Expense"])
    
    view_df = df.copy()
    if search:
        view_df = view_df[view_df['merchant'].str.contains(search, case=False, na=False)]
    if cat_filter != "All":
        view_df = view_df[view_df['category'] == cat_filter]
    if type_filter != "All":
        view_df = view_df[view_df['type'] == type_filter]
        
    view_df['date'] = view_df['date'].dt.strftime('%Y-%m-%d')
    
    st.dataframe(
        view_df[['date', 'merchant', 'amount', 'category', 'type']], 
        hide_index=True
    )

with tab3:
    st.header("Anomalies & Recurring")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("⚠️ Unusual Spending")
        anomalies = df[df['is_anomaly'] == True].copy()
        if anomalies.empty:
            st.success("No anomalies detected!")
        else:
            anomalies['date'] = anomalies['date'].dt.strftime('%Y-%m-%d')
            st.dataframe(anomalies[['date', 'merchant', 'amount', 'category']], hide_index=True)
            
    with c2:
        st.subheader("🔄 Recurring Subscriptions/Bills")
        recurring = df[df['is_recurring'] == True]
        if recurring.empty:
            st.info("No recurring expenses detected.")
        else:
            rec_summary = recurring.groupby(['merchant', 'category'])['amount'].mean().reset_index()
            rec_summary = rec_summary.rename(columns={'amount': 'Estimated Monthly Cost'})
            rec_summary['Estimated Monthly Cost'] = rec_summary['Estimated Monthly Cost'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(rec_summary, hide_index=True)

with tab4:
    st.header("Budget & Forecast")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Budget Settings")
        with st.form("budget_form"):
            new_budgets = {}
            for cat in list(RULES.keys()) + ['Other']:
                if cat == 'Income': continue
                default_val = float(budgets.get(cat, 0.0))
                new_budgets[cat] = st.number_input(f"{cat} Budget", value=default_val, step=50.0)
            if st.form_submit_button("Save Budgets"):
                save_budgets(new_budgets)
                st.success("Budgets updated!")
                st.rerun()
                
        # Utilization
        st.subheader("Budget Utilization")
        util = calculate_budget_utilization(df, budgets)
        if util:
            util_df = pd.DataFrame(util)
            st.dataframe(util_df[['category', 'budget', 'spent', 'status']], hide_index=True)
        else:
            st.info("Set budgets above to see utilization.")

    with c2:
        st.subheader("Next Month Forecast")
        forecasts = generate_forecast(df)
        if forecasts:
            f_df = pd.DataFrame([f.model_dump() for f in forecasts])
            f_df['predicted_amount'] = f_df['predicted_amount'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(f_df, hide_index=True)
            st.metric("Total Forecasted Expenses", format_currency(f_df['predicted_amount'].sum()))
        else:
            st.info("Not enough data to generate forecast.")

with tab5:
    st.header("Insights & Export")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("AI Financial Summary")
        if st.button("Generate AI Summary"):
            with st.spinner("Analyzing..."):
                summary = get_llm_financial_summary(df)
                st.write(summary)
                st.session_state['llm_summary'] = summary
                
        if 'llm_summary' in st.session_state:
            st.success("Generated Summary Available for Export")
            
        st.subheader("Heuristic Insights")
        insights = generate_heuristic_insights(df, budgets)
        for i in insights:
            icon = "ℹ️"
            if i.type == "warning": icon = "⚠️"
            elif i.type == "positive": icon = "✅"
            elif i.type == "opportunity": icon = "💡"
            st.info(f"{icon} **{i.title}**: {i.description}")
            
    with c2:
        st.subheader("Export Reports")
        
        if st.button("Export to CSV"):
            path = export_to_csv(df)
            st.success(f"Saved to {path}")
            
        if st.button("Export to JSON"):
            path = export_to_json(metrics, insights)
            st.success(f"Saved to {path}")
            
        if st.button("Export to PDF"):
            llm_text = st.session_state.get('llm_summary', '')
            path = export_to_pdf(metrics, insights, llm_text)
            st.success(f"Saved to {path}")

