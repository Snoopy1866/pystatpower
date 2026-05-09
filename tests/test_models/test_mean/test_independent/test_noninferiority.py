# Validation Software: PASS 15
# Module: Non-Inferiority Tests for the Difference Between Two Means

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.models.mean.independent.noninferiority import solve_power, solve_size


@dataclass
class TestCase:
    __test__ = False

    diff: float
    margin: float
    treatment_std: float
    reference_std: float
    treatment_size: int
    reference_size: int
    alpha: float
    power: float
    actual_power: float
    method: Literal["z", "t"]
    equal_var: bool
    df_adjust: Literal["welch", "satterthwaite"] | None = None


case_group = (
    [
        # Regular Test Cases: margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = True
        TestCase(
            diff=0,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=True,
        )
        for margin, treatment_size, reference_size, actual_power in [
            (-20, 95, 48, 0.8007),
            (-19, 105, 53, 0.8000),
            (-18, 117, 59, 0.8003),
            (-17, 131, 66, 0.8000),
            (-16, 149, 75, 0.8032),
            (-15, 169, 85, 0.8022),
            (-14, 193, 97, 0.8003),
            (-13, 225, 113, 0.8025),
            (-12, 263, 132, 0.8011),
            (-11, 313, 157, 0.8013),
            (-10, 379, 190, 0.8017),
        ]
    ]
    + [
        # Regular Test Cases: margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, Ratio = 0.5, alpha = 0.025, power = 0.80, method = "t", equal_var = True
        TestCase(
            diff=0,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=True,
        )
        for margin, treatment_size, reference_size, actual_power in [
            (10, 190, 380, 0.8020),
            (11, 157, 314, 0.8017),
            (12, 132, 264, 0.8016),
            (13, 113, 226, 0.8031),
            (14, 97, 194, 0.8010),
            (15, 85, 170, 0.8029),
            (16, 75, 150, 0.8041),
            (17, 66, 132, 0.8010),
            (18, 59, 118, 0.8014),
            (19, 53, 106, 0.8013),
            (20, 48, 96, 0.8021),
        ]
    ]
    + [
        # Regular Test Cases: margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "welch"
        TestCase(
            diff=0,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="welch",
        )
        for margin, treatment_size, reference_size, actual_power in [
            (-20, 97, 49, 0.8064),
            (-19, 107, 54, 0.8052),
            (-18, 119, 60, 0.8049),
            (-17, 133, 67, 0.8041),  #
            (-16, 149, 75, 0.8016),
            (-15, 169, 85, 0.8007),
            (-14, 195, 98, 0.8031),
            (-13, 225, 113, 0.8014),
            (-12, 263, 132, 0.8002),
            (-11, 313, 157, 0.8005),
            (-10, 379, 190, 0.8010),
        ]
    ]
    + [
        # Regular Test Cases: margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "welch"
        TestCase(
            diff=0,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="welch",
        )
        for margin, treatment_size, reference_size, actual_power in [
            (10, 379, 190, 0.8010),
            (11, 313, 157, 0.8005),
            (12, 263, 132, 0.8002),
            (13, 225, 113, 0.8014),
            (14, 195, 98, 0.8031),
            (15, 169, 85, 0.8007),
            (16, 149, 75, 0.8016),
            (17, 133, 67, 0.8041),
            (18, 119, 60, 0.8049),
            (19, 107, 54, 0.8052),
            (20, 97, 49, 0.8064),
        ]
    ]
    + [
        # Regular Test Cases: margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "satterthwaite"
        TestCase(
            diff=0,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="satterthwaite",
        )
        for margin, treatment_size, reference_size, actual_power in [
            (-20, 97, 49, 0.8063),
            (-19, 107, 54, 0.8051),
            (-18, 119, 60, 0.8048),
            (-17, 133, 67, 0.8041),
            (-16, 149, 75, 0.8015),
            (-15, 169, 85, 0.8007),
            (-14, 195, 98, 0.8031),
            (-13, 225, 113, 0.8014),
            (-12, 263, 132, 0.8002),  #
            (-11, 313, 157, 0.8005),
            (-10, 379, 190, 0.8010),
        ]
    ]
    + [
        # Regular Test Cases: margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "satterthwaite"
        TestCase(
            diff=0,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="satterthwaite",
        )
        for margin, treatment_size, reference_size, actual_power in [
            (10, 379, 190, 0.8010),
            (11, 313, 157, 0.8005),
            (12, 263, 132, 0.8002),
            (13, 225, 113, 0.8014),
            (14, 195, 98, 0.8031),
            (15, 169, 85, 0.8007),
            (16, 149, 75, 0.8015),
            (17, 133, 67, 0.8041),
            (18, 119, 60, 0.8048),
            (19, 107, 54, 0.8051),
            (20, 97, 49, 0.8063),
        ]
    ]
    + [
        # Regular Test Cases: margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "z", equal_var = True
        TestCase(
            diff=0,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=True,
        )
        for margin, treatment_size, reference_size, actual_power in [
            (-20, 96, 48, 0.8074),
            (-19, 106, 53, 0.8061),
            (-18, 118, 59, 0.8057),
            (-17, 132, 66, 0.8049),
            (-16, 148, 74, 0.8022),
            (-15, 168, 84, 0.8013),
            (-14, 194, 97, 0.8036),
            (-13, 224, 112, 0.8019),
            (-12, 262, 131, 0.8006),
            (-11, 312, 156, 0.8008),
            (-10, 378, 189, 0.8013),
        ]
    ]
    + [
        # Regular Test Cases: margin = 10 to 20 by 1, treatment_std = 40, reference_std = 30, Ratio = 2, alpha = 0.025, power = 0.80, method = "z", equal_var = False
        TestCase(
            diff=0,
            margin=margin,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=False,
        )
        for margin, treatment_size, reference_size, actual_power in [
            (10, 268, 134, 0.8017),
            (11, 222, 111, 0.8026),
            (12, 186, 93, 0.8014),
            (13, 158, 79, 0.8002),
            (14, 138, 69, 0.8053),
            (15, 120, 60, 0.8046),
            (16, 106, 53, 0.8065),
            (17, 94, 47, 0.8069),
            (18, 84, 42, 0.8077),
            (19, 74, 37, 0.8004),
            (20, 68, 34, 0.8074),
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
                case.diff,
                case.margin,
                case.treatment_std,
                case.reference_std,
                case.treatment_size,
                case.reference_size,
                case.alpha,
                case.method,
                case.equal_var,
                case.df_adjust,
            ),
            4,
        )
        == case.actual_power
    )

    with pytest.raises(ValueError):
        solve_power(
            diff=0,
            margin=10,
            treatment_std=10,
            reference_std=20,
            treatment_size=20,
            reference_size=20,
            method="z",
            equal_var=True,
        )


