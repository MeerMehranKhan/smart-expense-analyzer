# Smart Expense Analyzer

An AI-powered expense tracking web application that automatically categorizes transactions, predicts future spending, and detects unusual financial behavior using machine learning.

Built as a collaborative portfolio project demonstrating full-stack Python development, REST API design, and applied ML.

---

## Live Demo

> Coming soon — deployment in progress

| Service | URL |
|---|---|
| Frontend | — |
| API Docs | — |

---

## Features

### Core
- JWT-based user authentication (register, login, protected routes)
- Full expense CRUD (create, read, update, delete)
- Per-category budget tracking with overspend alerts
- Monthly spending summaries with interactive charts

### Machine Learning
- **Auto-categorization** — classifies expenses into categories using TF-IDF + Random Forest (achieved ~91% accuracy on held-out test set)
- **Spending prediction** — forecasts next month's spending per category using linear regression on historical data
- **Anomaly detection** — flags unusual transactions using Isolation Forest

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, SQLAlchemy, Pydantic, Python 3.11 |
| ML | Scikit-learn, Pandas, NumPy |
| Database | PostgreSQL (production), SQLite (development) |
| Frontend | React 18, Vite, Tailwind CSS, Recharts |
| Auth | JWT (python-jose), bcrypt password hashing |
| Deployment | Render (backend + DB), Vercel (frontend) |

---

## Project Structure

smart-expense-analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── database.py          # SQLAlchemy engine
│   │   ├── models/              # ORM models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── routers/             # API route handlers
│   │   ├── services/            # Business logic
│   │   └── ml/                  # ML pipeline
│   │       ├── categorizer.py
│   │       ├── predictor.py
│   │       └── anomaly.py
│   ├── data/
│   │   └── sample_expenses.csv
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── api/
│   │   └── context/
│   └── package.json
│
└── README.md