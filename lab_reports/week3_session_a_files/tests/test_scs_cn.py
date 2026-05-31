"""Unit tests for SCS-CN runoff calculation."""

import math

import numpy as np
import pytest

from src.scs_cn import calculate_runoff, calculate_runoff_series, summarize_runoff


class TestCalculateRunoff:
    """Tests for the scalar calculate_runoff function."""

    def test_zero_rainfall(self):
        assert calculate_runoff(0, 80) == 0.0

    def test_rainfall_less_than_ia(self):
        Q = calculate_runoff(10, 80)
        # Ia = 0.2 * (25400/80 - 254) = 0.2 * (317.5 - 254) = 0.2 * 63.5 = 12.7
        # P = 10 < 12.7  => Q = 0
        assert Q == 0.0

    def test_normal_case(self):
        Q = calculate_runoff(50, 80)
        # S = 25400/80 - 254 = 63.5
        # Ia = 12.7
        # Q = (50-12.7)^2 / (50-12.7+63.5) = 37.3^2 / (37.3+63.5) = 1391.29 / 100.8
        expected = (50 - 12.7) ** 2 / (50 - 12.7 + 63.5)
        assert Q == pytest.approx(expected, rel=1e-9)

    def test_invalid_cn_too_low(self):
        with pytest.raises(ValueError, match="must be >= 1"):
            calculate_runoff(50, 0)

    def test_invalid_cn_too_high(self):
        with pytest.raises(ValueError, match="must be <= 100"):
            calculate_runoff(50, 101)

    def test_invalid_cn_nan(self):
        with pytest.raises(ValueError, match="must not be NaN"):
            calculate_runoff(50, math.nan)

    def test_invalid_p_negative(self):
        with pytest.raises(ValueError, match="must be >= 0"):
            calculate_runoff(-1, 80)

    def test_runoff_never_exceeds_rainfall(self):
        for P in [5, 10, 25, 50, 100, 200]:
            for CN in [30, 50, 70, 90, 99]:
                Q = calculate_runoff(P, CN)
                assert 0 <= Q <= P, f"P={P}, CN={CN}: Q={Q} not in [0, {P}]"

    def test_cn_close_to_100(self):
        Q = calculate_runoff(50, 100)
        # S = 25400/100 - 254 = 0
        # Ia = 0
        # Q = P = 50
        assert Q == pytest.approx(50.0)

    def test_cn_1_edge(self):
        # CN = 1 => S = 25400/1 - 254 = 25146
        # Ia = 5029.2 -> huge, so Q = 0 for any reasonable P
        Q = calculate_runoff(50, 1)
        assert Q == 0.0


class TestCalculateRunoffSeries:
    """Tests for the vectorised calculate_runoff_series."""

    def test_all_zero(self):
        Q = calculate_runoff_series([0, 0], [80, 90])
        assert (Q == 0).all()

    def test_mixed(self):
        P = np.array([10, 50, 100])
        CN = np.array([80, 80, 80])
        Q = calculate_runoff_series(P, CN)
        # confirm monotonic and Q <= P
        assert (Q >= 0).all()
        assert (Q <= P).all()
        assert Q[0] == 0.0  # P < Ia

    def test_shape_mismatch(self):
        with pytest.raises(ValueError, match="shape"):
            calculate_runoff_series([1, 2, 3], [1, 2])

    def test_nan_handling(self):
        with pytest.raises(ValueError, match="NaN"):
            calculate_runoff_series([1, 2], [1, math.nan])

    def test_q_le_p_vectorised(self):
        rng = np.random.default_rng(42)
        P = rng.uniform(1, 200, 50)
        CN = rng.integers(30, 99, 50)
        Q = calculate_runoff_series(P, CN)
        assert np.all(Q >= 0)
        assert np.all(Q <= P)


class TestSummarizeRunoff:
    """Tests for the summary DataFrame builder."""

    def test_basic(self):
        df = summarize_runoff([50], [80])
        assert list(df.columns) == ["P (mm)", "CN", "S (mm)", "Ia (mm)", "Q (mm)"]
        expected = (50 - 12.7) ** 2 / (50 - 12.7 + 63.5)
        assert df["Q (mm)"].iloc[0] == pytest.approx(expected)

    def test_with_labels(self):
        df = summarize_runoff([50, 50], [70, 98], labels=["forest", "paved"])
        assert list(df.columns) == ["label", "P (mm)", "CN", "S (mm)", "Ia (mm)", "Q (mm)"]
        assert df["label"].tolist() == ["forest", "paved"]


class TestIntegration:
    """Integration-level checks."""

    def test_manual_cn_lookup_values(self):
        # Known calculation check
        # P=50, CN=80: S=63.5, Ia=12.7, Q=(37.3^2)/(37.3+63.5) ≈ 13.80
        Q = calculate_runoff(50, 80)
        expected = (50 - 12.7) ** 2 / (50 - 12.7 + 63.5)
        assert Q == pytest.approx(expected, abs=0.01)
        # P=50, CN=70: S=25400/70-254=108.857, Ia=21.771, Q=(28.229^2)/(28.229+108.857)
        Q = calculate_runoff(50, 70)
        S70 = 25400 / 70 - 254
        expected70 = (50 - 0.2 * S70) ** 2 / (50 - 0.2 * S70 + S70)
        assert Q == pytest.approx(expected70, abs=0.01)
