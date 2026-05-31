#!/usr/bin/env python3
"""Exercise 4: rising water level and monotonicity check."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

from flood_inundation import check_monotonic_area, flood_statistics, simulate_flood

LEVEL_MIN = 40.0
LEVEL_MAX = 60.0
LEVEL_STEP = 1.0


def main() -> None:
    dem = np.load("data/dem.npy")
    levels = np.arange(LEVEL_MIN, LEVEL_MAX + LEVEL_STEP * 0.5, LEVEL_STEP)
    pcts = []
    for level in levels:
        mask, depth = simulate_flood(dem, level)
        stats = flood_statistics(dem, mask, depth, level)
        pcts.append(stats.flooded_percent)
    pcts_arr = np.array(pcts)
    monotone = check_monotonic_area(levels, pcts_arr)
    print(f"Levels {LEVEL_MIN}-{LEVEL_MAX} m step {LEVEL_STEP} m")
    print(f"Flooded % at 40 m: {pcts_arr[0]:.2f} | at 60 m: {pcts_arr[-1]:.2f}")
    print(f"Monotonicity check: {'PASS' if monotone else 'FAIL'}")
    if not monotone:
        diffs = np.diff(pcts_arr)
        bad = np.where(diffs < -1e-9)[0]
        print(f"  Decreases at step index: {bad.tolist()}")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(levels, pcts_arr, "o-", linewidth=2, markersize=5)
    ax.set_xlabel("Flood level (m)")
    ax.set_ylabel("Flooded area (%)")
    ax.set_title("Flooded domain percentage vs water surface elevation")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    os.makedirs("figures", exist_ok=True)
    out = "figures/flooded_pct_vs_level.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Saved {out}")

    np.savetxt(
        "figures/rising_water_data.csv",
        np.column_stack([levels, pcts_arr]),
        delimiter=",",
        header="flood_level_m,flooded_percent",
        comments="",
    )


if __name__ == "__main__":
    main()
