# Submission Package — Smart Water Lab

**Mahmudul Hasan (4125999049)**

Compiled PDFs and LaTeX sources for LMS upload and portfolio review.

## PDF index

| Deliverable | Path |
|-------------|------|
| AI case study | [`portfolio/AI_Engineering_Portfolio.pdf`](portfolio/AI_Engineering_Portfolio.pdf) |
| Experiment 1 | [`experiment_reports/Experiment1_Rainfall_Alert/Experiment1_Rainfall_Alert_Report.pdf`](experiment_reports/Experiment1_Rainfall_Alert/Experiment1_Rainfall_Alert_Report.pdf) |
| Experiment 2 | [`experiment_reports/Experiment2_SCSCN_Runoff/Experiment2_SCSCN_Runoff_Report.pdf`](experiment_reports/Experiment2_SCSCN_Runoff/Experiment2_SCSCN_Runoff_Report.pdf) |
| Experiment 3 | [`experiment_reports/Experiment3_Reservoir_Optimization/Experiment3_Reservoir_Optimization_Report.pdf`](experiment_reports/Experiment3_Reservoir_Optimization/Experiment3_Reservoir_Optimization_Report.pdf) |
| Experiment 4 | [`experiment_reports/Experiment4_Flood_Inundation/Experiment4_Flood_Inundation_Report.pdf`](experiment_reports/Experiment4_Flood_Inundation/Experiment4_Flood_Inundation_Report.pdf) |

## Figures (case study)

- [`portfolio/figures/smart_water_pipeline.png`](portfolio/figures/smart_water_pipeline.png) — integrated workflow
- [`portfolio/figures/case_study_radar.png`](portfolio/figures/case_study_radar.png) — engineering maturity

## Regenerate locally

```bash
# From Software Development/ root
pdflatex AI_Engineering_Portfolio.tex && pdflatex AI_Engineering_Portfolio.tex

cd Experiment-reports/Experiment1_Rainfall_Alert
pdflatex Experiment1_Rainfall_Alert_Report.tex && pdflatex Experiment1_Rainfall_Alert_Report.tex
# repeat for Experiments 2–4

cd ai_water_lab && python3 generate_case_study_figures.py
```

Experiment screenshots: `python3 generate_report_figures.py` inside each `ai_water_lab/experimentN_.../` folder.
