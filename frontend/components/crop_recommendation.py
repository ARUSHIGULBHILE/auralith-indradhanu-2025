# frontend/components/crop_recommendation.py
from typing import List, Dict

def render_crop_recommendations(recs: List[Dict] = None, show_images: bool = False):
    import streamlit as st
    st.markdown("", unsafe_allow_html=True)
    if not recs:
        recs = [
            {"crop":"Wheat","score":87,"reason":"Suitable soil & strong market price"},
            {"crop":"Maize","score":78,"reason":"Moderate water requirement"},
            {"crop":"Soybean","score":70,"reason":"High margin & low input"},
        ]
    for r in recs:
        color = "#22C55E" if r["score"]>=80 else ("#FFD166" if r["score"]>=60 else "#FF6B6B")
        st.markdown(f"""
        <div style="display:flex; gap:12px; align-items:center; padding:10px; border-radius:10px; margin-bottom:8px; background:linear-gradient(180deg,#fff,#fbfdff);">
          <div style="width:56px; height:56px; border-radius:8px; background:linear-gradient(135deg,#e6f4ff,#eafff1); display:flex;align-items:center;justify-content:center;">{r['crop'][0]}</div>
          <div style="flex:1;">
            <div style="font-weight:700">{r['crop']} <span style='color:{color}; font-weight:800; margin-left:8px'>{r['score']}%</span></div>
            <div style="font-size:13px; color:#6B7280">{r['reason']}</div>
          </div>
          <div style="font-size:13px; color:#6B7280">Est. Profit: ₹{int(2000 + r['score']*10):,}</div>
        </div>""", unsafe_allow_html=True)
