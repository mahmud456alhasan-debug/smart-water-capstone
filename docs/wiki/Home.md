# Home

Welcome to **Smart Water Lab** — an AI-augmented water resources decision support platform.

**Student:** Mahmudul Hasan (4125999049) · Xi'an Jiaotong University · 2026

## Pipeline

Weather → Rainfall alert → Runoff → Reservoir optimization → Flood mapping

![Pipeline](../../assets/smart_water_pipeline.png)

## Wiki navigation

```text
Home
├── System Architecture
├── Validation Strategy
├── AI Engineering Workflow  →  AI Engineering Portfolio
├── Experiment Overview      →  Experiments 1–4
└── Reproducibility Guide
```

## Quick links

| Page | Topic |
|------|-------|
| [System Architecture](System-Architecture.md) | End-to-end pipeline and capstone integration |
| [Validation Strategy](Validation-Strategy.md) | Swiss Cheese verification, threats to validity |
| [AI Engineering Portfolio](AI-Engineering-Portfolio.md) | AI workflow, statistics, case study |
| [Reproducibility Guide](Reproducibility-Guide.md) | PDFs, tests, audit summaries |
| [Experiment 1 — Rainfall Alert](Experiment-1-Rainfall-Alert.md) | Monitoring and forecasting |
| [Experiment 2 — SCS-CN Runoff](Experiment-2-SCSCN-Runoff.md) | Runoff modeling |
| [Experiment 3 — Reservoir Optimization](Experiment-3-Reservoir-Optimization.md) | Dispatch optimization |
| [Experiment 4 — Flood Inundation](Experiment-4-Flood-Inundation.md) | DEM flood mapping |

> When pasting into **GitHub Wiki**, create each page without `.md` in the title (e.g. `System-Architecture`) and use wiki-style `[[Page-Name]]` links.

## Results snapshot

| Experiment | Key result |
|------------|------------|
| Rainfall monitoring | GREEN/YELLOW/RED classification validated |
| SCS-CN runoff | Reference Q = 13.80 mm verified |
| Reservoir optimization | Monte Carlo P10/P50/P90 analysis |
| Flood inundation | 9/9 physical validation checks passed |

## Metrics

| Item | Value |
|------|------:|
| Tests | 88 |
| PDF reports | 5 |
| Lab reports | 16 |
| Validation CLIs | 4 |
| AI corrections | 9 |

## Capstone

```bash
streamlit run app/main.py
pytest -q
```

Main repository: [smart-water-capstone](https://github.com/mahmud456alhasan-debug/smart-water-capstone)
