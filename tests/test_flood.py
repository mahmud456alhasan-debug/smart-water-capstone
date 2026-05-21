import numpy as np

from src.flood.inundation import simulate_flood


def test_monotonic_wet_count():
    dem = np.linspace(40.0, 60.0, 10).reshape(2, 5)
    counts = []
    for level in [45.0, 50.0, 55.0]:
        mask, _ = simulate_flood(dem, level)
        counts.append(mask.sum())
    assert counts == sorted(counts)
