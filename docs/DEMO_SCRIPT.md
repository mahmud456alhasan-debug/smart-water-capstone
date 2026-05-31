# Live Demo Script — 5-Minute Defense

**Before class:** `cd capstone && streamlit run app/main.py`  
**URL:** http://localhost:8501  
**Timer:** Align with [PRESENTATION_OUTLINE.md](PRESENTATION_OUTLINE.md)

---

## Tab 1: Weather & Alerts (~15 s) — demo block 2:00–2:15

1. Point to rainfall table (5 rows).
2. Line chart peak **22 mm** at 10:00.
3. Say: "Amber 10 mm/h, red 20 mm/h — peak triggers **RED** watch."

---

## Tab 2: Runoff SCS-CN (~15 s) — 2:15–2:30

1. **P = 50 mm**, **CN = 80**.
2. Say: "Hand-validated **Q ≈ 13.8 mm**; physical check **Q ≤ P** is green."
3. Optional: mention sensitivity plot.

---

## Tab 3: Reservoir (~15 s) — 2:30–2:45

1. Eco flow **10 m³/s** (default).
2. Say: "Seven-day dispatch; revenue **~$708,849**; validation **PASS**."
3. Scroll day-7 release in schedule table.

---

## Tab 4: Flood map (~15 s) — 2:45–3:00

1. Flood level **50 m** — note flooded %.
2. Move to **60 m** — flooded % **increases** (monotonic rule).
3. Say: "DEM from Week 6; wet cells where elevation < stage."

---

## If something breaks

```bash
pytest -q    # expect 33 passed
```

Show backup PNGs:
- `lab_reports/week7_session_b_Streamlit_page.png`
- `lab_reports/week8_session_a_terminal.png`

Mention: `docs/PHYSICAL_VALIDATION.md` lists 18 constraint checks.

---

## One-line summary

"Four labs, one dashboard, 33 tests, nine AI corrections documented — repo on GitHub."
