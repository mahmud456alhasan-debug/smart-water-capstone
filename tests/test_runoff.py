from src.runoff.scs_cn import scs_runoff_mm


def test_runoff_not_exceed_rainfall():
    p = 50.0
    q = scs_runoff_mm(p, cn=80.0)
    assert q <= p + 1e-6
