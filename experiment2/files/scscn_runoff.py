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


def rational_runoff(P: float, C: float) -> float:
    """
    Rational-method runoff depth (mm): Q = C * P.

    C is a dimensionless runoff coefficient in (0, 1]. At C = 1 (impervious),
    all rainfall becomes runoff — comparable to SCS-CN at CN = 100.
    """
    if P < 0:
        raise ValueError(f"P must be >= 0, got {P}")
    if C <= 0 or C > 1:
        raise ValueError(f"C must be in (0, 1], got {C}")
    return C * P


def compare_at_impervious_limit(P: float) -> dict:
    """Cross-check SCS-CN (CN=100) vs Rational (C=1) at the same rainfall depth."""
    return {
        "P_mm": P,
        "scs_cn_Q": calculate_runoff(P, 100),
        "rational_Q": rational_runoff(P, 1.0),
    }


def adjust_cn_for_amc(cn_ii: float, amc: str = "II") -> float:
    """
    Adjust AMC-II curve number to AMC I (dry) or AMC III (wet).

    NRCS TR-55 conversions (CN_I < CN_II < CN_III for typical values).
    """
    if cn_ii <= 0 or cn_ii > 100:
        raise ValueError(f"CN must be in (0, 100], got {cn_ii}")
    amc_key = amc.upper().strip()
    if amc_key == "II":
        return cn_ii
    if amc_key == "I":
        return (4.2 * cn_ii) / (10.0 - 0.058 * cn_ii)
    if amc_key == "III":
        return (23.2 * cn_ii) / (10.0 + 0.13 * cn_ii)
    raise ValueError(f"AMC must be I, II, or III, got {amc!r}")


def calculate_runoff_amc(P: float, cn_ii: float, amc: str = "II") -> float:
    """Runoff depth using AMC-adjusted curve number."""
    return calculate_runoff(P, adjust_cn_for_amc(cn_ii, amc))
