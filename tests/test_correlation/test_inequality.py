from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.correlation.inequality import solve_correlation, solve_null_correlation, solve_power, solve_size


@dataclass
class TestCase:
    __test__ = False

    null_correlation: float
    correlation: float
    alternative: Literal["two-sided", "lower one-sided", "upper one-sided"]
    size: int
    alpha: float
    power: float
    bias_adj: bool
    actual_power: float


case_group = (
    [
        # Regular Test Cases: null_correlation = 0.70, correlation = 0.80 to 0.85 by 0.01, alternative="two-sided", alpha = 0.05, power = 0.80, bias_adj = False
        TestCase(null_correlation=0.70, correlation=correlation, alternative="two-sided", size=size, alpha=0.05, power=0.80, bias_adj=False, actual_power=actual_power)
        for correlation, size, actual_power in [
            (0.80, 150, 0.8008),
            (0.81, 120, 0.8022),
            (0.82, 97, 0.8015),
            (0.83, 80, 0.8038),
            (0.84, 66, 0.8020),
            (0.85, 55, 0.8007),
        ]
    ]
    + [
        # Regular Test Cases: null_correlation = 0.70, correlation = 0.80 to 0.85 by 0.01, alternative="upper one-sided", alpha = 0.05, power = 0.80, bias_adj = False
        TestCase(null_correlation=0.70, correlation=correlation, alternative="upper one-sided", size=size, alpha=0.05, power=0.80, bias_adj=False, actual_power=actual_power)
        for correlation, size, actual_power in [
            (0.80, 119, 0.8013),
            (0.81, 95, 0.8013),
            (0.82, 77, 0.8011),
            (0.83, 64, 0.8054),
            (0.84, 53, 0.8044),
            (0.85, 44, 0.8009),
        ]
    ]
    + [
        # Regular Test Cases: null_correlation = 0.70, correlation = 0.50 to 0.55 by 0.01, alternative="lower one-sided", alpha = 0.05, power = 0.80, bias_adj = False
        TestCase(null_correlation=0.70, correlation=correlation, alternative="lower one-sided", size=size, alpha=0.05, power=0.80, bias_adj=False, actual_power=actual_power)
        for correlation, size, actual_power in [
            (0.50, 65, 0.8048),
            (0.51, 70, 0.8018),
            (0.52, 77, 0.8046),
            (0.53, 84, 0.8022),
            (0.54, 93, 0.8028),
            (0.55, 103, 0.8008),
        ]
    ]
    + [
        # Regular Test Cases: null_correlation = 0.70, correlation = 0.80 to 0.85 by 0.01, alternative="two-sided", alpha = 0.05, power = 0.80, bias_adj = True
        TestCase(null_correlation=0.70, correlation=correlation, alternative="two-sided", size=size, alpha=0.05, power=0.80, bias_adj=True, actual_power=actual_power)
        for correlation, size, actual_power in [
            (0.80, 150, 0.8020),
            (0.81, 119, 0.8002),
            (0.82, 97, 0.8032),
            (0.83, 79, 0.8007),
            (0.84, 66, 0.8044),
            (0.85, 55, 0.8035),
        ]
    ]
    + [
        # Regular Test Cases: null_correlation = 0.70, correlation = 0.80 to 0.85 by 0.01, alternative="upper one-sided", alpha = 0.05, power = 0.80, bias_adj = True
        TestCase(null_correlation=0.70, correlation=correlation, alternative="upper one-sided", size=size, alpha=0.05, power=0.80, bias_adj=True, actual_power=actual_power)
        for correlation, size, actual_power in [
            (0.80, 119, 0.8026),
            (0.81, 95, 0.8029),
            (0.82, 77, 0.8030),
            (0.83, 63, 0.8019),
            (0.84, 52, 0.8001),
            (0.85, 44, 0.8041),
        ]
    ]
    + [
        # Regular Test Cases: null_correlation = 0.70, correlation = 0.50 to 0.55 by 0.01, alternative="lower one-sided", alpha = 0.05, power = 0.80, bias_adj = True
        TestCase(null_correlation=0.70, correlation=correlation, alternative="lower one-sided", size=size, alpha=0.05, power=0.80, bias_adj=True, actual_power=actual_power)
        for correlation, size, actual_power in [
            (0.50, 64, 0.8027),
            (0.51, 70, 0.8049),
            (0.52, 76, 0.8027),
            (0.53, 83, 0.8005),
            (0.54, 92, 0.8012),
            (0.55, 103, 0.8028),
        ]
    ]
)


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


def test_solve_power(case: TestCase) -> None:
    assert (
        round(
            solve_power(
                null_correlation=case.null_correlation,
                correlation=case.correlation,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                bias_adj=case.bias_adj,
            ),
            4,
        )
        == case.actual_power
    )


def test_solve_size(case: TestCase) -> None:
    assert (
        solve_size(
            null_correlation=case.null_correlation,
            correlation=case.correlation,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.power,
            bias_adj=case.bias_adj,
        )
        == case.size
    )


def test_solve_null_correlation(case: TestCase) -> None:
    search_direction = "above" if case.null_correlation > case.correlation else "below"
    assert (
        round(
            solve_null_correlation(
                correlation=case.correlation,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                bias_adj=case.bias_adj,
                search_direction=search_direction,
            ),
            2,
        )
        == case.null_correlation
    )

    with pytest.raises(ValueError):
        solve_null_correlation(correlation=0.80, size=100, alpha=0.05, power=0.80, bias_adj=True, search_direction="equal")


def test_solve_correlation(case: TestCase) -> None:
    search_direction = "above" if case.correlation > case.null_correlation else "below"
    assert (
        round(
            solve_correlation(
                null_correlation=case.null_correlation,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                bias_adj=case.bias_adj,
                search_direction=search_direction,
            ),
            2,
        )
        == case.correlation
    )

    with pytest.raises(ValueError):
        solve_correlation(null_correlation=0.80, size=100, alpha=0.05, power=0.80, bias_adj=True, search_direction="equal")
