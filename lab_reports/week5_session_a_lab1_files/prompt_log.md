# Prompt Log - Week 5 Session A Lab 1

**Student:** Mahmudul Hasan (4125999049)  
**Lab:** Rainfall Forecasting & Alert System

---

## API integration (Exercise 1)

**API field used for rain:** `rain.1h` (mm/h); if absent, `rain.3h`; if no `rain` object → **0 mm** (documented in `openweather_client.py`).

**Endpoint:** `https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric`

**Threshold units:** mm/h (aligned with OpenWeather `rain.1h`).

**Prompt used:** `prompt_weather_api.txt` (optional OpenCode polish); baseline code in repo.

**OpenCode changes:** [If you enhanced via OpenCode, note here; otherwise “used provided openweather_client.py”.]

**Validation cities run:**
- First attempt: `401 Invalid API key` (key not yet activated)
- After activation: Dhaka,BD; Beijing,CN; Delhi,IND; Moscow,RUS; Islamabad,PK — all **0.00 mm/h**, **GREEN**

**What domain checks caught:** Dry conditions correctly show 0 mm/h when API omits `rain`; thresholds interpreted as mm/h.

---

## Alerts (Exercise 2)

**Thresholds:** GREEN &lt; 10 mm/h | YELLOW 10–20 mm/h | RED &gt; 20 mm/h (env: `GREEN_MAX_MM_H`, `YELLOW_MAX_MM_H`).

**History storage:** `data/alert_history.csv` (5 rows after multi-city CLI test).

**Functions:** `check_alert()`, `log_alert()`, `append_alert_history()`.

**Prompt used:** `prompt_alert.txt` (if sent to OpenCode).

---

## Dashboard (Exercise 3)

**Prompt used:** `prompt_dashboard.txt` (if sent to OpenCode).

**Run:** `python3 -m streamlit run dashboard.py` → http://localhost:8501

**UI:** City input, Refresh, rainfall metric, color-coded alert, history table, last update.

---

## Validation (Exercise 4)

- [x] Dry cities → 0 mm/h, GREEN (multiple cities)
- [x] Invalid key → `API ERROR: Invalid API key (401)` before activation
- [x] CSV append → 5 rows in `alert_history.csv`
- [x] Dashboard runs at localhost:8501
- [ ] Wet/high rain city (optional if no rain globally — note in report)

**Failure test command:**
```bash
OPENWEATHER_API_KEY=bad python3 main.py Dhaka,BD
```

---

## Lessons learned

OpenWeather keys may need activation time (401 then success). Use `export OPENWEATHER_API_KEY` only in terminal. Same `python3 -m streamlit` pattern as Week 4B. Terminal screenshot showing 401 → success is good evidence for the report.
