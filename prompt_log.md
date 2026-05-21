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

**GitHub URL:** `REPLACE_WITH_YOUR_REPO_URL` *(fill after you push)*

**Planned repo name:** `smart-water-capstone`

**Commit message:** `Week 7 Session A: capstone scope and architecture`

---

## Lessons learned

Planning works best when capstone scope explicitly reuses lab modules instead of starting a new stack. Documenting wet-cell and unit conventions early avoids Week 8 debugging. Cursor can generate scaffold and report artifacts in one session; GitHub push and one screenshot remain manual. Cross-checking architecture with a second LLM (ChatGPT/Gemini) is optional but useful before Session B coding.
