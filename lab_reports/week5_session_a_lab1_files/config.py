"""Week 5 Session A Lab 1 — configuration (no secrets in code)."""

import os
from dataclasses import dataclass


class ConfigError(Exception):
    """Invalid or missing configuration."""


@dataclass
class Settings:
    openweather_api_key: str
    default_city: str
    cache_ttl_sec: int
    api_timeout_sec: float
    # Thresholds in mm/h (rain.1h from OpenWeather current weather)
    green_max_mm_h: float
    yellow_max_mm_h: float
    alert_history_csv: str


def _require_api_key() -> str:
    key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not key:
        raise ConfigError(
            "OPENWEATHER_API_KEY is not set. Export your key before running."
        )
    return key


def load_settings() -> Settings:
    return Settings(
        openweather_api_key=_require_api_key(),
        default_city=os.getenv("MONITOR_CITY", "Dhaka,BD"),
        cache_ttl_sec=int(os.getenv("CACHE_TTL_SEC", "300")),
        api_timeout_sec=float(os.getenv("API_TIMEOUT_SEC", "10")),
        green_max_mm_h=float(os.getenv("GREEN_MAX_MM_H", "10")),
        yellow_max_mm_h=float(os.getenv("YELLOW_MAX_MM_H", "20")),
        alert_history_csv=os.getenv(
            "ALERT_HISTORY_CSV", "data/alert_history.csv"
        ),
    )
