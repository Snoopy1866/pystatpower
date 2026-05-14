# Validation Software: PASS 15
# Module: Confidence Interval for One Proportion

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.models.proportion.single.ci import solve_ci_width, solve_proportion, solve_size


@dataclass
class TestCase:
    __test__ = False

    proportion: float
    ci_width: float
    size: int
    alpha: float
    method: Literal["wald", "wilson", "clopper_pearson"]
    continuity_correction: bool | None = None


case_group = (
    [
        # Regular Test Cases: proportion = 0.90, ci_width = 0.01 to 0.10 by 0.01, alpha = 0.05, method = "clopper_pearson"
        TestCase(proportion=0.90, ci_width=ci_width, size=size, alpha=0.05, method="clopper_pearson")
        for ci_width, size in [
            (0.01, 14029),
            (0.02, 3557),
            (0.03, 1603),
            (0.04, 914),
            (0.05, 593),
            (0.06, 417),
            (0.07, 310),
            (0.08, 241),
            (0.09, 192),
            (0.10, 158),
        ]
    ]
    + [
        # Regular Test Cases: proportion = 0.90, ci_width = 0.01 to 0.10 by 0.01, alpha = 0.05, method = "wald", continuity_correction = False
        TestCase(proportion=0.90, ci_width=ci_width, size=size, alpha=0.05, method="wald", continuity_correction=False)
        for ci_width, size in [
            (0.01, 13830),
            (0.02, 3458),
            (0.03, 1537),
            (0.04, 865),
            (0.05, 554),
            (0.06, 385),
            (0.07, 283),
            (0.08, 217),
            (0.09, 171),
            (0.10, 139),
        ]
    ]
    + [
        # Regular Test Cases: proportion = 0.90, ci_width = 0.01 to 0.10 by 0.01, alpha = 0.05, method = "wald", continuity_correction = True
        TestCase(proportion=0.90, ci_width=ci_width, size=size, alpha=0.05, method="wald", continuity_correction=True)
        for ci_width, size in [
            (0.01, 14029),
            (0.02, 3557),
            (0.03, 1603),
            (0.04, 914),
            (0.05, 593),
            (0.06, 417),
            (0.07, 311),
            (0.08, 241),
            (0.09, 193),
            (0.10, 158),
        ]
    ]
    + [
        # Regular Test Cases: proportion = 0.90, ci_width = 0.01 to 0.10 by 0.01, alpha = 0.05, method = "wilson", continuity_correction = False
        TestCase(proportion=0.90, ci_width=ci_width, size=size, alpha=0.05, method="wilson", continuity_correction=False)
        for ci_width, size in [
            (0.01, 13833),
            (0.02, 3461),
            (0.03, 1540),
            (0.04, 868),
            (0.05, 557),
            (0.06, 388),
            (0.07, 286),
            (0.08, 219),
            (0.09, 174),
            (0.10, 141),
        ]
    ]
    + [
        # Regular Test Cases: proportion = 0.90, ci_width = 0.01 to 0.10 by 0.01, alpha = 0.05, method = "wilson", continuity_correction = True
        TestCase(proportion=0.90, ci_width=ci_width, size=size, alpha=0.05, method="wilson", continuity_correction=True)
        for ci_width, size in [
            (0.01, 14032),
            (0.02, 3560),
            (0.03, 1606),
            (0.04, 917),
            (0.05, 595),
            (0.06, 420),
            (0.07, 313),
            (0.08, 243),
            (0.09, 195),
            (0.10, 160),
        ]
    ]
    + [
        # Regular Test Cases: proportion = 0.10, ci_width = 0.01 to 0.10 by 0.01, alpha = 0.05, method = "wilson", continuity_correction = True
        TestCase(proportion=0.10, ci_width=ci_width, size=size, alpha=0.05, method="wilson", continuity_correction=True)
        for ci_width, size in [
            (0.01, 14032),
            (0.02, 3560),
            (0.03, 1606),
            (0.04, 917),
            (0.05, 595),
            (0.06, 420),
            (0.07, 313),
            (0.08, 243),
            (0.09, 195),
            (0.10, 160),
        ]
    ]
)


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


def test_solve_size(case: TestCase) -> None:
    assert (
        solve_size(
            proportion=case.proportion,
            ci_width=case.ci_width,
            alpha=case.alpha,
            method=case.method,
            continuity_correction=case.continuity_correction,
        )
        == case.size
    )


def test_solve_wilson_cc_no_solution() -> None:
    with pytest.raises(ValueError):
        assert solve_size(proportion=0.90, ci_width=0.99, alpha=0.05, method="wilson", continuity_correction=True)


def test_solve_ci_width(case: TestCase) -> None:
    assert (
        round(
            solve_ci_width(
                proportion=case.proportion,
                size=case.size,
                alpha=case.alpha,
                method=case.method,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.ci_width
    )


def test_solve_proportion(case: TestCase) -> None:
    side = "lower" if case.proportion < 0.5 else "upper"
    assert (
        round(
            solve_proportion(
                size=case.size,
                ci_width=case.ci_width,
                alpha=case.alpha,
                method=case.method,
                continuity_correction=case.continuity_correction,
                side=side,
            ),
            2,
        )
        == case.proportion
    )

    with pytest.raises(ValueError):
        solve_proportion(size=10, ci_width=0.2, alpha=0.05, method="wald", continuity_correction=True, side="neutral")
