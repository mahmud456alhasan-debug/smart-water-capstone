"""Tests for flood_animation extra (Experiment 4)."""

from pathlib import Path

import numpy as np

from flood_animation import build_flood_animation
from flood_inundation import generate_dem


def test_flood_animation_creates_gif(tmp_path: Path) -> None:
    dem = generate_dem(size=20, seed=7)
    out = tmp_path / "test.gif"
    path = build_flood_animation(dem, levels=np.linspace(35, 45, 4), outpath=out, fps=4)
    assert path.exists()
    assert path.stat().st_size > 500
