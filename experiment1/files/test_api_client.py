"""Mocked API client tests - no network."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from api_client import (
    WeatherAPIError,
    clear_weather_cache,
    extract_rainfall_mm_h,
    fetch_current_weather,
)
from config import Settings


@pytest.fixture(autouse=True)
def _clear_cache():
    clear_weather_cache()
    yield
    clear_weather_cache()


def _settings() -> Settings:
    return Settings(
        openweather_api_key="test-key",
        default_city="Beijing,CN",
        cache_ttl_sec=300,
        api_timeout_sec=10,
        green_max_mm_h=10,
        yellow_max_mm_h=20,
        alert_log_path="alert_log.txt",
    )


def test_extract_rain_1h():
    rain, field = extract_rainfall_mm_h({"rain": {"1h": 3.5}})
    assert rain == 3.5
    assert field == "rain.1h"


def test_extract_rain_3h():
    rain, field = extract_rainfall_mm_h({"rain": {"3h": 9.0}})
    assert rain == 9.0
    assert field == "rain.3h"


def test_extract_no_rain():
    rain, field = extract_rainfall_mm_h({"weather": [{"description": "clear"}]})
    assert rain == 0.0
    assert field == "none"


@patch("api_client.requests.get")
def test_fetch_success(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        ok=True,
        json=lambda: {
            "rain": {"1h": 2.0},
            "weather": [{"description": "light rain"}],
        },
    )
    reading = fetch_current_weather("London,GB", _settings(), use_cache=False)
    assert reading.rainfall_mm_h == 2.0
    assert reading.rain_field_used == "rain.1h"


@patch("api_client.requests.get")
def test_fetch_401(mock_get):
    mock_get.return_value = MagicMock(status_code=401, ok=False, text="Unauthorized")
    with pytest.raises(WeatherAPIError, match="401"):
        fetch_current_weather("London,GB", _settings(), use_cache=False)


@patch("api_client.requests.get")
def test_fetch_404(mock_get):
    mock_get.return_value = MagicMock(status_code=404, ok=False, text="Not Found")
    with pytest.raises(WeatherAPIError, match="not found"):
        fetch_current_weather("BadCity,XX", _settings(), use_cache=False)


@patch("api_client.requests.get")
def test_fetch_network_error(mock_get):
    mock_get.side_effect = requests.Timeout("timed out")
    with pytest.raises(WeatherAPIError, match="Network"):
        fetch_current_weather("London,GB", _settings(), use_cache=False)
