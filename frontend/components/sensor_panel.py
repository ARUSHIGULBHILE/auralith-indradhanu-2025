# frontend/components/sensor_panel.py
from typing import List, Dict, Any
import pandas as pd
import time

def render_sensor_panel(sensors: List[Dict[str, Any]] = None, animated: bool = False) -> None:
    """
    Renders the Live Sensor Feed KPI cards and a small table of latest readings.

    Args:
        sensors: list of sensor dicts (each must contain soil_moisture, temperature, humidity)
        animated: if True, animate KPI numbers briefly (nice for demo)
    """
    import streamlit as st

    st.markdown("<h4 style='margin-bottom:6px'>📡 Live Sensor Feed</h4>", unsafe_allow_html=True)

    # fallback mock sensor if none provided
    if not sensors:
        from time import strftime
        sensors = [{
            "device_id": "sim-01",
            "soil_moisture": 35.2,
            "temperature": 27.1,
            "humidity": 62.3,
            "timestamp": strftime("%Y-%m-%d %H:%M:%S")
        }]

    # Use first sensor as the primary KPI source
    primary = sensors[0]

    # Helper to render a single KPI card with optional animation
    def _render_kpi(label: str, value: float, suffix: str = "", note: str = "", key: str = ""):
        # container to avoid duplicate element IDs
        container = st.container()
        with container:
            st.markdown(
                f"""
                <div style='padding:10px; border-radius:10px; background:linear-gradient(180deg,#ffffff,#fbfdff);'>
                  <div style='font-size:12px; color:#6B7280'>{label}</div>
                  <div id="{key}" style='font-size:22px; font-weight:700; color:#0F172A; margin-top:6px'>{int(value)}{suffix}</div>
                  <div style='font-size:12px; color:#10B981; margin-top:6px'>{note}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        # perform a short animation by incrementing shown number if requested
        if animated:
            try:
                # small, fast animation — total ~0.3s per KPI (keeps demo snappy)
                display_steps = min(20, max(5, int(abs(value) // 1) // 1))
                display_steps = max(6, display_steps)
                step_delay = 0.30 / display_steps
                current = 0.0
                step = float(value) / display_steps if display_steps else float(value)
                for _ in range(display_steps):
                    current += step
                    # write updated number with the same HTML id to minimize layout thrash
                    container.markdown(
                        f"""
                        <div style='padding:10px; border-radius:10px; background:linear-gradient(180deg,#ffffff,#fbfdff);'>
                          <div style='font-size:12px; color:#6B7280'>{label}</div>
                          <div style='font-size:22px; font-weight:700; color:#0F172A; margin-top:6px'>{int(round(current))}{suffix}</div>
                          <div style='font-size:12px; color:#10B981; margin-top:6px'>{note}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    time.sleep(step_delay)
            except Exception:
                # If animation fails (e.g., environment restrictions), silently show final value
                container.markdown(
                    f"""
                    <div style='padding:10px; border-radius:10px; background:linear-gradient(180deg,#ffffff,#fbfdff);'>
                      <div style='font-size:12px; color:#6B7280'>{label}</div>
                      <div style='font-size:22px; font-weight:700; color:#0F172A; margin-top:6px'>{int(round(value))}{suffix}</div>
                      <div style='font-size:12px; color:#10B981; margin-top:6px'>{note}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # Render three KPI cards in a row using columns (unique keys ensure no duplication)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        _render_kpi("Soil Moisture", float(primary.get("soil_moisture", 0)), suffix="%", note="Optimal: 30–60%", key="kpi_soil")
    with col2:
        _render_kpi("Temperature", float(primary.get("temperature", 0)), suffix=" °C", note="Ideal: 20–28 °C", key="kpi_temp")
    with col3:
        _render_kpi("Humidity", float(primary.get("humidity", 0)), suffix="%", note="Ideal: 50–70%", key="kpi_humid")

    # small table of recent readings
    st.markdown("<div style='margin-top:10px'><small style='color:#6B7280'>Latest readings</small></div>", unsafe_allow_html=True)
    try:
        df = pd.DataFrame(sensors)
        # format/limit columns for nicer display
        display_df = df[["device_id", "soil_moisture", "temperature", "humidity", "timestamp"]].copy()
        display_df.columns = ["Device", "Soil (%)", "Temp (°C)", "Humidity (%)", "Timestamp"]
        st.table(display_df)
    except Exception:
        # fallback simple table if columns missing
        st.write(sensors)
