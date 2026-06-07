"""Tests for offline --simulate CLI mode."""

from __future__ import annotations

import pytest

from simulate import SCENARIO_MM_H, auto_simulate_mm, simulate_reading


def test_simulate_reading_fields():
    r = simulate_reading("London,GB", 15.0)
    assert r.rainfall_mm_h == 15.0
    assert r.rain_field_used == "simulate"
    assert "London,GB" in r.city


@pytest.mark.parametrize("name,mm", list(SCENARIO_MM_H.items()))
def test_scenario_presets(name, mm):
    r = simulate_reading("TestCity", mm)
    assert r.rainfall_mm_h == mm


def test_auto_simulate_bounded():
    for city in ("Paris,FR", "Tokyo,JP", "Dhaka,BD", "Beijing,CN"):
        mm = auto_simulate_mm(city)
        assert 0.0 <= mm < 25.0


def test_auto_simulate_deterministic():
    assert auto_simulate_mm("Berlin,DE") == auto_simulate_mm("Berlin,DE")
