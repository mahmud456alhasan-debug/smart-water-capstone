import pytest
from src.runoff import calculate_runoff


def test_normal_case():
    """P=50 mm, CN=80 → hand-calculated Q ≈ 13.81 mm."""
    P = 50.0
    CN = 80
    # S = 25400/80 - 254 = 63.5 mm
    # Ia = 0.2 * 63.5 = 12.7 mm
    # Q = (50 - 12.7)**2 / (50 - 12.7 + 63.5)
    #   = 37.3**2 / 100.8
    #   = 1391.29 / 100.8 ≈ 13.8025
    expected = 13.80
    result = calculate_runoff(P, CN)
    assert result == pytest.approx(expected, abs=0.01)


def test_no_rainfall():
    """P=0 → Q must be 0 regardless of CN."""
    assert calculate_runoff(0.0, 80) == 0.0
    assert calculate_runoff(0.0, 50) == 0.0
    assert calculate_runoff(0.0, 100) == 0.0


def test_rainfall_less_than_initial_abstraction():
    """P < Ia → no runoff (Q = 0)."""
    # CN=80 → Ia=12.7 mm; P=10 < 12.7
    assert calculate_runoff(10.0, 80) == 0.0


def test_impervious_surface():
    """CN=100 → S=0, Ia=0, Q=P."""
    P = 50.0
    result = calculate_runoff(P, 100)
    assert result == pytest.approx(P, abs=1e-9)


def test_negative_rainfall_raises_error():
    """Negative P is physically impossible → ValueError."""
    with pytest.raises(ValueError):
        calculate_runoff(-1.0, 80)
    with pytest.raises(ValueError):
        calculate_runoff(-0.1, 80)


def test_invalid_cn_raises_error():
    """CN outside [1, 100] → ValueError."""
    with pytest.raises(ValueError):
        calculate_runoff(50.0, 0)
    with pytest.raises(ValueError):
        calculate_runoff(50.0, 101)
    with pytest.raises(ValueError):
        calculate_runoff(50.0, -1)


def test_runoff_never_exceeds_rainfall():
    """Physical validation: Q <= P for a range of inputs."""
    import itertools
    for P, CN in itertools.product([0, 5, 10, 25, 50, 100, 200],
                                   [1, 30, 50, 70, 80, 90, 100]):
        q = calculate_runoff(float(P), CN)
        assert 0.0 <= q <= float(P), f"Q={q} out of [0, {P}] for CN={CN}"
