# Experiment 1 — Submission Package

**Student:** Mahmudul Hasan (4125999049)  
**Code (runnable):** `../../ai_water_lab/experiment1_rainfall_alert/`

## Upload to Overleaf (this folder)

```
Experiment1_Rainfall_Alert/
├── Experiment1_Rainfall_Alert_Report.tex   ← main document
├── README.md
├── files/                                   ← appendix (ASCII source)
└── screenshots/                             ← figures only (see list below)
```

**Do not upload** to Overleaf: `*_fallback.png`, `.pytest_cache/`, `.env`, real API keys.

## Required screenshots (8 figures)

| File | Report reference |
|------|------------------|
| `architecture.png` | Figure: architecture |
| `experiment1_terminal.png` | Figure: 50-city terminal |
| `experiment1_pytest.png` | Figure: pytest |
| `demo_green.png` | Figure: demo (GREEN) |
| `demo_yellow.png` | Figure: demo (YELLOW) |
| `demo_red.png` | Figure: demo (RED) |
| `experiment1_invalid-key.png` | Figure: 401 |
| `experiment1_streamlit.png` | Figure: Streamlit dashboard |

## Before you submit

- [ ] Compile PDF twice on Overleaf (references stable)
- [ ] All 8 PNGs show in PDF preview
- [ ] No red “missing figure” boxes
- [ ] Student name and ID on title page
- [ ] Run locally: `pytest -q` → 14 passed
- [ ] No API key in `files/` appendix or git

## Compile

Menu: **Recompile** on Overleaf, or locally:

```bash
pdflatex Experiment1_Rainfall_Alert_Report.tex
pdflatex Experiment1_Rainfall_Alert_Report.tex
```

## Code zip (if LMS asks separately)

Zip `experiment1_rainfall_alert/` excluding:

- `.pytest_cache/`, `__pycache__/`, `.env`
- `*_fallback.png` (report folder only)

Include: `weather_monitor.py`, `api_client.py`, `alerts.py`, `config.py`, `main.py`, `tests/`, `prompt_log.md`, `requirements.txt`, `.env.example`, `README.md`.
