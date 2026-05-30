# Smart Water Lab

### AI-Augmented Water Resources Decision Support Platform

Integrated rainfall monitoring, runoff modeling, reservoir optimization, and flood-risk analysis with documented AI-assisted software engineering practices.

**Student:** Mahmudul Hasan (4125999049) · **Xi'an Jiaotong University** · 2026

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-88-success)
![Reports](https://img.shields.io/badge/PDF_Reports-5-blue)
![Validation](https://img.shields.io/badge/Validation_CLIs-4-informational)
![AI Review](https://img.shields.io/badge/AI_Corrections-9-orange)

---

## Quick navigation

- [Integrated architecture](#integrated-system-architecture)
- [Engineering outcomes](#engineering-outcomes)
- [Submission package](#submission-package)
- [Platform modules](#platform-modules)
- [Validation and AI engineering](#validation-and-ai-engineering)
- [Quick start](#quick-start)
- [Documentation](#documentation)

---

## Integrated system architecture

![Smart Water Decision Support Pipeline — weather to flood assessment workflow](assets/smart_water_pipeline.png)

End-to-end decision-support workflow: **weather data → rainfall alert → SCS-CN runoff → reservoir dispatch → flood inundation mapping**, with validation and formal reports at each stage.

---

## Engineering outcomes

- **88** automated pytest cases across four experiments  
- **4** dedicated validation CLI tools (`validate_*`, batch API, constraint checks)  
- **5** formal PDF reports including AI engineering case study  
- **Monte Carlo** inflow uncertainty — 100 scenarios, P10/P50/P90 revenue and storage  
- **9** documented AI corrections (83% first-pass rate on 52 reviewed deliverables)  
- **End-to-end pipeline** linking monitoring, operations, and flood impact assessment  
- **4** reproducibility scorecards (`audit_summary.txt` per experiment)  

---

## Key metrics

| Metric | Value |
|--------|------:|
| Specialized experiments | 4 |
| PDF reports + case study | **5** |
| Automated tests | **88** |
| Validation CLI scripts | 4 |
| AI outputs reviewed / corrected | 52 / **9** |
| Monte Carlo inflow scenarios | 100 |
| Streamlit dashboards (experiments + capstone) | 5 |
| Reproducibility scorecards | 4 |

> **Official release:** [v1.0 — Smart Water Lab Submission](https://github.com/mahmud456alhasan-debug/smart-water-capstone/releases/tag/v1.0.0) — PDFs in [`release/`](release/) (create release via [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md) if link is empty).

---

## Submission package

| Document | Description | Download |
|----------|-------------|----------|
| AI Engineering Case Study | Pipeline, AI statistics, threats to validity | [PDF](submission/portfolio/AI_Engineering_Portfolio.pdf) |
| Experiment 1 | Rainfall monitoring & alerting | [PDF](submission/experiment_reports/Experiment1_Rainfall_Alert/Experiment1_Rainfall_Alert_Report.pdf) |
| Experiment 2 | SCS-CN runoff modeling | [PDF](submission/experiment_reports/Experiment2_SCSCN_Runoff/Experiment2_SCSCN_Runoff_Report.pdf) |
| Experiment 3 | Reservoir dispatch optimization | [PDF](submission/experiment_reports/Experiment3_Reservoir_Optimization/Experiment3_Reservoir_Optimization_Report.pdf) |
| Experiment 4 | Flood inundation analysis | [PDF](submission/experiment_reports/Experiment4_Flood_Inundation/Experiment4_Flood_Inundation_Report.pdf) |

Short filenames for GitHub Releases: [`release/`](release/) · Full packages (LaTeX + PDF + figures): [`submission/`](submission/) — see [submission README](submission/README.md) for `.tex` paths

---

## Engineering maturity

![Engineering maturity self-assessment — typical course project vs this submission](assets/case_study_radar.png)

Six axes: technical quality, testing, physical validation, AI collaboration, reproducibility, documentation (1–10 self-assessment).

---

## Platform modules

| Rainfall monitoring | Runoff modeling |
|:--:|:--:|
| ![Rainfall dashboard — OpenWeather alerts and forecast risk](assets/rainfall_dashboard.png) | ![SCS-CN runoff sensitivity and uncertainty](assets/runoff_analysis.png) |
| Exp 1 — API, GREEN/YELLOW/RED, 3h/6h forecast | Exp 2 — hand-validated Q=13.80 mm at P=50, CN=80 |

| Reservoir optimization | Flood analysis |
|:--:|:--:|
| ![Monte Carlo revenue and storage distributions](assets/reservoir_optimization.png) | ![Flood extent at 40 m vs 50 m water level](assets/flood_analysis.png) |
| Exp 3 — trust-constr, eco trade-off, P10/P50/P90 | Exp 4 — DEM inundation, 9/9 validation PASS |

---

## Validation and AI engineering

| Layer | Implementation |
|-------|----------------|
| Swiss Cheese verification | AI review → pytest → physical rules → validation CLI → report evidence |
| Jagged Frontier | AI mistakes documented in `prompt_log.md` and case study |
| Critical AI use | 52 deliverables reviewed, 9 required human correction |
| Threats to validity | OpenWeather sparsity, SCS-CN lumped CN, bathtub flood model, LLM hallucination risk |

Full narrative: [`submission/portfolio/AI_Engineering_Portfolio.md`](submission/portfolio/AI_Engineering_Portfolio.md) · Capstone reflection: [`JAGGED_FRONTIER.md`](JAGGED_FRONTIER.md)

---

## Quick start

```bash
git clone https://github.com/mahmud456alhasan-debug/smart-water-capstone.git
cd smart-water-capstone
python3 -m pip install -r requirements.txt
streamlit run app/main.py
pytest -q
```

Copy `dem.npy` into `data/` for the flood tab (from Week 6 lab or local Experiment 4 output).

---

## Repository map

```text
smart-water-capstone/
├── assets/           README showcase figures
├── release/          PDFs with short names (for GitHub Releases)
├── submission/       Full LaTeX + screenshots + appendix code
├── docs/             Wiki pages + GitHub setup guide
├── app/              Streamlit capstone dashboard
├── src/              weather · runoff · reservoir · flood modules
└── tests/            Capstone pytest suite
```

Experiment source code: local `ai_water_lab/experiment*` folders (not duplicated in this repo).

---

## Documentation

| Resource | Purpose |
|----------|---------|
| [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md) | **About description, topics, Release v1.0** |
| [`docs/wiki/`](docs/wiki/) | Wiki pages — copy to GitHub Wiki |
| [`submission/README.md`](submission/README.md) | Regenerate PDFs and figures |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Capstone system design |
| [`AGENTS.md`](AGENTS.md) | AI collaboration protocol |

---

## License

Academic coursework — Xi'an Jiaotong University, 2026.
