"""Configuration for rainfall monitoring integration (Week 4 Session B).

Validates all environment variables at load time for fast failure on bad config.
"""

import os
from dataclasses import dataclass


class ConfigError(Exception):
    """Invalid environment configuration."""


@dataclass
class Settings:
    latitude: float
    longitude: float
    openweather_api_key: str
    use_open_meteo: bool
    rainfall_alert_mm: float
    runoff_alert_mm: float
    default_cn: int
    csv_path: str
    api_timeout_sec: float
    api_max_retries: int


def _parse_float(key: str, default: float) -> float:
    raw = os.getenv(key)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        raise ConfigError(
            f"{key}={raw!r} is not a valid float"
        )


def _parse_int(key: str, default: int) -> int:
    raw = os.getenv(key)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        raise ConfigError(
            f"{key}={raw!r} is not a valid integer"
        )


def _parse_bool(key: str, default: bool) -> bool:
    raw = os.getenv(key)
    if raw is None:
        return default
    return raw == "1"


def load_settings() -> Settings:
    return Settings(
        latitude=_parse_float("MONITOR_LAT", 23.8103),
        longitude=_parse_float("MONITOR_LON", 90.4125),
        openweather_api_key=os.getenv("OPENWEATHER_API_KEY", ""),
        use_open_meteo=_parse_bool("USE_OPEN_METEO", True),
        rainfall_alert_mm=_parse_float("RAINFALL_ALERT_MM", 20.0),
        runoff_alert_mm=_parse_float("RUNOFF_ALERT_MM", 15.0),
        default_cn=_parse_int("DEFAULT_CN", 80),
        csv_path=os.getenv("MONITOR_CSV", "data/monitoring_log.csv"),
        api_timeout_sec=_parse_float("API_TIMEOUT_SEC", 10),
        api_max_retries=_parse_int("API_MAX_RETRIES", 3),
    )
