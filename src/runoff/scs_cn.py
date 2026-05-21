"""SCS Curve Number runoff — stub for Week 7 Session B."""

from __future__ import annotations


def scs_runoff_mm(p_mm: float, cn: float) -> float:
    """
    Surface runoff depth (mm) from rainfall p_mm and curve number cn.
    Returns 0 when P < Ia. Full implementation in Session B.
    """
    s_mm = 25400.0 / cn - 254.0
    ia_mm = 0.2 * s_mm
    if p_mm <= ia_mm:
        return 0.0
    return (p_mm - ia_mm) ** 2 / (p_mm - ia_mm + s_mm)
