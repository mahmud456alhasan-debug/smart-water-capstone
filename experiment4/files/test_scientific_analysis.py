"""Tests for scientific_analysis extensions."""

from pathlib import Path

import numpy as np

from flood_inundation import generate_dem, simulate_rising_water
from scientific_analysis import (
    benchmark_performance,
    plot_dem_histogram,
    run_seed_sensitivity,
    run_scientific_outputs,
)


def test_seed_sensitivity_three_rows():
    rows = run_seed_sensitivity(seeds=(42, 7, 99))
    assert len(rows) == 3
    pcts = [r[3] for r in rows]
    assert all(0 <= p <= 100 for p in pcts)


def test_benchmark_positive_ms():
    dem = generate_dem(size=30, seed=1)
    b = benchmark_performance(dem, n_repeat=5)
    assert b["dem_load_ms"] >= 0
    assert b["single_flood_ms"] >= 0
    assert b["curve_simulation_ms"] >= 0


def test_scientific_outputs_create_files(tmp_path):
    dem = generate_dem(size=40, seed=2)
    curve = simulate_rising_water(dem, [40.0, 45.0, 50.0])
    run_scientific_outputs(tmp_path, dem, curve)
    for name in (
        "dem_overview.png",
        "dem_histogram.png",
        "flood_extent_40m.png",
        "flood_curve.png",
        "flood_volume_curve.png",
        "interpretation.md",
        "sensitivity_seeds.csv",
    ):
        assert (tmp_path / name).is_file()


def test_histogram_saves(tmp_path):
    dem = generate_dem(size=25, seed=3)
    out = plot_dem_histogram(dem, tmp_path / "hist.png")
    assert out.is_file()
