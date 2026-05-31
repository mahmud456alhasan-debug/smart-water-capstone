# Assignment 3 — Evidence Chain

**Mahmudul Hasan (4125999049)**

Answers the five verification questions for graders: prompt → AI output → test → failure → fix.

---

## Quick verdict

| Question | Answer |
|----------|--------|
| Did tests exist before the report? | **Yes** — built Week 8 Session A; reports package existing work |
| Is there ≥1 AI hallucination with proof? | **Yes — two documented cases** (Case A + Case B below) |
| Reproducible from clean clone? | **Yes** — see [Reproduce](#reproduce-from-clean-clone) |
| Screenshot / log evidence? | **Yes** — `lab_reports/week8_session_a_terminal.png`, Week 2 terminal logs |

---

## Case A — Capstone Week 8 (test-design assumption)

Used for `test_hallucination_cn95_p6_produces_runoff` in the capstone.

### 1. Prompt that led to the mistake

**Source:** Week 8 lab guide + Cursor Agent, [`prompt_log.md`](../prompt_log.md) Session 8A:

```text
Write pytest tests with normal, edge, invalid, and physical cases;
fixtures; target >80% coverage for capstone src/ functions.
```

While drafting tests, the **AI-assisted assumption** (documented in prompt log) was:

> “For CN = 95, rainfall P = 5 mm is always below Ia, so runoff Q = 0.”

This is a **verbal / test-design hallucination** — not a bug in `scs_cn.py`, but wrong hydrology reasoning during test writing.

### 2. AI response / wrong belief

Not a separate code file — the mistaken **generalization** is recorded in:

- [`prompt_log.md`](../prompt_log.md) line 141  
- [`lab_reports/Week8_SessionA_Report.tex`](../lab_reports/Week8_SessionA_Report.tex) § Exercise 3  
- [`docs/JAGGED_FRONTIER.md`](../docs/JAGGED_FRONTIER.md)

### 3. Test that exposes it

[`tests/test_runoff.py`](../tests/test_runoff.py):

```python
def test_hallucination_cn95_p6_produces_runoff():
    assert scs_runoff_mm(2.0, 95.0) == 0.0   # P < Ia  → OK
    q5 = scs_runoff_mm(5.0, 95.0)
    assert q5 > 0.0   # AI assumed Q=0 here — would FAIL if we asserted == 0
```

### 4. Failure (reproduce)

Run the demo script that simulates the **draft wrong assertion**:

```bash
python3 assignment3/scripts/demo_wrong_assumption_fails.py
```

Expected: `AssertionError` — Q ≈ 0.345 mm, not 0.

### 5. Fix applied

- Correct zero-runoff example: **P = 2 mm, CN = 80** (true P < Ia)  
- Regression test documents CN = 95, P = 5 → Q > 0  
- Physical layer: [`src/validation.py`](../src/validation.py) enforces Q ≤ P  

**Screenshot:** `lab_reports/week8_session_a_terminal.png` (Week 8A snapshot at 29 tests; now **33** — see [docs/TEST_COUNTS.md](../docs/TEST_COUNTS.md))

---

## Case B — Week 2 / Experiment 2 (AI-generated **wrong code**)

**Stronger evidence** — literal buggy AI-style formula in code.

### 1. Prompt

[`lab_reports/prompt_log_week2_session_a.md`](../lab_reports/prompt_log_week2_session_a.md):

```text
This code has bugs. Walk through it line by line, identify what's wrong, and suggest fixes.
```

(Attached `buggy_rainfall.py` — intentional SCS-CN errors for CoT debugging lab.)

### 2. AI wrong output (code)

[`evidence/buggy_rainfall.py`](evidence/buggy_rainfall.py):

```python
S = 25400 * CN - 254      # WRONG: should be 25400 / CN - 254
Ia = 0.2 * P              # WRONG: should be 0.2 * S
Q = (P - Ia)**2 / (P + S) # WRONG: denominator should be (P - Ia + S)
```

**Terminal before fix:**

```text
P = 80 mm, CN = 85 → Q = 0.0019 mm   (expected ~43.6 mm)
```

**AI closing claim (also wrong):** suggested buggy script might give ~48.9 mm — **terminal proved ~0.002 mm**.

### 3. Tests that catch it

- Week 2 hand check: P=80, CN=85 → Q≈43.6 mm  
- Experiment 2: **20 pytest cases** + `validate_reference.py` → Q = **13.80 mm** at P=50, CN=80  
- Report: [`submission/experiment_reports/Experiment2_SCSCN_Runoff/`](../submission/experiment_reports/Experiment2_SCSCN_Runoff/)

### 4. Fix

[`evidence/rainfall_fixed.py`](evidence/rainfall_fixed.py) → capstone [`src/runoff/scs_cn.py`](../src/runoff/scs_cn.py)

---

## Test suite coverage (Assignment 3 deliverable)

**Capstone:** **33** tests in [`tests/`](../tests/)

| Category | Examples |
|----------|----------|
| Boundary | P=0; P below Ia; P=1000; CN=1 and CN=100 |
| Invalid | P<0; CN<1; CN>100; wrong types |
| Physical | Q ≤ P; storage bounds; flood monotonicity |
| Regression | `test_hallucination_cn95_p6_produces_runoff` |
| Integration | CSV→alert, reservoir PASS, DEM→stats |

Run: `pytest -q` → **33 passed**

---

## Reproduce from clean clone

```bash
git clone https://github.com/mahmud456alhasan-debug/smart-water-capstone.git
cd smart-water-capstone
python3 -m pip install -r requirements.txt

# Full suite
pytest -q

# Show wrong AI assumption failing
python3 assignment3/scripts/demo_wrong_assumption_fails.py

# Show correct physics
python3 -c "from src.runoff.scs_cn import scs_runoff_mm; print('Q(5,95)=', scs_runoff_mm(5,95))"
```

---

## Honest note

- **Case B** is the clearest “AI generated wrong code → tests/math caught it” story.  
- **Case A** is “AI-assisted wrong assumption during test design → formula check caught it.”  
- Both satisfy the assignment; **Case B** has the strongest prompt + code + terminal trail.
