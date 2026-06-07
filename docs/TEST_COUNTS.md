# Test Counts — Canonical Reference

**Mahmudul Hasan (4125999049)** · Use this page when a grader asks “how many tests?”

Verified: `pytest --collect-only` on 2026-05-31.

---

## One-sentence answer (safe for professors)

> **Capstone GitHub CI:** **33** automated pytest tests (`pytest -q` at repo root).  
> **Experiment appendix suites:** **114** pytest tests in `experiment1/files/` … `experiment4/files/`.  
> **Total verification tests:** **147** — only **33** run in GitHub Actions CI.

---

## Verification summary

| Scope | Command | Count |
|-------|---------|------:|
| Capstone CI (integrated app) | `pytest -q` (repo root) | **33** |
| Experiment 1 — Rainfall | `cd experiment1/files && pytest -q` | **25** |
| Experiment 2 — SCS-CN | `cd experiment2/files && pytest -q` | **27** |
| Experiment 3 — Reservoir | `cd experiment3/files && pytest -q` | **22** |
| Experiment 4 — Flood | `cd experiment4/files && pytest -q` | **40** |
| **Experiment subtotal** | | **114** |
| **Grand total** | | **147** |

---

## Capstone repository (GitHub CI)

Breakdown by file: `test_runoff.py` (11), `test_weather.py` (6), `test_flood.py` (5), `test_reservoir.py` (5), `test_integration.py` (4), `test_validation.py` (2), `conftest.py` (fixtures only).

**History:** Week 8 Session A report snapshot = **29** tests; expanded to **33** for Assignment 3 boundary + hallucination regression tests.

---

## Experiment appendix tests (in this repository)

Each `experimentN/files/` folder contains standalone pytest for that experiment (simulate/email, rational/AMC, rolling horizon, routing/GIF/DEM loader, etc.).

Evidence: per-experiment `audit_summary.txt`, README feature tables, and formal PDF reports.

---

## What to tell a grader

| Claim | Accurate? |
|-------|-----------|
| “This repo has 33 CI tests” | ✅ Run `pytest -q` at root |
| “Each experiment has its own test suite” | ✅ Run pytest inside `experimentN/files/` |
| “147 total verification tests” | ✅ 33 + 114 (not all in one CI job) |
| “Clone and `pytest -q` gives 147” | ❌ Root pytest collects **33** only |

---

## Related

| Document | Purpose |
|----------|---------|
| [PHYSICAL_VALIDATION.md](PHYSICAL_VALIDATION.md) | 18 physical constraint checks |
| [assignment3/EVIDENCE_CHAIN.md](../assignment3/EVIDENCE_CHAIN.md) | Hallucination evidence |
| [GRADER_AUDIT.md](GRADER_AUDIT.md) | Consistency audit log |
