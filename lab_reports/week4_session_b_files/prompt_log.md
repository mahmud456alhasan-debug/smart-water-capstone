# Prompt Log - Week 4 Session B

**Student:** Mahmudul Hasan (4125999049)  
**Lab:** Integration & Flow Practice

---

## Integration

**Data flow (one sentence):** `load_settings` → `fetch_precipitation_mm` (Open-Meteo) → `process_reading` (SCS-CN runoff) → `evaluate_alerts` → `append_reading` → `data/monitoring_log.csv`.

**Hardest handoff between components:** Weather API → processor: retries must complete before alert/storage; storage errors must not mask weather failures.

**Prompt used (Exercise 1):** `prompt_integration.txt`

**OpenCode changes (Exercise 1):** `main.py` logging + error boundaries; `weather_client.py` retry with exponential backoff + jitter.

**Terminal (success):** `OK rain=0.00 mm runoff=0.00 mm alert=OK` — CSV row appended with `open-meteo`.

---

## Errors & resilience

**Prompt used (Exercise 2):** `prompt_errors.txt`

**OpenCode changes (Exercise 2):**
- `config.py`: `ConfigError`, `load_settings()` validates env (no parse at import time)
- `weather_client.py`: invalid JSON → `WeatherAPIError`
- `storage.py`: `OSError` → `StorageError` in `ensure_csv`
- `main.py`: `ConfigError` → `CONFIG ERROR` exit 1; weather → `DEGRADED` exit 1; storage → `WARNING` non-fatal

**Failure modes tested:**

| Test | Command | Expected | Result |
|------|---------|----------|--------|
| Bad config | `MONITOR_LAT=abc python3 main.py` | CONFIG ERROR, exit 1 | Yes — no traceback |
| Bad API coords | `MONITOR_LAT=999 python3 main.py` | 4 retries, DEGRADED, exit 1 | Yes — no new bad row |
| API timeout | `API_TIMEOUT_SEC=0.001 python3 main.py` | retries, DEGRADED, exit 1 | Yes |
| Normal | `python3 main.py` | exit 0, CSV append | Yes |

**Note:** `MONITOR_LAT=not_a_number` crashed at import *before* Exercise 2 fix (class-level `float()`). After fix, invalid env is caught in `load_settings()` with a clear message.

**Still fragile (if any):** No cached last-good reading when API fails; dashboard pending (Exercise 3).

---

## Dashboard

**Prompt used (Exercise 3):** `prompt_dashboard.txt`

**OpenCode changes:** `dashboard.py` — metrics (rain, alert, timestamp, health), color-coded alert, line chart, last-10 table, empty/missing CSV handling.

**Run command (use module form if `streamlit` not on PATH):**

```bash
python3 -m pip install --user streamlit   # once
python3 -m streamlit run dashboard.py
```

Browser opens at http://localhost:8501 — screenshot for submission.

---

## Flow

**What kept you in flow / broke flow:** Same OpenCode thread for Exercises 1–2; testing three env variants (`abc`, `999`, timeout) immediately after each change. Clear exit messages (`CONFIG ERROR` vs `DEGRADED`) made screenshots easy to label.

---

## Verification (Exercise 4)

- [x] Cold start: `python3 main.py` works
- [x] API failure: DEGRADED, exit 1, logs show retries
- [x] Config failure: CONFIG ERROR, exit 1
- [x] CSV append on success path
- [x] Dashboard: `python3 -m streamlit run dashboard.py` (after install)

---

## Lessons learned

Boundary errors at config, network, and storage kept `main.py` readable. Retries belong in the client module. Always re-test failure paths after AI changes — import-time config parsing was a real bug until Exercise 2.
