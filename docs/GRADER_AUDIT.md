# Grader Audit — Assignments 3 & 4

**Adversarial review** (2026-05-31): inconsistencies found and fixes applied.

---

## Fixed before submission

| Issue | Severity | Fix |
|-------|----------|-----|
| Test counts 29/30/33/88 mixed in docs | **High** | Canonical page: [TEST_COUNTS.md](TEST_COUNTS.md) |
| `buggy_rainfall.py` not in repo (only local week2) | **High** | Copied to `assignment3/evidence/` |
| README said `tests/` = 88 | **High** | Clarified: 88 = experiments, 33 = capstone |
| EVIDENCE_CHAIN linked missing `week2_session_a_files/` | **Medium** | Links → `assignment3/evidence/` |
| Assignment 3 .tex files stale (29 tests) | **Low** | Recompile after .tex update (optional LMS) |

---

## Intentionally unchanged (historical snapshots)

| Item | Why left as-is |
|------|----------------|
| `lab_reports/Week8_SessionA_Report.pdf` | Week 8 lab deliverable at **29** tests — historical |
| `week8_session_a_terminal.png` | Screenshot from Session 8A session |
| `prompt_log.md` Week 8A “29 passed” | Accurate for that session; see note at end of section |

---

## Grader checklist — Assignment 3

- [x] Real tests in `tests/` — **33** passing
- [x] Reproducible failure — `assignment3/scripts/demo_wrong_assumption_fails.py`
- [x] Wrong AI code in repo — `assignment3/evidence/buggy_rainfall.py`
- [x] Fixed code in repo — `assignment3/evidence/rainfall_fixed.py` + `src/runoff/scs_cn.py`
- [x] Evidence chain — `assignment3/EVIDENCE_CHAIN.md`
- [x] Code attribution — `assignment3/CODE_ATTRIBUTION.md`

---

## Grader checklist — Assignment 4

- [x] App runs — `streamlit run app/main.py`
- [x] AGENTS.md, prompt_log.md, JAGGED_FRONTIER.md
- [x] Physical rules — [PHYSICAL_VALIDATION.md](PHYSICAL_VALIDATION.md)
- [x] AI failures table — [assignment4/AI_FAILURES.md](../assignment4/AI_FAILURES.md)
- [x] Demo script — [PRESENTATION_OUTLINE.md](PRESENTATION_OUTLINE.md)
- [ ] **Live 5-min presentation** — student must rehearse

---

## Remaining weak spots (honest)

| Item | Risk | Mitigation |
|------|------|------------|
| Experiments not in capstone repo | Grader may not see 88 tests | Point to portfolio + local paths in TEST_COUNTS.md |
| Case A = test-design assumption, not wrong code | Slightly weaker than Case B | Lead with Case B (`buggy_rainfall.py`) |
| GitHub About / Release empty | Presentation | Manual — GITHUB_SETUP.md |
| No PDF compiled for assignment3/4 | LMS upload | Run pdflatex in assignment3/ and assignment4/ |

---

## Quick verify commands

```bash
pytest -q                                    # 33 passed
python3 assignment3/evidence/buggy_rainfall.py
python3 assignment3/evidence/rainfall_fixed.py
python3 assignment3/scripts/demo_wrong_assumption_fails.py   # exit 1 expected
```
