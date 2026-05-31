# Code Attribution — AI vs Human

**Mahmudul Hasan (4125999049)**

Which code was **AI-generated** (with human review) vs **written/adjusted manually** — required for honest Assignment 3 & 4 grading.

**Primary tool:** Cursor Agent (Weeks 7–8 capstone). **OpenCode:** Week 1–2 labs only (optional). **ChatGPT/Gemini:** rubric review only.

---

## Capstone (`smart-water-capstone/`)

| File / area | Origin | Human role |
|-------------|--------|------------|
| `app/main.py` | AI scaffold (7A) + AI implementation (7B) | Verified tab wiring, restarted Streamlit |
| `src/runoff/scs_cn.py` | AI from Week 5 lab logic | Reviewed Q≤P cap, Ia branch |
| `src/weather/`, `src/reservoir/`, `src/flood/` | AI wired from prior lab modules | Unit checks, DEM copy |
| `src/validation.py` | AI (Week 8A) | Defined physical rules list |
| `tests/*.py` (33 tests) | AI draft (Week 8A) | **Caught Ia assumption error**, added boundary cases |
| `AGENTS.md`, `README.md` | AI draft | Edited scope, links |
| `prompt_log.md` | **Human-written** log of AI sessions | Required course deliverable |
| `docs/JAGGED_FRONTIER.md` | AI draft + human edit | Reflection |
| Git push, LMS, live demo | **Human only** | — |

---

## Assignment 3 — hallucination cases (full chain)

### Case B — Wrong AI **code** (strongest)

| Step | Artifact | Path |
|------|----------|------|
| **Prompt** | “Walk through buggy code line by line…” | `lab_reports/prompt_log_week2_session_a.md` |
| **AI-style wrong output** | `S = 25400 * CN - 254` | [`evidence/buggy_rainfall.py`](evidence/buggy_rainfall.py) |
| **Failure evidence** | Terminal Q ≈ 0.002 mm (expected ~43.6) | `python3 assignment3/evidence/buggy_rainfall.py` |
| **Corrected code** | `S = 25400 / CN - 254`, proper Ia, Q≤P | [`evidence/rainfall_fixed.py`](evidence/rainfall_fixed.py) → `src/runoff/scs_cn.py` |
| **Tests catching it** | Hand check + 20 Exp2 pytest + capstone runoff tests | `submission/.../test_scscn.py`, `tests/test_runoff.py` |

### Case A — Wrong AI **assumption** (Week 8)

| Step | Artifact | Path |
|------|----------|------|
| **Prompt** | “Write pytest… edge, invalid, physical cases” | `prompt_log.md` Week 8A |
| **AI-assisted wrong belief** | “P=5 mm, CN=95 → Q=0 always” | `prompt_log.md`, Week 8A report |
| **Failure reproduced** | `assert scs_runoff_mm(5,95)==0` fails | `assignment3/scripts/demo_wrong_assumption_fails.py` |
| **Corrected tests** | P=2/CN=80 for zero case; regression test | `tests/test_runoff.py` → `test_hallucination_cn95_p6_produces_runoff` |
| **Production code** | `scs_cn.py` was already correct | No formula change — **test design** fixed |

---

## Experiments 1–4 (local `ai_water_lab/`)

| Experiment | AI generated | Human verified |
|------------|--------------|----------------|
| Exp 1 | API client, alert logic | Missing `rain` → 0; forecast added |
| Exp 2 | SCS-CN module | Formula, Q≤P, reference 13.80 mm |
| Exp 3 | Optimizer scaffold | trust-constr, feasible x₀ |
| Exp 4 | DEM flood sim | depth ≥ 0, monotonic 9/9 |

Full table: [assignment4/AI_FAILURES.md](../assignment4/AI_FAILURES.md)

---

## If the grader asks one sentence

> “AI wrote most of the capstone scaffold and tests; I verified every hydrology rule with pytest, `validation.py`, and hand calculations, and documented nine corrections where AI was wrong.”

See also: [EVIDENCE_CHAIN.md](EVIDENCE_CHAIN.md)
