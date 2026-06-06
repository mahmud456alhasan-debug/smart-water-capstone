"""OpenWeather current weather API client - Experiment 1 Part 1."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import requests

from config import Settings

_cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}


class WeatherAPIError(Exception):
    """API request or parse failure."""


@dataclass
class WeatherReading:
    city: str
    rainfall_mm_h: float
    rain_field_used: str
    description: str


def extract_rainfall_mm_h(data: Dict[str, Any]) -> Tuple[float, str]:
    """
    Prefer rain.1h (mm in last hour); fallback rain.3h; missing -> 0.
    Document field in prompt_log for physical interpretation.
    """
    rain = data.get("rain") or {}
    if "1h" in rain:
        return float(rain["1h"]), "rain.1h"
    if "3h" in rain:
        return float(rain["3h"]), "rain.3h"
    return 0.0, "none"


def fetch_current_weather(
    city: str, settings: Settings, use_cache: bool = True
) -> WeatherReading:
    city_key = city.strip().lower()
    now = time.time()
    if use_cache and city_key in _cache:
        ts, cached = _cache[city_key]
        if now - ts < settings.cache_ttl_sec:
            rain, field = extract_rainfall_mm_h(cached)
            desc = (cached.get("weather") or [{}])[0].get("description", "")
            return WeatherReading(city, rain, field, desc)

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": settings.openweather_api_key, "units": "metric"}
    try:
        resp = requests.get(url, params=params, timeout=settings.api_timeout_sec)
    except requests.RequestException as exc:
        raise WeatherAPIError(f"Network error: {exc}") from exc

    if resp.status_code == 401:
        raise WeatherAPIError("Invalid API key (401 Unauthorized)")
    if resp.status_code == 404:
        raise WeatherAPIError(f"City not found: {city!r}")
    if not resp.ok:
        raise WeatherAPIError(f"HTTP {resp.status_code}: {resp.text[:200]}")

    data = resp.json()
    _cache[city_key] = (now, data)
    rain, field = extract_rainfall_mm_h(data)
    desc = (data.get("weather") or [{}])[0].get("description", "")
    return WeatherReading(city, rain, field, desc)


def clear_weather_cache() -> None:
    """Clear in-memory cache (for tests)."""
    _cache.clear()
