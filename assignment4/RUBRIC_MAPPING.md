# Rubric Mapping — Assignment 4 Final Capstone

**Mahmudul Hasan (4125999049)** · Smart Water Lab

Maps course rubric criteria to **exact evidence** in this repository.

---

## Grading rubric (40% total)

### 1. Technical Implementation — 30%

| Criterion | Evidence | Location |
|-----------|----------|----------|
| Code runs | Streamlit app starts; pytest green | `streamlit run app/main.py` · `pytest -q` → **33 passed** |
| Architecture sound | Modular `src/`, tabbed UI, pipeline diagram | [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) · [assets/smart_water_pipeline.png](../assets/smart_water_pipeline.png) |
| Outputs correct | Rainfall alerts, runoff Q, reservoir dispatch, flood maps | [README gallery](../README.md#platform-gallery) |
| Integrated pipeline | Four modules in one dashboard | [app/main.py](../app/main.py) |
| CI | GitHub Actions test workflow | [.github/workflows/tests.yml](../.github/workflows/tests.yml) |

---

### 2. AI Collaboration Log — 30%

| Criterion | Evidence | Location |
|-----------|----------|----------|
| AGENTS.md used during development | Agent instructions, validation rules | [AGENTS.md](../AGENTS.md) |
| Prompt log | Sessions 7A, 7B, 8A, 8B documented | [prompt_log.md](../prompt_log.md) |
| AI errors corrected | 9 documented corrections | [AI_FAILURES.md](AI_FAILURES.md) |
| Jagged Frontier reflection | Where AI excelled vs failed | [docs/JAGGED_FRONTIER.md](../docs/JAGGED_FRONTIER.md) |
| Case study (extended) | Statistics, threats to validity | [submission/portfolio/AI_Engineering_Portfolio.pdf](../submission/portfolio/AI_Engineering_Portfolio.pdf) |
| Tool comparison | Cursor, ChatGPT, OpenCode notes | JAGGED_FRONTIER § Tool comparison |

---

### 3. Physical Validity — 20%

| Rule | Enforcement | Location |
|------|-------------|----------|
| Runoff Q ≤ rainfall P | `validate_runoff_mm`, pytest | [src/validation.py](../src/validation.py) · [tests/test_runoff.py](../tests/test_runoff.py) |
| Storage within bounds | V_MIN ≤ S ≤ V_MAX | `validate_storage_mcm` |
| Flood extent monotonic with stage | Rising water → non-decreasing wet cells | `validate_flood_monotonic` · Exp 4 **9/9 PASS** |
| Alert thresholds physically ordered | GREEN < YELLOW < RED mm/h | [tests/test_weather.py](../tests/test_weather.py) |
| Reference hand-check | Q = **13.80 mm** at P = 50, CN = 80 | Exp 2 report + `validate_reference` CLI |
| Reservoir revenue band | Expected USD range after optimize | `validate_reservoir_result` |

Full validation narrative: [docs/ENGINEERING.md](../docs/ENGINEERING.md)

---

### 4. Presentation — 20%

| Criterion | Evidence | Location |
|-----------|----------|----------|
| 5-minute structure | Intro → demo → AI → lessons | [docs/PRESENTATION_OUTLINE.md](../docs/PRESENTATION_OUTLINE.md) |
| Live demo script | Four Streamlit tabs, timing | [docs/DEMO_SCRIPT.md](../docs/DEMO_SCRIPT.md) |
| Tool evaluation | AI tools compared in reflection | [docs/JAGGED_FRONTIER.md](../docs/JAGGED_FRONTIER.md) |
| Backup evidence | Screenshots if live demo fails | `lab_reports/week7_session_b_Streamlit_page.png`, `week8_session_a_terminal.png` |

**Student action:** timed rehearsal + live defense (not in repo).

---

## Assignment 4 deliverable checklist

| Deliverable | Required | Evidence |
|-------------|:--------:|----------|
| Code repository | ✓ | GitHub |
| Documentation | ✓ | README, docs/ |
| AGENTS.md | ✓ | Root + per-experiment in submission |
| Prompt log | ✓ | prompt_log.md |
| Jagged Frontier report | ✓ | docs/JAGGED_FRONTIER.md |
| Live demo | ✓ | You present; script in docs/ |

---

## Related assignments

| Assignment | Package |
|------------|---------|
| Assignment 3 — Swiss Cheese Test Suite | [assignment3/README.md](../assignment3/README.md) |
| Assignment 1 — Reasoning Log | lab_reports Weeks 1–2 |
| Assignment 2 — Legacy modernization | lab_reports Week 4 Session A |
