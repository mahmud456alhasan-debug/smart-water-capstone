#!/usr/bin/env python3
"""
Specialized Experiment 3: 7-day reservoir dispatch optimization.

Unit convention (documented in formulation.md and prompt_log.md):
  - Storage V in m^3
  - Inflow and release Q in m^3/s (daily average)
  - Timestep DT = 86400 s (one day)
  - Daily volume from flow: Vol = Q * DT  (m^3)

Revenue model:
  - Turbine head H = 80 m, efficiency eta = 0.85
  - Power (kW) = eta * rho * g * H * Q / 1000,  Q in m^3/s
  - Energy (kWh/day) = Power_kW * 24
  - Revenue ($/day) = price ($/kWh) * Energy_kWh

Multi-objective handling:
  - Hard constraint: Q_release >= Q_eco via optimizer bounds
  - Maximize hydropower revenue (ecological deficit = 0 when bounds enforced)

Solver: scipy.optimize.minimize (trust-constr primary; SLSQP cross-check).
Sequential optimize_day() provided for pedagogy and cross-check.
"""

from __future__ import annotations

import csv
import time
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy.optimize import minimize, minimize_scalar

# --- Experiment 3 parameters (guide) ---
V0 = 500_000.0
V_MIN, V_MAX = 100_000.0, 1_000_000.0
Q_ECO, Q_MAX = 10.0, 100.0
INFLOW = np.array([15.0, 12.0, 10.0, 8.0, 12.0, 15.0, 18.0])
PRICE = np.array([0.08, 0.08, 0.08, 0.08, 0.10, 0.12, 0.10])
DT = 86_400.0
HORIZON = 7

# Hydropower proxy (link m^3/s release to kWh via head and efficiency)
HEAD_M = 80.0
HEAD_GUIDE_REFERENCE_M = 30.0  # peer/guide magnitude for revenue comparison
ETA = 0.85
RHO = 1000.0
G = 9.81

ROOT = Path(__file__).resolve().parent


def day_energy_kwh_at_head(q_m3s: float, head_m: float) -> float:
    """Daily energy (kWh) at a given hydraulic head."""
    power_kw = ETA * RHO * G * head_m * q_m3s / 1000.0
    return power_kw * 24.0


def day_revenue_at_head(
    q_m3s: float, price_usd_per_kwh: float, head_m: float = HEAD_M
) -> float:
    return price_usd_per_kwh * day_energy_kwh_at_head(q_m3s, head_m)


def total_revenue_for_releases(
    releases: np.ndarray,
    prices: np.ndarray = PRICE,
    head_m: float = HEAD_M,
) -> float:
    releases = np.asarray(releases, dtype=float)
    return float(
        sum(day_revenue_at_head(releases[t], float(prices[t]), head_m) for t in range(len(releases)))
    )


def ecological_deficit_m3s_days(
    releases: np.ndarray, eco_flow_m3s: float = Q_ECO
) -> float:
    """Sum of daily max(0, Q_eco - Q_t) in (m^3/s)-day units."""
    releases = np.asarray(releases, dtype=float)
    return float(np.sum(np.maximum(0.0, eco_flow_m3s - releases)))


def daily_volume_m3(q_m3s: float) -> float:
    """Convert average flow (m^3/s) over one day to volume (m^3)."""
    return q_m3s * DT


def release_power_kw(q_m3s: float) -> float:
    """Hydropower power (kW) from release rate."""
    return ETA * RHO * G * HEAD_M * q_m3s / 1000.0


def day_energy_kwh(q_m3s: float) -> float:
    """Daily energy (kWh) from constant release over 24 h."""
    return day_energy_kwh_at_head(q_m3s, HEAD_M)


def day_revenue(q_m3s: float, price_usd_per_kwh: float) -> float:
    """Hydropower revenue for one day ($)."""
    return day_revenue_at_head(q_m3s, price_usd_per_kwh, HEAD_M)


