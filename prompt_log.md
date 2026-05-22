# Prompt Log - Week 7 Session A (Capstone Planning)

**Student:** Mahmudul Hasan (4125999049)  
**Tool:** Cursor Agent (Auto); OpenCode not used

---

## Exercise 1 - Project scope

**AI used?** Partial — scope drafted from completed Weeks 3--6 lab work, then saved to `SCOPE.md`.

**Prompt (summary):** Integrate week5_session_a_lab1 (weather/alerts), week5_session_b_lab2 (SCS-CN), week6_session_a_lab3 (reservoir), week6_session_b_lab4 (flood) into one Streamlit capstone; list functional/non-functional requirements and scope boundaries.

**Output file:** `SCOPE.md`

**Changes made:** Fixed title "Smart Water Integrated Dashboard"; excluded production deployment and real GIS DEM from scope.

---

## Exercise 2 - Architecture design

**Date:** 2026-05-21

**Prompt (from lab guide, filled):**

```text
I want to build a Smart Water Integrated Monitoring and Decision Support Dashboard.

Requirements:
1. Load or fetch rainfall/weather data (CSV default; optional API).
2. Compute SCS-CN runoff with physical checks (runoff <= rainfall).
3. Run 7-day reservoir release optimization (scipy; MCM storage; m3/s flows).
4. Flood inundation from 100x100 synthetic DEM and flood_level (m).
5. Streamlit UI with tabs: Weather/Alerts, Runoff, Reservoir, Flood map.
6. prompt_log.md and AGENTS.md for AI-assisted development.

Please help me design:
1. System architecture diagram (describe components)
2. Directory structure
3. Main modules and their responsibilities
4. Data flow between components
5. Technology stack recommendations
6. API design (if applicable)
```

**Summary:** Five-layer flow (weather → runoff → reservoir → flood → Streamlit). Modular `src/` packages mapped to prior labs. Internal Python function API; CSV-first for reproducibility.

**Output file:** `ARCHITECTURE.md`

**Changes made:** ASCII diagram for LaTeX/report compatibility; no FastAPI (unlike week2 demo) to keep capstone scope teachable.

---

## Exercise 3 - Technical plan / scaffold

**Prompt (from lab guide):**

```text
Based on our architecture design, please generate:
1. Complete directory structure
2. Main file templates with docstrings
3. requirements.txt with all dependencies
4. README.md with setup instructions
5. Initial AGENTS.md template
6. Sample data files (if needed)

Make it ready for development in Week 7 Session B. Python 3.8+, Streamlit, numpy, pandas, matplotlib, scipy.
```

**Summary:** Created `app/main.py` stub, `src/{weather,runoff,reservoir,flood}` packages, `tests/`, `data/sample_rainfall.csv`, README, AGENTS.md, requirements.txt.

**Changes made:** Stubs only — implementation deferred to Session B.

---

## Exercise 4 - Repository

**GitHub URL:** https://github.com/mahmud456alhasan-debug/smart-water-capstone

**Planned repo name:** `smart-water-capstone`

**Commit message:** `Week 7 Session A: capstone scope and architecture`

**Push result:** `main` branch, 30 objects, tracking `origin/main`.

**Report screenshots:** `week7_session_a_github_page_a.png` (file tree), `week7_session_a_github_page_b.png` (README).

---

## Lessons learned

Planning works best when capstone scope explicitly reuses lab modules instead of starting a new stack. Documenting wet-cell and unit conventions early avoids Week 8 debugging. Cursor can generate scaffold and report artifacts in one session; GitHub push and one screenshot remain manual. Cross-checking architecture with a second LLM (ChatGPT/Gemini) is optional but useful before Session B coding.

---

# Week 7 Session B — Core Development

**Tool:** Cursor Agent | **Date:** 2026-05-22

## Feature: pytest path + modules

**Issue:** `ModuleNotFoundError: No module named 'src'` when running `pytest -q`.

**Fix:** Added `pytest.ini` (`pythonpath = .`) and `conftest.py` to insert project root on `sys.path`. Same pattern in `app/main.py` for Streamlit.

**Result:** `2 passed in 0.11s`

## Feature: Streamlit four-tab dashboard

**Prompt (summary):** Wire Week 5–6 lab logic into capstone `src/` packages and replace `app/main.py` stubs with Weather, Runoff, Reservoir, and Flood tabs.

**Implementation:**
- `src/runoff/scs_cn.py` — full SCS-CN with Q <= P
- `src/reservoir/optimizer.py` + `wrapper.py` — 7-day schedule (~$708,849)
- `src/flood/inundation.py` — DEM load + map
- `src/weather/` — CSV load + GREEN/AMBER/RED alerts
- `data/dem.npy` copied from week6_session_b_lab4

**Run:** `streamlit run app/main.py` → http://localhost:8501

**GitHub push:** commit `408f211` on `main` — https://github.com/mahmud456alhasan-debug/smart-water-capstone

**Screenshot:** `week7_session_b_Streamlit_page.png` (Weather & Alerts tab, RED alert at 22 mm/h)

## Lessons learned (Session B)

Add `pytest.ini` early when using a `src/` layout. Restart Streamlit after code changes. One screenshot of the dashboard plus `pytest -q` terminal output is enough for submission.
