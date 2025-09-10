# frontend/components/profit_report.py
from typing import List, Dict, Any, Optional

def render_profit_report(crops: Optional[List[Dict[str, Any]]] = None, theme: str = "plotly_white") -> None:
    """
    Render the Profit & Market Report panel.

    Args:
        crops: List of crop recommendations with fields: name, yield, revenue, cost, profit
        theme: Plotly theme string ("plotly_white", "plotly_dark", etc.)
    """
    import streamlit as st
    import pandas as pd
    import plotly.express as px

    st.markdown("<h4 style='margin-bottom:6px'>💰 Profit & Market Report</h4>", unsafe_allow_html=True)

    # fallback mock crops
    if not crops:
        crops = [
            {"crop": "Wheat", "yield": 1.2, "revenue": 3500, "cost": 630, "profit": 2870},
            {"crop": "Maize", "yield": 1.1, "revenue": 3400, "cost": 620, "profit": 2780},
            {"crop": "Soybean", "yield": 0.9, "revenue": 3300, "cost": 600, "profit": 2700},
        ]

    df = pd.DataFrame(crops)

    # profit chart (bar)
    try:
        fig = px.bar(
            df,
            x="crop",
            y="profit",
            color="profit",
            color_continuous_scale=["#FF6B6B", "#FFD166", "#06D6A0"],
            text="profit",
            template=theme
        )
        fig.update_traces(texttemplate="₹%{text}", textposition="outside")
        fig.update_layout(
            title="Estimated Profit by Crop",
            yaxis_title="Profit (₹)",
            xaxis_title="Crop",
            margin={"l": 20, "r": 20, "t": 40, "b": 20},
            height=320
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.error("Error rendering profit chart")

    # cost vs revenue stacked bar
    try:
        cost_rev_df = df.melt(id_vars="crop", value_vars=["cost", "revenue"], var_name="type", value_name="amount")
        fig2 = px.bar(
            cost_rev_df,
            x="crop",
            y="amount",
            color="type",
            barmode="group",
            template=theme,
            color_discrete_map={"revenue": "#2563EB", "cost": "#EF4444"}
        )
        fig2.update_layout(
            title="Cost vs Revenue Breakdown",
            yaxis_title="Amount (₹)",
            xaxis_title="Crop",
            margin={"l": 20, "r": 20, "t": 40, "b": 20},
            height=320
        )
        st.plotly_chart(fig2, use_container_width=True)
    except Exception:
        st.error("Error rendering cost vs revenue chart")

    # show table
    st.markdown("<small style='color:#6B7280'>Detailed Report</small>", unsafe_allow_html=True)
    st.table(df)
