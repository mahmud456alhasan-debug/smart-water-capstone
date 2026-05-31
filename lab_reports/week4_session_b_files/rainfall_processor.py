"""Rainfall processing — SCS-CN runoff from depth and curve number."""

from __future__ import annotations

from typing import Dict


def scs_runoff_mm(rainfall_mm: float, cn: int) -> float:
    """SCS-CN direct runoff Q (mm). Same physics as Week 3/4 labs."""
    if rainfall_mm <= 0:
        return 0.0
    s = 25400.0 / cn - 254.0
    ia = 0.2 * s
    if rainfall_mm <= ia:
        return 0.0
    q = (rainfall_mm - ia) ** 2 / (rainfall_mm - ia + s)
    return min(q, rainfall_mm)


def process_reading(rainfall_mm: float, cn: int = 80) -> Dict[str, float]:
    """Return processed metrics for downstream alert/storage."""
    runoff_mm = scs_runoff_mm(rainfall_mm, cn)
    return {
        "rainfall_mm": rainfall_mm,
        "runoff_mm": runoff_mm,
        "cn": float(cn),
    }
