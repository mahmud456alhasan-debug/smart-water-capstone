#!/usr/bin/env python3
"""
CN uncertainty band analysis — Experiment 2 depth extension.

Shows runoff sensitivity when curve number is uncertain:
  CN in [75, 85] at fixed P = 50 mm (typical calibration band).

Outputs: cn_uncertainty.csv, cn_uncertainty_band.png
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scscn_runoff import calculate_runoff

ROOT = Path(__file__).resolve().parent
P_FIXED = 50.0
CN_LOW, CN_MID, CN_HIGH = 75.0, 80.0, 85.0
CN_SAMPLES = np.linspace(CN_LOW, CN_HIGH, 21)
OUT_CSV = ROOT / "cn_uncertainty.csv"
OUT_PNG = ROOT / "cn_uncertainty_band.png"


def runoff_band_at_p(
    p_mm: float = P_FIXED,
    cn_low: float = CN_LOW,
    cn_high: float = CN_HIGH,
    cn_mid: float = CN_MID,
) -> dict:
    """Runoff at CN bounds and midpoint."""
    q_low = calculate_runoff(p_mm, cn_high)  # higher CN → more runoff
    q_high = calculate_runoff(p_mm, cn_low)  # lower CN → less runoff
    q_mid = calculate_runoff(p_mm, cn_mid)
    return {
        "P_mm": p_mm,
        "CN_low": cn_low,
        "CN_mid": cn_mid,
        "CN_high": cn_high,
        "Q_at_CN_low_mm": round(q_high, 4),
        "Q_at_CN_mid_mm": round(q_mid, 4),
        "Q_at_CN_high_mm": round(q_low, 4),
        "Q_range_mm": round(q_low - q_high, 4),
        "Q_relative_spread_pct": round(100.0 * (q_low - q_high) / q_mid, 2) if q_mid else 0.0,
    }


def build_uncertainty_table(
    p_mm: float = P_FIXED,
    cn_samples: np.ndarray = CN_SAMPLES,
) -> pd.DataFrame:
    rows = []
    for cn in cn_samples:
        q = calculate_runoff(p_mm, float(cn))
        rows.append({"P_mm": p_mm, "CN": round(float(cn), 2), "Q_mm": round(q, 4)})
    return pd.DataFrame(rows)


def plot_uncertainty_band(
    df: pd.DataFrame,
    summary: dict,
    outpath: Optional[Path] = None,
) -> Path:
    outpath = outpath or OUT_PNG
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df["CN"], df["Q_mm"], color="#2471a3", linewidth=2.5, label="Q(P=50 mm)")
    ax.fill_between(
        df["CN"],
        df["Q_mm"].min(),
        df["Q_mm"],
        alpha=0.15,
        color="#2471a3",
    )
    ax.axvline(CN_LOW, color="#27ae60", linestyle="--", linewidth=1, label=f"CN={CN_LOW}")
    ax.axvline(CN_HIGH, color="#c0392b", linestyle="--", linewidth=1, label=f"CN={CN_HIGH}")
    ax.scatter([CN_MID], [summary["Q_at_CN_mid_mm"]], color="#2c3e50", s=60, zorder=5)
    ax.annotate(
        f"Q range: {summary['Q_at_CN_low_mm']:.2f}–{summary['Q_at_CN_high_mm']:.2f} mm\n"
        f"({summary['Q_relative_spread_pct']:.1f}% at CN=80)",
        xy=(CN_MID, summary["Q_at_CN_mid_mm"]),
        xytext=(CN_MID - 6, summary["Q_at_CN_mid_mm"] + 2),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="#566573"),
    )
    ax.set_xlabel("Curve number CN")
    ax.set_ylabel("Runoff Q (mm)")
    ax.set_title(f"Runoff uncertainty: CN in [{CN_LOW}, {CN_HIGH}] at P = {P_FIXED} mm")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(outpath, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return outpath


def main() -> None:
    summary = runoff_band_at_p()
    df = build_uncertainty_table()
    summary_row = pd.DataFrame([summary])
    out = pd.concat([summary_row, df], ignore_index=True, sort=False)
    out.to_csv(OUT_CSV, index=False)
    plot_uncertainty_band(df, summary)
    print("CN uncertainty band analysis")
    print(f"  P = {P_FIXED} mm, CN in [{CN_LOW}, {CN_HIGH}]")
    print(f"  Q range: {summary['Q_at_CN_low_mm']:.2f} – {summary['Q_at_CN_high_mm']:.2f} mm")
    print(f"  Reference (CN=80): {summary['Q_at_CN_mid_mm']:.2f} mm")
    print(f"Wrote {OUT_CSV.name}, {OUT_PNG.name}")


if __name__ == "__main__":
    main()
