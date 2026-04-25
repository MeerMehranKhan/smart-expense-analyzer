import streamlit as st

def metric_card(title: str, value: str, delta: str = None, delta_color: str = "normal"):
    """Displays a styled metric card in Streamlit."""
    st.metric(label=title, value=value, delta=delta, delta_color=delta_color)

def apply_custom_css():
    """Injects custom CSS for premium UI feel."""
    st.markdown("""
        <style>
        .stMetric {
            background-color: #1e1e2e;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .stDataFrame {
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
