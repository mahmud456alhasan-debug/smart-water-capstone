<p align="center">
  <img src="assets/smart_water_pipeline.png" alt="Smart Water Decision Support Pipeline" width="100%">
</p>

<h1 align="center">Smart Water Lab</h1>

<p align="center">
  AI-Augmented Water Resources Decision Support Platform for rainfall monitoring,<br>
  hydrological runoff prediction, reservoir optimization, and flood-risk analysis.
</p>

<p align="center">
  <strong>Course Project Portfolio</strong> — AI-Augmented Software Engineering<br>
  Xi'an Jiaotong University · 2026 · Mahmudul Hasan (4125999049)
</p>

<p align="center">
  <a href="#project-snapshot">Snapshot</a> ·
  <a href="#core-engineering-experiments">Experiments</a> ·
  <a href="#reports">Reports</a> ·
  <a href="#platform-gallery">Gallery</a> ·
  <a href="#results-snapshot">Results</a> ·
  <a href="#course-assignments">Assignments</a> ·
  <a href="#lab-reports">Labs</a> ·
  <a href="#quick-start">Quick Start</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://github.com/mahmud456alhasan-debug/smart-water-capstone/actions/workflows/tests.yml/badge.svg" alt="Tests CI">
  <img src="https://img.shields.io/badge/Experiments-4-blue" alt="4 experiments">
  <img src="https://img.shields.io/badge/Tests-33-green" alt="33 tests">
  <img src="https://img.shields.io/badge/Coverage-96%25-brightgreen" alt="Coverage">
  <img src="https://img.shields.io/badge/PDF_Reports-5-orange" alt="PDF Reports">
  <img src="https://img.shields.io/badge/Lab_Reports-16-lightgrey" alt="Lab Reports">
  <img src="https://img.shields.io/badge/XJTU-Software_Development-red" alt="XJTU">
</p>

---

## Why this project matters

Water managers must act under uncertainty — heavy rain, limited storage, and flood exposure at the same time. This portfolio builds **four validated hydrology experiments** and integrates them into one Streamlit decision-support workflow, with documented AI-assisted engineering (prompt logs, Swiss Cheese testing, physical validation). Details: [docs/ENGINEERING.md](docs/ENGINEERING.md).

---

## Project snapshot

<a id="project-snapshot"></a>

| | |
|--|--|
| **4** core engineering experiments | **5** formal PDF reports |
| **33** automated tests in this repository (CI) | **96%** coverage on `src/` |
| **18** physical validation rules | **16** weekly lab reports (supporting) |

*Additional local experiment verification:* **88** supplementary pytest tests in development folders (not in this repo). See [docs/TEST_COUNTS.md](docs/TEST_COUNTS.md).

---

## Core engineering experiments

<a id="core-engineering-experiments"></a>

These four experiments are the **primary technical component** of the course project. Each includes a formal PDF report, figures, and LaTeX sources in [`submission/`](submission/).

| Experiment | Topic | Report |
|------------|-------|--------|
| **Experiment 1** | Rainfall Monitoring & Alert System | [PDF](submission/experiment_reports/Experiment1_Rainfall_Alert/Experiment1_Rainfall_Alert_Report.pdf) |
| **Experiment 2** | SCS-CN Runoff Modeling | [PDF](submission/experiment_reports/Experiment2_SCSCN_Runoff/Experiment2_SCSCN_Runoff_Report.pdf) |
| **Experiment 3** | Reservoir Dispatch Optimization | [PDF](submission/experiment_reports/Experiment3_Reservoir_Optimization/Experiment3_Reservoir_Optimization_Report.pdf) |
| **Experiment 4** | Flood Inundation Analysis | [PDF](submission/experiment_reports/Experiment4_Flood_Inundation/Experiment4_Flood_Inundation_Report.pdf) |

All four modules are integrated in the capstone app: `streamlit run app/main.py`

