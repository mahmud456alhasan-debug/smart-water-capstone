#!/usr/bin/env python3
"""Experiment 2 Part 3 - CN sensitivity plots and CSV export."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scscn_runoff import calculate_runoff

ROOT = Path(__file__).resolve().parent
CN_VALUES = [60, 70, 80, 90, 95, 100]
P_FIXED = 50.0


def build_cn_sensitivity_table() -> pd.DataFrame:
    rows = []
    for cn in CN_VALUES:
        q = calculate_runoff(P_FIXED, cn)
        rows.append({"CN": cn, "P_mm": P_FIXED, "Q_mm": round(q, 4)})
    return pd.DataFrame(rows)


def plot_cn_vs_q_at_fixed_p(out: Path) -> None:
    df = build_cn_sensitivity_table()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df["CN"], df["Q_mm"], "o-", linewidth=2, markersize=8, color="#2980b9")
    ax.set_xlabel("Curve number CN")
    ax.set_ylabel(f"Runoff Q (mm) at P = {P_FIXED} mm")
    ax.set_title("SCS-CN sensitivity: runoff vs curve number")
    ax.grid(True, alpha=0.3)
    for _, row in df.iterrows():
        ax.annotate(f"{row['Q_mm']:.1f}", (row["CN"], row["Q_mm"]), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved {out}")


def plot_rainfall_vs_runoff(out: Path) -> None:
    rainfall = np.linspace(0, 120, 241)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for cn in CN_VALUES:
        q_vals = [calculate_runoff(float(p), cn) for p in rainfall]
        ax.plot(rainfall, q_vals, label=f"CN = {cn}", linewidth=2)
    # Mark initial abstraction threshold for CN=80 (guide reference case)
    from scscn_runoff import calculate_Ia

    ia80 = calculate_Ia(80)
    ax.axvline(ia80, color="#e74c3c", linestyle=":", linewidth=1.2, alpha=0.8)
    ax.text(ia80 + 1, 2, f"$I_a$={ia80:.1f} mm (CN=80)", fontsize=9, color="#c0392b")
    ax.plot(rainfall, rainfall, "k--", alpha=0.35, linewidth=1, label="Q = P (upper bound)")
    ax.set_xlabel("Rainfall P (mm)")
    ax.set_ylabel("Runoff Q (mm)")
    ax.set_title("SCS-CN: rainfall vs runoff for selected curve numbers")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 120)
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved {out}")


def domain_checks() -> None:
    df = build_cn_sensitivity_table()
    qs = df["Q_mm"].tolist()
    assert qs == sorted(qs), "Higher CN must yield >= Q at fixed P"
    for p in [0, 10, 50, 100]:
        for cn in CN_VALUES:
            q = calculate_runoff(p, cn)
            assert q <= p + 1e-9
    print("Domain checks: Q <= P; CN ordering at P=50 - PASS")
    print(df.to_string(index=False))


def main() -> None:
    out_main = ROOT / "runoff_comparison.png"
    out_cn = ROOT / "cn_sensitivity.png"
    plot_rainfall_vs_runoff(out_main)
    plot_cn_vs_q_at_fixed_p(out_cn)
    df = build_cn_sensitivity_table()
    df.to_csv(ROOT / "sensitivity_at_P50.csv", index=False)
    domain_checks()


if __name__ == "__main__":
    main()
