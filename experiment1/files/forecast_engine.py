"""Short-term rainfall forecast and risk classification — Experiment 1 extension."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple

import requests

from alerts import AlertResult, check_alert
from api_client import WeatherAPIError
from config import Settings


@dataclass
class ForecastStep:
    """One 3-hour OpenWeather forecast interval."""

    timestamp_utc: datetime
    rain_mm_3h: float


@dataclass
class ForecastAssessment:
    """Current + short-term forecast risk pipeline."""

    city: str
    current_mm_h: float
    forecast_3h_mm_h: float
    forecast_6h_mm_h: float
    current_risk: AlertResult
    forecast_3h_risk: AlertResult
    forecast_6h_risk: AlertResult
    worst_level: str


def extract_forecast_steps(data: Dict[str, Any]) -> List[ForecastStep]:
    """Parse OpenWeather 5-day/3-hour forecast JSON into chronological steps."""
    steps: List[ForecastStep] = []
    for item in data.get("list", []):
        ts = datetime.fromtimestamp(int(item.get("dt", 0)), tz=timezone.utc)
        rain_block = item.get("rain") or {}
        rain_mm = float(rain_block.get("3h", 0.0))
        steps.append(ForecastStep(timestamp_utc=ts, rain_mm_3h=rain_mm))
    return steps


def average_rate_mm_h(steps: Sequence[ForecastStep], num_intervals: int) -> float:
    """
    Mean rainfall intensity (mm/h) over the first `num_intervals` 3-hour blocks.

    OpenWeather `rain.3h` is accumulation per 3-hour period; divide by 3 for mm/h.
    """
    if num_intervals <= 0 or not steps:
        return 0.0
    selected = steps[:num_intervals]
    total_mm = sum(s.rain_mm_3h for s in selected)
    hours = 3.0 * len(selected)
    return max(0.0, total_mm / hours)


def forecast_horizons_mm_h(steps: Sequence[ForecastStep]) -> Tuple[float, float]:
    """Return (3-hour, 6-hour) average forecast rates in mm/h."""
    return average_rate_mm_h(steps, 1), average_rate_mm_h(steps, 2)


def worst_alert_level(*levels: str) -> str:
    order = {"GREEN": 0, "YELLOW": 1, "RED": 2}
    return max(levels, key=lambda lv: order.get(lv, 0))


def build_forecast_assessment(
    city: str,
    current_mm_h: float,
    steps: Sequence[ForecastStep],
    settings: Settings,
) -> ForecastAssessment:
    """Current → 3h forecast → 6h forecast → risk classification."""
    f3, f6 = forecast_horizons_mm_h(steps)
    cur = check_alert(current_mm_h, settings)
    r3 = check_alert(f3, settings)
    r6 = check_alert(f6, settings)
    return ForecastAssessment(
        city=city,
        current_mm_h=current_mm_h,
        forecast_3h_mm_h=f3,
        forecast_6h_mm_h=f6,
        current_risk=cur,
        forecast_3h_risk=r3,
        forecast_6h_risk=r6,
        worst_level=worst_alert_level(cur.level, r3.level, r6.level),
    )


def demo_forecast_steps(current_mm_h: float) -> List[ForecastStep]:
    """Synthetic forecast for demo mode (no API)."""
    now = datetime.now(timezone.utc)
    # Decay pattern: current intensity persists then eases
    rates = [current_mm_h, current_mm_h * 0.85, current_mm_h * 0.7]
    steps: List[ForecastStep] = []
    for i, rate in enumerate(rates):
        steps.append(
            ForecastStep(
                timestamp_utc=now.replace(microsecond=0),
                rain_mm_3h=max(0.0, rate * 3.0),
            )
        )
    return steps


def fetch_forecast(city: str, settings: Settings) -> List[ForecastStep]:
    """Fetch OpenWeather 5-day/3-hour forecast for a city."""
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": settings.openweather_api_key, "units": "metric"}
    try:
        resp = requests.get(url, params=params, timeout=settings.api_timeout_sec)
    except requests.RequestException as exc:
        raise WeatherAPIError(f"Forecast network error: {exc}") from exc

    if resp.status_code == 401:
        raise WeatherAPIError("Invalid API key (401 Unauthorized)")
    if resp.status_code == 404:
        raise WeatherAPIError(f"City not found: {city!r}")
    if not resp.ok:
        raise WeatherAPIError(f"Forecast HTTP {resp.status_code}: {resp.text[:200]}")

    return extract_forecast_steps(resp.json())


def assessment_to_rows(assessment: ForecastAssessment) -> List[dict]:
    """Tabular rows for CLI / Streamlit display."""
    return [
        {
            "horizon": "Current",
            "rainfall_mm_h": round(assessment.current_mm_h, 2),
            "risk": assessment.current_risk.level,
            "message": assessment.current_risk.message,
        },
        {
            "horizon": "3-hour forecast",
            "rainfall_mm_h": round(assessment.forecast_3h_mm_h, 2),
            "risk": assessment.forecast_3h_risk.level,
            "message": assessment.forecast_3h_risk.message,
        },
        {
            "horizon": "6-hour forecast",
            "rainfall_mm_h": round(assessment.forecast_6h_mm_h, 2),
            "risk": assessment.forecast_6h_risk.level,
            "message": assessment.forecast_6h_risk.message,
        },
    ]
