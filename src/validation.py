"""Physical validation layer (Swiss Cheese Model — Layer 3)."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np

from src.flood.inundation import simulate_flood
from src.reservoir.optimizer import V_MAX, V_MIN, validate_schedule
from src.runoff.scs_cn import scs_runoff_mm


def validate_runoff_mm(p_mm: float, q_mm: float, tol: float = 1e-6) -> Dict[str, Any]:
    """Runoff must be non-negative and not exceed rainfall."""
    ok = (q_mm >= -tol) and (q_mm <= p_mm + tol)
    return {"ok": ok, "p_mm": p_mm, "q_mm": q_mm, "message": "Q <= P" if ok else "Runoff exceeds rainfall"}


def validate_storage_mcm(storage_mcm: float, tol: float = 1e-3) -> Dict[str, Any]:
    ok = V_MIN - tol <= storage_mcm <= V_MAX + tol
    return {
        "ok": ok,
        "storage_mcm": storage_mcm,
        "bounds": (V_MIN, V_MAX),
    }


def validate_flood_monotonic(
    dem: np.ndarray, levels: List[float], tol: float = 1e-9
) -> Dict[str, Any]:
    """Flooded cell count must not decrease as stage rises."""
    counts = []
    for level in levels:
        mask, _ = simulate_flood(dem, level)
        counts.append(int(mask.sum()))
    ok = all(counts[i] <= counts[i + 1] + tol for i in range(len(counts) - 1))
    return {"ok": ok, "wet_counts": counts, "levels": levels}


def validate_reservoir_result(result: Dict[str, Any], tol: float = 1.0) -> Dict[str, Any]:
    """Check wrapper output: PASS validation and plausible revenue."""
    revenue = result.get("total_revenue_usd", 0.0)
    ok_val = result.get("validation") == "PASS"
    ok_rev = 600_000 <= revenue <= 800_000
    return {
        "ok": ok_val and ok_rev,
        "validation": result.get("validation"),
        "total_revenue_usd": revenue,
        "revenue_in_expected_band": ok_rev,
    }
