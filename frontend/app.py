import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Digital Twin Farm", layout="wide")

st.title("Digital Twin Farm - Dashboard (Starter)")

# Placeholder panels
col1, col2 = st.columns([2,1])

with col1:
    st.header("Live Sensor Feed")
    st.write("Sensor data will appear here (placeholder).")
    df = pd.DataFrame([{"soil_moisture":35, "temperature":28, "humidity":60, "timestamp":"2025-09-05 20:00"}])
    st.table(df)

    st.header("Digital Twin Simulator")
    rainfall = st.slider("Rainfall (mm)", 0, 200, 50)
    temperature = st.slider("Temperature (°C)", -10, 50, 25)
    if st.button("Run Simulation"):
        # Call backend simulate endpoint (adjust host if needed)
        try:
            resp = requests.post("http://localhost:8000/simulate/", json={"rainfall": rainfall, "temperature": temperature, "crop":"Wheat"})
            st.write(resp.json())
        except Exception as e:
            st.error("Simulation API not reachable. Use backend or mock data.")

with col2:
    st.header("Top Crop Recommendations")
    st.write("Top 3 crops (placeholder)")
    st.info("1. Wheat (score:87)\n2. Maize (78)\n3. Soybean (70)")

    st.header("Eco-Score")
    st.metric("Eco Score", "78 / 100")
