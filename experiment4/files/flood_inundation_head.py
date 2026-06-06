#!/usr/bin/env python3
"""
Specialized Experiment 4: DEM-based flood inundation (bathtub model).

Conventions (documented in prompt_log.md):
  - flood_level: flat water-surface elevation (m), same datum as DEM
  - Flooded mask: elevation < flood_level (strict less-than)
  - Depth: max(0, flood_level - elevation); zero where not flooded
  - Cell size: 1 m x 1 m (100 x 100 grid)
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple, Union

import numpy as np

# --- Experiment 4 parameters ---
DEM_SIZE = 100
ELEV_MIN = 30.0
ELEV_MAX = 80.0
DEM_SEED = 42
CELL_SIZE_M = 1.0
CURVE_LEVEL_START = 40.0
CURVE_LEVEL_END = 50.0
CURVE_LEVEL_STEP = 0.5  # 21 levels: 40.0, 40.5, ..., 50.0
DEFAULT_LEVELS = np.arange(
    CURVE_LEVEL_START, CURVE_LEVEL_END + CURVE_LEVEL_STEP / 2, CURVE_LEVEL_STEP
)

ROOT = Path(__file__).resolve().parent
DEM_PATH = ROOT / "dem_data.npy"


def add_dem_contours(ax, dem: np.ndarray, n_levels: int = 10) -> None:
    """GIS-style elevation contours on an imshow axis (origin='lower')."""
    ny, nx = dem.shape
    x = np.arange(nx)
    y = np.arange(ny)
    ax.contour(x, y, dem, levels=n_levels, colors="black", linewidths=0.4, alpha=0.5)


@dataclass
class FloodResult:
    water_level_m: float
    flooded_mask: np.ndarray
    depth: np.ndarray
    percentage: float
    mean_depth_wet_m: float
    flooded_area_m2: float
    max_depth_m: float
    flood_volume_m3: float = 0.0


@dataclass
class ValidationCheck:
    name: str
    passed: bool
    detail: str


def generate_dem(
    size: int = DEM_SIZE,
    seed: int = DEM_SEED,
    elev_min: float = ELEV_MIN,
    elev_max: float = ELEV_MAX,
) -> np.ndarray:
    """Synthetic DEM with valleys and hills (reproducible)."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:size, 0:size]
    valley = -18.0 * np.exp(-((x - size / 2) ** 2 + (y - size / 2) ** 2) / (2.0 * 22.0**2))
    hill_nw = 14.0 * np.exp(-((x - 0.22 * size) ** 2 + (y - 0.78 * size) ** 2) / (2.0 * 14.0**2))
    hill_se = 12.0 * np.exp(-((x - 0.78 * size) ** 2 + (y - 0.22 * size) ** 2) / (2.0 * 16.0**2))
    ridge = 0.035 * (x - 0.6 * y)
    rough = rng.normal(0.0, 1.2, (size, size))
    dem = 55.0 + valley + hill_nw + hill_se + ridge + rough
    return np.clip(dem, elev_min, elev_max).astype(np.float64)


def load_dem(filepath: Union[str, Path, None] = None) -> np.ndarray:
    """Load dem_data.npy or generate and save if missing."""
    path = Path(filepath) if filepath else DEM_PATH
    if path.is_file():
        dem = np.load(path)
        if dem.shape != (DEM_SIZE, DEM_SIZE):
            raise ValueError(f"DEM shape {dem.shape} expected ({DEM_SIZE}, {DEM_SIZE})")
        return np.asarray(dem, dtype=np.float64)
    dem = generate_dem()
    save_dem(dem, path)
    return dem


def save_dem(dem: np.ndarray, filepath: Union[str, Path, None] = None) -> Path:
    path = Path(filepath) if filepath else DEM_PATH
    np.save(path, dem)
    return path

