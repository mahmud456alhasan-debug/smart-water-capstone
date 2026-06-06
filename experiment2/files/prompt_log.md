# Prompt Log - Experiment 2: SCS-CN Runoff

**Student:** Mahmudul Hasan (4125999049)  
**Folder:** `experiment2_scscn_runoff/` (separate from Week 5 Lab 2 and capstone)

---

## Part 1: Formula Implementation

**Prompt used:**

```text
Implement calculate_runoff(P, CN) for SCS-CN: S = 25400/CN - 254, Ia = 0.2*S,
return 0 if P <= Ia, else Q = (P-Ia)^2/(P-Ia+S), cap Q <= P. Type hints and docstring.
Validate P >= 0 and CN in (0, 100].
```

**CN validation rule:** CN must be in (0, 100] to avoid division by zero.

**Trickiest edge case:** P = Ia must return Q = 0 (not divide by zero).

---

## Part 2: Testing

**Tests added beyond AI suggestions:**

- `test_p_equals_ia` at Ia for CN=80
- Parametrized `test_q_never_exceeds_p`
- Grid test for Q <= P across P and CN
- CN ordering at P = 50 mm

**Result:** `pytest -v` - 20 passed (including parametrized boundaries and S/Ia checks).

**CLI validation:** `validate_reference.py` prints hand calc steps and physical matrix (report Figure).

---

## Part 3: Sensitivity Analysis

**Figure paths:**

- `runoff_comparison.png` - rainfall vs runoff, CN = 60–100
- `cn_sensitivity.png` - CN vs Q at P = 50 mm
- `sensitivity_at_P50.csv` - numeric table

**Main trend:** At fixed rainfall, higher CN (more impervious) produces more direct runoff; curves approach Q = P for CN = 100.

---

## Part 4: Domain Validation

**Published reference:** Experiment guide hand calc P = 50, CN = 80 -> Q = 13.8 mm.

**Verification:** `calculate_runoff(50, 80)` matches within 0.1 mm.

**AI corrections:** Ensured `P <= Ia` uses inclusive comparison; capped `min(Q, P)`.
