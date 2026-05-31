#!/usr/bin/env python3
"""Exercise 2: flood logic at three water levels."""

from __future__ import annotations

import numpy as np

from flood_inundation import DEM_PATH, flood_statistics, simulate_flood

TEST_LEVELS = [40.0, 50.0, 60.0]


def main() -> None:
    dem = np.load(DEM_PATH)
    print("Flood_level (m) | Flooded % | Mean depth (m) | Wet cells")
    print("-" * 58)
    rows = []
    for level in TEST_LEVELS:
        mask, depth = simulate_flood(dem, level)
        stats = flood_statistics(dem, mask, depth, level)
        rows.append(stats)
        print(
            f"{stats.flood_level_m:13.1f} | {stats.flooded_percent:8.2f} | "
            f"{stats.mean_depth_m:13.3f} | {stats.wet_cell_count:9d}"
        )
    print("\nConvention: wet if elevation <= flood_level; depth=0 off wet cells.")


if __name__ == "__main__":
    main()
