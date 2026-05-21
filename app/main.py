"""Streamlit entry point — Week 7 Session B will implement tabs."""

import streamlit as st

st.set_page_config(page_title="Smart Water Capstone", layout="wide")
st.title("Smart Water Integrated Dashboard")
st.caption("Mahmudul Hasan (4125999049) — capstone scaffold (Week 7 Session A)")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Weather & Alerts", "Runoff (SCS-CN)", "Reservoir", "Flood map"]
)

with tab1:
    st.info("Week 7 Session B: wire src.weather")
with tab2:
    st.info("Week 7 Session B: wire src.runoff")
with tab3:
    st.info("Week 7 Session B: wire src.reservoir")
with tab4:
    st.info("Week 7 Session B: wire src.flood")
