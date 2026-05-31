# Assignment 3 — Evidence Files

These files are **in the repository** so graders can verify Case B without hunting outside the repo.

| File | Role |
|------|------|
| [buggy_rainfall.py](buggy_rainfall.py) | AI-style **wrong** SCS-CN (Week 2 debug lab) |
| [rainfall_fixed.py](rainfall_fixed.py) | **Corrected** version after terminal + hand check |
| Production capstone | [`../../src/runoff/scs_cn.py`](../../src/runoff/scs_cn.py) |

**Run wrong version:**

```bash
python3 assignment3/evidence/buggy_rainfall.py
# P=80, CN=85 → Q ≈ 0.002 mm (wrong)
```

**Run fixed version:**

```bash
python3 assignment3/evidence/rainfall_fixed.py
# P=80, CN=85 → Q ≈ 43.6 mm
```

Prompt log: [`../../lab_reports/prompt_log_week2_session_a.md`](../../lab_reports/prompt_log_week2_session_a.md)
