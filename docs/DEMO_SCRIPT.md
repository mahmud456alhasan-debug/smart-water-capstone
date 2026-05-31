# Live Demo Script — Streamlit

**Before class:** `cd capstone && streamlit run app/main.py`  
**URL:** http://localhost:8501

---

## Tab 1: Weather & Alerts (~30 s)

1. Point to the rainfall table (5 rows).
2. Point to the line chart — peak **22 mm** at 10:00.
3. Say: "Amber at 10 mm/h, red at 20 mm/h — peak triggers **RED** flood watch."
4. Optional: move sliders to show GREEN at lower thresholds.

---

## Tab 2: Runoff SCS-CN (~30 s)

1. Set **P = 50 mm**, **CN = 80**.
2. Say: "SCS-CN runoff from Week 5; physical check **Q <= P** shows green."
3. Briefly show sensitivity plot vs CN.

---

## Tab 3: Reservoir (~30 s)

1. Eco flow **10 m3/s** (default).
2. Say: "Seven-day dispatch from Week 6; total revenue about **$708,849**, validation **PASS**."
3. Scroll schedule table — day 7 feasible release.

---

## Tab 4: Flood map (~30 s)

1. Flood level **50 m** — note flooded %.
2. Move to **60 m** — flooded % increases (monotonic).
3. Say: "DEM inundation from Week 6; wet cells use elevation <= stage."

---

## If something breaks

- Run `pytest -q` in terminal (29 passed).
- Show backup PNG: Streamlit screenshot, GitHub repo, pytest 96% coverage.

---

## One-line summary

"Four labs, one dashboard, tested and on GitHub."
