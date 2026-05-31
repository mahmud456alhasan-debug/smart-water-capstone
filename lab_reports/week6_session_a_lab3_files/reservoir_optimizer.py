#!/usr/bin/env python3
"""
Reservoir dispatch optimization -- Week 6 Session A Lab 3.

Unit convention: storage in MCM; inflow/release as m3/s converted to MCM/day
via MCM_PER_M3S_DAY = 86400 / 1e6 = 0.0864.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

import numpy as np
from scipy.optimize import minimize_scalar

# --- Reservoir (MCM) ---
V_MIN = 50.0
V_MAX = 200.0
S0 = 120.0

# --- Flows (m3/s) ---
Q_MIN_RELEASE = 10.0
Q_MAX = 150.0
ECO_FLOW_DEFAULT = 10.0

# m3/s for one day -> MCM
MCM_PER_M3S_DAY = 86400.0 / 1e6  # 0.0864

# --- Hydropower ---
HEAD_M = 80.0
ETA = 0.85
MW_PER_M3S = HEAD_M * ETA * 9.81e-3  # approximate

# Lab data
DAILY_INFLOW_M3S = [20.0, 18.0, 25.0, 22.0, 19.0, 21.0, 23.0]
DAILY_PRICE_USD_PER_MWH = [45.0, 42.0, 50.0, 48.0, 44.0, 46.0, 52.0]
HORIZON_DAYS = 7


def flow_to_volume_mcm(flow_m3s: float) -> float:
    """Convert average flow (m3/s) over one day to volume (MCM)."""
    return flow_m3s * MCM_PER_M3S_DAY


def release_energy_mwh(release_m3s: float) -> float:
    """Daily hydropower energy (MWh) from release rate."""
    power_mw = MW_PER_M3S * release_m3s
    return power_mw * 24.0


def day_revenue(release_m3s: float, price_usd_per_mwh: float) -> float:
    """Hydropower revenue for one day ($)."""
    return price_usd_per_mwh * release_energy_mwh(release_m3s)


def storage_after_day(
    storage_mcm: float, inflow_m3s: float, release_m3s: float
) -> float:
    """Mass balance: S_next = S + I_vol - R_vol."""
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
    storage_mcm: float,
    inflow_m3s: float,
    eco_flow_m3s: float,
    q_max: float = Q_MAX,
) -> Tuple[float, float]:
    """
    Release bounds from policy limits and storage feasibility.

    S_end = S + (I - Q) * k must lie in [V_MIN, V_MAX] with k = MCM_PER_M3S_DAY.
    """
    k = MCM_PER_M3S_DAY
    low = max(Q_MIN_RELEASE, eco_flow_m3s)
    high = q_max
    # S_end >= V_MIN  =>  Q <= I + (S - V_MIN) / k
    high = min(high, inflow_m3s + (storage_mcm - V_MIN) / k)
    # S_end <= V_MAX  =>  Q >= I - (V_MAX - S) / k
    low = max(low, inflow_m3s - (V_MAX - storage_mcm) / k)
    return low, high


def optimize_day(
    storage_mcm: float,
    inflow_m3s: float,
    price_usd_per_mwh: float,
    eco_flow_m3s: float = ECO_FLOW_DEFAULT,
    q_max: float = Q_MAX,
) -> Tuple[float, float]:
    """
    Maximize daily revenue subject to release bounds and end-of-day storage limits.

    Returns (optimal_release_m3s, revenue_usd). Raises ValueError if infeasible.
    """
    low, high = feasible_release_bounds(
        storage_mcm, inflow_m3s, eco_flow_m3s, q_max
    )
    if low > high:
        raise ValueError(
            f"Release bounds infeasible: low={low:.2f}, high={high:.2f}, "
            f"S={storage_mcm:.2f}, I={inflow_m3s}"
        )

    def neg_revenue(q: float) -> float:
        s_end = storage_after_day(storage_mcm, inflow_m3s, q)
        if s_end < V_MIN - 1e-6 or s_end > V_MAX + 1e-6:
            return 1e12  # penalize infeasible storage
        return -day_revenue(q, price_usd_per_mwh)

    result = minimize_scalar(
        neg_revenue,
        bounds=(low, high),
        method="bounded",
        options={"xatol": 1e-4},
    )

    q_opt = float(result.x)
    s_end = storage_after_day(storage_mcm, inflow_m3s, q_opt)
    if s_end < V_MIN - 1e-3 or s_end > V_MAX + 1e-3:
        raise ValueError(
            f"No feasible release: S_start={storage_mcm:.2f}, "
            f"inflow={inflow_m3s}, eco={eco_flow_m3s}, S_end={s_end:.2f}"
        )
    return q_opt, day_revenue(q_opt, price_usd_per_mwh)


def optimize_horizon(
    initial_storage_mcm: float = S0,
    inflows_m3s: Optional[List[float]] = None,
    prices: Optional[List[float]] = None,
    eco_flow_m3s: float = ECO_FLOW_DEFAULT,
) -> Tuple[List[DayResult], float]:
    """Sequential 7-day (or len(inflows)) optimization with storage carried forward."""
    if inflows_m3s is None:
        inflows_m3s = DAILY_INFLOW_M3S
    if prices is None:
        prices = DAILY_PRICE_USD_PER_MWH
    n = min(len(inflows_m3s), len(prices))
    results: List[DayResult] = []
    storage = initial_storage_mcm
    total_revenue = 0.0

    for day in range(n):
        q_opt, rev = optimize_day(
            storage, inflows_m3s[day], prices[day], eco_flow_m3s=eco_flow_m3s
        )
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
    results: List[DayResult],
    eco_flow_m3s: float = ECO_FLOW_DEFAULT,
    tol: float = 1e-3,
) -> dict:
    """Exercise 4 constraint checks."""
    violations = []
    for r in results:
        if r.storage_end_mcm < V_MIN - tol or r.storage_end_mcm > V_MAX + tol:
            violations.append(
                f"Day {r.day}: storage {r.storage_end_mcm:.2f} outside [{V_MIN},{V_MAX}]"
            )
        if r.release_m3s < Q_MIN_RELEASE - tol or r.release_m3s > Q_MAX + tol:
            violations.append(f"Day {r.day}: release {r.release_m3s:.2f} outside bounds")
        if r.release_m3s < eco_flow_m3s - tol:
            violations.append(
                f"Day {r.day}: release {r.release_m3s:.2f} < eco {eco_flow_m3s}"
            )
        expected_s = storage_after_day(
            r.storage_start_mcm, r.inflow_m3s, r.release_m3s
        )
        if abs(expected_s - r.storage_end_mcm) > tol:
            violations.append(f"Day {r.day}: water balance mismatch")

    return {
        "ok": len(violations) == 0,
        "violations": violations,
        "worst_storage_slack": min(
            min(r.storage_end_mcm - V_MIN, V_MAX - r.storage_end_mcm)
            for r in results
        ),
    }


def print_summary(results: List[DayResult], total_revenue: float) -> None:
    print("Day  S_start  Inflow  Release  S_end    Revenue($)")
    print("-" * 58)
    for r in results:
        print(
            f"{r.day:3d}  {r.storage_start_mcm:7.2f}  {r.inflow_m3s:5.1f}  "
            f"{r.release_m3s:7.2f}  {r.storage_end_mcm:7.2f}  {r.revenue_usd:10.2f}"
        )
    print("-" * 58)
    print(f"Total revenue: ${total_revenue:,.2f}")


def main() -> None:
    print("Unit convention: storage MCM; flows m3/s; daily volume factor = 0.0864 MCM/(m3/s)/day")
    print(f"Eco flow minimum: {ECO_FLOW_DEFAULT} m3/s\n")
    results, total = optimize_horizon()
    print_summary(results, total)
    check = validate_schedule(results)
    print("\nValidation:", "PASS" if check["ok"] else "FAIL")
    if check["violations"]:
        for v in check["violations"]:
            print(" ", v)
    else:
        print(f"  Min storage slack to bound: {check['worst_storage_slack']:.3f} MCM")


if __name__ == "__main__":
    main()
