from math import ceil

import pytest

from pystatpower.models.correlation.difference import solve_correlation, solve_null_correlation, solve_power, solve_size


@pytest.fixture(
    params=[
        # null_correlation = 0.70, correlation = 0.80 to 0.85 by 0.01, alpha = 0.05, power = 0.80, bias_adj = False
        (0.70, 0.80, 0.05, 0.80, 150, False),
        (0.70, 0.81, 0.05, 0.80, 120, False),
        (0.70, 0.82, 0.05, 0.80, 97, False),
        (0.70, 0.83, 0.05, 0.80, 80, False),
        (0.70, 0.84, 0.05, 0.80, 66, False),
        (0.70, 0.85, 0.05, 0.80, 55, False),
        # null_correlation = 0.70, correlation = 0.80 to 0.85 by 0.01, alpha = 0.05, power = 0.80, bias_adj = True
        (0.70, 0.80, 0.05, 0.80, 150, True),
        (0.70, 0.81, 0.05, 0.80, 119, True),
        (0.70, 0.82, 0.05, 0.80, 97, True),
        (0.70, 0.83, 0.05, 0.80, 79, True),
        (0.70, 0.84, 0.05, 0.80, 66, True),
        (0.70, 0.85, 0.05, 0.80, 55, True),
        # null_correlation = 0.70, correlation = 0.50 to 0.55 by 0.01, alpha = 0.05, power = 0.80, bias_adj = True
        (0.70, 0.50, 0.05, 0.80, 81, True),
        (0.70, 0.51, 0.05, 0.80, 88, True),
        (0.70, 0.52, 0.05, 0.80, 96, True),
        (0.70, 0.53, 0.05, 0.80, 105, True),
        (0.70, 0.54, 0.05, 0.80, 116, True),
        (0.70, 0.55, 0.05, 0.80, 130, True),
    ],
    ids=lambda p: f"{p[0]}, {p[1]}, {p[2]}, {p[3]}, {p[4]}, {p[5]}",
)
def case(request: pytest.FixtureRequest):
    return request.param


def test_solve_size(case) -> None:
    null_correlation, correlation, alpha, power, expected_size, bias_adj = case
    assert ceil(solve_size(null_correlation, correlation, alpha, power, bias_adj)) == expected_size


def test_solve_power(case) -> None:
    null_correlation, correlation, alpha, expected_power, size, bias_adj = case
    assert round(solve_power(null_correlation, correlation, size, alpha, bias_adj), 2) == expected_power


def test_solve_correlation(case) -> None:
    null_correlation, expected_correlation, alpha, power, size, bias_adj = case
    search_direction = "upper" if expected_correlation > null_correlation else "lower"
    assert round(solve_correlation(null_correlation, size, alpha, power, bias_adj, search_direction), 2) == expected_correlation

    with pytest.raises(ValueError):
        solve_correlation(null_correlation, size, alpha, power, bias_adj, "equal")


def test_solve_null_correlation(case) -> None:
    expected_null_correlation, correlation, alpha, power, size, bias_adj = case
    search_direction = "upper" if expected_null_correlation > correlation else "lower"
    assert round(solve_null_correlation(correlation, size, alpha, power, bias_adj, search_direction), 2) == expected_null_correlation

    with pytest.raises(ValueError):
        solve_null_correlation(correlation, size, alpha, power, bias_adj, "equal")
