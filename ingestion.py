import pandas as pd
import uuid

def ingest_file(file_obj, file_name: str) -> pd.DataFrame:
    """
    Ingests a CSV or Excel file and returns a raw DataFrame.
    """
    if file_name.endswith('.csv'):
        df = pd.read_csv(file_obj)
    elif file_name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_obj)
    else:
        raise ValueError(f"Unsupported file format: {file_name}")
    
    return df

def create_manual_transaction(date: str, merchant: str, amount: float, category: str, t_type: str) -> pd.DataFrame:
    """
    Creates a single-row DataFrame for a manually entered transaction.
    """
    data = {
        'id': [str(uuid.uuid4())],
        'date': [pd.to_datetime(date)],
        'merchant': [merchant],
        'amount': [float(amount)],
        'category': [category],
        'type': [t_type],
        'is_recurring': [False],
        'is_anomaly': [False]
    }
    return pd.DataFrame(data)
