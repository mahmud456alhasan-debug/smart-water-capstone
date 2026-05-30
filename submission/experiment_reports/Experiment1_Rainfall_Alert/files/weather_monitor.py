#!/usr/bin/env python3
"""
Experiment 1: Rainfall Monitor - Streamlit dashboard (main application).

Run: streamlit run weather_monitor.py
Screenshot URLs: ?demo_mm=5  ?demo_mm=15  ?demo_mm=21  (auto demo mode)
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

import pandas as pd
import streamlit as st

from alerts import (
    alert_log_dataframe,
    check_alert,
    log_alert,
    parse_alert_log_rows,
)
from api_client import WeatherAPIError, WeatherReading, fetch_current_weather
from config import ConfigError, Settings, load_settings

LEVEL_COLORS = {"GREEN": "#2ecc71", "YELLOW": "#f39c12", "RED": "#e74c3c"}


def demo_settings() -> Settings:
    return Settings(
        openweather_api_key="demo",
        default_city="Beijing,CN",
        cache_ttl_sec=300,
        api_timeout_sec=10,
        green_max_mm_h=10,
        yellow_max_mm_h=20,
        alert_log_path="alert_log.txt",
    )


def get_query_param(name: str) -> Optional[str]:
    if hasattr(st, "query_params"):
        val = st.query_params.get(name)
        if isinstance(val, list):
            return val[0] if val else None
        return val
    return None


def apply_demo_reading(city: str, mm: float, settings: Settings, log: bool = True) -> None:
    reading = WeatherReading(
        city=city,
        rainfall_mm_h=mm,
        rain_field_used="demo",
        description="Demo storm mode (Streamlit)",
    )
    alert = check_alert(reading.rainfall_mm_h, settings)
    if log:
        log_alert(city, alert, settings)
    st.session_state.reading = reading
    st.session_state.alert = alert
    st.session_state.updated = datetime.now(timezone.utc)
    st.session_state.api_error = None


def render_stats(df: pd.DataFrame) -> None:
    if df.empty:
        return
    rainy = df[df["rainfall_mm_h"] > 0]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Log entries", len(df))
    with c2:
        st.metric("Cities in log", df["city"].nunique())
    with c3:
        st.metric("Rainy readings", len(rainy))
    with c4:
        idx = df["rainfall_mm_h"].idxmax()
        st.metric("Max rainfall", f"{df.loc[idx, 'rainfall_mm_h']:.2f} mm/h")
        st.caption(str(df.loc[idx, "city"]))


st.set_page_config(page_title="Rainfall Monitor", layout="wide")
st.title("Rainfall Forecasting & Alert System")

query_demo_mm = get_query_param("demo_mm")
url_capture = query_demo_mm is not None
url_mm = 0.0
if url_capture:
    try:
        url_mm = float(query_demo_mm)
    except (TypeError, ValueError):
        url_mm = 0.0
    st.info(f"Demo capture mode: **{url_mm:.1f} mm/h** (`?demo_mm={query_demo_mm}`)")

with st.sidebar:
    st.header("Controls")
    preset = st.selectbox(
        "Quick demo preset",
        ["Custom", "GREEN (5 mm/h)", "YELLOW (15 mm/h)", "RED (21 mm/h)"],
        index=0,
    )
    preset_mm = {"GREEN (5 mm/h)": 5.0, "YELLOW (15 mm/h)": 15.0, "RED (21 mm/h)": 21.0}
    demo_mode = st.checkbox(
        "Demo storm mode",
        value=url_capture or preset in preset_mm,
        help="Slider rainfall instead of live API.",
    )
    auto_refresh = st.checkbox("Auto-refresh every 5 min (live API only)")
    default_slider = preset_mm.get(preset, url_mm if url_capture else 0.0)
    if demo_mode:
        demo_rain = st.slider("Demo rainfall (mm/h)", 0.0, 30.0, default_slider, 0.1)
    else:
        demo_rain = 0.0

if demo_mode:
    settings = demo_settings()
else:
    try:
        settings = load_settings()
    except ConfigError as exc:
        st.error(str(exc))
        st.info("Enable **Demo storm mode** or open `?demo_mm=15` without an API key.")
        st.stop()

city = st.text_input("City", value=settings.default_city)
refresh = st.button("Refresh data", type="primary")

if auto_refresh and not demo_mode:
    try:
        from streamlit_autorefresh import st_autorefresh

        st_autorefresh(interval=300_000, key="exp1_autorefresh")
    except ImportError:
        st.sidebar.warning("Install streamlit-autorefresh for auto-refresh.")

need_load = refresh or "reading" not in st.session_state or url_capture
if need_load:
    if demo_mode:
        apply_demo_reading(city, demo_rain, settings, log=refresh or url_capture)
    else:
        try:
            reading = fetch_current_weather(city, settings, use_cache=False)
            alert = check_alert(reading.rainfall_mm_h, settings)
            log_alert(city, alert, settings)
            st.session_state.reading = reading
            st.session_state.alert = alert
            st.session_state.updated = datetime.now(timezone.utc)
            st.session_state.api_error = None
        except WeatherAPIError as exc:
            st.session_state.api_error = str(exc)

if st.session_state.get("api_error"):
    st.error(f"API error: {st.session_state.api_error}")

if st.session_state.get("reading"):
    r = st.session_state.reading
    a = st.session_state.alert
    st.subheader(f"Rainfall Monitor - {r.city}")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Current rainfall (mm/h)", f"{r.rainfall_mm_h:.2f}")
        st.caption(f"Source: {r.rain_field_used}")
    with c2:
        color = LEVEL_COLORS.get(a.level, "#888")
        st.markdown(
            f"### Alert: <span style='color:{color};font-weight:bold'>{a.level}</span>",
            unsafe_allow_html=True,
        )
        st.write(a.message)
    with c3:
        if st.session_state.get("updated"):
            st.metric(
                "Last update (UTC)",
                st.session_state.updated.strftime("%Y-%m-%d %H:%M:%S"),
            )
    st.caption(f"Weather: {r.description}")

df = alert_log_dataframe(settings.alert_log_path)
if df is not None and not df.empty:
    st.subheader("Alert statistics")
    render_stats(df)
    st.subheader("Rainfall history")
    chart_df = df.copy()
    chart_df["rainfall_mm_h"] = pd.to_numeric(chart_df["rainfall_mm_h"], errors="coerce")
    st.line_chart(chart_df.set_index("timestamp_utc")["rainfall_mm_h"], height=220)
    st.subheader("Recent log entries")
    st.dataframe(df.iloc[::-1].head(30), use_container_width=True)
else:
    rows = parse_alert_log_rows(settings.alert_log_path)
    if rows:
        st.dataframe(pd.DataFrame(rows).iloc[::-1], use_container_width=True)
    else:
        st.info("No alerts logged yet - click Refresh or use Demo storm mode.")
