# Assignment 3 — Swiss Cheese Test Suite

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026  
**Course:** AI-Augmented Software Engineering · **Weight:** 20% · **Due:** Week 12

---

## What this folder is

Assignment 3 is **not** “write some pytest files.” It proves you used **layered verification** to catch **AI-generated mistakes** before trusting hydrology code.

| File | Purpose |
|------|---------|
| [EVIDENCE_CHAIN.md](EVIDENCE_CHAIN.md) | Prompt → AI output → test → failure → fix |
| [evidence/](evidence/) | **buggy_rainfall.py** + **rainfall_fixed.py** in repo |
| [SWISS_CHEESE_REPORT.md](SWISS_CHEESE_REPORT.md) | Full narrative: layers, test strategy, evidence |
| [HALLUCINATION_CASE_STUDY.md](HALLUCINATION_CASE_STUDY.md) | Primary case study (AI claim → test → failure → fix) |
| [SWISS_CHEESE_REPORT.pdf](SWISS_CHEESE_REPORT.pdf) | PDF for LMS upload (compile from `.tex`) |
| [HALLUCINATION_CASE_STUDY.pdf](HALLUCINATION_CASE_STUDY.pdf) | PDF case study (compile from `.tex`) |

---

## Swiss Cheese layers (this project)

```text
AI-generated code
      ↓
Layer 1 — Human / AI review     (units, formulas, AGENTS.md)
      ↓
Layer 2 — Unit & boundary tests     33 capstone tests (+ 88 experiment tests — see docs/TEST_COUNTS.md)
      ↓
Layer 3 — Physical validity     (src/validation.py)
      ↓
Layer 4 — Integration tests     (tests/test_integration.py)
      ↓
Layer 5 — Validation CLI        (experiment validate_* scripts)
      ↓
Trusted result
```

---

## Test code locations

**The code and tests are NOT inside `assignment3/`** — they live in the main capstone tree (built in Week 8 Session A). This folder is the **submission narrative** that points graders to the evidence.

| What | Path | Count |
|------|------|------:|
| **Capstone tests (Assignment 3 focus)** | [`../tests/`](../tests/) | **33** |
| Application code | [`../src/`](../src/), [`../app/`](../app/) | — |
| Physical rules layer | [`../src/validation.py`](../src/validation.py) | 4 validators |
| Hallucination regression test | [`../tests/test_runoff.py`](../tests/test_runoff.py) → `test_hallucination_cn95_p6_produces_runoff` | 1 |
| Full experiment suite | local `ai_water_lab/experiment*/tests/` | **88** total |

Run capstone tests:

```bash
cd smart-water-capstone
pytest -q --cov=src --cov-report=term-missing
```

---

## Hallucination requirement (≥1)

**Primary documented case:** SCS-CN initial-abstraction assumption — see [HALLUCINATION_CASE_STUDY.md](HALLUCINATION_CASE_STUDY.md).

**Additional AI errors caught:** [../assignment4/AI_FAILURES.md](../assignment4/AI_FAILURES.md) (9 total across experiments + capstone).

---

## Related

| Resource | Link |
|----------|------|
| Prompt log (Week 8A) | [../prompt_log.md](../prompt_log.md) |
| Jagged Frontier | [../docs/JAGGED_FRONTIER.md](../docs/JAGGED_FRONTIER.md) |
| Assignment 4 capstone | [../assignment4/README.md](../assignment4/README.md) |
| Test counts | [docs/TEST_COUNTS.md](../docs/TEST_COUNTS.md) |
| Grader audit | [docs/GRADER_AUDIT.md](../docs/GRADER_AUDIT.md) |
| GitHub repo | https://github.com/mahmud456alhasan-debug/smart-water-capstone |

---

## Regenerate PDFs

```bash
cd assignment3
pdflatex SWISS_CHEESE_REPORT.tex && pdflatex SWISS_CHEESE_REPORT.tex
pdflatex HALLUCINATION_CASE_STUDY.tex && pdflatex HALLUCINATION_CASE_STUDY.tex
```
