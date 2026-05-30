"""Experiment 1 - configuration (API key from environment only)."""

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
    green_max_mm_h: float
    yellow_max_mm_h: float
    alert_log_path: str


def load_settings() -> Settings:
    key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not key:
        raise ConfigError(
            "Set OPENWEATHER_API_KEY before running (never commit keys to git)."
        )
    return Settings(
        openweather_api_key=key,
        default_city=os.getenv("MONITOR_CITY", "Beijing,CN"),
        cache_ttl_sec=int(os.getenv("CACHE_TTL_SEC", "300")),
        api_timeout_sec=float(os.getenv("API_TIMEOUT_SEC", "10")),
        green_max_mm_h=float(os.getenv("GREEN_MAX_MM_H", "10")),
        yellow_max_mm_h=float(os.getenv("YELLOW_MAX_MM_H", "20")),
        alert_log_path=os.getenv("ALERT_LOG_PATH", "alert_log.txt"),
    )
