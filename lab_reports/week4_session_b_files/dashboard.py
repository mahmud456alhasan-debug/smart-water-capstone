"""Streamlit dashboard for rainfall monitoring — reads data/monitoring_log.csv."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import load_settings

st.set_page_config(
    page_title="Rainfall Monitor",
    page_icon="🌧",
    layout="wide",
)

st.title("Rainfall Monitoring Dashboard")
st.markdown("Real-time precipitation, runoff, and alert status.")

settings = load_settings()
csv_path = settings.csv_path

try:
    df = pd.read_csv(csv_path, parse_dates=["timestamp_utc"])
except FileNotFoundError:
    st.error(f"CSV not found at {csv_path}. Run `python3 main.py` first.")
    st.stop()

if df.empty:
    st.warning("CSV is empty — no readings recorded yet.")
    col1, col2, _ = st.columns([1, 1, 2])
    with col1:
        st.metric("Row count", 0)
    with col2:
        st.metric("Last API source", "—")
    st.stop()

df = df.sort_values("timestamp_utc").reset_index(drop=True)
latest = df.iloc[-1]

alert_color_map = {"OK": "green", "WATCH": "orange", "ALERT": "red"}
alert_color = alert_color_map.get(latest["alert_level"], "grey")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Current Rainfall", f'{latest["rainfall_mm"]:.1f} mm')

with col2:
    st.markdown(
        f"<h3 style='color:{alert_color}; margin:0;'>"
        f"{latest['alert_level']}</h3>"
        f"<p style='margin:0;'>{latest['alert_message']}</p>",
        unsafe_allow_html=True,
    )
    st.caption("Alert Status")

with col3:
    st.metric("Last Update", latest["timestamp_utc"].strftime("%H:%M UTC"))

with col4:
    st.metric("Row count", len(df))
    st.caption(f"Source: {latest['api_source']}")

st.subheader("Rainfall & Runoff Over Time")
st.line_chart(
    df.set_index("timestamp_utc")[["rainfall_mm", "runoff_mm"]],
)

st.subheader("Recent Readings")
st.dataframe(
    df[["timestamp_utc", "rainfall_mm", "runoff_mm", "alert_level", "api_source"]]
    .tail(10)
    .style.applymap(
        lambda v: (
            "background-color: #ffcccc" if v == "ALERT" else
            "background-color: #ffe0b3" if v == "WATCH" else
            "background-color: #ccffcc" if v == "OK" else ""
        ),
        subset=["alert_level"],
    ),
    use_container_width=True,
    hide_index=True,
)
