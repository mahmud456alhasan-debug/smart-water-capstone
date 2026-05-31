# Swiss Cheese Test Suite — Assignment 3 Report

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026

---

## 1. Assignment objective

Use AI to generate hydrology code, then **attack it** with a multi-layer test strategy until at least **one AI hallucination or false assumption** is exposed and corrected.

The Swiss Cheese model: each verification layer has holes, but **stacked layers** catch errors that slip through a single check.

---

## 2. AI-generated code under test

**Tool used:** Cursor Agent (course-allowed AI assistant; OpenCode not required).

**Prompt (Week 8 Session A, from lab guide):**

> Write pytest tests with normal, edge, invalid, and physical cases; fixtures; target >80% coverage for capstone `src/` functions.

**AI also generated / extended:** `src/runoff/scs_cn.py`, `src/validation.py`, and test modules in `tests/`.

---

## 3. Verification layers implemented

| Layer | Implementation | What it catches |
|-------|----------------|-----------------|
| **1 — Review** | Manual read of SCS-CN, reservoir units, flood mask logic | Wrong formulas, API keys, unit mix-ups |
| **2 — Unit tests** | **33** pytest cases in `tests/` | Edge inputs, type errors, regression |
| **3 — Physical validity** | `src/validation.py` | Q ≤ P, storage bounds, monotonic flood extent |
| **4 — Integration** | `tests/test_integration.py` | End-to-end rainfall → alert, reservoir wrapper |
| **5 — Coverage gate** | `pytest --cov=src` | Untested modules (weather, reservoir were 0% early) |

---

## 4. Boundary & physical test design

Tests intentionally target **jagged edges** where LLMs fail:

### Runoff (`tests/test_runoff.py`)

| Test | Category | Rule enforced |
|------|----------|---------------|
| `test_runoff_zero_rainfall` | Boundary | P = 0 → Q = 0 |
| `test_runoff_below_initial_abstraction` | Boundary | P below Ia → Q = 0 |
| `test_runoff_normal_storm` | Normal + physical | 0 < Q < P at P = 50, CN = 80 |
| `test_runoff_not_exceed_rainfall_high_cn` | Physical + extreme CN | Q ≤ P for CN = 60, 80, 95 |
| `test_runoff_negative_p_raises` | Invalid input | P < 0 → ValueError |
| `test_runoff_invalid_cn_raises` | Invalid input | CN outside [1, 100] → ValueError |
| `test_runoff_type_errors` | Invalid input | Non-numeric → TypeError |

### Validation layer (`tests/test_validation.py`)

| Test | Purpose |
|------|---------|
| `test_validate_runoff_fail_case` | Deliberately Q > P must fail validator |
| `test_validate_storage_fail` | Storage below V_MIN must fail |

### Other modules

- **Weather:** alert thresholds at GREEN/YELLOW/RED boundaries  
- **Reservoir:** schedule feasibility, revenue band  
- **Flood:** monotonic wet-cell count vs stage  
- **Integration:** full workflows with realistic inputs  

---

## 5. Results

```text
**33 passed** in ~0.5s
96% statement coverage on src/
```

Evidence screenshot: `lab_reports/week8_session_a_terminal.png`  
Evidence report: `lab_reports/Week8_SessionA_Report.pdf`

---

## 6. Hallucination discovered (summary)

| Step | Evidence |
|------|----------|
| **AI assumption** | “For CN = 95, rainfall P = 5 mm is always below initial abstraction Ia, so runoff is zero.” |
| **Test created** | `test_runoff_below_initial_abstraction` and high-CN sweep in `test_runoff_not_exceed_rainfall_high_cn` |
| **Failure** | For high CN, Ia is **smaller**; P = 5 mm can produce **non-zero** runoff |
| **Fix** | Corrected test design (P = 2 mm, CN = 80 for zero-runoff case); verified Ia formula in `scs_cn.py` |

Full narrative: [HALLUCINATION_CASE_STUDY.md](HALLUCINATION_CASE_STUDY.md)

---

## 7. Lessons learned

1. **Never trust AI hydrology “always” statements** — verify Ia, units, and bounds with formulas.  
2. **Physical rules belong in code** (`validation.py`), not only in prose.  
3. **Coverage reports** reveal Swiss-cheese holes (untested modules) quickly.  
4. **Assignment 3 is about the story:** AI output → layered tests → caught mistake → fix.

---

## 8. References

- Capstone tests: [`../tests/`](../tests/)  
- Validation: [`../src/validation.py`](../src/validation.py)  
- Prompt log: [`../prompt_log.md`](../prompt_log.md) (Week 8 Session A)  
- All AI failures: [`../assignment4/AI_FAILURES.md`](../assignment4/AI_FAILURES.md)
