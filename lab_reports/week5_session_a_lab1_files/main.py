#!/usr/bin/env python3
"""CLI test: fetch weather → alert → history (Exercise 1–2 smoke test)."""

import logging
import sys

from alerts import append_alert_history, check_alert, log_alert
from config import ConfigError, load_settings
from openweather_client import WeatherAPIError, fetch_current_weather

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


def main() -> int:
    try:
        settings = load_settings()
    except ConfigError as exc:
        print(f"CONFIG ERROR: {exc}")
        return 1

    city = settings.default_city
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])

    try:
        reading = fetch_current_weather(city, settings)
    except WeatherAPIError as exc:
        print(f"API ERROR: {exc}")
        return 1

    alert = check_alert(reading.rainfall_mm_h, settings)
    log_alert(city, alert)
    append_alert_history(settings, city, alert)

    print(
        f"{city}: rain={reading.rainfall_mm_h:.2f} mm/h "
        f"({reading.description}) → {alert.level}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
