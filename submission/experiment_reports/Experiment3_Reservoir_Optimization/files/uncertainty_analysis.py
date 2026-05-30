#!/usr/bin/env python3
"""
Monte Carlo inflow uncertainty — Experiment 3 depth extension.

Perturbs the 7-day inflow forecast with multiplicative Normal noise
(default 10% std), re-optimizes each realization, and reports revenue /
final-storage distributions with P10/P50/P90 percentiles.

Distinct from scenario_analysis.py (deterministic drought/normal/wet).
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from reservoir_optimize import (
    INFLOW,
    PRICE,
    Q_ECO,
    ROOT,
    results_from_releases,
    solve_schedule,
    validate_schedule,
)

OUT_CSV = ROOT / "uncertainty_results.csv"
OUT_STATS = ROOT / "uncertainty_report.txt"
OUT_PNG = ROOT / "uncertainty_histograms.png"
DEFAULT_SCENARIOS = 100
DEFAULT_NOISE_STD = 0.10
DEFAULT_SEED = 42


def perturb_inflows(
    base: np.ndarray,
    rng: np.random.Generator,
    noise_std: float = DEFAULT_NOISE_STD,
) -> np.ndarray:
    """Multiplicative noise: I' = I * (1 + N(0, noise_std)), clipped >= 0."""
    factors = 1.0 + rng.normal(0.0, noise_std, size=len(base))
    return np.maximum(0.0, np.asarray(base, dtype=float) * factors)


def run_monte_carlo(
    num_scenarios: int = DEFAULT_SCENARIOS,
    noise_std: float = DEFAULT_NOISE_STD,
    seed: int = DEFAULT_SEED,
    base_inflow: Optional[np.ndarray] = None,
    eco_flow_m3s: float = Q_ECO,
) -> Dict[str, object]:
    """
    Run Monte Carlo over perturbed inflows.

    Returns dict with arrays, deterministic baseline, and summary stats.
    """
    base = np.asarray(base_inflow if base_inflow is not None else INFLOW, dtype=float)
    rng = np.random.default_rng(seed)

    det_releases, det_rev, det_opt = solve_schedule(inflows=base, eco_flow_m3s=eco_flow_m3s)
    det_results = results_from_releases(det_releases, inflows=base)
    det_final = float(det_results[-1].storage_end_m3)

    rows: List[dict] = []
    for i in range(num_scenarios):
        inflows_i = perturb_inflows(base, rng, noise_std)
        try:
            releases, rev, opt = solve_schedule(
                inflows=inflows_i, eco_flow_m3s=eco_flow_m3s
            )
            results = results_from_releases(releases, inflows=inflows_i)
            check = validate_schedule(results, eco_flow_m3s=eco_flow_m3s)
            ok = bool(check["ok"] and opt.success)
            rows.append(
                {
                    "scenario": i + 1,
                    "total_revenue_usd": float(rev),
                    "final_storage_m3": float(results[-1].storage_end_m3),
                    "feasible": ok,
                    "solver_ok": bool(opt.success),
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "scenario": i + 1,
                    "total_revenue_usd": np.nan,
                    "final_storage_m3": np.nan,
                    "feasible": False,
                    "solver_ok": False,
                    "error": str(exc)[:80],
                }
            )

    df = pd.DataFrame(rows)
    feasible = df[df["feasible"]]
    rev = feasible["total_revenue_usd"].astype(float)
    stor = feasible["final_storage_m3"].astype(float)

    def pct(arr: pd.Series, p: float) -> float:
        if arr.empty:
            return float("nan")
        return float(np.percentile(arr.values, p))

    stats = {
        "num_scenarios": num_scenarios,
        "noise_std": noise_std,
        "feasible_count": int(len(feasible)),
        "deterministic_revenue_usd": float(det_rev),
        "deterministic_final_storage_m3": det_final,
        "mean_revenue_usd": float(rev.mean()) if len(rev) else float("nan"),
        "std_revenue_usd": float(rev.std()) if len(rev) > 1 else 0.0,
        "p10_revenue_usd": pct(rev, 10),
        "p50_revenue_usd": pct(rev, 50),
        "p90_revenue_usd": pct(rev, 90),
        "p10_final_storage_m3": pct(stor, 10),
        "p50_final_storage_m3": pct(stor, 50),
        "p90_final_storage_m3": pct(stor, 90),
    }

    return {
        "dataframe": df,
        "stats": stats,
        "deterministic_releases": det_releases,
        "deterministic_success": bool(det_opt.success),
    }


