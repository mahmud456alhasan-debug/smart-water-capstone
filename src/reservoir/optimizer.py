"""Reservoir dispatch (from week6_session_a_lab3). Storage MCM; flows m3/s."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np
from scipy.optimize import minimize_scalar

V_MIN = 50.0
V_MAX = 200.0
S0 = 120.0
Q_MIN_RELEASE = 10.0
Q_MAX = 150.0
ECO_FLOW_DEFAULT = 10.0
MCM_PER_M3S_DAY = 86400.0 / 1e6
MW_PER_M3S = 80.0 * 0.85 * 9.81e-3

DAILY_INFLOW_M3S = [20.0, 18.0, 25.0, 22.0, 19.0, 21.0, 23.0]
DAILY_PRICE_USD_PER_MWH = [45.0, 42.0, 50.0, 48.0, 44.0, 46.0, 52.0]


def flow_to_volume_mcm(flow_m3s: float) -> float:
    return flow_m3s * MCM_PER_M3S_DAY


def release_energy_mwh(release_m3s: float) -> float:
    return MW_PER_M3S * release_m3s * 24.0


def day_revenue(release_m3s: float, price_usd_per_mwh: float) -> float:
    return price_usd_per_mwh * release_energy_mwh(release_m3s)


def storage_after_day(storage_mcm: float, inflow_m3s: float, release_m3s: float) -> float:
    return storage_mcm + flow_to_volume_mcm(inflow_m3s - release_m3s)


@dataclass
class DayResult:
    day: int
    storage_start_mcm: float
    inflow_m3s: float
    release_m3s: float
    storage_end_mcm: float
    revenue_usd: float
    price_usd_per_mwh: float


def feasible_release_bounds(
    storage_mcm: float, inflow_m3s: float, eco_flow_m3s: float, q_max: float = Q_MAX
) -> Tuple[float, float]:
    k = MCM_PER_M3S_DAY
    low = max(Q_MIN_RELEASE, eco_flow_m3s)
    high = min(q_max, inflow_m3s + (storage_mcm - V_MIN) / k)
    low = max(low, inflow_m3s - (V_MAX - storage_mcm) / k)
    return low, high


def optimize_day(
    storage_mcm: float,
    inflow_m3s: float,
    price_usd_per_mwh: float,
    eco_flow_m3s: float = ECO_FLOW_DEFAULT,
) -> Tuple[float, float]:
    low, high = feasible_release_bounds(storage_mcm, inflow_m3s, eco_flow_m3s)
    if low > high:
        raise ValueError(f"Infeasible release bounds: low={low:.2f}, high={high:.2f}")

    def neg_revenue(q: float) -> float:
        s_end = storage_after_day(storage_mcm, inflow_m3s, q)
        if s_end < V_MIN - 1e-6 or s_end > V_MAX + 1e-6:
            return 1e12
        return -day_revenue(q, price_usd_per_mwh)

    result = minimize_scalar(neg_revenue, bounds=(low, high), method="bounded")
    q_opt = float(result.x)
    return q_opt, day_revenue(q_opt, price_usd_per_mwh)


def optimize_horizon(
    initial_storage_mcm: float = S0,
    inflows_m3s: Optional[List[float]] = None,
    prices: Optional[List[float]] = None,
    eco_flow_m3s: float = ECO_FLOW_DEFAULT,
) -> Tuple[List[DayResult], float]:
    if inflows_m3s is None:
        inflows_m3s = DAILY_INFLOW_M3S
    if prices is None:
        prices = DAILY_PRICE_USD_PER_MWH
    n = min(len(inflows_m3s), len(prices))
    results: List[DayResult] = []
    storage = initial_storage_mcm
    total_revenue = 0.0
    for day in range(n):
        q_opt, rev = optimize_day(storage, inflows_m3s[day], prices[day], eco_flow_m3s)
        s_end = storage_after_day(storage, inflows_m3s[day], q_opt)
        results.append(
            DayResult(
                day=day + 1,
                storage_start_mcm=storage,
                inflow_m3s=inflows_m3s[day],
                release_m3s=q_opt,
                storage_end_mcm=s_end,
                revenue_usd=rev,
                price_usd_per_mwh=prices[day],
            )
        )
        total_revenue += rev
        storage = s_end
    return results, total_revenue


def validate_schedule(
    results: List[DayResult], eco_flow_m3s: float = ECO_FLOW_DEFAULT, tol: float = 1e-3
) -> dict:
    violations = []
    for r in results:
        if r.storage_end_mcm < V_MIN - tol or r.storage_end_mcm > V_MAX + tol:
            violations.append(f"Day {r.day}: storage out of bounds")
        if r.release_m3s < eco_flow_m3s - tol:
            violations.append(f"Day {r.day}: release below eco minimum")
    return {
        "ok": len(violations) == 0,
        "violations": violations,
        "worst_storage_slack": min(
            min(r.storage_end_mcm - V_MIN, V_MAX - r.storage_end_mcm) for r in results
        ),
    }
