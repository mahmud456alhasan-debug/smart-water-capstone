"""pytest for Experiment 4 flood inundation."""

from __future__ import annotations

import numpy as np
import pytest

from flood_inundation import (
    CELL_SIZE_M,
    CURVE_LEVEL_STEP,
    DEFAULT_LEVELS,
    calculate_flood,
    calculate_flood_volume,
    flood_result,
    generate_dem,
    is_monotonic_non_decreasing,
    run_validation_checks,
    simulate_rising_water,
    validate_physics,
)


@pytest.fixture
def dem():
    return generate_dem(size=50, seed=7)


def test_dem_shape_and_range():
    d = generate_dem()
    assert d.shape == (100, 100)
    assert d.min() >= 30.0 - 1e-6
    assert d.max() <= 80.0 + 1e-6


def test_calculate_flood_mask_strict():
    dem = np.array([[30.0, 50.0], [70.0, 80.0]])
    mask, depth, pct = calculate_flood(dem, 50.0)
    assert mask.tolist() == [[True, False], [False, False]]
    assert depth[0, 0] == pytest.approx(20.0)
    assert depth[0, 1] == 0.0
    assert pct == pytest.approx(25.0)


def test_depth_zero_on_dry():
    dem = generate_dem(size=20, seed=1)
    mask, depth, _ = calculate_flood(dem, 45.0)
    assert np.all(depth[~mask] == 0.0)


def test_percentage_bounds(dem):
    for lv in [35.0, 55.0, 70.0]:
        _, _, pct = calculate_flood(dem, lv)
        assert 0.0 <= pct <= 100.0


def test_below_min_zero_flooded():
    dem = generate_dem(size=30, seed=3)
    r = flood_result(dem, dem.min() - 5.0)
    assert r.percentage == pytest.approx(0.0)


def test_above_max_full_flooded():
    dem = generate_dem(size=30, seed=3)
    r = flood_result(dem, dem.max() + 5.0)
    assert r.percentage == pytest.approx(100.0)


def test_monotonic_rising(dem):
    curve = simulate_rising_water(dem, DEFAULT_LEVELS)
    pcts = [p for _, p in curve]
    assert is_monotonic_non_decreasing(pcts)
    assert len(curve) == 21


def test_curve_step_half_meter():
    assert len(DEFAULT_LEVELS) == 21
    assert CURVE_LEVEL_STEP == 0.5
    assert DEFAULT_LEVELS[0] == 40.0
    assert DEFAULT_LEVELS[-1] == 50.0


def test_flood_volume():
    dem = generate_dem(size=20, seed=5)
    _, depth, _ = calculate_flood(dem, 50.0)
    vol = calculate_flood_volume(depth)
    assert vol == pytest.approx(float(depth.sum()) * CELL_SIZE_M**2)
    r = flood_result(dem, 50.0)
    assert r.flood_volume_m3 == pytest.approx(vol)


def test_validation_checklist_all_pass():
    dem = generate_dem()
    curve = simulate_rising_water(dem)
    checks = run_validation_checks(dem, curve)
    assert all(c.passed for c in checks)


def test_mean_depth_wet_only(dem):
    r = flood_result(dem, 48.0)
    if r.flooded_mask.any():
        manual = float(r.depth[r.flooded_mask].mean())
        assert r.mean_depth_wet_m == pytest.approx(manual)


def test_flooded_area_m2(dem):
    r = flood_result(dem, 45.0)
    expected = r.flooded_mask.sum() * CELL_SIZE_M**2
    assert r.flooded_area_m2 == pytest.approx(expected)


def test_validate_physics_passes():
    dem = generate_dem()
    check = validate_physics(dem)
    assert check["ok"]
    assert check["monotonic"]


def test_max_depth_at_lowest_wet_cell():
    dem = generate_dem(size=40, seed=99)
    lv = 55.0
    r = flood_result(dem, lv)
    if r.flooded_mask.any():
        assert r.max_depth_m == pytest.approx(lv - dem.min(), rel=0, abs=0.05)


def test_simulate_rising_length(dem):
    levels = [40.0, 42.0, 50.0]
    curve = simulate_rising_water(dem, levels)
    assert len(curve) == 3
    assert curve[0][0] == 40.0


def test_higher_level_more_or_equal_flood(dem):
    _, _, p40 = calculate_flood(dem, 40.0)
    _, _, p50 = calculate_flood(dem, 50.0)
    assert p50 >= p40


def test_reproducible_dem():
    a = generate_dem(seed=42)
    b = generate_dem(seed=42)
    np.testing.assert_array_equal(a, b)
