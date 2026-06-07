"""Shared pytest fixtures for Experiment 1."""

from __future__ import annotations

import pytest

from config import Settings


@pytest.fixture
def settings() -> Settings:
    return Settings(
        openweather_api_key="test-key",
        default_city="Beijing,CN",
        cache_ttl_sec=300,
        api_timeout_sec=10,
        green_max_mm_h=10,
        yellow_max_mm_h=20,
        alert_log_path="alert_log.txt",
    )
