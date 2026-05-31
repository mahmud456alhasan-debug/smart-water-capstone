"""SCS-CN runoff calculation module.

Formulas
--------
S = 25400 / CN - 254          (potential maximum retention, mm)
Ia = 0.2 * S                  (initial abstraction, mm)
Q = (P - Ia)^2 / (P - Ia + S) when P > Ia, else 0

Assumptions
-----------
- Ia = 0.2 * S (standard SCS assumption)
- CN is in [1, 100], rainfall P >= 0
- Q is clipped to P (physical upper bound)
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd


_VALID_CN_RANGE = (1, 100)
_MIN_RETENTION = 0.0


def _validate_scalar(value, name, lower=0.0, upper=None):
    if not isinstance(value, (int, float, np.floating, np.integer)):
        raise TypeError(f"{name} must be numeric, got {type(value).__name__}")
    if np.isnan(value):
        raise ValueError(f"{name} must not be NaN")
    if value < lower:
        raise ValueError(f"{name} ({value}) must be >= {lower}")
    if upper is not None and value > upper:
        raise ValueError(f"{name} ({value}) must be <= {upper}")
    return float(value)


def calculate_runoff(P: float, CN: float) -> float:
    """Compute SCS-CN runoff depth Q (mm) from rainfall P (mm) and curve number CN.

    Parameters
    ----------
    P : float
        Rainfall depth (mm). Must be >= 0.
    CN : float
        Curve number in [1, 100].

    Returns
    -------
    float
        Runoff depth Q (mm). Guaranteed 0 <= Q <= P.

    Raises
    ------
    TypeError
        If either argument is non-numeric.
    ValueError
        If P < 0, CN < 1, CN > 100, or either value is NaN.

    Examples
    --------
    >>> calculate_runoff(50, 80)
    24.36
    >>> calculate_runoff(10, 80)   # P < Ia
    0.0
    >>> calculate_runoff(0, 80)
    0.0
    """
    P = _validate_scalar(P, "P", lower=0.0)
    CN = _validate_scalar(CN, "CN", lower=_VALID_CN_RANGE[0], upper=_VALID_CN_RANGE[1])

    S = 25400.0 / CN - 254.0
    Ia = 0.2 * S

    if P <= Ia:
        return 0.0

    numerator = (P - Ia) ** 2
    denominator = P - Ia + S
    Q = numerator / denominator
    return min(Q, P)


def calculate_runoff_series(
    P: Sequence[float],
    CN: Sequence[float],
) -> np.ndarray:
    """Vectorised SCS-CN calculation over arrays of rainfall and CN values.

    Parameters
    ----------
    P : array-like of float
        Rainfall depth(s) (mm).
    CN : array-like of float
        Curve number(s) in [1, 100].

    Returns
    -------
    np.ndarray
        Runoff depths Q (mm), same shape as inputs.

    Raises
    ------
    ValueError
        If P and CN have different lengths or any value is invalid.
    """
    P_arr = np.asarray(P, dtype=float)
    CN_arr = np.asarray(CN, dtype=float)

    if P_arr.shape != CN_arr.shape:
        raise ValueError(
            f"P shape {P_arr.shape} does not match CN shape {CN_arr.shape}"
        )

    if np.any(P_arr < 0):
        raise ValueError("All P values must be >= 0")
    if np.any((CN_arr < _VALID_CN_RANGE[0]) | (CN_arr > _VALID_CN_RANGE[1])):
        raise ValueError(f"All CN values must be in [{_VALID_CN_RANGE[0]}, {_VALID_CN_RANGE[1]}]")
    if np.any(np.isnan(P_arr)) or np.any(np.isnan(CN_arr)):
        raise ValueError("P and CN must not contain NaN values")

    S = 25400.0 / CN_arr - 254.0
    Ia = 0.2 * S

    # Avoid division-by-zero: denominator is always > 0 when P > Ia
    Q = np.where(
        P_arr > Ia,
        (P_arr - Ia) ** 2 / (P_arr - Ia + S),
        0.0,
    )
    return np.clip(Q, 0.0, P_arr)


def summarize_runoff(
    P: Sequence[float],
    CN: Sequence[float],
    labels: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Return a DataFrame with P, CN, S, Ia, Q for each input pair.

    Parameters
    ----------
    P : array-like
        Rainfall depths (mm).
    CN : array-like
        Curve numbers.
    labels : list of str, optional
        Optional labels (e.g. land-use names or event IDs).

    Returns
    -------
    pd.DataFrame
        Columns: label (optional), P (mm), CN, S (mm), Ia (mm), Q (mm).
    """
    P_arr = np.asarray(P, dtype=float).ravel()
    CN_arr = np.asarray(CN, dtype=float).ravel()

    S = 25400.0 / CN_arr - 254.0
    Ia = 0.2 * S

    Q = calculate_runoff_series(P_arr, CN_arr)

    df = pd.DataFrame({"P (mm)": P_arr, "CN": CN_arr, "S (mm)": S, "Ia (mm)": Ia, "Q (mm)": Q})
    if labels is not None:
        df.insert(0, "label", labels)
    return df
