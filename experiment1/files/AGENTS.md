# AGENTS.md — Experiment 1: Rainfall Forecasting & Alert

**Student:** Mahmudul Hasan (4125999049)

## Experiment goal

Integrate OpenWeather API rainfall data, apply GREEN/YELLOW/RED thresholds (mm/h), log alerts, and provide CLI + Streamlit monitoring with human-verifiable tests.

## Physical constraints

| Rule | Enforcement |
|------|-------------|
| Rainfall ≥ 0 | `extract_rainfall_mm_h`; missing `rain` → 0 mm/h |
| Threshold order | GREEN < 10; YELLOW 10–20; RED ≥ 20 mm/h |
| No silent API failure | `WeatherAPIError` for 401/404/timeout |

## Known assumptions

- OpenWeather **current** weather (`/weather`), not forecast endpoints.
- Prefer `rain.1h`, fallback `rain.3h`.
- API key from `OPENWEATHER_API_KEY` only (never commit `.env`).

## Testing strategy

1. **Unit tests** — `tests/test_alerts.py`, `tests/test_api_client.py` (mocked HTTP).
2. **Boundary tests** — thresholds at 9.9 / 10 / 19.9 / 20 / 21 mm/h.
3. **Integration** — `main.py --file cities_world_famous.txt` (50-city batch).
4. **Demo mode** — Streamlit `?demo_mm=` for YELLOW/RED when live API is dry.

## Validation rules (Swiss Cheese)

| Layer | Check |
|-------|--------|
| AI-generated code | Manual review + modular split |
| Unit tests | `pytest -v` → 14 passed |
| Live API | 50/50 cities, 0 errors |
| Error paths | Invalid key → 401 message |
| Human demo | GREEN/YELLOW/RED at 5/15/21 mm/h |

## Run commands

```bash
cd experiment1_rainfall_alert
pip install -r requirements.txt
export OPENWEATHER_API_KEY=...   # or Demo storm mode
python3 main.py Beijing,CN
pytest -v
streamlit run weather_monitor.py
python3 generate_report_figures.py
```

## AI collaboration

Document every major prompt in `prompt_log.md`. Do not accept AI output without pytest + live/demo verification.
