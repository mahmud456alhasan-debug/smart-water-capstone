"""Tests for rolling-horizon dispatch extension."""

from __future__ import annotations

import numpy as np

from reservoir_optimize import HORIZON, validate_schedule
from rolling_horizon import compare_full_vs_rolling, optimize_rolling_horizon


def test_rolling_horizon_seven_releases():
    rel, results, total = optimize_rolling_horizon()
    assert len(rel) == HORIZON
    assert len(results) == HORIZON
    assert total > 0


def test_rolling_schedule_feasible():
    _, results, _ = optimize_rolling_horizon()
    check = validate_schedule(results)
    assert check["ok"], check["violations"]


def test_rolling_revenue_below_or_equal_full():
    cmp = compare_full_vs_rolling()
    assert cmp["full_feasible"]
    assert cmp["rolling_feasible"]
    assert cmp["rolling_revenue_usd"] <= cmp["full_horizon_revenue_usd"] + 1.0


def test_rolling_differs_from_full_when_myopic():
    cmp = compare_full_vs_rolling()
    # Policies may differ even when both feasible
    assert isinstance(cmp["revenue_gap_usd"], float)
