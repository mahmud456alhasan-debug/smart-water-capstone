"""Threshold-based alerts for rainfall and runoff."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from config import Settings


@dataclass
class AlertResult:
    level: str  # OK, WATCH, ALERT
    message: str
    rainfall_mm: float
    runoff_mm: float


def evaluate_alerts(processed: Dict[str, float], settings: Settings) -> AlertResult:
    rain = processed["rainfall_mm"]
    runoff = processed["runoff_mm"]
    if rain >= settings.rainfall_alert_mm or runoff >= settings.runoff_alert_mm:
        return AlertResult(
            level="ALERT",
            message=f"High rain ({rain:.1f} mm) or runoff ({runoff:.1f} mm)",
            rainfall_mm=rain,
            runoff_mm=runoff,
        )
    if rain >= settings.rainfall_alert_mm * 0.5:
        return AlertResult(
            level="WATCH",
            message=f"Elevated rainfall ({rain:.1f} mm)",
            rainfall_mm=rain,
            runoff_mm=runoff,
        )
    return AlertResult(
        level="OK",
        message="Conditions normal",
        rainfall_mm=rain,
        runoff_mm=runoff,
    )
