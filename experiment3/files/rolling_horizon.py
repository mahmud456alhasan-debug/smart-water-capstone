"""Rolling-horizon reservoir dispatch (Experiment 3 optional extension)."""

from __future__ import annotations

from typing import List, Tuple

import numpy as np

from reservoir_optimize import (
    HORIZON,
    INFLOW,
    PRICE,
    Q_ECO,
    V0,
    DayResult,
    results_from_releases,
    solve_schedule,
    storage_after_day,
    validate_schedule,
)


def optimize_rolling_horizon(
    initial_m3: float = V0,
    inflows: np.ndarray = INFLOW,
    prices: np.ndarray = PRICE,
    eco_flow_m3s: float = Q_ECO,
) -> Tuple[np.ndarray, List[DayResult], float]:
    """
    Each day: re-optimize on the remaining horizon and execute today's release.

    Mimics operations with updated forecasts; typically earns <= full-horizon optimum.
    """
    inflows = np.asarray(inflows, dtype=float)
    prices = np.asarray(prices, dtype=float)
    n = min(len(inflows), len(prices), HORIZON)
    storage = float(initial_m3)
    chosen: List[float] = []

    for day in range(n):
        releases, _, _ = solve_schedule(
            storage, inflows[day:], prices[day:], eco_flow_m3s
        )
        q = float(releases[0])
        chosen.append(q)
        storage = storage_after_day(storage, float(inflows[day]), q)

    rel = np.asarray(chosen, dtype=float)
    results = results_from_releases(rel, initial_m3, inflows[:n], prices[:n])
    total = sum(r.revenue_usd for r in results)
    return rel, results, total


def compare_full_vs_rolling(eco_flow_m3s: float = Q_ECO) -> dict:
    """Summary for reports: joint optimum vs rolling-horizon policy."""
    full_rel, full_rev, _ = solve_schedule(eco_flow_m3s=eco_flow_m3s)
    roll_rel, roll_res, roll_rev = optimize_rolling_horizon(eco_flow_m3s=eco_flow_m3s)
    full_check = validate_schedule(results_from_releases(full_rel), eco_flow_m3s=eco_flow_m3s)
    roll_check = validate_schedule(roll_res, eco_flow_m3s=eco_flow_m3s)
    return {
        "full_horizon_revenue_usd": full_rev,
        "rolling_revenue_usd": roll_rev,
        "revenue_gap_usd": full_rev - roll_rev,
        "full_feasible": full_check["ok"],
        "rolling_feasible": roll_check["ok"],
        "full_releases": full_rel.tolist(),
        "rolling_releases": roll_rel.tolist(),
    }
