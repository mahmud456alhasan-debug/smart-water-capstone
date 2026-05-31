# Prompt Log - Week 5 Session B Lab 2

**Student:** Mahmudul Hasan (4125999049)  
**Lab:** SCS-CN Runoff Modeling

---

## Implementation

**CN validation rule used:** CN in [1, 100] (minimum 1 avoids divide-by-zero on S = 25400/CN - 254)

**Trickiest edge case:** P just below Ia returns 0; CN=100 gives Q=P for large P (impervious limit)

**Prompt used (Exercise 1):** `prompt_implement.txt` (code reused from Week 3 Session B TDD lab)

**pytest result:** 7 passed (`python3 -m pytest tests/ -v`)

**Hand check:** P=50 CN=80 → Q≈13.80 mm; P=80 CN=85 → Q≈43.55 mm

---

## Sensitivity

**Figure path:** `figures/runoff_sensitivity.png`

**Data:** `figures/sensitivity_data.csv`

**CN values:** 60, 70, 80, 90, 95

**Main trend in one sentence:** For the same rainfall, higher curve number (more impervious land) produces more runoff; all curves rise with P and stay below the Q=P line.

**Prompt used (Exercise 2):** `prompt_sensitivity.txt`

---

## Domain validation

**Published reference used:** Course Week 1 Session B / Week 3 labs (P=80 mm, CN=85 → Q≈43.6 mm)

**Checks run:** Q≤P; Q=0 when P<Ia; higher CN → higher Q at P=50 mm

**Any mismatch and resolution:** None — P=80, CN=85 matches course reference (~43.55 mm)

---

## Lessons learned

[Your own words]
