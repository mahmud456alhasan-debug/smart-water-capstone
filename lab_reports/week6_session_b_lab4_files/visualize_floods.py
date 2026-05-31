#!/usr/bin/env python3
"""Exercise 3: publication-style inundation maps."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from flood_inundation import flood_statistics, simulate_flood

LEVELS = [40.0, 50.0, 60.0]


def plot_panel(dem: np.ndarray, flood_level: float, ax) -> None:
    mask, depth = simulate_flood(dem, flood_level)
    stats = flood_statistics(dem, mask, depth, flood_level)
    ax.imshow(dem, cmap="gray", origin="lower", vmin=dem.min(), vmax=dem.max())
    depth_ma = np.ma.masked_where(~mask, depth)
    im = ax.imshow(
        depth_ma,
        cmap="Blues",
        origin="lower",
        alpha=0.65,
        vmin=0,
        vmax=max(1.0, depth.max()),
    )
    ax.set_title(
        f"Flood level {flood_level:.0f} m\n"
        f"Flooded {stats.flooded_percent:.1f}% | mean depth {stats.mean_depth_m:.2f} m"
    )
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    return im


def main() -> None:
    dem = np.load("data/dem.npy")
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    last_im = None
    for ax, level in zip(axes, LEVELS):
        last_im = plot_panel(dem, level, ax)
    cbar = fig.colorbar(last_im, ax=axes, fraction=0.025, pad=0.02)
    cbar.set_label("Inundation depth (m)")
    fig.suptitle(
        "Flood inundation comparison (DEM background + depth overlay)",
        fontsize=12,
        y=1.02,
    )
    fig.tight_layout()
    os.makedirs("figures", exist_ok=True)
    out = "figures/flood_comparison_300dpi.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
