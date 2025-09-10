# frontend/components/eco_score.py
from typing import Optional

def render_eco_score(score: Optional[float] = None, gauge: bool = False) -> None:
    """
    Render eco-score panel.
    - If gauge=True and score provided, show a Plotly gauge.
    - Otherwise show a simple badge + description.
    """
    import streamlit as st
    st.markdown("<h4 style='margin-bottom:6px'>🌍 Eco Score</h4>", unsafe_allow_html=True)

    if score is None:
        st.markdown("<div style='color:#6B7280'>Eco-score will be shown after simulation (ranges 0–100).</div>", unsafe_allow_html=True)
        return

    try:
        score_val = float(score)
    except Exception:
        score_val = 0.0

    if gauge:
        try:
            import plotly.graph_objects as go
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score_val,
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#22C55E" if score_val >= 70 else ("#FFD166" if score_val >= 40 else "#FF6B6B")},
                    'steps': [
                        {'range': [0, 40], 'color': "#FFECEC"},
                        {'range': [40, 70], 'color': "#FFF7E1"},
                        {'range': [70, 100], 'color': "#E8F9EE"}
                    ],
                }
            ))
            fig.update_layout(height=220, margin={"t":0,"b":0,"l":0,"r":0}, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            # add a small explanatory text
            st.markdown(f"<div style='font-size:13px; color:#6B7280'>Eco Score: <strong>{score_val} / 100</strong> — Higher is better</div>", unsafe_allow_html=True)
            return
        except Exception:
            # if plotly fails, fall back to simple display below
            pass

    # fallback simple badge
    color = "#22C55E" if score_val >= 70 else ("#FFD166" if score_val >= 40 else "#FF6B6B")
    st.markdown(
        f"""
        <div style='display:flex; gap:12px; align-items:center;'>
          <div style='width:72px; height:72px; border-radius:12px; background:linear-gradient(135deg,{color},#fff); display:flex; align-items:center; justify-content:center; font-weight:800; color:#0F172A; font-size:20px'>
            {int(score_val)}
          </div>
          <div>
            <div style='font-weight:700'>Eco Score</div>
            <div style='color:#6B7280; font-size:13px'>Higher = more sustainable</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )
