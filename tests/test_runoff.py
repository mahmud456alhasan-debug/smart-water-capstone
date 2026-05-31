import pytest

from src.runoff.scs_cn import scs_runoff_mm
from src.validation import validate_runoff_mm


def test_runoff_zero_rainfall():
    assert scs_runoff_mm(0.0, 80.0) == 0.0


def test_runoff_below_initial_abstraction():
    # Correct case: P=2 mm, CN=80 (Ia ~ 20.3 mm) → Q=0
    # NOT the AI-assumed P=5/CN=95 generalization — see test_hallucination_cn95_p6_produces_runoff
    assert scs_runoff_mm(2.0, 80.0) == 0.0


def test_hallucination_cn95_p6_produces_runoff():
    """Assignment 3: AI claimed small storms always give Q=0 for high CN.

    For CN=95, Ia ~ 2.67 mm (not ~5.37). P=5 mm already yields Q > 0 — the AI
    verbal rule was wrong. See assignment3/HALLUCINATION_CASE_STUDY.md
    """
    assert scs_runoff_mm(2.0, 95.0) == 0.0  # P < Ia
    q5 = scs_runoff_mm(5.0, 95.0)
    assert q5 > 0.0  # AI wrongly assumed this would be zero
    assert q5 <= 5.0
    q6 = scs_runoff_mm(6.0, 95.0)
    assert q6 > q5


def test_runoff_normal_storm():
    p = 50.0
    q = scs_runoff_mm(p, cn=80.0)
    assert 0.0 < q < p
    assert validate_runoff_mm(p, q)["ok"]


def test_runoff_not_exceed_rainfall_high_cn():
    p = 100.0
    for cn in (60.0, 80.0, 95.0):
        q = scs_runoff_mm(p, cn)
        assert q <= p + 1e-6


def test_runoff_extreme_high_rainfall():
    p = 1000.0
    q = scs_runoff_mm(p, 80.0)
    assert 0.0 < q <= p


def test_runoff_cn_at_lower_bound():
    p = 50.0
    q = scs_runoff_mm(p, 1.0)
    assert 0.0 <= q <= p


def test_runoff_cn_at_upper_bound():
    p = 50.0
    q = scs_runoff_mm(p, 100.0)
    assert q == pytest.approx(p, rel=1e-6)


def test_runoff_negative_p_raises():
    with pytest.raises(ValueError):
        scs_runoff_mm(-1.0, 80.0)


def test_runoff_invalid_cn_raises():
    with pytest.raises(ValueError):
        scs_runoff_mm(50.0, 0.5)
    with pytest.raises(ValueError):
        scs_runoff_mm(50.0, -1.0)
    with pytest.raises(ValueError):
        scs_runoff_mm(50.0, 101.0)


def test_runoff_type_errors():
    with pytest.raises(TypeError):
        scs_runoff_mm("50", 80.0)
    with pytest.raises(TypeError):
        scs_runoff_mm(50.0, "80")
