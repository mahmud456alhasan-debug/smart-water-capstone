# Experiment 3 Report — Reservoir Optimization

**Student:** Mahmudul Hasan (4125999049)

## Build PDF (Overleaf or local)

Upload **only** from this folder:
- `Experiment3_Reservoir_Optimization_Report.tex`
- `files/` (ASCII appendix copies -- do not replace with code-folder UTF-8 files)
- `screenshots/` (includes `experiment3_optimize.png`, `experiment3_pytest.png`, `experiment3_validation.png`, plots)

```bash
cd Experiment-reports/Experiment3_Reservoir_Optimization
pdflatex Experiment3_Reservoir_Optimization_Report.tex
pdflatex Experiment3_Reservoir_Optimization_Report.tex
```

**Overleaf UTF-8 errors:** If you see `Invalid UTF-8 byte` on `\VerbatimInput`, the `files/formulation.md` or `files/prompt_log.md` contain characters like m³. Use the `files/` versions from this report folder (ASCII-safe), not the originals from `ai_water_lab/`.

## Regenerate figures

```bash
cd ../../ai_water_lab/experiment3_reservoir_optimization
python3 generate_report_figures.py
```

## LMS deliverables (code folder)

Copy from `ai_water_lab/experiment3_reservoir_optimization/`:

- `reservoir_optimize.py`
- `optimal_schedule.csv`
- `tradeoff_analysis.png`
- `validation_report.txt`
- `prompt_log.md`
