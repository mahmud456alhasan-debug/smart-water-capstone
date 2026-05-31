# Prompt Log - Week 3 Session B

## Red phase

**Prompt used:** `prompt_red.txt`

**Test file:** `tests/test_runoff.py` (7 tests; import `calculate_runoff` from `src.runoff`)

**pytest result:** `ModuleNotFoundError: No module named 'src.runoff'` — Red confirmed (no implementation yet)

**Notes on failing tests:** Collection error before any test ran; expected for TDD Red. Tests define normal case P=50 CN=80 (Q≈13.80), P=0, P<Ia, CN=100, invalid P/CN, and Q≤P grid.

---

## Green phase

**Prompt used:** `prompt_green.txt` with full `tests/test_runoff.py` pasted

**Implementation:** `src/runoff.py` (single function with inline validation)

**What AI got wrong on first try:** Nothing critical — all 7 tests passed on first implementation.

**How tests caught it:** Tests encode S, Ia, and expected Q; would fail on wrong formula, missing Q=0 branch, or missing ValueError.

**pytest result:** 7 passed in ~0.01 s

**Sanity check:** P=80, CN=85 → 43.55 mm; P=50, CN=80 → 13.80 mm (consistent with Week 1/2 and Week 3 Session A)

---

## Refactor phase

**Prompt used:** `prompt_refactor.txt` with Green-phase `src/runoff.py` pasted

**What changed:**
- Named constants (`_RETENTION_FACTOR`, `_RETENTION_OFFSET`, `_INITIAL_ABSTRACTION_RATIO`, CN bounds)
- Helpers: `_validate_positive_rainfall`, `_validate_curve_number`, `_compute_runoff`
- Clearer error messages (include invalid values)
- `effective_rainfall` named intermediate; `calculate_runoff` is a short validate → compute → clamp pipeline

**What stayed the same:** SCS-CN math and outputs; all test expectations unchanged

**pytest after refactor:** 7 passed

---

## Hallucination check

**One thing tests prevented or exposed:** Without tests, an AI could use wrong S formula or skip P≤Ia; the hand-calculated normal case (13.80 mm) and impervious case (Q=P) lock in correct physics. Red phase forced tests before code so behavior was specified first.

---

## Lessons learned

TDD with AI: write tests first (Red), implement minimum code (Green), refactor only while green. Tests are the contract; terminal pytest is mandatory even when the agent says “all pass.”
