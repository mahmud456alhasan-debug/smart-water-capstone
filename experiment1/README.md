# Experiment 1 — Rainfall Monitoring & Alert System

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026

| Resource | Link |
|----------|------|
| **Report (PDF)** | [Experiment1_Rainfall_Alert_Report.pdf](Experiment1_Rainfall_Alert_Report.pdf) |
| **LaTeX source** | [Experiment1_Rainfall_Alert_Report.tex](Experiment1_Rainfall_Alert_Report.tex) |
| Appendix code | [`files/`](files/) |
| Figures | [`screenshots/`](screenshots/) |

Integrated in capstone: [`app/main.py`](../app/main.py) · [`src/weather/`](../src/weather/)

## Features

| Feature | Status |
|---------|--------|
| OpenWeatherMap fetch + API error handling | Required |
| GREEN / YELLOW / RED alerts (10, 20 mm/h) + alert log | Required |
| Streamlit dashboard | Required |
| Demo storm mode (`?demo_mm=` URL + slider) | Extra |
| **`--simulate` / `--scenario` CLI (no API key)** | Extra |
| **`--email` RED alert notifications (SMTP or outbox log)** | Extra |
| 3h / 6h forecast risk pipeline | Extra |
| pytest suite (**25 tests**) | Extra |

## Run locally

```bash
cd files
pip install -r requirements.txt   # if present in dev repo
python main.py --scenario yellow Beijing,CN Dhaka,BD
python main.py --scenario red --email Beijing,CN   # logs to email_outbox.txt without SMTP
python main.py --simulate          # auto mm/h per city, offline
streamlit run weather_monitor.py
python -m pytest -q
```

```bash
pdflatex Experiment1_Rainfall_Alert_Report.tex && pdflatex Experiment1_Rainfall_Alert_Report.tex
```
