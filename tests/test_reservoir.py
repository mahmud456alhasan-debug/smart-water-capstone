import pytest

from src.reservoir.optimizer import (
    ECO_FLOW_DEFAULT,
    optimize_horizon,
    validate_schedule,
)
from src.reservoir.wrapper import run_baseline_schedule
from src.validation import validate_reservoir_result, validate_storage_mcm


def test_optimize_horizon_baseline_revenue():
    results, total = optimize_horizon(eco_flow_m3s=ECO_FLOW_DEFAULT)
    assert len(results) == 7
    assert 708_000 <= total <= 710_000


def test_validate_schedule_pass():
    results, _ = optimize_horizon()
    check = validate_schedule(results)
    assert check["ok"]
    assert check["worst_storage_slack"] >= -1e-3


def test_storage_bounds_each_day():
    results, _ = optimize_horizon()
    for r in results:
        assert validate_storage_mcm(r.storage_end_mcm)["ok"]


def test_wrapper_baseline():
    out = run_baseline_schedule()
    assert out["status"] == "ok"
    assert validate_reservoir_result(out)["ok"]
    assert len(out["schedule"]) == 7


def test_eco_flow_higher_still_feasible():
    out = run_baseline_schedule(eco_flow_m3s=12.0)
    assert out["validation"] == "PASS"
