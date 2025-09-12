# frontend/components/profit_report.py
from typing import Optional, List, Dict, Any
import pandas as pd

def render_profit_report(crops: Optional[List[Dict[str,Any]]] = None, theme: str = "plotly_white", show_compact: bool = False):
    import streamlit as st
    import plotly.express as px

    st.markdown("<div style='display:flex; justify-content:space-between; align-items:center;'><div style='font-weight:700'>Profit & Market Report</div></div>", unsafe_allow_html=True)

    if crops is None:
        crops = [
            {"crop":"Wheat","yield":1.2,"revenue":3500,"cost":630,"profit":2870},
            {"crop":"Maize","yield":1.1,"revenue":3400,"cost":620,"profit":2780},
            {"crop":"Soybean","yield":0.9,"revenue":3300,"cost":600,"profit":2700},
        ]
    df = pd.DataFrame(crops)

    # Animated profit bar
    fig = px.bar(df, x="crop", y="profit", text="profit", template=theme, color="profit", color_continuous_scale=["#FF6B6B","#FFD166","#06D6A0"])
    fig.update_traces(texttemplate='₹%{text}', textposition='outside')
    fig.update_layout(margin={"t":10,"b":20}, height=320)
    st.plotly_chart(fig, use_container_width=True)

    # compact small table in side
    if not show_compact:
        st.markdown("<small style='color:#6B7280'>Detailed numbers</small>", unsafe_allow_html=True)
        st.table(df)
