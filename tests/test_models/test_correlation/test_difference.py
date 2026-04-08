from math import ceil

import pytest

from pystatpower.models.correlation.difference import size


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
