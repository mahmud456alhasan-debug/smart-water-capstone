#!/usr/bin/env python3
"""Integrated rainfall monitor — wire-up target for Exercise 1–2.

Data flow:
  config.py --> weather_client.py --> rainfall_processor.py --> alert_system.py --> storage.py

Flow details:
  1. load_settings()        — reads env vars via config.Settings
  2. fetch_precipitation_mm() — Open-Meteo (default) or OpenWeather API,
                                with exponential-backoff retry (settings.api_max_retries)
  3. process_reading()      — SCS-CN runoff calculation
  4. evaluate_alerts()      — thresholds -> OK / WATCH / ALERT
  5. append_reading()       — writes CSV row at settings.csv_path

Error boundaries:
  - Config error (bad env var) -> log ERROR, print CONFIG ERROR, exit 1
  - Weather API failure         -> log ERROR, print DEGRADED, exit 1
  - Storage write failure       -> log ERROR, print WARNING, continue (non-fatal)
"""

from __future__ import annotations

import logging
import sys

from alert_system import evaluate_alerts
from config import ConfigError, load_settings
from rainfall_processor import process_reading
from storage import StorageError, append_reading
from weather_client import WeatherAPIError, fetch_precipitation_mm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("monitor")


def run_once() -> int:
    try:
        settings = load_settings()
    except ConfigError as exc:
        logger.error("Configuration error: %s", exc)
        print(f"CONFIG ERROR: {exc}")
        return 1

    api_source = "open-meteo" if settings.use_open_meteo else "openweather"

    logger.info("Fetching precipitation via %s (lat=%.4f lon=%.4f) ...",
                api_source, settings.latitude, settings.longitude)

    try:
        rainfall_mm = fetch_precipitation_mm(settings)
    except WeatherAPIError as exc:
        logger.error("Weather fetch failed after %d retries: %s",
                      settings.api_max_retries, exc)
        print(f"DEGRADED: weather unavailable ({exc})")
        return 1

    logger.info("Raw precipitation: %.2f mm", rainfall_mm)

    processed = process_reading(rainfall_mm, cn=settings.default_cn)
    logger.info("Processed: rain=%.2f mm  runoff=%.2f mm  CN=%.0f",
                processed["rainfall_mm"], processed["runoff_mm"],
                processed["cn"])

    alert = evaluate_alerts(processed, settings)
    logger.info("Alert level: %s — %s", alert.level, alert.message)

    try:
        append_reading(
            settings, processed, alert.level, alert.message, api_source,
        )
    except StorageError as exc:
        logger.error("Storage write failed: %s", exc)
        print(f"WARNING: could not persist reading ({exc})")

    print(
        f"OK rain={processed['rainfall_mm']:.2f} mm "
        f"runoff={processed['runoff_mm']:.2f} mm alert={alert.level}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(run_once())
