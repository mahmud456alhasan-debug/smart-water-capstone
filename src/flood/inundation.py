"""Flood inundation (from week6_session_b_lab4)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np

CELL_SIZE_M = 1.0
DEM_SEED = 42


@dataclass
class FloodStats:
    flood_level_m: float
    flooded_percent: float
    mean_depth_m: float
    flooded_area_m2: float
    wet_cell_count: int


def generate_dem(size: int = 100, seed: int = DEM_SEED) -> np.ndarray:
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:size, 0:size]
    valley = -18.0 * np.exp(-((x - 50.0) ** 2 + (y - 50.0) ** 2) / (2.0 * 22.0**2))
    hill_nw = 14.0 * np.exp(-((x - 22.0) ** 2 + (y - 78.0) ** 2) / (2.0 * 14.0**2))
    hill_se = 12.0 * np.exp(-((x - 78.0) ** 2 + (y - 22.0) ** 2) / (2.0 * 16.0**2))
    ridge = 0.035 * (x - 0.6 * y)
    rough = rng.normal(0.0, 1.2, (size, size))
    dem = 55.0 + valley + hill_nw + hill_se + ridge + rough
    return np.clip(dem, 30.0, 80.0).astype(np.float64)


def load_dem(path: str) -> np.ndarray:
    p = Path(path)
    if p.exists():
        return np.load(p)
    dem = generate_dem()
    p.parent.mkdir(parents=True, exist_ok=True)
    np.save(p, dem)
    return dem


def simulate_flood(dem: np.ndarray, flood_level: float) -> Tuple[np.ndarray, np.ndarray]:
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
    n_total = dem.size
    wet = int(flooded_mask.sum())
    pct = 100.0 * wet / n_total if n_total else 0.0
    mean_depth = float(depth[flooded_mask].mean()) if wet else 0.0
    return FloodStats(
        flood_level_m=flood_level,
        flooded_percent=pct,
        mean_depth_m=mean_depth,
        flooded_area_m2=wet * (cell_size_m**2),
        wet_cell_count=wet,
    )
