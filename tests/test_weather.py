import pandas as pd
import pytest

from src.weather.alerts import alert_level
from src.weather.load import load_rainfall_csv


def test_load_rainfall_csv(rainfall_csv_path):
    df = load_rainfall_csv(rainfall_csv_path)
    assert list(df.columns) == ["datetime", "rainfall_mm"]
    assert len(df) == 5
    assert df["rainfall_mm"].max() == 22.0


def test_load_rainfall_missing_columns(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("datetime,amount\n2026-01-01,1\n")
    with pytest.raises(ValueError, match="CSV must contain"):
        load_rainfall_csv(str(bad))


def test_alert_green():
    r = alert_level(5.0)
    assert r.level == "GREEN"


def test_alert_amber():
    r = alert_level(15.0, amber=10.0, red=20.0)
    assert r.level == "AMBER"


def test_alert_red():
    r = alert_level(22.0, amber=10.0, red=20.0)
    assert r.level == "RED"
    assert "flood" in r.message.lower() or "High" in r.message


def test_alert_boundary_red():
    r = alert_level(20.0, amber=10.0, red=20.0)
    assert r.level == "RED"
