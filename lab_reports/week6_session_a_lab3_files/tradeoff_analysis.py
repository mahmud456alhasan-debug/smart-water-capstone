#!/usr/bin/env python3
"""Exercise 3: ecological flow vs total revenue trade-off."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pandas as pd

from reservoir_optimizer import ECO_FLOW_DEFAULT, optimize_horizon, validate_schedule

ECO_SCENARIOS = [5.0, 8.0, 10.0, 12.0, 15.0]


def run_tradeoff() -> pd.DataFrame:
    rows = []
    for eco in ECO_SCENARIOS:
        try:
            results, total_rev = optimize_horizon(eco_flow_m3s=eco)
            check = validate_schedule(results, eco_flow_m3s=eco)
            rows.append(
                {
                    "eco_flow_m3s": eco,
                    "total_revenue_usd": total_rev,
                    "feasible": check["ok"],
                    "note": "",
                }
            )
        except ValueError as exc:
            rows.append(
                {
                    "eco_flow_m3s": eco,
                    "total_revenue_usd": float("nan"),
                    "feasible": False,
                    "note": str(exc),
                }
            )
    return pd.DataFrame(rows)


def plot_tradeoff(df: pd.DataFrame, out_path: str) -> None:
    feasible = df[df["feasible"]]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        feasible["eco_flow_m3s"],
        feasible["total_revenue_usd"] / 1000.0,
        "o-",
        linewidth=2,
        markersize=8,
        label="Feasible schedules",
    )
    infeasible = df[~df["feasible"]]
    if not infeasible.empty:
        ax.scatter(
            infeasible["eco_flow_m3s"],
            [0] * len(infeasible),
            color="red",
            marker="x",
            s=80,
            label="Infeasible",
        )
    ax.axvline(
        ECO_FLOW_DEFAULT,
        color="gray",
        linestyle="--",
        alpha=0.7,
        label=f"Baseline eco = {ECO_FLOW_DEFAULT} m3/s",
    )
    ax.set_xlabel("Ecological minimum release (m3/s)")
    ax.set_ylabel("Total 7-day revenue (thousand USD)")
    ax.set_title("Trade-off: ecological flow requirement vs hydropower revenue")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def main() -> None:
    df = run_tradeoff()
    print(df.to_string(index=False))
    df.to_csv("figures/tradeoff_data.csv", index=False)
    plot_tradeoff(df, "figures/tradeoff_revenue.png")
    print(
        "\nOperational balance: higher eco flow reduces feasible high-release "
        "days and lowers total revenue; ~10 m3/s balances ecology and revenue "
        "for this 7-day inflow series."
    )


if __name__ == "__main__":
    main()
