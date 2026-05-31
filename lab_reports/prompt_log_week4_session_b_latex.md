# Prompt Log - Week 4 Session B

**Student:** Mahmudul Hasan (4125999049)
**Lab:** Integration and Flow Practice

## Integration

Data flow: load_settings -> fetch_precipitation_mm -> process_reading -> evaluate_alerts -> append_reading -> CSV.

Prompt: prompt_integration.txt. OpenCode: main.py logging and boundaries; weather_client retry with backoff.

## Errors and resilience

Prompt: prompt_errors.txt. ConfigError, JSON parse errors, StorageError, CONFIG ERROR vs DEGRADED.

Tests: MONITOR_LAT=abc (config), MONITOR_LAT=999 (API), API_TIMEOUT_SEC=0.001 (timeout).

## Dashboard

Prompt: prompt_dashboard.txt. streamlit dashboard.py. Run: python3 -m streamlit run dashboard.py

## Verification

Cold start OK; API failure DEGRADED; config CONFIG ERROR; CSV append; dashboard screenshot.

## Lessons learned

Boundary errors and module-form streamlit run; re-test after AI config fix.
