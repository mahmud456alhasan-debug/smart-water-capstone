"""Streamlit rainfall monitor — Week 5 Lab 1 (enhance via OpenCode Exercise 3)."""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from alerts import append_alert_history, check_alert, load_alert_history, log_alert
from config import ConfigError, load_settings
from openweather_client import WeatherAPIError, fetch_current_weather

st.set_page_config(page_title="Rainfall Forecast & Alerts", layout="wide")
st.title("Rainfall Forecasting & Alert System")

LEVEL_COLORS = {"GREEN": "#2ecc71", "YELLOW": "#f39c12", "RED": "#e74c3c"}

try:
    settings = load_settings()
except ConfigError as exc:
    st.error(str(exc))
    st.stop()

city = st.text_input("City", value=settings.default_city)
col_refresh, col_time = st.columns([1, 2])
with col_refresh:
    refresh = st.button("Refresh data", type="primary")

if "last_reading" not in st.session_state:
    st.session_state.last_reading = None
    st.session_state.last_alert = None
    st.session_state.last_update = None
    st.session_state.last_error = None

if refresh or st.session_state.last_reading is None:
    try:
        reading = fetch_current_weather(city, settings, use_cache=not refresh)
        alert = check_alert(reading.rainfall_mm_h, settings)
        log_alert(city, alert)
        append_alert_history(settings, city, alert)
        st.session_state.last_reading = reading
        st.session_state.last_alert = alert
        st.session_state.last_update = datetime.now(timezone.utc)
        st.session_state.last_error = None
    except WeatherAPIError as exc:
        st.session_state.last_error = str(exc)

if st.session_state.last_error:
    st.error(f"API error: {st.session_state.last_error}")

if st.session_state.last_reading:
    r = st.session_state.last_reading
    a = st.session_state.last_alert
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Current rainfall (mm/h)", f"{r.rainfall_mm_h:.2f}")
    with c2:
        color = LEVEL_COLORS.get(a.level, "#888")
        st.markdown(
            f"### Alert: <span style='color:{color}'>{a.level}</span>",
            unsafe_allow_html=True,
        )
        st.caption(a.message)
    with c3:
        if st.session_state.last_update:
            st.metric(
                "Last update (UTC)",
                st.session_state.last_update.strftime("%Y-%m-%d %H:%M:%S"),
            )
    st.caption(f"Weather: {r.description}")

history = load_alert_history(settings)
if history:
    st.subheader("Alert history")
    st.dataframe(pd.DataFrame(history).tail(20), use_container_width=True)
else:
    st.info("No alert history yet — click Refresh.")
