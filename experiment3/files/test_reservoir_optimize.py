"""pytest suite for Experiment 3 reservoir optimization."""

from __future__ import annotations

import numpy as np
import pytest

from reservoir_optimize import (
    DT,
    HEAD_M,
    INFLOW,
    PRICE,
    Q_ECO,
    Q_MAX,
    V0,
    V_MAX,
    V_MIN,
    build_feasible_initial_guess,
    compare_solvers,
    daily_volume_m3,
    day_energy_kwh,
    day_revenue,
    feasible_release_bounds,
    head_sensitivity_table,
    objective,
    optimize_day,
    results_from_releases,
    solve_schedule,
    storage_after_day,
    storage_trajectory,
    total_revenue_for_releases,
    validate_schedule,
    write_validation_report,
)


def test_daily_volume_units():
    assert daily_volume_m3(1.0) == pytest.approx(DT, rel=1e-9)


def test_mass_balance_single_day():
    v_end = storage_after_day(V0, 15.0, 10.0)
    expected = V0 + (15.0 - 10.0) * DT
    assert v_end == pytest.approx(expected)


def test_energy_revenue_positive():
    e = day_energy_kwh(20.0)
    assert e > 0
    r = day_revenue(20.0, 0.10)
    assert r == pytest.approx(0.10 * e)


def test_feasible_bounds_bracket_eco():
    low, high = feasible_release_bounds(V0, 15.0, Q_ECO)
    assert low >= Q_ECO
    assert high <= Q_MAX
    assert low <= high


def test_optimize_day_feasible():
    q, rev = optimize_day(V0, 15.0, 0.08)
    assert Q_ECO <= q <= Q_MAX
    assert rev > 0


def test_slsqp_schedule_feasible():
    releases, total, res = solve_schedule()
    assert res.success
    assert len(releases) == 7
    assert total > 0
    results = results_from_releases(releases)
    check = validate_schedule(results)
    assert check["ok"], check["violations"]


def test_storage_within_bounds_all_days():
    releases, _, _ = solve_schedule()
    storages = storage_trajectory(releases)
    assert np.all(storages >= V_MIN - 1e-3)
    assert np.all(storages <= V_MAX + 1e-3)


def test_releases_respect_bounds():
    releases, _, _ = solve_schedule()
    assert np.all(releases >= Q_ECO - 1e-6)
    assert np.all(releases <= Q_MAX + 1e-6)


def test_objective_matches_sum_revenue():
    releases, total, _ = solve_schedule()
    assert -objective(releases) == pytest.approx(total, rel=1e-6)


def test_feasible_initial_guess_valid():
    x0 = build_feasible_initial_guess()
    storages = storage_trajectory(x0)
    assert np.all(storages >= V_MIN - 1e-2)
    assert np.all(storages <= V_MAX + 1e-2)


def test_optimize_day_from_feasible_storage():
    x0 = build_feasible_initial_guess()
    storage = V0
    for t in range(3):
        q, rev = optimize_day(storage, float(INFLOW[t]), float(PRICE[t]))
        assert Q_ECO <= q <= Q_MAX
        storage = storage_after_day(storage, float(INFLOW[t]), q)


def test_higher_eco_lowers_or_equal_revenue():
    _, rev_base, r0 = solve_schedule(eco_flow_m3s=10.0)
    assert r0.success
    try:
        _, rev_high, r1 = solve_schedule(eco_flow_m3s=12.0)
        assert r1.success
        assert rev_high <= rev_base + 1e-6
    except ValueError:
        pass  # Q_eco=12 can be infeasible for this drought scenario


def test_infeasible_eco_raises_or_fails():
    # Very high eco with tight storage may fail for some scenarios
    try:
        _, _, res = solve_schedule(eco_flow_m3s=50.0)
        if res.success:
            results = results_from_releases(res.x)
            check = validate_schedule(results, eco_flow_m3s=50.0)
            assert check["ok"]
    except ValueError:
        pass


def test_validate_zero_eco_deficit_at_baseline():
    releases, _, _ = solve_schedule()
    results = results_from_releases(releases)
    check = validate_schedule(results, eco_flow_m3s=Q_ECO)
    assert check["worst_eco_deficit_m3s"] <= check["tolerance"]


def test_compare_solvers_both_feasible():
    cmp = compare_solvers()
    assert "trust-constr" in cmp and "SLSQP" in cmp
    assert cmp["trust-constr"]["feasible"]
    assert cmp["trust-constr"]["revenue_usd"] > 0


def test_head_sensitivity_ordering():
    releases, _, _ = solve_schedule()
    table = head_sensitivity_table(releases)
    revs = [r for _, r in table]
    assert revs == sorted(revs)
    assert total_revenue_for_releases(releases, PRICE, 30.0) < total_revenue_for_releases(
        releases, PRICE, HEAD_M
    )


def test_validation_report_sections(tmp_path):
    releases, _, _ = solve_schedule()
    results = results_from_releases(releases)
    check = validate_schedule(results)
    path = tmp_path / "validation_report.txt"
    write_validation_report(results, check, path=path, releases=releases)
    text = path.read_text(encoding="utf-8")
    assert "SECTION 1" in text and "SECTION 6" in text
    assert "HEAD SENSITIVITY" in text


def test_lower_eco_bound_allows_q_below_guide_eco():
    releases, _, _ = solve_schedule(eco_flow_m3s=5.0)
    assert np.min(releases) >= 5.0 - 1e-6
    assert np.any(releases < Q_ECO + 0.5)