def storage_after_day(
    storage_m3: float, inflow_m3s: float, release_m3s: float
) -> float:
    """Mass balance: V_{t+1} = V_t + (I - Q) * DT."""
    return storage_m3 + daily_volume_m3(inflow_m3s - release_m3s)


def storage_trajectory(
    releases: np.ndarray,
    initial_m3: float = V0,
    inflows: np.ndarray = INFLOW,
) -> np.ndarray:
    """End-of-day storage for each day (length n)."""
    releases = np.asarray(releases, dtype=float)
    n = len(releases)
    storages = np.empty(n)
    v = initial_m3
    for t in range(n):
        v = storage_after_day(v, inflows[t], releases[t])
        storages[t] = v
    return storages


def objective(releases: np.ndarray, prices: np.ndarray = PRICE) -> float:
    """Negative total revenue for scipy minimize()."""
    releases = np.asarray(releases, dtype=float)
    total = sum(day_revenue(releases[t], prices[t]) for t in range(len(releases)))
    return -total


def mass_balance_constraint_funcs(
    initial_m3: float = V0,
    inflows: np.ndarray = INFLOW,
) -> List[dict]:
    """Nonlinear inequality constraints: V_MIN <= V_t <= V_MAX each day."""

    def make_lower(day_idx: int):
        def fun(x: np.ndarray) -> float:
            return storage_trajectory(x, initial_m3, inflows)[day_idx] - V_MIN

        return fun

    def make_upper(day_idx: int):
        def fun(x: np.ndarray) -> float:
            return V_MAX - storage_trajectory(x, initial_m3, inflows)[day_idx]

        return fun

    constraints = []
    for t in range(len(inflows)):
        constraints.append({"type": "ineq", "fun": make_lower(t)})
        constraints.append({"type": "ineq", "fun": make_upper(t)})
    return constraints


def feasible_release_bounds(
    storage_m3: float,
    inflow_m3s: float,
    eco_flow_m3s: float = Q_ECO,
    q_max: float = Q_MAX,
    v_min: float = V_MIN,
    v_max: float = V_MAX,
) -> Tuple[float, float]:
    """Release bounds from policy and storage feasibility."""
    low = max(0.0, eco_flow_m3s)
    high = q_max
    # V_end >= V_MIN  =>  Q <= I + (V - V_MIN) / DT
    high = min(high, inflow_m3s + (storage_m3 - v_min) / DT)
    # V_end <= V_MAX  =>  Q >= I - (V_MAX - V) / DT
    low = max(low, inflow_m3s - (v_max - storage_m3) / DT)
    return low, high


def optimize_day(
    storage_m3: float,
    inflow_m3s: float,
    price_usd_per_kwh: float,
    eco_flow_m3s: float = Q_ECO,
) -> Tuple[float, float]:
    """Maximize single-day revenue (bounded scalar search)."""
    low, high = feasible_release_bounds(storage_m3, inflow_m3s, eco_flow_m3s)
    if low > high + 1e-9:
        raise ValueError(
            f"Infeasible day: release bounds [{low:.3f}, {high:.3f}], "
            f"storage={storage_m3:.0f}, inflow={inflow_m3s}"
        )

    def neg_rev(q: float) -> float:
        s_end = storage_after_day(storage_m3, inflow_m3s, q)
        if s_end < V_MIN - 1e-6 or s_end > V_MAX + 1e-6:
            return 1e12
        return -day_revenue(q, price_usd_per_kwh)

    res = minimize_scalar(neg_rev, bounds=(low, high), method="bounded")
    q_opt = float(res.x)
    return q_opt, day_revenue(q_opt, price_usd_per_kwh)


