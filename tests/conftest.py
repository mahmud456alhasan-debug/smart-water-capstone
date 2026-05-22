"""Shared fixtures for capstone tests."""
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA_CSV = ROOT / "data" / "sample_rainfall.csv"
DEM_PATH = ROOT / "data" / "dem.npy"


@pytest.fixture
def rainfall_csv_path():
    return str(DATA_CSV)


@pytest.fixture
def sample_dem():
    return np.array([[45.0, 55.0], [60.0, 50.0]], dtype=float)


@pytest.fixture
def flat_dem_40_60():
    return np.linspace(40.0, 60.0, 12).reshape(3, 4)
