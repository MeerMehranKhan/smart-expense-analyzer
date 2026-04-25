import sqlite3
import pandas as pd
from typing import List, Optional
from pathlib import Path
from config import DB_PATH

def get_connection():
    """Returns a SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            date TEXT,
            merchant TEXT,
            amount REAL,
            category TEXT,
            is_recurring INTEGER,
            is_anomaly INTEGER,
            type TEXT
        )
    ''')
    
    # Create budgets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            category TEXT PRIMARY KEY,
            amount REAL
        )
    ''')
    
    conn.commit()
    conn.close()

def save_transactions_df(df: pd.DataFrame):
    """Saves a Pandas DataFrame of transactions to the SQLite database."""
    if df.empty:
        return
    
    # Ensure types are correct for SQLite
    df_sql = df.copy()
    if 'date' in df_sql.columns:
        df_sql['date'] = df_sql['date'].astype(str)
    
    conn = get_connection()
    df_sql.to_sql('transactions', conn, if_exists='replace', index=False)
    conn.close()

def load_transactions_df() -> pd.DataFrame:
    """Loads transactions from SQLite into a Pandas DataFrame."""
    conn = get_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM transactions", conn)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
    except Exception:
        df = pd.DataFrame()
    conn.close()
    return df

def save_budgets(budgets_dict: dict):
    """Saves budget limits."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM budgets")
    for cat, amount in budgets_dict.items():
        cursor.execute("INSERT INTO budgets (category, amount) VALUES (?, ?)", (cat, amount))
    conn.commit()
    conn.close()

def load_budgets() -> dict:
    """Loads budget limits."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, amount FROM budgets")
    rows = cursor.fetchall()
    conn.close()
    return {row['category']: row['amount'] for row in rows}

def clear_db():
    """Clears all data from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS budgets")
    conn.commit()
    conn.close()
    init_db()

# Initialize DB on import
init_db()
