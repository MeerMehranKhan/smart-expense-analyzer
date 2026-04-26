# 📈 Smart Expense Analyzer

Most expense trackers simply show you where your money went. **Smart Expense Analyzer** tells you what that spending means, how it impacts your future, and where you can optimize.

Built with Python and Streamlit, this production-grade personal finance assistant goes beyond simple ledger tracking. It acts as an intelligent financial analyst—ingesting raw data, detecting behavioral patterns, uncovering hidden subscriptions, and providing actionable insights to improve your financial health.

---

## 🎯 Why This Project?

Traditional budgeting apps are often just glorified spreadsheets that require manual tagging and offer passive reporting. I built Smart Expense Analyzer to bridge the gap between **data tracking** and **financial intelligence**.

Basic trackers tell you: *"You spent $400 on food."*  
This platform tells you: *"Your food delivery spending spiked 20% this month. You have 3 recurring subscriptions you rarely use, and based on your current velocity, you will exceed your monthly budget in 5 days."*

---

## 👥 Who Is This For?

- **Students & Young Professionals** looking to build healthy financial habits and understand their cash flow.
- **Freelancers** needing a clear separation of irregular income versus fixed monthly overhead.
- **Families** aiming to optimize recurring expenses and identify areas of budget creep.
- **Anyone** tired of manually combing through bank statements to figure out where their money actually goes.

---

## 🚀 Key Features & Value

We don't just list transactions; we interpret them.

- **🧠 Intelligent Insights & Recommendations**: Receive automated, human-readable insights. Instead of staring at charts, get direct feedback like *"You spend 26% of your monthly expenses on food delivery"* or *"You could save $45/mo by auditing your subscriptions."*
- **🕵️‍♂️ Automated Recurring Detection**: Silently scans your transaction history to identify hidden subscriptions, SaaS tools, and monthly bills, calculating their true annualized cost.
- **⚠️ Statistical Anomaly Flagging**: Employs Interquartile Range (IQR) analysis to flag unusually large transactions that deviate from your normal spending behavior.
- **🔮 Predictive Forecasting**: Uses historical moving averages to project next month’s spending velocity, preventing end-of-month surprises.
- **📊 Dynamic Budget Utilization**: Set limits per category and track your real-time burn rate.
- **📄 Exportable Intelligence**: Export your financial state to a clean PDF report, raw CSV, or structured JSON for external analysis.

---

## 🧠 The Intelligence Layer

The core differentiator of this platform is its analytical reasoning engine:

- **Behavioral Analysis**: Groups transactions to understand the *frequency* and *variance* of your spending.
- **Rule-Based Categorization**: Automatically assigns categories (e.g., Groceries, Transportation) using comprehensive regex heuristics, reducing manual data entry to near zero.
- **Optional LLM Integration**: Natively supports OpenAI and Anthropic. If API keys are provided, the system feeds aggregated metrics to an LLM to generate a concise, personalized financial summary.

---

## 🏗 Architecture & Data Flow

This project strictly adheres to the **Separation of Concerns** principle. The UI is completely decoupled from the analytical engine.

1. **Ingestion & Cleaning**: Raw CSV/Excel data is parsed, normalized, and sanitized by `ingestion.py` and `cleaning.py`.
2. **Analytical Pipeline**: The clean DataFrame flows through specialized, isolated modules (`categorization.py` → `recurring.py` → `anomalies.py`).
3. **Storage Layer**: Processed data is safely persisted using a local SQLite wrapper (`storage.py`), allowing users to maintain history across sessions and compare past runs.
4. **Presentation Layer**: `app.py` acts purely as a stateless UI shell. It invokes backend functions to retrieve Plotly charts (`charts.py`) and rendered metrics without holding business logic.

This modular design ensures that the analytical engine can be easily extracted and deployed as an API or microservice in the future.

---

## 🛠 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/MeerMehranKhan/smart-expense-analyzer.git
cd smart-expense-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

> **Tip:** You can instantly click **"Load Sample Data"** in the sidebar to populate the app and explore the features without uploading your own bank statements.

---

## 📂 Supported Formats

- Bank-exported CSV files
- Excel files (`.xlsx`, `.xls`)
- Manual transaction entry directly within the UI

---

## 🔮 Future Improvements

- **Direct Bank API Integration**: Connect securely via Plaid to sync transactions in real-time.
- **Advanced ML Categorization**: Upgrade from rule-based heuristics to a supervised learning model (like Random Forest) for higher accuracy classification.
- **Enhanced Forecasting Models**: Implement ARIMA or Prophet models for seasonality-aware predictions.
- **Multi-User Support**: Allow families or couples to maintain isolated financial profiles within the same deployment.

---

## ⚠️ Limitations

- **Forecasting Confidence**: Requires at least 2 months of historical data to generate reliable predictions.
- **Anomaly Detection Limits**: A category must have at least 4 recorded transactions before the statistical IQR baseline can identify true outliers.
