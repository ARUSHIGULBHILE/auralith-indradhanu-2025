# frontend/components/header.py
def render_header(title: str = "AgriTwin", subtitle: str = "") -> None:
    import streamlit as st
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
      <div style="display:flex; gap:12px; align-items:center;">
        <div style="width:56px; height:56px; border-radius:12px; background:linear-gradient(135deg,#3B82F6,#22C55E); display:flex; align-items:center; justify-content:center; color:white; font-weight:800;">🌾</div>
        <div>
          <div style="font-size:20px; font-weight:800; color:#0F172A;">{title}</div>
          <div style="font-size:13px; color:#6B7280;">{subtitle}</div>
        </div>
      </div>
      <div style="text-align:right; color:#6B7280; font-size:13px;">
        PCCOE Int. Grand Challenge 2025<br/>Team: Auralith-Indradhanu-2025
      </div>
    </div>
    """, unsafe_allow_html=True)
