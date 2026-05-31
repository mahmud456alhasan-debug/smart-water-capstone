#!/usr/bin/env python3
"""Exercise 2: SCS-CN parameter sensitivity — rainfall vs runoff by CN."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.runoff import calculate_runoff

CN_VALUES = [60, 70, 80, 90, 95]
P_MIN, P_MAX, P_STEP = 0, 100, 1  # mm


def build_sensitivity_dataframe() -> pd.DataFrame:
    """Wide format: rainfall_mm, Q_CN60, Q_CN70, ..."""
    rainfall = np.arange(P_MIN, P_MAX + P_STEP, P_STEP, dtype=float)
    data = {"rainfall_mm": rainfall}
    for cn in CN_VALUES:
        data[f"Q_CN{cn}"] = [calculate_runoff(float(p), cn) for p in rainfall]
    return pd.DataFrame(data)


def plot_sensitivity(df: pd.DataFrame, out_path: str) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    for cn in CN_VALUES:
        ax.plot(
            df["rainfall_mm"],
            df[f"Q_CN{cn}"],
            label=f"CN = {cn}",
            linewidth=2,
        )
    ax.plot(
        df["rainfall_mm"],
        df["rainfall_mm"],
        "k--",
        alpha=0.35,
        label="Q = P (upper bound)",
    )
    ax.set_xlabel("Rainfall P (mm)")
    ax.set_ylabel("Runoff Q (mm)")
    ax.set_title("SCS-CN sensitivity: runoff vs rainfall by curve number")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def domain_checks(df: pd.DataFrame) -> None:
    """Exercise 3: quick physical validation prints."""
    for cn in CN_VALUES:
        col = f"Q_CN{cn}"
        q = df[col].values
        p = df["rainfall_mm"].values
        assert np.all(q <= p + 1e-9), f"Q > P for CN={cn}"
    print("Check 1: Q <= P for all P, CN — PASS")
    # Higher CN -> more runoff for same P (where P > Ia for all)
    p_test = 50.0
    row = df.loc[df["rainfall_mm"] == p_test].iloc[0]
    qs = [row[f"Q_CN{cn}"] for cn in CN_VALUES]
    assert qs == sorted(qs), "Higher CN should yield >= runoff at P=50"
    print(f"Check 2: runoff increases with CN at P={p_test} mm — PASS")
    print(f"  Q values: {dict(zip(CN_VALUES, [round(q, 2) for q in qs]))}")
    # Hand check Week 1/3 reference
    ref = calculate_runoff(80, 85)
    print(f"Check 3: P=80 CN=85 -> Q={ref:.2f} mm (course reference ~43.6)")


def main() -> None:
    df = build_sensitivity_dataframe()
    df.to_csv("figures/sensitivity_data.csv", index=False)
    plot_sensitivity(df, "figures/runoff_sensitivity.png")
    domain_checks(df)


if __name__ == "__main__":
    main()