def build_feasible_initial_guess(
    initial_m3: float = V0,
    inflows: np.ndarray = INFLOW,
    eco_flow_m3s: float = Q_ECO,
) -> np.ndarray:
    """
    Forward pass: pick a release in feasible bounds that avoids hitting
    storage limits before low-inflow days (used as x0 for joint solver).
    """
    storage = initial_m3
    releases: List[float] = []
    n = len(inflows)
    for t in range(n):
        low, high = feasible_release_bounds(
            storage, float(inflows[t]), eco_flow_m3s=eco_flow_m3s
        )
        if low > high + 1e-9:
            raise ValueError(
                f"Day {t + 1} infeasible: release bounds [{low:.3f}, {high:.3f}], "
                f"storage={storage:.0f} m^3, inflow={inflows[t]} m^3/s"
            )
        if storage + daily_volume_m3(float(inflows[t]) - low) > V_MAX:
            q = high
        elif storage + daily_volume_m3(float(inflows[t]) - high) < V_MIN:
            q = low
        else:
            q = min(high, max(low, float(inflows[t])))
        releases.append(q)
        storage = storage_after_day(storage, float(inflows[t]), q)
    return np.asarray(releases, dtype=float)


def optimize_horizon_sequential(
    initial_m3: float = V0,
    inflows: np.ndarray = INFLOW,
    prices: np.ndarray = PRICE,
    eco_flow_m3s: float = Q_ECO,
) -> Tuple[List["DayResult"], float]:
    """
    Greedy day-by-day revenue maximization (pedagogical; can be infeasible
    myopic). Use solve_schedule() for the full 7-day optimum.
    """
    results: List[DayResult] = []
    storage = initial_m3
    total = 0.0
    n = min(len(inflows), len(prices))
    for day in range(n):
        q_opt, rev = optimize_day(storage, inflows[day], prices[day], eco_flow_m3s)
        s_end = storage_after_day(storage, inflows[day], q_opt)
        results.append(
            DayResult(
                day=day + 1,
                storage_start_m3=storage,
                inflow_m3s=float(inflows[day]),
                release_m3s=q_opt,
                storage_end_m3=s_end,
                revenue_usd=rev,
                price_usd_per_kwh=float(prices[day]),
            )
        )
        total += rev
        storage = s_end
    return results, total


@dataclass
class DayResult:
    day: int
    storage_start_m3: float
    inflow_m3s: float
    release_m3s: float
    storage_end_m3: float
    revenue_usd: float
    price_usd_per_kwh: float


def solve_schedule(
    initial_m3: float = V0,
    inflows: np.ndarray = INFLOW,
    prices: np.ndarray = PRICE,
    eco_flow_m3s: float = Q_ECO,
    method: str = "trust-constr",
) -> Tuple[np.ndarray, float, object]:
    """
    Joint 7-day optimization with scipy.optimize.minimize.

    Uses a feasibility-aware initial guess, then trust-constr (falls back to
    SLSQP). Returns (optimal_releases, total_revenue_usd, scipy_result).
    """
    n = min(len(inflows), len(prices))
    x0 = build_feasible_initial_guess(initial_m3, inflows, eco_flow_m3s)
    bounds = [(eco_flow_m3s, Q_MAX)] * n
    constraints = mass_balance_constraint_funcs(initial_m3, inflows)
    opts = {"maxiter": 1000, "gtol": 1e-9}

    result = minimize(
        objective,
        x0,
        args=(prices,),
        method=method,
        bounds=bounds,
        constraints=constraints,
        options=opts,
    )
    if not result.success and method != "SLSQP":
        result = minimize(
            objective,
            x0,
            args=(prices,),
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
            options={"ftol": 1e-9, "maxiter": 800},
        )
    releases = np.asarray(result.x, dtype=float)
    total = -float(result.fun)
    check = validate_schedule(
        results_from_releases(releases, initial_m3, inflows, prices),
        eco_flow_m3s=eco_flow_m3s,
    )
    if not check["ok"]:
        releases = x0
        total = -float(objective(releases, prices))
        result.success = False  # type: ignore[attr-defined]
    return releases, total, result


