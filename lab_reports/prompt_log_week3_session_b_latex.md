# Prompt Log - Week 3 Session B

## Red phase

**Prompt used:** prompt_red.txt

**Test file:** tests/test_runoff.py (7 tests)

**pytest result:** ModuleNotFoundError: No module named 'src.runoff' -- Red confirmed

**Notes:** Tests specify P=50 CN=80 (Q approx 13.80), P=0, P<Ia, CN=100, invalid P/CN, Q<=P grid.

---

## Green phase

**Prompt used:** prompt_green.txt with full test file pasted

**Implementation:** src/runoff.py

**First try:** All 7 tests passed

**Sanity:** P=80 CN=85 -> 43.55 mm; P=50 CN=80 -> 13.80 mm

---

## Refactor phase

**Changes:** Named constants; _validate_positive_rainfall; _validate_curve_number; _compute_runoff; clearer errors

**Unchanged:** SCS-CN outputs; test file unchanged

**pytest:** 7 passed after refactor

---

## Hallucination check

Tests lock hand-calculated Q and impervious Q=P; Red-before-code prevents implementing untested wrong formulas.

## Lessons learned

TDD with AI: Red, Green, Refactor; always run pytest locally.
