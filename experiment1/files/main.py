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
from config import ConfigError, load_settings, offline_settings
from email_alerts import send_red_alert_email
from simulate import SCENARIO_MM_H, auto_simulate_mm, simulate_reading


def load_cities_from_file(path: Path) -> list[str]:
    cities = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cities.append(line)
    return cities


def run_city(
    city: str,
    delay_sec: float = 0.0,
    simulate_mm: float | None = None,
    send_email: bool = False,
) -> tuple[int, str | None]:
    settings = offline_settings() if simulate_mm is not None else load_settings()
    if delay_sec > 0:
        time.sleep(delay_sec)
    if simulate_mm is not None:
        reading = simulate_reading(city, simulate_mm)
    else:
        try:
            reading = fetch_current_weather(city, settings, use_cache=False)
        except WeatherAPIError as exc:
            print(f"{city}: API ERROR: {exc}")
            return 1, None
    alert = check_alert(reading.rainfall_mm_h, settings)
    log_alert(city, alert, settings)
    if send_email and alert.level == "RED":
        send_red_alert_email(city, alert, settings)
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
    parser.add_argument(
        "--simulate",
        nargs="?",
        const=-1.0,
        type=float,
        metavar="MM_H",
        help="Offline mode: fixed mm/h for all cities, or per-city auto if flag alone",
    )
    parser.add_argument(
        "--scenario",
        choices=sorted(SCENARIO_MM_H),
        help="Offline preset: green=5, yellow=15, red=21 mm/h",
    )
    parser.add_argument(
        "--email",
        action="store_true",
        help="Send SMTP email (or log to email_outbox.txt) on RED alerts",
    )
    args = parser.parse_args()

    simulate_mm: float | None = None
    if args.scenario:
        simulate_mm = SCENARIO_MM_H[args.scenario]
    elif args.simulate is not None:
        simulate_mm = None if args.simulate < 0 else args.simulate

    offline = simulate_mm is not None or args.simulate is not None or args.scenario
    if not offline:
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
        city_mm = simulate_mm
        if args.simulate is not None and args.simulate < 0 and not args.scenario:
            city_mm = auto_simulate_mm(city)
        err, level = run_city(
            city, delay_sec=delay, simulate_mm=city_mm, send_email=args.email
        )
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