def compare_solvers(
    initial_m3: float = V0,
    inflows: np.ndarray = INFLOW,
    prices: np.ndarray = PRICE,
    eco_flow_m3s: float = Q_ECO,
) -> Dict[str, dict]:
    """Compare trust-constr and SLSQP; SLSQP warm-started from trust-constr solution."""
    x0 = build_feasible_initial_guess(initial_m3, inflows, eco_flow_m3s)
    bounds = [(eco_flow_m3s, Q_MAX)] * len(inflows)
    constraints = mass_balance_constraint_funcs(initial_m3, inflows)
    out: Dict[str, dict] = {}
    start = x0

    for method in ("trust-constr", "SLSQP"):
        t0 = time.perf_counter()
        opts = (
            {"maxiter": 1000, "gtol": 1e-9}
            if method == "trust-constr"
            else {"maxiter": 800, "ftol": 1e-9}
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            res = minimize(
                objective,
                start,
                args=(prices,),
                method=method,
                bounds=bounds,
                constraints=constraints,
                options=opts,
            )
        releases = np.asarray(res.x, dtype=float)
        results = results_from_releases(releases, initial_m3, inflows, prices)
        check = validate_schedule(results, eco_flow_m3s=eco_flow_m3s)
        out[method] = {
            "success": bool(res.success),
            "revenue_usd": total_revenue_for_releases(releases, prices),
            "iterations": int(getattr(res, "nit", -1)),
            "time_ms": (time.perf_counter() - t0) * 1000.0,
            "feasible": check["ok"],
            "message": str(res.message),
            "releases": releases,
        }
        if method == "trust-constr" and check["ok"]:
            start = releases
    return out


def head_sensitivity_table(
    releases: np.ndarray, prices: np.ndarray = PRICE
) -> List[Tuple[float, float]]:
    """Revenue at several heads for the same release schedule."""
    heads = [25.0, 30.0, 50.0, HEAD_M]
    return [(h, total_revenue_for_releases(releases, prices, h)) for h in heads]


def results_from_releases(
    releases: np.ndarray,
    initial_m3: float = V0,
    inflows: np.ndarray = INFLOW,
    prices: np.ndarray = PRICE,
) -> List[DayResult]:
    """Build DayResult list from release vector."""
    results: List[DayResult] = []
    storage = initial_m3
    for t, q in enumerate(releases):
        s_end = storage_after_day(storage, inflows[t], q)
        results.append(
            DayResult(
                day=t + 1,
                storage_start_m3=storage,
                inflow_m3s=float(inflows[t]),
                release_m3s=float(q),
                storage_end_m3=s_end,
                revenue_usd=day_revenue(float(q), float(prices[t])),
                price_usd_per_kwh=float(prices[t]),
            )
        )
        storage = s_end
    return results


def validate_schedule(
    results: List[DayResult],
    eco_flow_m3s: float = Q_ECO,
    tol: float = 1e-3,
) -> dict:
    """Constraint verification for validation_report.txt."""
    violations: List[str] = []
    worst_storage = 0.0
    worst_eco = 0.0
    worst_balance = 0.0

    for r in results:
        slack_lo = r.storage_end_m3 - V_MIN
        slack_hi = V_MAX - r.storage_end_m3
        worst_storage = min(worst_storage, slack_lo, slack_hi)

        if r.storage_end_m3 < V_MIN - tol:
            violations.append(
                f"Day {r.day}: storage {r.storage_end_m3:.1f} < V_MIN {V_MIN}"
            )
        if r.storage_end_m3 > V_MAX + tol:
            violations.append(
                f"Day {r.day}: storage {r.storage_end_m3:.1f} > V_MAX {V_MAX}"
            )
        if r.release_m3s < Q_ECO - tol or r.release_m3s > Q_MAX + tol:
            violations.append(
                f"Day {r.day}: release {r.release_m3s:.2f} outside [{Q_ECO}, {Q_MAX}]"
            )
        eco_deficit = max(0.0, eco_flow_m3s - r.release_m3s)
        worst_eco = max(worst_eco, eco_deficit)
        if eco_deficit > tol:
            violations.append(
                f"Day {r.day}: eco deficit {eco_deficit:.3f} m^3/s"
            )

        expected = storage_after_day(
            r.storage_start_m3, r.inflow_m3s, r.release_m3s
        )
        bal_err = abs(expected - r.storage_end_m3)
        worst_balance = max(worst_balance, bal_err)
        if bal_err > tol:
            violations.append(f"Day {r.day}: mass balance error {bal_err:.3f} m^3")

    total_rev = sum(r.revenue_usd for r in results)
    return {
        "ok": len(violations) == 0,
        "violations": violations,
        "worst_storage_slack_m3": worst_storage,
        "worst_eco_deficit_m3s": worst_eco,
        "worst_mass_balance_m3": worst_balance,
        "total_revenue_usd": total_rev,
        "tolerance": tol,
    }


def export_schedule_csv(
    results: List[DayResult],
    path: Path | str = ROOT / "optimal_schedule.csv",
) -> Path:
    """Export deliverable optimal_schedule.csv."""
    path = Path(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "day",
                "inflow_m3s",
                "release_m3s",
                "storage_start_m3",
                "storage_end_m3",
                "energy_kwh",
                "price_usd_per_kwh",
                "revenue_usd",
            ]
        )
        for r in results:
            e_kwh = day_energy_kwh(r.release_m3s)
            w.writerow(
                [
                    r.day,
                    f"{r.inflow_m3s:.4f}",
                    f"{r.release_m3s:.4f}",
                    f"{r.storage_start_m3:.1f}",
                    f"{r.storage_end_m3:.1f}",
                    f"{e_kwh:.2f}",
                    f"{r.price_usd_per_kwh:.4f}",
                    f"{r.revenue_usd:.2f}",
                ]
            )
    return path


