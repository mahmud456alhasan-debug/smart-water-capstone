"""Experiment 2 Part 2 - SCS-CN boundary and physical tests."""

from __future__ import annotations

import itertools

import pytest

from scscn_runoff import (
    adjust_cn_for_amc,
    calculate_Ia,
    calculate_S,
    calculate_runoff,
    calculate_runoff_amc,
    compare_at_impervious_limit,
    rational_runoff,
)


def test_zero_rainfall():
    assert calculate_runoff(0, 80) == 0.0


def test_p_less_than_ia():
    assert calculate_runoff(10, 80) == 0.0


def test_p_equals_ia():
    ia = calculate_Ia(80)
    assert calculate_runoff(ia, 80) == 0.0


def test_normal_case_hand_calc():
    assert calculate_runoff(50, 80) == pytest.approx(13.8, abs=0.1)


def test_maximum_cn_impervious():
    assert calculate_runoff(50, 100) == pytest.approx(50.0, abs=1e-9)


def test_higher_cn_more_runoff_at_fixed_p():
    p = 50.0
    cn_list = [60, 70, 80, 90, 95, 100]
    qs = [calculate_runoff(p, cn) for cn in cn_list]
    assert qs == sorted(qs)


@pytest.mark.parametrize(
    "p,cn",
    [(0, 80), (10, 80), (50, 80), (100, 60), (100, 100)],
)
def test_q_never_exceeds_p(p, cn):
    assert calculate_runoff(p, cn) <= p


def test_q_bounded_grid():
    for p, cn in itertools.product([0, 5, 10, 25, 50, 100], [60, 80, 100]):
        q = calculate_runoff(float(p), float(cn))
        assert 0.0 <= q <= float(p)


def test_negative_p_raises():
    with pytest.raises(ValueError, match="P must"):
        calculate_runoff(-1, 80)


def test_invalid_cn_raises():
    with pytest.raises(ValueError, match="CN must"):
        calculate_runoff(50, 0)
    with pytest.raises(ValueError, match="CN must"):
        calculate_runoff(50, 101)


def test_calculate_s_ia_cn80():
    assert calculate_S(80) == pytest.approx(63.5, abs=0.01)
    assert calculate_Ia(80) == pytest.approx(12.7, abs=0.01)


@pytest.mark.parametrize(
    "p,cn,expected_min,expected_max",
    [
        (9.9, 80, 0.0, 0.0),
        (10.0, 80, 0.0, 0.0),
        (12.6, 80, 0.0, 0.0),
        (50.0, 80, 13.7, 13.9),
        (20.0, 100, 20.0, 20.0),
    ],
)
def test_parametrized_boundaries(p, cn, expected_min, expected_max):
    q = calculate_runoff(p, cn)
    assert expected_min <= q <= expected_max


def test_rational_runoff_basic():
    assert rational_runoff(50.0, 0.8) == pytest.approx(40.0)
    assert rational_runoff(0.0, 0.9) == 0.0


def test_rational_q_never_exceeds_p():
    for p in (10.0, 50.0, 100.0):
        for c in (0.3, 0.7, 1.0):
            assert rational_runoff(p, c) <= p


def test_impervious_limit_scs_matches_rational():
    for p in (20.0, 50.0, 80.0):
        cmp = compare_at_impervious_limit(p)
        assert cmp["scs_cn_Q"] == pytest.approx(cmp["rational_Q"], abs=1e-9)


def test_rational_invalid_c_raises():
    with pytest.raises(ValueError, match="C must"):
        rational_runoff(10.0, 0.0)
    with pytest.raises(ValueError, match="C must"):
        rational_runoff(10.0, 1.1)


def test_amc_ordering_at_p50():
    p = 50.0
    cn = 80.0
    q_i = calculate_runoff_amc(p, cn, "I")
    q_ii = calculate_runoff_amc(p, cn, "II")
    q_iii = calculate_runoff_amc(p, cn, "III")
    assert q_i <= q_ii <= q_iii


def test_amc_ii_unchanged():
    assert adjust_cn_for_amc(80.0, "II") == pytest.approx(80.0)


def test_amc_invalid_raises():
    with pytest.raises(ValueError, match="AMC must"):
        adjust_cn_for_amc(80.0, "IV")