def test_solve_size(case: TestCase) -> None:
    if (
        case
        == TestCase(
            diff=0,
            margin=-17,
            treatment_std=40,
            reference_std=40,
            treatment_size=131,
            reference_size=66,
            alpha=0.025,
            power=0.8,
            actual_power=0.8,
            method="t",
            equal_var=True,
        )
        or case
        == TestCase(
            diff=0,
            margin=-12,
            treatment_std=40,
            reference_std=40,
            treatment_size=263,
            reference_size=132,
            alpha=0.025,
            power=0.8,
            actual_power=0.8002,
            method="t",
            equal_var=False,
            df_adjust="satterthwaite",
        )
        or case
        == TestCase(
            diff=0,
            margin=-12,
            treatment_std=40,
            reference_std=40,
            treatment_size=263,
            reference_size=132,
            alpha=0.025,
            power=0.8,
            actual_power=0.8011,
            method="t",
            equal_var=True,
        )
        or case
        == TestCase(
            diff=0,
            margin=-17,
            treatment_std=40,
            reference_std=40,
            treatment_size=133,
            reference_size=67,
            alpha=0.025,
            power=0.8,
            actual_power=0.8041,
            method="t",
            equal_var=False,
            df_adjust="welch",
        )
        or case
        == TestCase(
            diff=0,
            margin=-12,
            treatment_std=40,
            reference_std=40,
            treatment_size=263,
            reference_size=132,
            alpha=0.025,
            power=0.8,
            actual_power=0.8002,
            method="t",
            equal_var=False,
            df_adjust="welch",
        )
    ):
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    ratio = case.treatment_size / case.reference_size
    assert solve_size(
        case.diff,
        case.margin,
        case.treatment_std,
        case.reference_std,
        ratio,
        case.alpha,
        case.power,
        case.method,
        case.equal_var,
        case.df_adjust,
    ) == (case.treatment_size, case.reference_size)

    with pytest.raises(ValueError):
        solve_size(
            diff=0,
            margin=10,
            treatment_std=10,
            reference_std=20,
            ratio=1,
            method="z",
            equal_var=True,
        )
