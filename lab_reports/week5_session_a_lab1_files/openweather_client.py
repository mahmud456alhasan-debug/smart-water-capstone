"""OpenWeather current weather — rainfall extraction with cache."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import requests

from config import Settings

logger = logging.getLogger(__name__)

# In-memory cache: city -> (timestamp, payload)
_cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}


class WeatherAPIError(Exception):
    """Weather API failure."""


@dataclass
class WeatherReading:
    city: str
    rainfall_mm_h: float
    description: str
    raw: Dict[str, Any]


def _extract_rainfall_mm_h(data: Dict[str, Any]) -> float:
    """rain.1h preferred; rain.3h fallback; missing -> 0."""
    rain = data.get("rain") or {}
    if "1h" in rain:
        return float(rain["1h"])
    if "3h" in rain:
        return float(rain["3h"])
    return 0.0


def fetch_current_weather(
    city: str,
    settings: Settings,
    use_cache: bool = True,
) -> WeatherReading:
    """Fetch current weather for city; cache by city name."""
    city_key = city.strip().lower()
    now = time.time()

    if use_cache and city_key in _cache:
        ts, cached = _cache[city_key]
        if now - ts < settings.cache_ttl_sec:
            logger.info("Cache hit for %s (age %.0fs)", city, now - ts)
            rain = _extract_rainfall_mm_h(cached)
            return WeatherReading(
                city=city,
                rainfall_mm_h=rain,
                description=(cached.get("weather") or [{}])[0].get(
                    "description", ""
                ),
                raw=cached,
            )

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": settings.openweather_api_key,
        "units": "metric",
    }
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

    try:
        data = resp.json()
    except ValueError as exc:
        raise WeatherAPIError(f"Invalid JSON: {exc}") from exc

    _cache[city_key] = (now, data)
    rain = _extract_rainfall_mm_h(data)
    logger.info("Fetched %s — rain=%.2f mm/h", city, rain)
    return WeatherReading(
        city=city,
        rainfall_mm_h=rain,
        description=(data.get("weather") or [{}])[0].get("description", ""),
        raw=data,
    )
