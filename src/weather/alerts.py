"""Threshold-based alert levels."""

from __future__ import annotations


def alert_level(intensity_mm_h: float, amber: float = 10.0, red: float = 20.0) -> str:
    """Return GREEN, AMBER, or RED for rainfall intensity (mm/h)."""
    if intensity_mm_h >= red:
        return "RED"
    if intensity_mm_h >= amber:
        return "AMBER"
    return "GREEN"
