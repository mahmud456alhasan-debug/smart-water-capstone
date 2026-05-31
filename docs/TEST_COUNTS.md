# Test Counts — Canonical Reference

**Mahmudul Hasan (4125999049)** · Use this page when a grader asks “how many tests?”

Verified: `pytest --collect-only` on 2026-05-31.

---

## One-sentence answer

> **33** pytest cases in the capstone repo (`tests/`); **88** pytest cases across the four experiment codebases (local `ai_water_lab/experiment*`); **121** total pytest in the full Smart Water project.

---

## Capstone repository (GitHub)

| Scope | Command | Count |
|-------|---------|------:|
| Capstone pytest | `cd capstone && pytest -q` | **33** |

Breakdown by file: `test_runoff.py` (10), `test_weather.py` (6), `test_flood.py` (5), `test_reservoir.py` (5), `test_integration.py` (3), `test_validation.py` (2), `conftest.py` (fixtures only).

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

## What README “88 tests” means

The homepage **Key metrics** row **Automated tests: 88** refers to the **four specialized experiments**, consistent with the portfolio case study.

The **capstone** suite (**33** tests) is what runs in GitHub Actions on this repository.

---

## Related

| Document | Purpose |
|----------|---------|
| [PHYSICAL_VALIDATION.md](PHYSICAL_VALIDATION.md) | 18 physical constraint checks |
| [assignment3/EVIDENCE_CHAIN.md](../assignment3/EVIDENCE_CHAIN.md) | Hallucination evidence |
| [GRADER_AUDIT.md](GRADER_AUDIT.md) | Consistency audit log |
