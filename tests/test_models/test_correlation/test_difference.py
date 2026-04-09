from math import ceil

import pytest

from pystatpower.models.correlation.difference import power, size


@pytest.mark.parametrize(
    "alpha, power, null_correlation, correlation, expected",
    [
        (0.05, 0.80, 0.80, 0.90, 60),
        (0.05, 0.80, 0.80, 0.91, 46),
        (0.05, 0.80, 0.80, 0.92, 36),
        (0.05, 0.80, 0.80, 0.93, 29),
        (0.05, 0.80, 0.80, 0.94, 23),
        (0.05, 0.80, 0.80, 0.95, 18),
    ],
)
def test_size(alpha: float, power: float, null_correlation: float, correlation: float, expected: float):
    assert ceil(size(alpha, power, null_correlation, correlation)) == expected


@pytest.mark.parametrize(
    "alpha, null_correlation, correlation, size, expected",
    [
        (0.05, 0.5, 0.2, 24, 0.98),
        (0.05, 0.5, 0.3, 24, 0.98),
    ],
)
def test_power(alpha: float, null_correlation: float, correlation: float, size: float, expected: float):
    assert round(power(alpha, null_correlation, correlation, size), 4) == expected
