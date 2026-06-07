"""Tests for optional flood routing and building barriers (Experiment 4)."""

from __future__ import annotations

import numpy as np
import pytest

from flood_inundation import (
    building_barrier_mask,
    calculate_flood,
    calculate_flood_routed,
    compare_bathtub_vs_routed,
    default_building_footprints,
    flood_result_routed,
    generate_dem,
)


def test_routed_is_subset_of_bathtub():
    dem = generate_dem(size=40, seed=11)
    for level in (42.0, 45.0, 50.0):
        bath_mask, _, _ = calculate_flood(dem, level)
        routed_mask, _, _ = calculate_flood_routed(dem, level)
        assert np.all(~routed_mask | bath_mask)


def test_endorheic_basin_stays_dry_under_routing():
    """Center depression below water level but walled off from edges."""
    dem = np.full((5, 5), 55.0)
    dem[1:4, 1:4] = 35.0
    level = 50.0
    _, _, bath_pct = calculate_flood(dem, level)
    _, _, routed_pct = calculate_flood_routed(dem, level)
    assert bath_pct > 0.0
    assert routed_pct == pytest.approx(0.0)


def test_buildings_block_lateral_spread():
    dem = np.array(
        [
            [40.0, 40.0, 40.0, 40.0],
            [40.0, 40.0, 40.0, 40.0],
            [40.0, 40.0, 40.0, 40.0],
            [40.0, 40.0, 40.0, 40.0],
        ]
    )
    barrier = np.zeros((4, 4), dtype=bool)
    barrier[1:3, 2] = True
    level = 45.0
    without = flood_result_routed(dem, level)
    with_barrier = flood_result_routed(dem, level, barrier)
    assert with_barrier.percentage <= without.percentage


def test_default_building_footprints_mask():
    dem = generate_dem()
    mask = building_barrier_mask(dem.shape, default_building_footprints())
    assert mask.dtype == bool
    assert mask.shape == dem.shape
    assert mask.any()
    assert mask.sum() < dem.size


def test_compare_bathtub_vs_routed_keys():
    dem = generate_dem(size=30, seed=3)
    summary = compare_bathtub_vs_routed(dem, 48.0)
    assert summary["routed_is_subset"]
    assert summary["bathtub_pct"] >= summary["routed_pct"]
    assert summary["bathtub_volume_m3"] >= summary["routed_volume_m3"]


@pytest.mark.parametrize("level", [40.0, 45.0, 50.0])
def test_routed_depth_nonnegative(level: float):
    dem = generate_dem(size=25, seed=5)
    _, depth, _ = calculate_flood_routed(dem, level)
    assert np.all(depth >= 0.0)


@pytest.mark.parametrize("level", [42.0, 48.0, 52.0])
def test_routed_monotonic_vs_bathtub(level: float):
    dem = generate_dem(size=35, seed=8)
    _, _, bath_pct = calculate_flood(dem, level)
    _, _, routed_pct = calculate_flood_routed(dem, level)
    assert routed_pct <= bath_pct + 1e-9


def test_routing_with_default_buildings():
    dem = generate_dem(size=50, seed=12)
    barriers = building_barrier_mask(dem.shape, default_building_footprints())
    plain = flood_result_routed(dem, 50.0)
    blocked = flood_result_routed(dem, 50.0, barriers)
    assert blocked.percentage <= plain.percentage


def test_routed_empty_when_all_above_level():
    dem = np.full((10, 10), 60.0)
    mask, depth, pct = calculate_flood_routed(dem, 50.0)
    assert not mask.any()
    assert pct == 0.0
    assert np.all(depth == 0.0)


def test_building_footprint_clips_to_grid():
    dem = generate_dem(size=100, seed=1)
    fps = default_building_footprints(100)[:1]
    mask = building_barrier_mask(dem.shape, fps)
    assert mask.shape == dem.shape
    assert mask.sum() > 0
