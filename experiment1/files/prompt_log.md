# Prompt Log - Experiment 1: Rainfall Alert

**Student:** Mahmudul Hasan (4125999049)  
**Folder:** `experiment1_rainfall_alert/` (separate from Week 5 Lab 1)

---

## Part 1: API Integration

**Prompt used:**

```text
I am a water resources student building a rainfall monitoring system. Write Python using requests to fetch current weather for a city from OpenWeatherMap API 2.5/weather. Extract rainfall (rain.1h then rain.3h), handle 401/404/network errors, use OPENWEATHER_API_KEY from environment only.
```

**AI output summary:** `api_client.py` with `fetch_current_weather`, `extract_rainfall_mm_h`, in-memory cache.

**Corrections made:** Documented `rain_field_used` in `WeatherReading`; missing rain returns 0 mm/h.

**Threshold units:** mm/h when `rain.1h` is present.

---

## Part 2: Alert Logic

**Prompt used:**

```text
Implement check_alert for GREEN <10, YELLOW 10-20, RED >=20 mm/h. log_alert appends ISO lines to alert_log.txt.
```

**Corrections made:** RED uses `>= yellow_max` (20 mm/h) per experiment table.

---

## Part 3: Dashboard

**Prompt used:**

```text
Streamlit dashboard: city input, large rainfall metric, color alert status, refresh button, alert history from alert_log.txt.
```

**Run:** `streamlit run weather_monitor.py`

---

## Part 4: Validation

| Case | Result |
|------|--------|
| pytest alert thresholds | PASS (GREEN/YELLOW/RED) |
| 50-city batch (`cities_world_famous.txt`) | 50/50 GREEN, 0 API errors (2026-05-22) |
| Max live rainfall | Lagos,NG 1.75 mm/h (rain.1h) |
| Dry / no rain field | Most cities: none -> 0 mm/h, GREEN |
| alert_log.txt | 51 lines appended |
| Invalid API key | `OPENWEATHER_API_KEY=bad` -> 401 Unauthorized |
| Streamlit dashboard | `streamlit run weather_monitor.py` |
| Boundary pytest | 14 passed (9.9-25 mm/h + mock API) |
| Demo storm mode | Live Streamlit screenshots at ?demo_mm=5/15/21 |
| Architecture figure | architecture.png in report |
| Lessons learned | Documented in LaTeX report section |

**API field used for rain:** `rain.1h` when present; else none -> 0.

**Command:** `python3 main.py --file cities_world_famous.txt`

---

## Lessons learned

Keep Experiment 1 in its own folder separate from the capstone. Never commit API keys. Document which rain JSON field is used before trusting alert colors.
