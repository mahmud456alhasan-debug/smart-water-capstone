# 5-Minute Presentation Outline — Smart Water Capstone

**Student:** Mahmudul Hasan (4125999049)  
**Total time:** 5 minutes

---

## 1. Introduction and problem (1 min)

**Say:**
- "I built an integrated Smart Water dashboard for teaching and demo flood-risk screening."
- "Problem: rainfall, runoff, reservoir operations, and flood extent were separate lab scripts."
- "Solution: one Streamlit app reusing Weeks 3–6 modules with tests and physical validation."

**Show:** Title slide or GitHub repo URL.

---

## 2. Live demo (2 min)

Follow `DEMO_SCRIPT.md` — suggested order:

1. **Weather & Alerts** — sample CSV, RED alert at 22 mm/h  
2. **Runoff** — P=50 mm, CN=80, show Q <= P  
3. **Reservoir** — 7-day schedule, ~$708,849, PASS  
4. **Flood map** — slider 40 / 50 / 60 m, flooded %

**Backup:** Screenshots if Streamlit fails (`week7_session_b_Streamlit_page.png`, pytest 96%).

---

## 3. AI collaboration highlights (1 min)

**Say:**
- Used **Cursor Agent** (not OpenCode required).
- **Week 7A:** scope, architecture, GitHub scaffold.
- **Week 7B:** wired four tabs from prior labs.
- **Week 8A:** 29 tests, 96% coverage; caught bad assumption (P=5 mm vs Ia).
- **AGENTS.md** + **prompt_log.md** document prompts and fixes.

---

## 4. Tool evaluation and lessons (1 min)

**Say:**
- AI strong at: scaffolding, boilerplate tests, SciPy structure from lab guides.
- AI weak at: unit edge cases (SCS-CN Ia), mixed MCM/m3/s without explicit prompts.
- **Swiss Cheese:** code review + pytest + `validation.py` + integration tests.
- **Jagged Frontier:** see `JAGGED_FRONTIER.md`.

**Close:** "Repo and tests are public; app runs with `streamlit run app/main.py`."

---

## Timing checklist

| Block | Target |
|-------|--------|
| Intro | 0:00–1:00 |
| Demo | 1:00–3:00 |
| AI story | 3:00–4:00 |
| Lessons | 4:00–5:00 |
