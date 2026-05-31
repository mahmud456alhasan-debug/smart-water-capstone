# Physical Validation

**Mahmudul Hasan (4125999049)** · Smart Water Lab

Every hydrological and physical constraint enforced in this project — for Assignment 4 rubric (**Physical Validity 20%**).

[← Back to docs index](README.md) · Evidence: [`src/validation.py`](../src/validation.py) · Tests: [`tests/`](../tests/)

---

## Scope note (course rubric)

The rubric mentions examples such as **runoff ≤ rainfall** and **pH 0–14**. This capstone models **rainfall → runoff → reservoir → flood**; there is **no pH module**. All constraints below are **water-balance and stage rules** that apply to this codebase.

---

## Master constraint table

| # | Physical law / rule | Formula or check | Enforced in code | Test / CLI evidence |
|---|---------------------|------------------|------------------|---------------------|
| 1 | Runoff non-negative | Q ≥ 0 | `scs_runoff_mm()` → `max(0, …)` | `test_runoff_zero_rainfall` |
| 2 | **Runoff ≤ rainfall** | Q ≤ P | `scs_runoff_mm()` → `min(q, p)`; `validate_runoff_mm()` | `test_runoff_normal_storm`, `test_validate_runoff_fail_case` |
| 3 | No runoff below initial abstraction | Q = 0 if P ≤ Ia | SCS-CN branch in `scs_runoff_mm()` | `test_runoff_below_initial_abstraction` |
| 4 | Rainfall non-negative | P ≥ 0 | Input validation | `test_runoff_negative_p_raises` |
| 5 | Curve number valid | CN ∈ [1, 100] | `_validate_curve_number()` | `test_runoff_invalid_cn_raises` |
| 6 | Extreme storms bounded | Q ≤ P at high P | Numerical cap | `test_runoff_extreme_high_rainfall` |
| 7 | CN extremes | Q ≤ P at CN 1, 100 | Boundary tests | `test_runoff_cn_at_lower_bound`, `test_runoff_cn_at_upper_bound` |
| 8 | Reference hand case | Q = 13.80 mm at P=50, CN=80 | Exp 2 implementation | `validate_reference.py` (submission) |
| 9 | Storage within capacity | V_MIN ≤ S ≤ V_MAX | `validate_storage_mcm()` | `test_storage_bounds_each_day`, `test_validate_storage_fail` |
| 10 | Reservoir schedule feasible | Slack ≥ 0 each day | `validate_schedule()` | `test_validate_schedule_pass` |
| 11 | Revenue in expected band | ~$708k baseline | `validate_reservoir_result()` | `test_wrapper_baseline` |
| 12 | Eco release still feasible | PASS at higher eco flow | Optimizer + validator | `test_eco_flow_higher_still_feasible` |
| 13 | Flood depth non-negative | depth = max(0, stage − elev) | `simulate_flood()` | `test_simulate_flood_depth_zero_off_wet` |
| 14 | Flooded fraction bounded | 0 ≤ flooded % ≤ 100 | `flood_statistics()` | `test_flood_statistics_wet_and_dry` |
| 15 | **Monotonic inundation** | wet count non-decreasing as stage ↑ | `validate_flood_monotonic()` | `test_monotonic_wet_count`; Exp 4 **9/9 PASS** |
| 16 | DEM elevation range | Synthetic DEM 30–80 m | `generate_dem()` | `test_generate_dem_bounds` |
| 17 | Alert thresholds ordered | GREEN < AMBER < RED | `alert_level()` | `test_alert_green`, `test_alert_amber`, `test_alert_red` |
| 18 | Alert boundary at RED | rate ≥ red → RED | Inclusive upper tier | `test_alert_boundary_red` |

---

## Swiss Cheese layers (how constraints are checked)

```text
Layer 1 — Human / AI review     AGENTS.md validation rules; prompt_log corrections
Layer 2 — pytest (33 capstone)  tests/test_*.py
Layer 3 — validation.py         validate_runoff_mm, validate_storage_mcm, …
Layer 4 — Integration           tests/test_integration.py
Layer 5 — Experiment CLIs       validate_reference, validate_flood, … (88 tests total)
```

---

## Run validation yourself

```bash
# Capstone — all physical + unit tests
pytest -q tests/test_runoff.py tests/test_validation.py tests/test_flood.py tests/test_reservoir.py

# Full capstone suite
pytest -q

# Assignment 3 — reproduce AI assumption failure
python3 assignment3/scripts/demo_wrong_assumption_fails.py
```

---

## Related

| Document | Purpose |
|----------|---------|
| [assignment4/AI_FAILURES.md](../assignment4/AI_FAILURES.md) | AI mistakes tied to physical rules |
| [assignment3/EVIDENCE_CHAIN.md](../assignment3/EVIDENCE_CHAIN.md) | Prompt → test → failure → fix |
| [ENGINEERING.md](ENGINEERING.md) | Validation strategy overview |
