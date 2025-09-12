# frontend/components/sensor_panel.py
from typing import List, Dict, Any
import pandas as pd

def render_sensor_panel(sensors: List[Dict[str,Any]] = None, animated: bool = False, compact: bool = False):
    import streamlit as st, time
    # primary sensor
    if not sensors:
        from time import strftime
        sensors = [{"device_id":"sim-01","soil_moisture":35.2,"temperature":27.1,"humidity":62.3,"timestamp":strftime("%Y-%m-%d %H:%M:%S")}]
    primary = sensors[0]
    # Compact mode shows just a metric; full shows table
    if compact:
        # show three metrics horizontally in a small card
        cols = st.columns(3)
        cols[0].metric("Soil", f"{primary['soil_moisture']}%", "± optimal")
        cols[1].metric("Temp", f"{primary['temperature']} °C")
        cols[2].metric("Humidity", f"{primary['humidity']}%")
        return

    st.markdown("<div style='display:flex; gap:12px;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div style='font-size:12px;color:#6B7280'>Soil Moisture</div><div style='font-weight:700;font-size:20px'>{primary['soil_moisture']}%</div><div class='small'>Optimal: 30–60%</div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='font-size:12px;color:#6B7280'>Temperature</div><div style='font-weight:700;font-size:20px'>{primary['temperature']} °C</div><div class='small'>Ideal: 20–28°C</div>", unsafe_allow_html=True)
    col3.markdown(f"<div style='font-size:12px;color:#6B7280'>Humidity</div><div style='font-weight:700;font-size:20px'>{primary['humidity']}%</div><div class='small'>Ideal: 50–70%</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # show table
    try:
        df = pd.DataFrame(sensors)
        display = df[["device_id","soil_moisture","temperature","humidity","timestamp"]].copy()
        display.columns = ["Device","Soil (%)","Temp (°C)","Humidity (%)","Time"]
        st.table(display)
    except Exception:
        st.write(sensors)
