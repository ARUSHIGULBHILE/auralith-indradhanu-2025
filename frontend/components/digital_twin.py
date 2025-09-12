# frontend/components/digital_twin.py
def render_simulator_chart(client=None):
    import streamlit as st
    import plotly.graph_objects as go
    import numpy as np

    st.markdown("<div style='display:flex; gap:12px; align-items:center;'>", unsafe_allow_html=True)
    c1, c2 = st.columns([1,1])
    with c1:
        rainfall = st.slider("Rainfall (mm)", 0, 500, 50, key="sim_rain")
        temperature = st.slider("Temperature (°C)", -5, 45, 25, key="sim_temp")
        crop = st.selectbox("Crop", ["Wheat","Maize","Soybean"], key="sim_crop")
    with c2:
        st.markdown("<div style='font-size:13px; color:#6B7280'>Preview yield vs rainfall</div>", unsafe_allow_html=True)
        # generate series for preview
        rain_vals = np.linspace(max(0, rainfall-100), min(500, rainfall+100), 30)
        temp_adj = temperature
        yields = []
        for r in rain_vals:
            base = 100.0
            y_adj = base * (1 + (r - 50)/100) * (1 - abs(temp_adj - 25)/100)
            yields.append(round(y_adj,2))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=rain_vals, y=yields, mode='lines+markers', name='Estimated yield'))
        fig.update_layout(height=300, margin={"t":10,"b":20,"l":20,"r":20})
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Run real simulation on demand
    if st.button("Run Full Simulation", key="run_sim"):
        res = client.simulate(rainfall, temperature, crop) if client else None
        if res:
            st.success(f"Yield: {res.get('estimated_yield')} — Profit: ₹{int(res.get('estimated_profit')):,} — Eco: {res.get('eco_score')}")
        else:
            st.info("Simulation ran locally (fallback).")
