# frontend/components/eco_score.py
def render_eco_score(score: float = None, gauge: bool = False):
    import streamlit as st
    st.markdown("<div style='font-weight:700'>Eco Score</div>", unsafe_allow_html=True)
    if not score:
        st.markdown("<div style='color:#6B7280'>Eco-score will appear after simulation — higher is better.</div>", unsafe_allow_html=True)
        return
    try:
        import plotly.graph_objects as go
        fig = go.Figure(go.Indicator(mode="gauge+number", value=score,
                                     gauge={'axis': {'range': [0,100]},
                                            'bar': {'color': "#22C55E"},
                                            'steps':[{'range':[0,40],'color':'#FFD7D7'},{'range':[40,70],'color':'#FFF4D6'},{'range':[70,100],'color':'#E8F9EE'}]}))
        fig.update_layout(height=220, margin={"t":0,"b":0,"l":0,"r":0})
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        color = "#22C55E" if score>=70 else ("#FFD166" if score>=40 else "#FF6B6B")
        st.markdown(f"<div style='padding:10px;border-radius:10px;background:{color};'>{int(score)}</div>", unsafe_allow_html=True)
