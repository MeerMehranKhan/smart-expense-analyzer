from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Transaction(BaseModel):
    id: Optional[str] = None
    date: date
    merchant: str
    amount: float
    category: str = "Uncategorized"
    is_recurring: bool = False
    is_anomaly: bool = False
    type: str = Field(description="Income or Expense")

class Budget(BaseModel):
    category: str
    amount: float

class Insight(BaseModel):
    title: str
    description: str
    type: str = Field(description="warning, positive, opportunity, info")

class Forecast(BaseModel):
    category: str
    predicted_amount: float
    confidence: str

class ReportSummary(BaseModel):
    total_income: float
    total_expense: float
    net_savings: float
    savings_rate: float
    top_categories: dict
