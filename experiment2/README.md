# Experiment 2 — SCS-CN Runoff Modeling

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026

| Resource | Link |
|----------|------|
| **Report (PDF)** | [Experiment2_SCSCN_Runoff_Report.pdf](Experiment2_SCSCN_Runoff_Report.pdf) |
| **LaTeX source** | [Experiment2_SCSCN_Runoff_Report.tex](Experiment2_SCSCN_Runoff_Report.tex) |
| Appendix code | [`files/`](files/) |
| Figures | [`screenshots/`](screenshots/) |

Integrated in capstone: [`src/runoff/`](../src/runoff/)

Reference: Q = **13.80 mm** at P = 50 mm, CN = 80

## Features

| Feature | Status |
|---------|--------|
| `calculate_runoff(P, CN)` + physical boundaries | Required |
| Boundary test suite (P=0, P<Ia, CN=100, Q≤P) | Required |
| Sensitivity plots (Q vs CN, rainfall vs runoff) | Required |
| Hand-validation CLI (`validate_reference.py`) | Extra |
| **Rational method compare (`rational_runoff`, `scs_vs_rational.png`)** | Extra |
| **AMC I/II/III moisture adjustment (`adjust_cn_for_amc`)** | Extra |
| CN uncertainty band analysis (CN ∈ [75, 85]) | Extra |
| pytest suite (**27 tests**) | Extra |

## Run locally

```bash
cd files
python sensitivity_analysis.py      # generates comparison plots
python validate_reference.py
python -m pytest -q
```

```bash
pdflatex Experiment2_SCSCN_Runoff_Report.tex && pdflatex Experiment2_SCSCN_Runoff_Report.tex
```
