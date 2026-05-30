"""Threshold alerts and file logging - Experiment 1 Part 2."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

from config import Settings

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None  # type: ignore


@dataclass
class AlertResult:
    level: str
    message: str
    rainfall_mm_h: float


def check_alert(rainfall_mm_h: float, settings: Settings) -> AlertResult:
    """GREEN <10; YELLOW 10-20; RED >=20 mm/h (configurable)."""
    r = rainfall_mm_h
    if r < settings.green_max_mm_h:
        return AlertResult(
            level="GREEN",
            message=f"Normal conditions ({r:.1f} mm/h)",
            rainfall_mm_h=r,
        )
    if r < settings.yellow_max_mm_h:
        return AlertResult(
            level="YELLOW",
            message=f"Moderate rainfall ({r:.1f} mm/h) - monitor closely",
            rainfall_mm_h=r,
        )
    return AlertResult(
        level="RED",
        message=f"ALERT: Heavy rainfall ({r:.1f} mm/h) - flood risk elevated",
        rainfall_mm_h=r,
    )


def log_alert(
    city: str, alert: AlertResult, settings: Settings, log_all_levels: bool = True
) -> None:
    """Append ISO timestamp lines to alert_log.txt."""
    if alert.level != "RED" and not log_all_levels:
        return
    path = settings.alert_log_path
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    line = (
        f"{ts} | {city} | {alert.level} | {alert.rainfall_mm_h:.2f} mm/h | {alert.message}\n"
    )
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)


def read_alert_log(path: str, max_lines: int = 500) -> List[str]:
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    return [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")][-max_lines:]


_RAIN_RE = re.compile(r"([\d.]+)\s*mm/h", re.I)


def parse_alert_log_rows(path: str, max_lines: int = 500) -> List[dict]:
    """Parse pipe-separated log lines into dict rows."""
    rows: List[dict] = []
    for line in read_alert_log(path, max_lines=max_lines):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 5:
            continue
        rain_match = _RAIN_RE.search(parts[3])
        rain_val = float(rain_match.group(1)) if rain_match else 0.0
        rows.append(
            {
                "timestamp_utc": parts[0],
                "city": parts[1],
                "level": parts[2],
                "rainfall_mm_h": rain_val,
                "message": parts[4],
            }
        )
    return rows


def alert_log_dataframe(path: str, max_lines: int = 500):
    """Return pandas DataFrame of log history (empty if pandas missing)."""
    rows = parse_alert_log_rows(path, max_lines=max_lines)
    if pd is None:
        return None
    if not rows:
        return pd.DataFrame(
            columns=["timestamp_utc", "city", "level", "rainfall_mm_h", "message"]
        )
    return pd.DataFrame(rows)
