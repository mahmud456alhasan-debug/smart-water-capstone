#!/usr/bin/env python3
"""Exercise 1: generate and visualize synthetic DEM."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

from flood_inundation import CELL_SIZE_M, DEM_PATH, DEM_SEED, generate_dem


def main() -> None:
    dem = generate_dem(size=100, seed=DEM_SEED)
    os.makedirs("data", exist_ok=True)
    np.save(DEM_PATH, dem)
    meta_path = DEM_PATH.replace(".npy", "_meta.npz")
    np.savez(
        meta_path,
        cell_size_m=CELL_SIZE_M,
        crs_note="synthetic grid, no real CRS",
        elevation_min_m=dem.min(),
        elevation_max_m=dem.max(),
        seed=DEM_SEED,
    )

    print(f"Saved DEM: {DEM_PATH} shape={dem.shape}")
    print(
        f"Elevation range: {dem.min():.2f} - {dem.max():.2f} m | "
        f"cell size: {CELL_SIZE_M} m | seed: {DEM_SEED}"
    )

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(dem, cmap="terrain", origin="lower")
    ax.set_title("Synthetic DEM (100x100, 1 m cells)")
    ax.set_xlabel("Column index (east)")
    ax.set_ylabel("Row index (north)")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Elevation (m)")
    fig.tight_layout()
    os.makedirs("figures", exist_ok=True)
    out = "figures/dem_heatmap.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
