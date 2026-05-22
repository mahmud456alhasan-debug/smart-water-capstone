from pathlib import Path

import numpy as np

from src.flood.inundation import (
    flood_statistics,
    generate_dem,
    load_dem,
    simulate_flood,
)
from src.validation import validate_flood_monotonic


def test_monotonic_wet_count(flat_dem_40_60):
    out = validate_flood_monotonic(flat_dem_40_60, [45.0, 50.0, 55.0])
    assert out["ok"]


def test_simulate_flood_depth_zero_off_wet(sample_dem):
    mask, depth = simulate_flood(sample_dem, 52.0)
    assert depth[~mask].sum() == 0.0
    assert np.all(depth[mask] >= 0.0)


def test_flood_statistics_wet_and_dry(sample_dem):
    mask, depth = simulate_flood(sample_dem, 50.0)
    stats = flood_statistics(sample_dem, mask, depth, 50.0)
    assert 0.0 <= stats.flooded_percent <= 100.0
    if stats.wet_cell_count:
        assert stats.mean_depth_m > 0.0
    else:
        assert stats.mean_depth_m == 0.0


def test_generate_dem_bounds():
    dem = generate_dem(size=20, seed=42)
    assert dem.shape == (20, 20)
    assert dem.min() >= 30.0
    assert dem.max() <= 80.0


def test_load_dem_from_file():
    root = Path(__file__).resolve().parents[1]
    dem = load_dem(str(root / "data" / "dem.npy"))
    assert dem.ndim == 2
    assert dem.shape[0] == dem.shape[1]
