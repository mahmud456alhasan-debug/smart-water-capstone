#!/usr/bin/env python3
"""Flood inundation core logic -- Week 6 Session B Lab 4."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np

CELL_SIZE_M = 1.0
DEM_SEED = 42
DEM_PATH = "data/dem.npy"


@dataclass
class FloodStats:
    flood_level_m: float
    flooded_percent: float
    mean_depth_m: float
    flooded_area_m2: float
    wet_cell_count: int


def generate_dem(size: int = 100, seed: int = DEM_SEED) -> np.ndarray:
    """Synthetic 100x100 DEM with valleys and hills (30-80 m)."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:size, 0:size]
    valley = -18.0 * np.exp(-((x - 50.0) ** 2 + (y - 50.0) ** 2) / (2.0 * 22.0**2))
    hill_nw = 14.0 * np.exp(-((x - 22.0) ** 2 + (y - 78.0) ** 2) / (2.0 * 14.0**2))
    hill_se = 12.0 * np.exp(-((x - 78.0) ** 2 + (y - 22.0) ** 2) / (2.0 * 16.0**2))
    ridge = 0.035 * (x - 0.6 * y)
    rough = rng.normal(0.0, 1.2, (size, size))
    dem = 55.0 + valley + hill_nw + hill_se + ridge + rough
    return np.clip(dem, 30.0, 80.0).astype(np.float64)


def simulate_flood(
    dem: np.ndarray, flood_level: float
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Flat water-surface inundation (absolute stage, same datum as DEM).

    Wet cells: elevation <= flood_level (inclusive at the water surface).
    Depth: max(0, flood_level - elevation) on wet cells; 0 elsewhere.
    """
    flooded_mask = dem <= flood_level
    depth = np.maximum(0.0, flood_level - dem)
    depth = np.where(flooded_mask, depth, 0.0)
    return flooded_mask, depth


def flood_statistics(
    dem: np.ndarray,
    flooded_mask: np.ndarray,
    depth: np.ndarray,
    flood_level: float,
    cell_size_m: float = CELL_SIZE_M,
) -> FloodStats:
    """Flooded area %, mean depth on wet cells, and flooded area (m^2)."""
    n_total = dem.size
    wet = int(flooded_mask.sum())
    pct = 100.0 * wet / n_total if n_total else 0.0
    if wet:
        mean_depth = float(depth[flooded_mask].mean())
    else:
        mean_depth = 0.0
    area_m2 = wet * (cell_size_m**2)
    return FloodStats(
        flood_level_m=flood_level,
        flooded_percent=pct,
        mean_depth_m=mean_depth,
        flooded_area_m2=area_m2,
        wet_cell_count=wet,
    )


def check_monotonic_area(
    levels: np.ndarray, flooded_pct: np.ndarray, tol: float = 1e-9
) -> bool:
    """Flooded percentage should not decrease as water level rises."""
    diffs = np.diff(flooded_pct)
    return bool(np.all(diffs >= -tol))
