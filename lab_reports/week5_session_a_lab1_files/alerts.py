"""Threshold-based rainfall alerts — GREEN / YELLOW / RED (mm/h)."""

from __future__ import annotations

import csv
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Tuple

from config import Settings

logger = logging.getLogger(__name__)

HISTORY_COLUMNS = [
    "timestamp_utc",
    "city",
    "rainfall_mm_h",
    "level",
    "message",
]


@dataclass
class AlertResult:
    level: str  # GREEN, YELLOW, RED
    message: str
    rainfall_mm_h: float


def check_alert(rainfall_mm_h: float, settings: Settings) -> AlertResult:
    """Thresholds: GREEN <10, YELLOW 10–20, RED >20 mm/h (configurable)."""
    r = rainfall_mm_h
    if r < settings.green_max_mm_h:
        return AlertResult(
            level="GREEN",
            message=f"Normal conditions ({r:.1f} mm/h)",
            rainfall_mm_h=r,
        )
    if r <= settings.yellow_max_mm_h:
        return AlertResult(
            level="YELLOW",
            message=f"Moderate rainfall ({r:.1f} mm/h) — monitor closely",
            rainfall_mm_h=r,
        )
    return AlertResult(
        level="RED",
        message=f"Heavy rainfall ({r:.1f} mm/h) — flood risk elevated",
        rainfall_mm_h=r,
    )


def log_alert(city: str, alert: AlertResult) -> None:
    logger.info(
        "ALERT %s | %s | %s | %.2f mm/h",
        alert.level,
        city,
        alert.message,
        alert.rainfall_mm_h,
    )


def append_alert_history(
    settings: Settings,
    city: str,
    alert: AlertResult,
) -> None:
    path = settings.alert_history_csv
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    write_header = not os.path.isfile(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HISTORY_COLUMNS)
        if write_header:
            w.writeheader()
        w.writerow(
            {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "city": city,
                "rainfall_mm_h": f"{alert.rainfall_mm_h:.2f}",
                "level": alert.level,
                "message": alert.message,
            }
        )


def load_alert_history(settings: Settings) -> List[dict]:
    path = settings.alert_history_csv
    if not os.path.isfile(path):
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))
