# frontend/app.py
"""
AgriTwin — Designer-grade Streamlit frontend
Run:
    streamlit run frontend/app.py
Notes:
- Uses APIClient for backend; falls back to mocks.
- Requires the components in frontend/components/ (listed below).
"""
import logging, time
from typing import Any, Dict, List, Optional

import streamlit as st

# local imports (these must be present under frontend/)
from config import Config
from api_client import APIClient

# UI components (place these files in frontend/components/)
from components.header import render_header
from components.sensor_panel import render_sensor_panel
from components.crop_recommendation import render_crop_recommendations
from components.profit_report import render_profit_report
from components.digital_twin import render_simulator_chart
from components.eco_score import render_eco_score

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("agritwin.frontend")
logger.info("Starting AgriTwin premium frontend")

# ---------- Theme & CSS ----------
def inject_css():
    st.set_page_config(page_title="AgriTwin — Digital Twin Farming", layout="wide", page_icon="🌱")
    css = """
    <style>
    :root{
      --primary: #3B82F6;
      --accent: #22C55E;
      --muted: #6B7280;
      --bg1: #F6FDFF;
      --glass: rgba(255,255,255,0.86);
    }
    .stApp { background: linear-gradient(180deg, var(--bg1), #E8F9F3); }
    .card {
      background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(255,255,255,0.82));
      border-radius: 14px;
      padding: 16px;
      box-shadow: 0 10px 40px rgba(11,31,48,0.06);
      backdrop-filter: blur(6px);
    }
    .hero-title { font-size: 24px; font-weight:800; background: linear-gradient(90deg,var(--accent),var(--primary)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
    .muted { color: var(--muted); font-size:13px; }
    .kpi { font-size:20px; font-weight:700; color:#0F172A; }
    /* improved slider thumb (modern) */
    .stSlider > div > div > div { border-radius: 8px !important; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ---------- Utility: small wait loader for polished feel ----------
def micro_wait(ms: float = 0.18):
    try:
        time.sleep(ms)
    except Exception:
        pass


# ---------- App pages ----------
def page_home(client: APIClient):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex; justify-content:space-between; align-items:center;">'
                '<div><div class="hero-title">AgriTwin</div><div class="muted">Digital Twin Farming — AI + Simulation + Eco-score</div></div>'
                '<div style="text-align:right" class="muted">Team: Auralith-Indradhanu-2025</div>'
                '</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Fetch data - client returns mock if backend offline
    sensors = client.get_latest_sensors()
    recs = client.get_recommendations()

    # Hero KPI row
    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
    k1, k2, k3 = st.columns([1.6,1,1])
    with k1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        render_sensor_panel(sensors, animated=True, compact=False)
        st.markdown('</div>', unsafe_allow_html=True)
    with k2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        render_crop_recommendations(recs, show_images=False)
        st.markdown('</div>', unsafe_allow_html=True)
    with k3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        render_profit_report(theme="plotly_white", show_compact=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)


def page_simulator(client: APIClient):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex; justify-content:space-between; align-items:center;"><div class="hero-title">Digital Twin Simulator</div>'
                '<div class="muted">Interactive "what-if" scenarios</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    render_simulator_chart(client)
    st.markdown('</div>', unsafe_allow_html=True)


def page_reports(client: APIClient):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Reports & Exports</div><div class="muted">Download PDF/CSV, view historic trends</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    # sample: show profit chart bigger
    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    render_profit_report(theme="plotly_white", show_compact=False)
    st.markdown('</div>', unsafe_allow_html=True)


def page_settings():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Settings</div><div class="muted">Configure API, demo behaviour</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    cfg = Config.from_env()
    st.markdown(f"**Current API base:** `{cfg.API_BASE_URL}`")
    st.markdown("Use environment variables `API_BASE_URL` and `API_TIMEOUT_SECONDS` for production.")


# ---------- Main ----------
def main():
    inject_css()
    cfg = Config.from_env()
    client = APIClient(base_url=cfg.API_BASE_URL, timeout_seconds=cfg.API_TIMEOUT_SECONDS)

    # Sidebar navigation (SaaS-style)
    with st.sidebar:
        st.markdown("<div style='padding:8px 0;'><strong style='font-size:16px'>Menu</strong></div>", unsafe_allow_html=True)
        page = st.radio("", ["Home", "Simulator", "Reports", "Settings"], index=0)
        st.markdown("---")
        st.markdown("**Quick actions**")
        if st.button("Run demo sim (quick)"):
            st.toast("Demo simulation queued — use Simulator page for full control")
        st.markdown("---")
        st.markdown("Team: Auralith-Indradhanu-2025")

    # Route to page
    if page == "Home":
        page_home(client)
    elif page == "Simulator":
        page_simulator(client)
    elif page == "Reports":
        page_reports(client)
    else:
        page_settings()

    st.markdown("---")
    st.caption("✨ Prototype — AgriTwin | Present confidently. Practice 90s pitch + 2min demo.")

if __name__ == "__main__":
    main()
