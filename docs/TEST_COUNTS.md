# Test Counts — Canonical Reference

**Mahmudul Hasan (4125999049)** · Use this page when a grader asks “how many tests?”

Verified: `pytest --collect-only` on 2026-05-31.

---

## One-sentence answer (safe for professors)

> **Capstone GitHub repository:** **33** automated pytest tests (`pytest -q` in this repo).  
> **Additional experiment development folders** (local `ai_water_lab/experiment*`, not in this repo): **88** pytest tests.  
> **Total verification tests:** **121** — only **33** run in this repo’s CI.

---

## Capstone repository (GitHub)

| Scope | Command | Count |
|-------|---------|------:|
| Capstone pytest | `cd capstone && pytest -q` | **33** |

Breakdown by file: `test_runoff.py` (11), `test_weather.py` (6), `test_flood.py` (5), `test_reservoir.py` (5), `test_integration.py` (4), `test_validation.py` (2), `conftest.py` (fixtures only).

**History:** Week 8 Session A report snapshot = **29** tests; expanded to **33** for Assignment 3 boundary + hallucination regression tests.

---

## Experiment codebases (local `ai_water_lab/`, not duplicated in capstone repo)

| Experiment | Folder | pytest count |
|------------|--------|-------------:|
| Exp 1 Rainfall | `experiment1_rainfall_alert/` | 20 |
| Exp 2 SCS-CN | `experiment2_scscn_runoff/` | 23 |
| Exp 3 Reservoir | `experiment3_reservoir_optimization/` | 23 |
| Exp 4 Flood | `experiment4_flood_inundation/` | 22 |
| **Subtotal** | | **88** |

Evidence in formal reports: [`submission/portfolio/AI_Engineering_Portfolio.md`](../submission/portfolio/AI_Engineering_Portfolio.md)

---

## What “88 tests” means

**88** = supplementary pytest in local experiment development folders (not run in this repo’s GitHub CI).

**33** = automated tests in this capstone repository (`pytest -q`).

See portfolio PDF for experiment-level test evidence.

---

## Related

| Document | Purpose |
|----------|---------|
| [PHYSICAL_VALIDATION.md](PHYSICAL_VALIDATION.md) | 18 physical constraint checks |
| [assignment3/EVIDENCE_CHAIN.md](../assignment3/EVIDENCE_CHAIN.md) | Hallucination evidence |
| [GRADER_AUDIT.md](GRADER_AUDIT.md) | Consistency audit log |
