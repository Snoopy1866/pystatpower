from dataclasses import dataclass, asdict

import pytest

from pystatpower.models.correlation.inequality import solve_correlation, solve_null_correlation, solve_power, solve_size


@dataclass
class TestCase:
    __test__ = False

    null_correlation: float
    correlation: float
    size: int
    alpha: float
    power: float
    bias_adj: bool


case_group = (
    [
        # Regular Test Cases: null_correlation = 0.70, correlation = 0.80 to 0.85 by 0.01, alpha = 0.05, power = 0.80, bias_adj = False
        TestCase(null_correlation=0.70, correlation=correlation, size=size, alpha=0.05, power=0.80, bias_adj=False)
        for correlation, size in [
            (0.80, 150),
            (0.81, 120),
            (0.82, 97),
            (0.83, 80),
            (0.84, 66),
            (0.85, 55),
            (0.85, 55),
        ]
    ]
    + [
        # Regular Test Cases: null_correlation = 0.70, correlation = 0.80 to 0.85 by 0.01, alpha = 0.05, power = 0.80, bias_adj = True
        TestCase(null_correlation=0.70, correlation=correlation, size=size, alpha=0.05, power=0.80, bias_adj=True)
        for correlation, size in [
            (0.80, 150),
            (0.81, 119),
            (0.82, 97),
            (0.83, 79),
            (0.84, 66),
            (0.85, 55),
        ]
    ]
    + [
        # Regular Test Cases: null_correlation = 0.70, correlation = 0.50 to 0.55 by 0.01, alpha = 0.05, power = 0.80, bias_adj = True
        TestCase(null_correlation=0.70, correlation=correlation, size=size, alpha=0.05, power=0.80, bias_adj=True)
        for correlation, size in [
            (0.50, 81),
            (0.51, 88),
            (0.52, 96),
            (0.53, 105),
            (0.54, 116),
            (0.55, 130),
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
                alpha=case.alpha,
                bias_adj=case.bias_adj,
            ),
            2,
        )
        == case.power
    )


def test_solve_size(case: TestCase) -> None:
    assert (
        solve_size(
            null_correlation=case.null_correlation,
            correlation=case.correlation,
            alpha=case.alpha,
            power=case.power,
            bias_adj=case.bias_adj,
        )
        == case.size
    )


def test_solve_null_correlation(case: TestCase) -> None:
    search_direction = "upper" if case.null_correlation > case.correlation else "lower"
    assert (
        round(
            solve_null_correlation(
                correlation=case.correlation,
                size=case.size,
                alpha=case.alpha,
                power=case.power,
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
    search_direction = "upper" if case.correlation > case.null_correlation else "lower"
    assert (
        round(
            solve_correlation(
                null_correlation=case.null_correlation,
                size=case.size,
                alpha=case.alpha,
                power=case.power,
                bias_adj=case.bias_adj,
                search_direction=search_direction,
            ),
            2,
        )
        == case.correlation
    )

    with pytest.raises(ValueError):
        solve_correlation(null_correlation=0.80, size=100, alpha=0.05, power=0.80, bias_adj=True, search_direction="equal")
