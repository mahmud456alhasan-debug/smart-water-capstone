# Prompt Log - Week 2 Session B

## Exercise 1: Create AGENTS.md

**Date:** 2026-05-17

**Prompt used:**

I want to create an AGENTS.md file for my rainfall monitoring project.

The project is:
- A Python application using Streamlit
- Fetches weather data from OpenWeather API
- Displays rainfall data and alerts
- Uses pandas for data processing

Please generate a complete AGENTS.md file that includes:
1. Project overview
2. Tech stack
3. Directory structure
4. Key functions and their purposes
5. Data formats
6. API endpoints used

**AI output summary:**

OpenCode explored week2_session_a/ and wrote AGENTS.md documenting the actual codebase: FastAPI (not Streamlit), Open-Meteo (not OpenWeather), TimescaleDB/Redis, zone-based flood model, alert router, and real module names (data_pipeline.py, flood_model.py, etc.). Sections match the lab checklist.

**Edits you made before saving:**

- Matched documentation to real code rather than the lab prompt Streamlit/OpenWeather wording.
- Saved as week2_session_b/AGENTS.md (documents code in week2_session_a/).
- Verified no API keys in the file; conventions and run commands included.

**Where saved:** ai_water_lab/week2_session_b/AGENTS.md

---

## Exercise 2: Test AGENTS.md effectiveness

**Same question (both tests):** Write a function to fetch weather data

### Without AGENTS.md

**How you ran it:** New OpenCode chat in an empty folder (no AGENTS.md, no existing project files). Agent first asked for language and path; follow-up requested Python and fetch_weather_demo.py.

**Summary of AI output:**

- Libraries: requests (synchronous HTTP)
- API: Open-Meteo (https://api.open-meteo.com/v1/forecast), no API key
- Return type: plain dict with temperature_c, precipitation_mm, timestamp
- Error handling: try/except on requests.RequestException, raises RuntimeError
- Structure: single function + if __name__ == __main__ demo for New York City coordinates
- Not present: async/aiohttp, WeatherData dataclass, multi-zone fetch_all_zones, project-specific station_id or zone config

### With AGENTS.md

**How you ran it:** Project folder open with AGENTS.md and existing week2_session_a/ code visible to the agent.

**Summary of AI output:**

- File: week2_session_b/weather_fetcher.py
- Libraries: aiohttp, asyncio, dataclass
- API: Open-Meteo with current variables aligned to project needs
- Return type: WeatherData dataclass (station_id, time, precipitation, temp, humidity, pressure, wind)
- Extra: fetch_all_zones(zones) using asyncio.gather for concurrent multi-zone fetch
- Error handling: per-request timeout, returns None on failure, filters exceptions in fetch_all_zones
- Follow-up: second chat in same directory only fixed missing import asyncio (file already existed)

### Comparison

| Aspect | Without context | With AGENTS.md |
|--------|-----------------|----------------|
| HTTP style | Sync requests | Async aiohttp |
| Data model | dict | WeatherData dataclass |
| Multi-zone | No | fetch_all_zones() |
| Project alignment | Generic standalone script | Matches AGENTS.md conventions |

**Conclusion:** AGENTS.md steered the agent toward the project's async stack, typed models, and Open-Meteo usage patterns. Without context, the answer was still valid Python but simpler and not integrated with the urban flood-warning architecture.

---

## Exercise 3: Refine AGENTS.md

**What I changed after testing:**

- Clarified that application code lives under week2_session_a/ while AGENTS.md is stored in week2_session_b/.
- Added Do/Don't guidance: use async I/O and env vars; do not commit .env or API keys; do not use buggy_rainfall.py in production.
- Linked weather_fetcher.py as an example fetch module consistent with data_pipeline.py patterns.
- Kept sections scannable (overview, stack, structure, conventions) rather than pasting full source files.

**Reusable template ideas:**

- Start AGENTS.md from real repo scan, not only the lab prompt.
- Always run a without vs with comparison using an empty folder for the baseline.
- Keep secrets out of AGENTS.md; document env vars only.

---

## Lessons learned

AGENTS.md acts as durable project memory: the with context run produced code aligned with FastAPI/async/Open-Meteo conventions, while the empty-folder run needed clarifying questions and yielded a minimal sync wrapper. Context window limits mean AGENTS.md should stay scannable (overview, stack, structure, conventions) rather than duplicating entire files. Human review still matters (e.g. fixing import asyncio, verifying APIs).
