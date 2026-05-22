"""Threshold alerts: GREEN / AMBER / RED (mm/h)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AlertResult:
    level: str
    message: str
    rainfall_mm_h: float


def alert_level(
    intensity_mm_h: float, amber: float = 10.0, red: float = 20.0
) -> AlertResult:
    if intensity_mm_h >= red:
        return AlertResult(
            level="RED",
            message=f"High intensity ({intensity_mm_h:.1f} mm/h) — flood watch",
            rainfall_mm_h=intensity_mm_h,
        )
    if intensity_mm_h >= amber:
        return AlertResult(
            level="AMBER",
            message=f"Elevated rainfall ({intensity_mm_h:.1f} mm/h)",
            rainfall_mm_h=intensity_mm_h,
        )
    return AlertResult(
        level="GREEN",
        message=f"Normal conditions ({intensity_mm_h:.1f} mm/h)",
        rainfall_mm_h=intensity_mm_h,
    )
