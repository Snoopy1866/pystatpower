from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.correlation.inequality import solve_correlation
from pystatpower.correlation.inequality import solve_null_correlation
from pystatpower.correlation.inequality import solve_power
from pystatpower.correlation.inequality import solve_size
from tests.models import BaseTestCase

pytestmark = pytest.mark.skip(
    reason="The methods used by PASS and SAS are quite complex and cannot be used directly as test cases, so this module is skipped for now"
)


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    null_correlation: float
    correlation: float
    alternative: Literal["two-sided", "greater", "less"]
    size: int
    alpha: float
    power: float
    actual_power: float

    direction: Literal["greater", "less"] | None = None


case_group = (
    [
        # null_correlation = 0.70, correlation = 0.80 to 0.85 by 0.01, alternative="two-sided"
        TestCase(
            null_correlation=null_correlation,
            correlation=correlation,
            alternative="two-sided",
            size=size,
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
        )
        for null_correlation, correlation, size, actual_power in [
            (0.70, 0.80, 149, 0.800033602915902),
            (0.70, 0.81, 119, 0.801172107171729),
            (0.70, 0.82, 96, 0.800214888681120),
            (0.70, 0.83, 79, 0.802216867132290),
            (0.70, 0.84, 66, 0.806165364615654),
            (0.70, 0.85, 55, 0.805663960470385),
        ]
    ]
    + [
        # null_correlation = 0.70, correlation = 0.80 to 0.85 by 0.01, alternative="greater"
        TestCase(
            null_correlation=null_correlation,
            correlation=correlation,
            alternative="greater",
            size=size,
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
        )
        for null_correlation, correlation, size, actual_power in [
            (0.70, 0.80, 118, 0.800918493524417),
            (0.70, 0.81, 94, 0.800758189202634),
            (0.70, 0.82, 76, 0.800386731516288),
            (0.70, 0.83, 63, 0.804433060505794),
            (0.70, 0.84, 52, 0.803190833888237),
            (0.70, 0.85, 44, 0.807790593965972),
        ]
    ]
    + [
        # null_correlation = 0.70, correlation = 0.50 to 0.55 by 0.01, alternative="less"
        TestCase(
            null_correlation=null_correlation,
            correlation=correlation,
            alternative="less",
            size=size,
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
        )
        for null_correlation, correlation, size, actual_power in [
            (0.70, 0.50, 64, 0.804873804392821),
            (0.70, 0.51, 69, 0.801841619643146),
            (0.70, 0.52, 76, 0.804569720197291),
            (0.70, 0.53, 83, 0.802188625071084),
            (0.70, 0.54, 92, 0.802734426274549),
            (0.70, 0.55, 102, 0.800714288976865),
        ]
    ]
)


def test_solve_power(case: TestCase) -> None:
    assert (
        round(
            solve_power(
                null_correlation=case.null_correlation,
                correlation=case.correlation,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
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
        )
        == case.size
    )


def test_solve_correlation(case: TestCase) -> None:
    case.direction = "greater" if case.correlation > case.null_correlation else "less"
    assert (
        round(
            solve_correlation(
                null_correlation=case.null_correlation,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                direction=case.direction,
            ),
            2,
        )
        == case.correlation
    )


def test_solve_null_correlation(case: TestCase) -> None:
    case.direction = "greater" if case.null_correlation > case.correlation else "less"
    assert (
        round(
            solve_null_correlation(
                correlation=case.correlation,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                direction=case.direction,
            ),
            2,
        )
        == case.null_correlation
    )
