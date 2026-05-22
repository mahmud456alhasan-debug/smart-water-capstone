import pytest

from src.runoff.scs_cn import scs_runoff_mm
from src.validation import validate_runoff_mm


def test_runoff_zero_rainfall():
    assert scs_runoff_mm(0.0, 80.0) == 0.0


def test_runoff_below_initial_abstraction():
    assert scs_runoff_mm(2.0, 80.0) == 0.0


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


def test_runoff_negative_p_raises():
    with pytest.raises(ValueError):
        scs_runoff_mm(-1.0, 80.0)


def test_runoff_invalid_cn_raises():
    with pytest.raises(ValueError):
        scs_runoff_mm(50.0, 0.5)
    with pytest.raises(ValueError):
        scs_runoff_mm(50.0, 101.0)


def test_runoff_type_errors():
    with pytest.raises(TypeError):
        scs_runoff_mm("50", 80.0)
    with pytest.raises(TypeError):
        scs_runoff_mm(50.0, "80")