def write_report(stats: Dict[str, float], path: Path = OUT_STATS) -> Path:
    lines = [
        "MONTE CARLO INFLOW UNCERTAINTY REPORT",
        "=" * 60,
        f"Scenarios: {stats['num_scenarios']}  |  Noise std: {stats['noise_std']:.0%}",
        f"Feasible solutions: {stats['feasible_count']} / {stats['num_scenarios']}",
        "",
        "REVENUE (USD, 7-day)",
        "-" * 40,
        f"  Deterministic:  {stats['deterministic_revenue_usd']:,.2f}",
        f"  Mean (MC):      {stats['mean_revenue_usd']:,.2f}",
        f"  Std dev:        {stats['std_revenue_usd']:,.2f}",
        f"  P10:            {stats['p10_revenue_usd']:,.2f}",
        f"  P50:            {stats['p50_revenue_usd']:,.2f}",
        f"  P90:            {stats['p90_revenue_usd']:,.2f}",
        "",
        "FINAL STORAGE (m3)",
        "-" * 40,
        f"  Deterministic:  {stats['deterministic_final_storage_m3']:,.0f}",
        f"  P10:            {stats['p10_final_storage_m3']:,.0f}",
        f"  P50:            {stats['p50_final_storage_m3']:,.0f}",
        f"  P90:            {stats['p90_final_storage_m3']:,.0f}",
        "",
        "INTERPRETATION",
        "-" * 40,
        "  Inflow forecast error (10% multiplicative) propagates to revenue",
        "  and end-of-horizon storage. P10/P90 bracket the risk envelope.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def plot_histograms(df: pd.DataFrame, stats: Dict[str, float], outpath: Path = OUT_PNG) -> Path:
    feasible = df[df["feasible"]]
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    rev = feasible["total_revenue_usd"].astype(float)
    stor = feasible["final_storage_m3"].astype(float) / 1000.0

    ax = axes[0]
    ax.hist(rev, bins=20, color="#2471a3", edgecolor="white", alpha=0.85)
    for label, key, color in (
        ("P10", "p10_revenue_usd", "#e67e22"),
        ("P50", "p50_revenue_usd", "#27ae60"),
        ("P90", "p90_revenue_usd", "#c0392b"),
    ):
        ax.axvline(stats[key], color=color, linestyle="--", linewidth=1.2, label=label)
    ax.axvline(stats["deterministic_revenue_usd"], color="#2c3e50", linewidth=2, label="Deterministic")
    ax.set_xlabel("7-day revenue (USD)")
    ax.set_ylabel("Count")
    ax.set_title("Revenue distribution (Monte Carlo)")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.3)

    ax2 = axes[1]
    ax2.hist(stor, bins=20, color="#16a085", edgecolor="white", alpha=0.85)
    for label, key, color in (
        ("P10", "p10_final_storage_m3", "#e67e22"),
        ("P50", "p50_final_storage_m3", "#27ae60"),
        ("P90", "p90_final_storage_m3", "#c0392b"),
    ):
        ax2.axvline(stats[key] / 1000.0, color=color, linestyle="--", linewidth=1.2, label=label)
    ax2.axvline(
        stats["deterministic_final_storage_m3"] / 1000.0,
        color="#2c3e50",
        linewidth=2,
        label="Deterministic",
    )
    ax2.set_xlabel("Final storage (×1000 m³)")
    ax2.set_ylabel("Count")
    ax2.set_title("End-of-horizon storage")
    ax2.legend(fontsize=8)
    ax2.grid(axis="y", alpha=0.3)

    fig.suptitle(
        f"Monte Carlo inflow uncertainty ({stats['feasible_count']}/{stats['num_scenarios']} feasible)",
        fontsize=10,
        y=1.02,
    )
    fig.tight_layout()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return outpath


def percentile_table(stats: Dict[str, float]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "metric": "revenue_usd",
                "deterministic": stats["deterministic_revenue_usd"],
                "mean": stats["mean_revenue_usd"],
                "p10": stats["p10_revenue_usd"],
                "p50": stats["p50_revenue_usd"],
                "p90": stats["p90_revenue_usd"],
            },
            {
                "metric": "final_storage_m3",
                "deterministic": stats["deterministic_final_storage_m3"],
                "mean": np.nan,
                "p10": stats["p10_final_storage_m3"],
                "p50": stats["p50_final_storage_m3"],
                "p90": stats["p90_final_storage_m3"],
            },
        ]
    )


def main() -> None:
    result = run_monte_carlo()
    df = result["dataframe"]
    stats = result["stats"]
    df.to_csv(OUT_CSV, index=False)
    write_report(stats)
    plot_histograms(df, stats)
    print("Monte Carlo inflow uncertainty analysis")
    print(percentile_table(stats).to_string(index=False))
    print(f"\nWrote {OUT_CSV.name}, {OUT_STATS.name}, {OUT_PNG.name}")


if __name__ == "__main__":
    main()
