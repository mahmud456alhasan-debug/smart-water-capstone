"""Offline simulate mode for Experiment 1 (no OpenWeather API key)."""

from __future__ import annotations

from api_client import WeatherReading

SCENARIO_MM_H = {
    "green": 5.0,
    "yellow": 15.0,
    "red": 21.0,
}


def simulate_reading(city: str, mm_h: float) -> WeatherReading:
    """Return a synthetic reading for CLI / batch demos."""
    return WeatherReading(
        city=city,
        rainfall_mm_h=float(mm_h),
        rain_field_used="simulate",
        description=f"Simulated storm ({mm_h:.1f} mm/h)",
    )


def auto_simulate_mm(city: str) -> float:
    """Deterministic per-city rain in [0, 25) mm/h for multi-city demos."""
    key = city.strip().lower()
    return (hash(key) % 250) / 10.0
