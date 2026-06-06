"""
SCS-CN direct runoff - Experiment 2.

Formulas (metric, mm):
    S  = 25400 / CN - 254
    Ia = 0.2 * S
    Q  = 0           if P <= Ia
    Q  = (P-Ia)^2 / (P-Ia+S)  otherwise, capped at P
"""

from __future__ import annotations


def calculate_S(CN: float) -> float:
    """Potential maximum retention S (mm) from curve number."""
    return (25400.0 / CN) - 254.0


def calculate_Ia(CN: float) -> float:
    """Initial abstraction Ia (mm) = 0.2 * S."""
    return 0.2 * calculate_S(CN)


def calculate_runoff(P: float, CN: float) -> float:
    """
    SCS-CN direct runoff depth Q (mm).

    Args:
        P: Rainfall depth (mm), must be >= 0.
        CN: Curve number, must be in (0, 100].

    Returns:
        Runoff Q (mm); 0 if P <= Ia; always Q <= P.
    """
    if P < 0:
        raise ValueError(f"P must be >= 0, got {P}")
    if CN <= 0 or CN > 100:
        raise ValueError(f"CN must be in (0, 100], got {CN}")

    if P == 0:
        return 0.0

    S = calculate_S(CN)
    Ia = 0.2 * S

    if P <= Ia:
        return 0.0

    excess = P - Ia
    Q = (excess**2) / (excess + S)
    return min(Q, P)
