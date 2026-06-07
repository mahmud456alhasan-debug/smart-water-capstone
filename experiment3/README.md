# Experiment 3 — Reservoir Dispatch Optimization

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026

| Resource | Link |
|----------|------|
| **Report (PDF)** | [Experiment3_Reservoir_Optimization_Report.pdf](Experiment3_Reservoir_Optimization_Report.pdf) |
| **LaTeX source** | [Experiment3_Reservoir_Optimization_Report.tex](Experiment3_Reservoir_Optimization_Report.tex) |
| Appendix code | [`files/`](files/) |
| Figures | [`screenshots/`](screenshots/) |

Integrated in capstone: [`src/reservoir/`](../src/reservoir/)

Monte Carlo **P10 / P50 / P90** analysis (100 scenarios)

## Features

| Feature | Status |
|---------|--------|
| 7-day LP formulation + `scipy.optimize` solve | Required |
| Optimal schedule + Pareto eco-flow trade-off | Required |
| Validation report (storage, ecology, mass balance) | Required |
| Monte Carlo inflow uncertainty (100 scenarios) | Extra |
| **Rolling-horizon daily re-optimization** | Extra |
| Solver comparison + head sensitivity | Extra |
| `formulation.md` written before code | Extra |
| pytest suite (**22 tests**) | Extra |

## Run locally

```bash
cd files
python reservoir_optimize.py
python -c "from rolling_horizon import compare_full_vs_rolling; print(compare_full_vs_rolling())"
python -m pytest -q
```

```bash
pdflatex Experiment3_Reservoir_Optimization_Report.tex && pdflatex Experiment3_Reservoir_Optimization_Report.tex
```
