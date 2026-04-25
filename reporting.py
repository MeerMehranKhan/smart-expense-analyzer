import pandas as pd
import json
from fpdf import FPDF
from pathlib import Path
from config import EXPORTS_DIR

def export_to_csv(df: pd.DataFrame) -> Path:
    """Exports transactions to CSV."""
    path = EXPORTS_DIR / 'transactions_export.csv'
    df.to_csv(path, index=False)
    return path

def export_to_json(metrics: dict, insights: list) -> Path:
    """Exports metrics and insights to JSON."""
    path = EXPORTS_DIR / 'analysis_export.json'
    
    data = {
        "metrics": metrics,
        "insights": [{"title": i.title, "description": i.description, "type": i.type} for i in insights]
    }
    
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    return path

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Smart Expense Analyzer - Financial Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def export_to_pdf(metrics: dict, insights: list, llm_summary: str) -> Path:
    """Exports a simple PDF report."""
    path = EXPORTS_DIR / 'financial_report.pdf'
    
    pdf = PDFReport()
    pdf.add_page()
    
    # Metrics
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Key Metrics', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, f"Total Income: ${metrics['total_income']:,.2f}", 0, 1)
    pdf.cell(0, 8, f"Total Expenses: ${metrics['total_expense']:,.2f}", 0, 1)
    pdf.cell(0, 8, f"Net Savings: ${metrics['net_savings']:,.2f}", 0, 1)
    pdf.cell(0, 8, f"Savings Rate: {metrics['savings_rate']:.1f}%", 0, 1)
    pdf.ln(5)
    
    # LLM Summary
    if llm_summary:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'AI Financial Summary', 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 8, llm_summary)
        pdf.ln(5)
        
    # Insights
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Key Insights', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    for i in insights:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, f"[{i.type.upper()}] {i.title}", 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 8, i.description)
        pdf.ln(2)
        
    pdf.output(str(path))
    return path
