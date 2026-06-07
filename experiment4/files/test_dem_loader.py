"""Tests for real DEM loader optional extension."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from flood_inundation import DEM_SIZE, load_dem, load_dem_ascii, resize_dem_to_grid


def test_resize_dem_to_grid():
    src = np.arange(400, dtype=float).reshape(20, 20)
    out = resize_dem_to_grid(src, 10)
    assert out.shape == (10, 10)


def test_load_dem_ascii_roundtrip(tmp_path: Path):
    asc = tmp_path / "tiny.asc"
    asc.write_text(
        "ncols 4\nnrows 4\nxllcorner 0\nyllcorner 0\ncellsize 1\nNODATA_value -9999\n"
        "10 11 12 13\n"
        "14 15 16 17\n"
        "18 19 20 21\n"
        "22 23 24 25\n",
        encoding="utf-8",
    )
    dem = load_dem_ascii(asc)
    assert dem.shape == (DEM_SIZE, DEM_SIZE)
    assert dem.min() >= 10.0
    assert dem.max() <= 25.0


def test_load_dem_accepts_asc(tmp_path: Path):
    asc = tmp_path / "patch.asc"
    asc.write_text(
        "ncols 3\nnrows 3\nxllcorner 0\nyllcorner 0\ncellsize 1\nNODATA_value -1\n"
        "40 41 42\n43 44 45\n46 47 48\n",
        encoding="utf-8",
    )
    dem = load_dem(asc)
    assert dem.shape == (DEM_SIZE, DEM_SIZE)


def test_load_dem_ascii_invalid_header(tmp_path: Path):
    bad = tmp_path / "bad.asc"
    bad.write_text("not a dem\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid ASC"):
        load_dem_ascii(bad)