➡️ Full package: [submission/](submission/) · [Release v1.0](https://github.com/mahmud456alhasan-debug/smart-water-capstone/releases/tag/v1.0.0)

---

## Reports

<a id="reports"></a>

| | Document | Download |
|--|----------|----------|
| 📘 | **AI Engineering Portfolio** — pipeline, AI statistics, threats to validity | [PDF](submission/portfolio/AI_Engineering_Portfolio.pdf) |
| 📄 | **Experiment 1** — Rainfall monitoring & alerting | [PDF](submission/experiment_reports/Experiment1_Rainfall_Alert/Experiment1_Rainfall_Alert_Report.pdf) |
| 📄 | **Experiment 2** — SCS-CN runoff modeling | [PDF](submission/experiment_reports/Experiment2_SCSCN_Runoff/Experiment2_SCSCN_Runoff_Report.pdf) |
| 📄 | **Experiment 3** — Reservoir dispatch optimization | [PDF](submission/experiment_reports/Experiment3_Reservoir_Optimization/Experiment3_Reservoir_Optimization_Report.pdf) |
| 📄 | **Experiment 4** — Flood inundation analysis | [PDF](submission/experiment_reports/Experiment4_Flood_Inundation/Experiment4_Flood_Inundation_Report.pdf) |

➡️ Folder: [`submission/`](submission/) (PDF + LaTeX) · Release bundle: [`release/`](release/)

---

## Platform gallery

<a id="platform-gallery"></a>

Outputs from the four core experiments:

| Experiment 1 — Rainfall monitoring | Experiment 2 — SCS-CN runoff |
|:--:|:--:|
| ![Rainfall dashboard](assets/rainfall_dashboard.png) | ![Runoff analysis](assets/runoff_analysis.png) |
| GREEN / YELLOW / RED alerts · 3h/6h forecast | Q = 13.80 mm verified at P = 50, CN = 80 |

| Experiment 3 — Reservoir optimization | Experiment 4 — Flood inundation |
|:--:|:--:|
| ![Reservoir optimization](assets/reservoir_optimization.png) | ![Flood analysis](assets/flood_analysis.png) |
| Monte Carlo P10 / P50 / P90 · 100 scenarios | 9/9 physical validation checks passed |

---

## Results snapshot

<a id="results-snapshot"></a>

| Experiment | Key result |
|------------|------------|
| Rainfall monitoring | GREEN / YELLOW / RED classification validated; 3h/6h forecast risk pipeline |
| SCS-CN runoff | Reference Q = **13.80 mm** verified at P = 50 mm, CN = 80 |
| Reservoir optimization | Monte Carlo **P10 / P50 / P90** revenue and storage analysis (100 scenarios) |
| Flood inundation | **9/9** physical validation checks passed (monotonicity, bounds, DEM consistency) |

Full evidence: [docs/ENGINEERING.md](docs/ENGINEERING.md) · [docs/PHYSICAL_VALIDATION.md](docs/PHYSICAL_VALIDATION.md)

---

## Course assignments

<a id="course-assignments"></a>

Supporting deliverables across the semester (experiments above are the core technical work):

| Assignment | Topic | Link |
|------------|-------|------|
| **1** | LLM Universe Educational Website (MiniMax) | [Live site](https://d00r08r76qg9.space.minimaxi.com/) · [assignment1/](assignment1/) |
| **2** | CNN-Based MNIST Digit Classification | [assignment2/](assignment2/) |
| **3** | Swiss Cheese Testing & AI Failure Analysis | [assignment3/](assignment3/) |
| **4** | Smart Water Decision Support Capstone | [assignment4/](assignment4/) |

<p align="center">
  <a href="https://d00r08r76qg9.space.minimaxi.com/">
    <img src="assets/llm_universe_preview.png" alt="Assignment 1 — LLM Universe" width="70%">
  </a><br>
  <em>Assignment 1 — <a href="https://d00r08r76qg9.space.minimaxi.com/">LLM Universe</a> (MiniMax educational website)</em>
</p>

---

## Supporting coursework — weekly laboratory reports

<a id="lab-reports"></a>

**16 laboratory reports** document the semester learning journey (Weeks 1–8):

| Weeks | Topics |
|-------|--------|
| 1–2 | AI tools, prompt engineering, Chain-of-Thought reasoning |
| 3–4 | Agile development, refactoring, test-driven development |
| 5–6 | Hydrology experiments and engineering analysis |
| 7–8 | Smart Water capstone design, implementation, and testing |

➡️ [lab_reports/](lab_reports/) — 16 PDFs · LaTeX sources · appendix code

<p align="center">
  <a href="lab_reports/README.md">
    <img src="lab_reports/week5_session_a_lab1_streamlit.png" alt="Week 5 Lab 1" width="22%" />
    <img src="lab_reports/week5_session_b_lab2_sensitivity.png" alt="Week 5 Lab 2" width="22%" />
    <img src="lab_reports/week6_session_a_lab3_tradeoff.png" alt="Week 6 Lab 3" width="22%" />
    <img src="lab_reports/week6_session_b_lab4_comparison.png" alt="Week 6 Lab 4" width="22%" />
  </a>
</p>

---

## Quick start

<a id="quick-start"></a>

```bash
git clone https://github.com/mahmud456alhasan-debug/smart-water-capstone.git
cd smart-water-capstone
python3 -m pip install -r requirements.txt
streamlit run app/main.py
pytest -q    # 33 passed
```

Copy `dem.npy` into `data/` for the flood tab.

---

## Documentation

<a id="documentation"></a>

| Resource | Purpose |
|----------|---------|
| [submission/README.md](submission/README.md) | Experiment reports (PDF + LaTeX) |
| [docs/README.md](docs/README.md) | Full documentation index |
| [docs/ENGINEERING.md](docs/ENGINEERING.md) | Validation & AI engineering evidence |
| [docs/PRESENTATION_OUTLINE.md](docs/PRESENTATION_OUTLINE.md) | 5-minute demo script |
| [assignment1/](assignment1/) · [assignment2/](assignment2/) · [assignment3/](assignment3/) · [assignment4/](assignment4/) | Course assignments |
| [lab_reports/](lab_reports/) | Weekly lab reports |

---

## License

Academic coursework — Xi'an Jiaotong University, 2026.
