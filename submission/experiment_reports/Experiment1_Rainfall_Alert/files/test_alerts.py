"""Alert threshold tests including experiment boundary values."""

import pytest

from alerts import check_alert


@pytest.mark.parametrize(
    "rainfall_mm,expected",
    [
        (9.9, "GREEN"),
        (10.0, "YELLOW"),
        (15.0, "YELLOW"),
        (19.9, "YELLOW"),
        (20.0, "RED"),
        (25.0, "RED"),
        (5.0, "GREEN"),
    ],
)
def test_alert_boundaries(settings, rainfall_mm, expected):
    assert check_alert(rainfall_mm, settings).level == expected
