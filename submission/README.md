# Submission Package — Smart Water Lab

**Mahmudul Hasan (4125999049)**

Compiled **PDFs**, **LaTeX sources**, screenshots, and appendix code — one folder per deliverable.

## Folder layout

```text
submission/
├── portfolio/
│   ├── AI_Engineering_Portfolio.tex    ← LaTeX source (case study)
│   ├── AI_Engineering_Portfolio.pdf    ← compiled PDF
│   ├── AI_Engineering_Portfolio.md     ← markdown source
│   └── figures/                        ← pipeline + radar PNGs
└── experiment_reports/
    ├── Experiment1_Rainfall_Alert/
    │   ├── Experiment1_Rainfall_Alert_Report.tex
    │   ├── Experiment1_Rainfall_Alert_Report.pdf
    │   ├── files/                      ← appendix code + AGENTS.md
    │   └── screenshots/                ← report figures
    ├── Experiment2_SCSCN_Runoff/        (same pattern)
    ├── Experiment3_Reservoir_Optimization/
    └── Experiment4_Flood_Inundation/
```

Each experiment folder keeps **`.tex` and `.pdf` together** so you can recompile on Overleaf or locally without hunting for sources.

---

## Deliverable index (PDF + LaTeX)

| Deliverable | PDF | LaTeX source |
|-------------|-----|--------------|
| AI case study | [portfolio/AI_Engineering_Portfolio.pdf](portfolio/AI_Engineering_Portfolio.pdf) | [portfolio/AI_Engineering_Portfolio.tex](portfolio/AI_Engineering_Portfolio.tex) |
| Experiment 1 — Rainfall alert | [Experiment1_Rainfall_Alert_Report.pdf](experiment_reports/Experiment1_Rainfall_Alert/Experiment1_Rainfall_Alert_Report.pdf) | [Experiment1_Rainfall_Alert_Report.tex](experiment_reports/Experiment1_Rainfall_Alert/Experiment1_Rainfall_Alert_Report.tex) |
| Experiment 2 — SCS-CN runoff | [Experiment2_SCSCN_Runoff_Report.pdf](experiment_reports/Experiment2_SCSCN_Runoff/Experiment2_SCSCN_Runoff_Report.pdf) | [Experiment2_SCSCN_Runoff_Report.tex](experiment_reports/Experiment2_SCSCN_Runoff/Experiment2_SCSCN_Runoff_Report.tex) |
| Experiment 3 — Reservoir optimization | [Experiment3_Reservoir_Optimization_Report.pdf](experiment_reports/Experiment3_Reservoir_Optimization/Experiment3_Reservoir_Optimization_Report.pdf) | [Experiment3_Reservoir_Optimization_Report.tex](experiment_reports/Experiment3_Reservoir_Optimization/Experiment3_Reservoir_Optimization_Report.tex) |
| Experiment 4 — Flood inundation | [Experiment4_Flood_Inundation_Report.pdf](experiment_reports/Experiment4_Flood_Inundation/Experiment4_Flood_Inundation_Report.pdf) | [Experiment4_Flood_Inundation_Report.tex](experiment_reports/Experiment4_Flood_Inundation/Experiment4_Flood_Inundation_Report.tex) |

Short filenames for GitHub Releases: see [`../release/`](../release/) at repo root.

---

## Case study figures

| Figure | Path |
|--------|------|
| Integrated pipeline | [portfolio/figures/smart_water_pipeline.png](portfolio/figures/smart_water_pipeline.png) |
| Engineering maturity radar | [portfolio/figures/case_study_radar.png](portfolio/figures/case_study_radar.png) |

---

## Regenerate PDFs (from this repository)

**Case study** (upload `portfolio/figures/` to Overleaf if needed):

```bash
cd submission/portfolio
pdflatex AI_Engineering_Portfolio.tex && pdflatex AI_Engineering_Portfolio.tex
```

**Experiment reports** (each folder must include `files/` and `screenshots/`):

```bash
cd submission/experiment_reports/Experiment1_Rainfall_Alert
pdflatex Experiment1_Rainfall_Alert_Report.tex && pdflatex Experiment1_Rainfall_Alert_Report.tex
# repeat for Experiments 2–4
```

**Figures** (requires local `ai_water_lab` code, not in this repo):

```bash
cd ai_water_lab && python3 generate_case_study_figures.py
cd ai_water_lab/experiment1_rainfall_alert && python3 generate_report_figures.py
# repeat for experiment2, 3, 4
```

After recompiling, copy updated PDFs to [`../release/`](../release/) if publishing a new GitHub Release.
