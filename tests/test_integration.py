"""Layer 4: end-to-end workflow tests."""
from pathlib import Path

from src.flood.inundation import load_dem, simulate_flood, flood_statistics
from src.reservoir.wrapper import run_baseline_schedule
from src.runoff.scs_cn import scs_runoff_mm
from src.validation import validate_flood_monotonic, validate_reservoir_result, validate_runoff_mm
from src.weather.alerts import alert_level
from src.weather.load import load_rainfall_csv

ROOT = Path(__file__).resolve().parents[1]


def test_rainfall_to_alert_workflow():
    df = load_rainfall_csv(str(ROOT / "data" / "sample_rainfall.csv"))
    peak = float(df["rainfall_mm"].max())
    alert = alert_level(peak, amber=10.0, red=20.0)
    assert alert.level == "RED"
    assert peak == 22.0


def test_runoff_storm_workflow():
    p = 50.0
    q = scs_runoff_mm(p, 80.0)
    assert validate_runoff_mm(p, q)["ok"]


def test_reservoir_workflow():
    assert validate_reservoir_result(run_baseline_schedule())["ok"]


def test_flood_dem_workflow():
    dem = load_dem(str(ROOT / "data" / "dem.npy"))
    levels = [40.0, 50.0, 60.0]
    assert validate_flood_monotonic(dem, levels)["ok"]
    mask, depth = simulate_flood(dem, 50.0)
    stats = flood_statistics(dem, mask, depth, 50.0)
    assert stats.flooded_percent >= 0.0
