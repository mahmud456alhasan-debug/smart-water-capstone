"""Smart Water Capstone — Streamlit dashboard (Week 7 Session B)."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.flood.inundation import flood_statistics, load_dem, simulate_flood
from src.reservoir.wrapper import run_baseline_schedule
from src.runoff.scs_cn import scs_runoff_mm
from src.weather.alerts import alert_level
from src.weather.load import load_rainfall_csv

DATA_CSV = ROOT / "data" / "sample_rainfall.csv"
DEM_PATH = ROOT / "data" / "dem.npy"

st.set_page_config(page_title="Smart Water Capstone", layout="wide")
st.title("Smart Water Integrated Dashboard")
st.caption("Mahmudul Hasan (4125999049) | Week 7 Session B")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Weather & Alerts", "Runoff (SCS-CN)", "Reservoir", "Flood map"]
)

with tab1:
    st.subheader("Rainfall sample & alerts")
    df = load_rainfall_csv(str(DATA_CSV))
    st.dataframe(df, use_container_width=True)
    max_mm = float(df["rainfall_mm"].max())
    st.line_chart(df.set_index("datetime")["rainfall_mm"])
    amber = st.slider("Amber threshold (mm/h)", 5.0, 30.0, 10.0, 0.5)
    red = st.slider("Red threshold (mm/h)", 10.0, 50.0, 20.0, 0.5)
    result = alert_level(max_mm, amber=amber, red=red)
    colors = {"GREEN": "green", "AMBER": "orange", "RED": "red"}
    st.markdown(
        f"**Alert:** :{colors.get(result.level, 'blue')}[{result.level}] — {result.message}"
    )

with tab2:
    st.subheader("SCS-CN runoff")
    p_mm = st.number_input("Storm rainfall depth P (mm)", 0.0, 200.0, 50.0, 1.0)
    cn = st.number_input("Curve number CN", 1.0, 100.0, 80.0, 1.0)
    try:
        q_mm = scs_runoff_mm(p_mm, cn)
        st.metric("Runoff Q (mm)", f"{q_mm:.2f}")
        st.metric("Runoff / rainfall", f"{(q_mm / p_mm * 100) if p_mm else 0:.1f} %")
        if q_mm > p_mm + 1e-6:
            st.error("Invalid: runoff exceeds rainfall")
        else:
            st.success("Physical check: Q <= P")
        cn_sweep = np.arange(60, 96, 5)
        qs = [scs_runoff_mm(p_mm, c) for c in cn_sweep]
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.plot(cn_sweep, qs, "o-")
        ax.set_xlabel("Curve number CN")
        ax.set_ylabel("Runoff Q (mm)")
        ax.set_title(f"SCS-CN sensitivity at P={p_mm:.0f} mm")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    except (ValueError, TypeError) as exc:
        st.error(str(exc))

with tab3:
    st.subheader("7-day reservoir dispatch")
    eco = st.slider("Eco minimum release (m3/s)", 5.0, 15.0, 10.0, 0.5)
    out = run_baseline_schedule(eco_flow_m3s=eco)
    st.metric("Total revenue (USD)", f"${out['total_revenue_usd']:,.2f}")
    st.metric("Validation", out["validation"])
    st.metric("Min storage slack (MCM)", f"{out['storage_slack_mcm']:.3f}")
    st.dataframe(pd.DataFrame(out["schedule"]), use_container_width=True)

with tab4:
    st.subheader("Flood inundation map")
    dem = load_dem(str(DEM_PATH))
    elev_min, elev_max = float(dem.min()), float(dem.max())
    level = st.slider(
        "Flood level (m, absolute stage)",
        elev_min,
        elev_max,
        50.0,
        0.5,
    )
    mask, depth = simulate_flood(dem, level)
    stats = flood_statistics(dem, mask, depth, level)
    c1, c2, c3 = st.columns(3)
    c1.metric("Flooded %", f"{stats.flooded_percent:.2f}")
    c2.metric("Mean depth on wet (m)", f"{stats.mean_depth_m:.2f}")
    c3.metric("Wet cells", stats.wet_cell_count)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.imshow(dem, cmap="gray", origin="lower")
    depth_ma = np.ma.masked_where(~mask, depth)
    im = ax.imshow(depth_ma, cmap="Blues", origin="lower", alpha=0.65, vmin=0)
    ax.set_title(f"Flood level {level:.1f} m")
    fig.colorbar(im, ax=ax, label="Depth (m)")
    st.pyplot(fig)
    plt.close(fig)
