# Prompt Log - Week 5 Session B Lab 2 (LaTeX-safe excerpt)

**Student:** Mahmudul Hasan (4125999049)  
**Lab:** SCS-CN Runoff Modeling

## Implementation

**CN validation rule used:** CN in [1, 100] (minimum 1 avoids divide-by-zero on S = 25400/CN - 254)

**Trickiest edge case:** P just below Ia returns 0; CN=100 gives Q=P for large P (impervious limit)

**pytest result:** 7 passed (`python3 -m pytest tests/ -v`)

**Hand check:** P=50 CN=80 → Q≈13.80 mm; P=80 CN=85 → Q≈43.55 mm

## Sensitivity

**Figure path:** `figures/runoff_sensitivity.png`

**CN values:** 60, 70, 80, 90, 95

**Main trend:** For the same rainfall, higher curve number produces more runoff; all curves rise with P and stay below the Q=P line.

## Domain validation

**Reference:** P=80 mm, CN=85 → Q≈43.55 mm (course ~43.6 mm)

**Checks:** Q≤P; Q=0 when P<Ia; higher CN → higher Q at P=50 mm

## Lessons learned

Terminal screenshots of pytest, sensitivity script, and validate_reference are sufficient submission evidence alongside the plot file. Reusing Week 3 TDD code saved time; focus shifted to visualization and physical checks.
