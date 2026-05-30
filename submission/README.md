# Smart Water Lab — Submission Package

**Student:** Mahmudul Hasan (4125999049)  
**GitHub:** [smart-water-capstone](https://github.com/mahmud456alhasan-debug/smart-water-capstone)

This folder contains compiled PDFs and LaTeX sources for LMS / portfolio submission.

## Contents

| Path | Description |
|------|-------------|
| `portfolio/AI_Engineering_Portfolio.pdf` | AI-Augmented Engineering Case Study (compile from `.tex`) |
| `portfolio/figures/` | `smart_water_pipeline.png`, `case_study_radar.png` |
| `experiment_reports/Experiment1_Rainfall_Alert/` | Report PDF + `.tex` + screenshots + appendix `files/` |
| `experiment_reports/Experiment2_SCSCN_Runoff/` | Same |
| `experiment_reports/Experiment3_Reservoir_Optimization/` | Same |
| `experiment_reports/Experiment4_Flood_Inundation/` | Same |

## Regenerate PDFs locally

```bash
# Case study portfolio (run twice from repo root Software Development/)
pdflatex AI_Engineering_Portfolio.tex

# Per experiment (from each report folder)
cd experiment_reports/Experiment1_Rainfall_Alert
pdflatex Experiment1_Rainfall_Alert_Report.tex
pdflatex Experiment1_Rainfall_Alert_Report.tex
```

Figures for experiments: run `generate_report_figures.py` in each `ai_water_lab/experimentN_.../` folder.

Pipeline + radar figures:

```bash
cd ai_water_lab
python3 generate_case_study_figures.py
```

## Code

Runnable Python lives in `../` sibling folders under `ai_water_lab/` (not duplicated here).
