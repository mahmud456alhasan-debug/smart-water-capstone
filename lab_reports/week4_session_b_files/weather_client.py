"""Weather API client — Open-Meteo (no key) or OpenWeather (env key).

Retry with exponential backoff is applied in the unified entry point.
"""

from __future__ import annotations

import logging
import random
import time
from typing import Any, Dict, Optional

import requests

from config import Settings

logger = logging.getLogger(__name__)


class WeatherAPIError(Exception):
    """Raised when weather data cannot be fetched or parsed."""


def fetch_open_meteo_precipitation_mm(settings: Settings) -> float:
    """Current-hour precipitation (mm) from Open-Meteo."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": settings.latitude,
        "longitude": settings.longitude,
        "current": "precipitation",
        "timezone": "auto",
    }
    resp = requests.get(url, params=params, timeout=settings.api_timeout_sec)
    resp.raise_for_status()
    try:
        data = resp.json()
    except ValueError as exc:
        raise WeatherAPIError(
            f"Open-Meteo invalid JSON: {exc}"
        ) from exc
    current = data.get("current") or {}
    precip = current.get("precipitation")
    if precip is None:
        raise WeatherAPIError("Open-Meteo response missing current.precipitation")
    return float(precip)


def fetch_openweather_precipitation_mm(settings: Settings) -> float:
    """Rain in last 1h (mm) from OpenWeather — requires OPENWEATHER_API_KEY."""
    if not settings.openweather_api_key:
        raise WeatherAPIError("OPENWEATHER_API_KEY not set")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": settings.latitude,
        "lon": settings.longitude,
        "appid": settings.openweather_api_key,
        "units": "metric",
    }
    resp = requests.get(url, params=params, timeout=settings.api_timeout_sec)
    resp.raise_for_status()
    try:
        data = resp.json()
    except ValueError as exc:
        raise WeatherAPIError(
            f"OpenWeather invalid JSON: {exc}"
        ) from exc
    rain = (data.get("rain") or {}).get("1h")
    if rain is None:
        return 0.0
    return float(rain)


def fetch_precipitation_mm(settings: Settings) -> float:
    """Unified entry: Open-Meteo by default, with retry + exponential backoff."""
    max_retries = settings.api_max_retries
    last_exc = None

    for attempt in range(1, max_retries + 2):
        try:
            if settings.use_open_meteo:
                return fetch_open_meteo_precipitation_mm(settings)
            return fetch_openweather_precipitation_mm(settings)
        except (requests.RequestException, WeatherAPIError) as exc:
            last_exc = exc
            logger.warning(
                "Weather fetch attempt %d/%d failed: %s",
                attempt, max_retries + 1, exc,
            )
            if attempt <= max_retries:
                delay = 2.0 ** (attempt - 1)
                jitter = random.uniform(0, 0.5)
                time.sleep(delay + jitter)

    raise WeatherAPIError(
        f"All {max_retries + 1} attempts failed"
    ) from last_exc
