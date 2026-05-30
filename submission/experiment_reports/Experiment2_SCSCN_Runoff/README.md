# Experiment 2 — Submission Package

**Student:** Mahmudul Hasan (4125999049)  
**Code:** `../../ai_water_lab/experiment2_scscn_runoff/`

## Overleaf upload

```
Experiment2_SCSCN_Runoff/
├── Experiment2_SCSCN_Runoff_Report.tex
├── files/
└── screenshots/
    ├── architecture.png
    ├── experiment2_main.png
    ├── experiment2_validation.png
    ├── experiment2_pytest.png
    ├── runoff_comparison.png
    └── cn_sensitivity.png
```

## Before submit

- [ ] Compile PDF twice on Overleaf
- [ ] All figures visible (architecture, main, validation, pytest, plots)
- [ ] Local: `pytest -v` → 20 passed

## Regenerate figures

```bash
cd ai_water_lab/experiment2_scscn_runoff
python3 sensitivity_analysis.py
python3 generate_report_figures.py
```
