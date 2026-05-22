"""SCS Curve Number runoff (from week5_session_b_lab2)."""

from __future__ import annotations

from typing import Union

_RETENTION_FACTOR = 25400.0
_RETENTION_OFFSET = 254.0
_INITIAL_ABSTRACTION_RATIO = 0.2
_MIN_CN = 1
_MAX_CN = 100


def _validate_positive_rainfall(p_mm: Union[int, float]) -> float:
    if not isinstance(p_mm, (int, float)):
        raise TypeError(f"P must be a number, got {type(p_mm).__name__}")
    p_mm = float(p_mm)
    if p_mm < 0:
        raise ValueError(f"Rainfall depth P cannot be negative, got {p_mm}")
    return p_mm


def _validate_curve_number(cn: Union[int, float]) -> float:
    if not isinstance(cn, (int, float)):
        raise TypeError(f"CN must be a number, got {type(cn).__name__}")
    cn = float(cn)
    if not (_MIN_CN <= cn <= _MAX_CN):
        raise ValueError(f"Curve number CN must be in [{_MIN_CN}, {_MAX_CN}], got {cn}")
    return cn


def scs_runoff_mm(p_mm: Union[int, float], cn: float) -> float:
    """Direct runoff Q (mm); enforced 0 <= Q <= P."""
    p_mm = _validate_positive_rainfall(p_mm)
    cn = _validate_curve_number(cn)
    s_mm = _RETENTION_FACTOR / cn - _RETENTION_OFFSET
    ia_mm = _INITIAL_ABSTRACTION_RATIO * s_mm
    if p_mm <= ia_mm:
        return 0.0
    effective = p_mm - ia_mm
    q_mm = effective**2 / (effective + s_mm)
    return max(0.0, min(q_mm, p_mm))
