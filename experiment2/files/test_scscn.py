"""Experiment 2 Part 2 - SCS-CN boundary and physical tests."""

from __future__ import annotations

import itertools

import pytest

from scscn_runoff import calculate_Ia, calculate_S, calculate_runoff


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