def write_validation_report(
    results: List[DayResult],
    check: dict,
    path: Path | str = ROOT / "validation_report.txt",
    solver_comparison: Optional[Dict[str, dict]] = None,
    releases: Optional[np.ndarray] = None,
) -> Path:
    """Write multi-section validation_report.txt (Part 4 deliverable)."""
    path = Path(path)
    if releases is None:
        releases = np.array([r.release_m3s for r in results])
    status = "PASS" if check["ok"] else "FAIL"
    lines = [
        "=" * 72,
        "  EXPERIMENT 3: RESERVOIR DISPATCH — VALIDATION REPORT",
        "  Student: Mahmudul Hasan (4125999049)",
        "=" * 72,
        "",
        f"  >>> OVERALL: {status} <<<",
        "",
        "SECTION 0 — PROBLEM PARAMETERS",
        "-" * 72,
        f"  V0 (initial storage)     : {V0:>14,.0f} m^3",
        f"  V_min / V_max            : {V_MIN:>14,.0f} / {V_MAX:,.0f} m^3",
        f"  Q_eco / Q_max            : {Q_ECO:>14.1f} / {Q_MAX:.1f} m^3/s",
        f"  Timestep DT              : {DT:>14,.0f} s (1 day)",
        f"  Head H (optimization)    : {HEAD_M:>14.1f} m",
        f"  Turbine efficiency eta   : {ETA:>14.2f}",
        f"  Inflows (m^3/s)          : {list(INFLOW)}",
        f"  Prices ($/kWh)           : {list(PRICE)}",
        "",
        "SECTION 1 — VALIDATION SUMMARY",
        "-" * 72,
        f"  Storage bounds           : {'PASS' if check['ok'] else 'CHECK'}",
        f"  Release bounds           : {'PASS' if check['ok'] else 'CHECK'}",
        f"  Mass balance             : {'PASS' if check['worst_mass_balance_m3'] <= check['tolerance'] else 'FAIL'}",
        f"  Ecological deficit       : {'PASS' if check['worst_eco_deficit_m3s'] <= check['tolerance'] else 'FAIL'}",
        f"  Worst storage slack (m^3): {check['worst_storage_slack_m3']:.4f}",
        f"  Worst eco deficit (m^3/s): {check['worst_eco_deficit_m3s']:.6f}",
        f"  Worst balance error (m^3): {check['worst_mass_balance_m3']:.2e}",
        f"  Tolerance                : {check['tolerance']}",
        f"  Total revenue (USD)      : {check['total_revenue_usd']:,.2f}",
        "",
        "SECTION 2 — OPTIMAL SCHEDULE (DAY BY DAY)",
        "-" * 72,
        f"  {'Day':>3} {'Inflow':>8} {'Release':>9} {'S_start':>12} {'S_end':>12} "
        f"{'Energy':>10} {'Price':>6} {'Revenue':>10}",
        f"  {'':>3} {'(m3/s)':>8} {'(m3/s)':>9} {'(m3)':>12} {'(m3)':>12} "
        f"{'(kWh)':>10} {'($/kWh)':>6} {'($)':>10}",
    ]
    for r in results:
        e = day_energy_kwh(r.release_m3s)
        lines.append(
            f"  {r.day:3d} {r.inflow_m3s:8.2f} {r.release_m3s:9.4f} "
            f"{r.storage_start_m3:12,.0f} {r.storage_end_m3:12,.0f} "
            f"{e:10,.1f} {r.price_usd_per_kwh:6.2f} {r.revenue_usd:10,.2f}"
        )
    lines.extend(
        [
            "",
            "SECTION 3 — STORAGE & RELEASE CONSTRAINT DETAIL",
            "-" * 72,
        ]
    )
    for r in results:
        margin_lo = r.storage_end_m3 - V_MIN
        margin_hi = V_MAX - r.storage_end_m3
        eco_ok = "OK" if r.release_m3s >= Q_ECO - check["tolerance"] else "VIOLATION"
        lines.append(
            f"  Day {r.day}: storage margin to V_min={margin_lo:,.1f} m^3, "
            f"to V_max={margin_hi:,.1f} m^3 | release={r.release_m3s:.4f} m^3/s [{eco_ok}]"
        )
    lines.extend(
        [
            "",
            "SECTION 4 — MASS BALANCE (CONTINUITY)",
            "-" * 72,
        ]
    )
    s0 = results[0].storage_start_m3
    total_in = sum(r.inflow_m3s * DT for r in results)
    total_out = sum(r.release_m3s * DT for r in results)
    s_final = results[-1].storage_end_m3
    expected = s0 + total_in - total_out
    lines.append(f"  S0 + sum(I*DT) - sum(Q*DT) = {expected:,.1f} m^3")
    lines.append(f"  Computed final storage     = {s_final:,.1f} m^3")
    lines.append(f"  Horizon error              = {abs(expected - s_final):.2e} m^3")
    lines.append(
        f"  Per-day max error          = {check['worst_mass_balance_m3']:.2e} m^3"
    )
    if solver_comparison:
        lines.extend(["", "SECTION 5 — SOLVER COMPARISON (SLSQP vs trust-constr)", "-" * 72])
        for name, info in solver_comparison.items():
            lines.append(
                f"  {name:12s}: success={info['success']}, revenue=${info['revenue_usd']:,.2f}, "
                f"feasible={info['feasible']}, iters={info['iterations']}, "
                f"time={info['time_ms']:.1f} ms"
            )
    lines.extend(["", "SECTION 6 — HEAD SENSITIVITY (same optimal releases)", "-" * 72])
    for h, rev in head_sensitivity_table(releases):
        tag = " <-- optimization head" if abs(h - HEAD_M) < 1e-6 else ""
        if abs(h - HEAD_GUIDE_REFERENCE_M) < 1e-6:
            tag = " <-- guide/peer reference (~$45k--$55k scale)"
        lines.append(f"  H = {h:5.1f} m  ->  total revenue = ${rev:,.2f}{tag}")
    lines.extend(
        [
            "",
            "NOTE: Experiment guide sample revenue ~$45,000 uses lower head (25--30 m).",
            "This project optimizes at H = 80 m (documented in formulation.md); schedule",
            "and constraints remain valid; only revenue magnitude scales with head.",
            "",
        ]
    )
    if check["violations"]:
        lines.extend(["VIOLATIONS:", "-" * 72])
        lines.extend(f"  - {v}" for v in check["violations"])
    else:
        lines.append("All constraint checks passed. Solution is physically valid.")
    lines.append("=" * 72)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def plot_storage_trajectory(
    results: List[DayResult],
    path: Path | str = ROOT / "storage_trajectory.png",
) -> Path:
    """Storage trajectory figure for validation."""
    import matplotlib.pyplot as plt

    path = Path(path)
    days = [r.day for r in results]
    storage = [r.storage_end_m3 for r in results]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(days, storage, "o-", linewidth=2, markersize=8, color="#2980b9")
    ax.axhline(V_MIN, color="#e74c3c", linestyle="--", label=f"V_min = {V_MIN/1e3:.0f}k m^3")
    ax.axhline(V_MAX, color="#e74c3c", linestyle=":", label=f"V_max = {V_MAX/1e3:.0f}k m^3")
    ax.set_xlabel("Day")
    ax.set_ylabel("Storage at end of day (m^3)")
    ax.set_title("Reservoir storage trajectory (7-day optimal schedule)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def print_summary(results: List[DayResult], total: float) -> None:
    print("Day  Storage_start  Inflow  Release  Storage_end  Revenue($)")
    print("-" * 72)
    for r in results:
        print(
            f"{r.day:3d}  {r.storage_start_m3:12,.0f}  {r.inflow_m3s:5.1f}  "
            f"{r.release_m3s:7.2f}  {r.storage_end_m3:12,.0f}  {r.revenue_usd:10,.2f}"
        )
    print("-" * 72)
    print(f"Total revenue: ${total:,.2f}")


def run_pipeline(
    eco_flow_m3s: float = Q_ECO,
    csv_path: Optional[Path] = None,
) -> Tuple[List[DayResult], float, dict]:
    """Solve, validate, export CSV and validation report."""
    releases, total, opt_res = solve_schedule(eco_flow_m3s=eco_flow_m3s)
    results = results_from_releases(releases)
    check = validate_schedule(results, eco_flow_m3s=eco_flow_m3s)
    solver_cmp = compare_solvers(eco_flow_m3s=eco_flow_m3s)
    export_schedule_csv(results, csv_path or ROOT / "optimal_schedule.csv")
    write_validation_report(results, check, solver_comparison=solver_cmp, releases=releases)
    plot_storage_trajectory(results)
    return results, total, check


def main() -> None:
    print("Experiment 3 — Reservoir dispatch (units: m^3, m^3/s, DT=86400 s)")
    print(f"Revenue: head={HEAD_M} m, eta={ETA}, price in USD/kWh\n")

    releases, total, opt_res = solve_schedule()
    results = results_from_releases(releases)
    check = validate_schedule(results)

    print_summary(results, total)
    print(f"\nOptimizer: success={opt_res.success}, iterations={opt_res.nit}")
    print("Validation:", "PASS" if check["ok"] else "FAIL")
    if check["violations"]:
        for v in check["violations"]:
            print(" ", v)

    x0 = build_feasible_initial_guess()
    print(f"\nFeasible initial guess total revenue: ${-objective(x0):,.2f}")

    export_schedule_csv(results)
    write_validation_report(
        results, check, solver_comparison=compare_solvers(), releases=releases
    )
    plot_storage_trajectory(results)
    print("\nWrote optimal_schedule.csv, validation_report.txt, storage_trajectory.png")


if __name__ == "__main__":
    main()
