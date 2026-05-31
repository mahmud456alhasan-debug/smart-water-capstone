from typing import Union

# SCS-CN constants (mm)
_RETENTION_FACTOR = 25400.0
_RETENTION_OFFSET = 254.0
_INITIAL_ABSTRACTION_RATIO = 0.2
_MIN_CN = 1
_MAX_CN = 100


def _validate_positive_rainfall(P: Union[int, float]) -> float:
    """Validate and convert rainfall depth P (mm)."""
    if not isinstance(P, (int, float)):
        raise TypeError(f"P must be a number, got {type(P).__name__}")
    P = float(P)
    if P < 0:
        raise ValueError(f"Rainfall depth P cannot be negative, got {P}")
    return P


def _validate_curve_number(CN: Union[int, float]) -> float:
    """Validate and convert curve number CN (dimensionless)."""
    if not isinstance(CN, (int, float)):
        raise TypeError(f"CN must be a number, got {type(CN).__name__}")
    CN = float(CN)
    if not (_MIN_CN <= CN <= _MAX_CN):
        raise ValueError(
            f"Curve number CN must be between {_MIN_CN} and {_MAX_CN}, got {CN}"
        )
    return CN


def _compute_runoff(P: float, CN: float) -> float:
    """SCS-CN runoff depth (pre-validated inputs only)."""
    S = _RETENTION_FACTOR / CN - _RETENTION_OFFSET
    Ia = _INITIAL_ABSTRACTION_RATIO * S
    if P <= Ia:
        return 0.0
    effective_rainfall = P - Ia
    return effective_rainfall ** 2 / (effective_rainfall + S)


def calculate_runoff(P: Union[int, float], CN: Union[int, float]) -> float:
    """Compute direct runoff Q (mm) using the SCS-CN method.

    The Soil Conservation Service Curve Number (SCS-CN) method estimates
    rainfall excess (direct runoff) from total rainfall and a curve number.

    Parameters
    ----------
    P : float
        Total rainfall depth (mm). Must be >= 0.
    CN : float
        Curve number in [1, 100]. dimensionless.

    Returns
    -------
    float
        Direct runoff depth Q (mm), clipped so that 0 <= Q <= P.

    Raises
    ------
    ValueError
        If P < 0 or CN is outside [1, 100].

    Formulas
    --------
    S = 25400 / CN - 254          (maximum retention, mm)
    Ia = 0.2 * S                  (initial abstraction, mm)
    If P <= Ia: Q = 0
    Else:       Q = (P - Ia)**2 / (P - Ia + S)
    """
    P = _validate_positive_rainfall(P)
    CN = _validate_curve_number(CN)
    Q = _compute_runoff(P, CN)
    return max(0.0, min(Q, P))
