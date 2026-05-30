#!/usr/bin/env python3
"""CLI validation for Experiment 1 (terminal screenshot evidence)."""

from __future__ import annotations

import argparse
import sys
import time
from collections import Counter
from pathlib import Path

from alerts import check_alert, log_alert
from api_client import WeatherAPIError, fetch_current_weather
from config import ConfigError, load_settings


def load_cities_from_file(path: Path) -> list[str]:
    cities = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cities.append(line)
    return cities


def run_city(city: str, delay_sec: float = 0.0) -> tuple[int, str | None]:
    settings = load_settings()
    if delay_sec > 0:
        time.sleep(delay_sec)
    try:
        reading = fetch_current_weather(city, settings, use_cache=False)
    except WeatherAPIError as exc:
        print(f"{city}: API ERROR: {exc}")
        return 1, None
    alert = check_alert(reading.rainfall_mm_h, settings)
    log_alert(city, alert, settings)
    print(
        f"{city}: rain={reading.rainfall_mm_h:.2f} mm/h "
        f"({reading.rain_field_used}) -> {alert.level}"
    )
    return 0, alert.level


def main() -> int:
    parser = argparse.ArgumentParser(description="Experiment 1 multi-city rainfall CLI")
    parser.add_argument(
        "cities",
        nargs="*",
        help="City names (e.g. Beijing,CN). Default: Beijing,CN Dhaka,BD",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=Path,
        help="Text file of cities (one per line), e.g. cities_world_famous.txt",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.15,
        help="Seconds between API calls when using --file (default 0.15)",
    )
    args = parser.parse_args()

    try:
        load_settings()
    except ConfigError as exc:
        print(exc)
        return 1

    if args.file:
        if not args.file.is_file():
            print(f"City file not found: {args.file}")
            return 1
        cities = load_cities_from_file(args.file)
        print(f"Loaded {len(cities)} cities from {args.file.name}\n")
    elif args.cities:
        cities = args.cities
    else:
        cities = ["Beijing,CN", "Dhaka,BD"]

    code = 0
    levels: Counter[str] = Counter()
    errors = 0
    for i, city in enumerate(cities):
        delay = args.delay if args.file and i > 0 else 0.0
        err, level = run_city(city, delay_sec=delay)
        code |= err
        if level:
            levels[level] += 1
        else:
            errors += 1

    if len(cities) > 1:
        print("\n--- Summary ---")
        print(f"Cities queried: {len(cities)}")
        for lvl in ("GREEN", "YELLOW", "RED"):
            if levels[lvl]:
                print(f"  {lvl}: {levels[lvl]}")
        if errors:
            print(f"  API errors: {errors}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
