"""Append monitoring readings to CSV."""

from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from typing import Dict

from config import Settings


CSV_COLUMNS = [
    "timestamp_utc",
    "rainfall_mm",
    "runoff_mm",
    "cn",
    "alert_level",
    "alert_message",
    "api_source",
]


class StorageError(Exception):
    """CSV read/write failure."""


def ensure_csv(settings: Settings) -> None:
    if os.path.isfile(settings.csv_path):
        return
    try:
        os.makedirs(os.path.dirname(settings.csv_path) or ".", exist_ok=True)
        with open(settings.csv_path, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=CSV_COLUMNS).writeheader()
    except OSError as exc:
        raise StorageError(
            f"Cannot create CSV at {settings.csv_path}: {exc}"
        ) from exc


def append_reading(
    settings: Settings,
    processed: Dict[str, float],
    alert_level: str,
    alert_message: str,
    api_source: str,
) -> None:
    ensure_csv(settings)
    row = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "rainfall_mm": processed["rainfall_mm"],
        "runoff_mm": processed["runoff_mm"],
        "cn": processed["cn"],
        "alert_level": alert_level,
        "alert_message": alert_message,
        "api_source": api_source,
    }
    try:
        with open(settings.csv_path, "a", newline="") as f:
            csv.DictWriter(f, fieldnames=CSV_COLUMNS).writerow(row)
    except OSError as exc:
        raise StorageError(str(exc)) from exc
