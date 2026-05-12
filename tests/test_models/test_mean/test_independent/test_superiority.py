# Validation Software: PASS 15
# Module: Superiority by a Margin Tests for the Difference Between Two Means

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.models.mean.independent.superiority import solve_power, solve_size, solve_diff, solve_margin, solve_treatment_std, solve_reference_std


@dataclass
class TestCase:
    __test__ = False

    diff: float
    margin: float
    treatment_std: float
    reference_std: float
    treatment_size: int
    reference_size: int
    alternative: Literal["lower", "upper"]
    alpha: float
    power: float
    actual_power: float
    method: Literal["z", "t"]
    equal_var: bool
    df_adjust: Literal["welch", "satterthwaite"] | None = None


case_group = (
    [
        # Regular Test Cases: diff = -30, margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = True
        TestCase(
            diff=-30,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="lower",
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=True,
        )
        for margin, treatment_size, reference_size, actual_power in [
            (-20, 379, 190, 0.8017),
            (-19, 313, 157, 0.8013),
            (-18, 263, 132, 0.8011),
            (-17, 225, 113, 0.8025),
            (-16, 193, 97, 0.8003),
            (-15, 169, 85, 0.8022),
            (-14, 149, 75, 0.8032),
            (-13, 131, 66, 0.8000),
            (-12, 117, 59, 0.8003),
            (-11, 105, 53, 0.8000),
            (-10, 95, 48, 0.8007),
        ]
    ]
    + [
        # Regular Test Cases: diff = 30, margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, Ratio = 0.5, alpha = 0.025, power = 0.80, method = "t", equal_var = True
        TestCase(
            diff=30,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="upper",
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=True,
        )
        for margin, treatment_size, reference_size, actual_power in [
            (10, 48, 96, 0.8021),
            (11, 53, 106, 0.8013),
            (12, 59, 118, 0.8014),
            (13, 66, 132, 0.8010),
            (14, 75, 150, 0.8041),
            (15, 85, 170, 0.8029),
            (16, 97, 194, 0.8010),
            (17, 113, 226, 0.8031),
            (18, 132, 264, 0.8016),
            (19, 157, 314, 0.8017),
            (20, 190, 380, 0.8020),
        ]
    ]
    + [
        # Regular Test Cases: diff = -30, margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "welch"
        TestCase(
            diff=-30,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="lower",
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="welch",
        )
        for margin, treatment_size, reference_size, actual_power in [
            (-20, 379, 190, 0.8010),
            (-19, 313, 157, 0.8005),
            (-18, 263, 132, 0.8002),
            (-17, 225, 113, 0.8014),
            (-16, 195, 98, 0.8031),
            (-15, 169, 85, 0.8007),
            (-14, 149, 75, 0.8016),
            (-13, 133, 67, 0.8041),
            (-12, 119, 60, 0.8049),
            (-11, 107, 54, 0.8052),
            (-10, 97, 49, 0.8064),
        ]
    ]
    + [
        # Regular Test Cases: diff = 30, margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "welch"
        TestCase(
            diff=30,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="upper",
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="welch",
        )
        for margin, treatment_size, reference_size, actual_power in [
            (10, 49, 98, 0.8077),
            (11, 54, 108, 0.8064),
            (12, 60, 120, 0.8060),
            (13, 67, 134, 0.8051),
            (14, 75, 150, 0.8024),
            (15, 85, 170, 0.8015),
            (16, 98, 196, 0.8038),
            (17, 113, 226, 0.8020),
            (18, 132, 264, 0.8007),
            (19, 157, 314, 0.8009),
            (20, 190, 380, 0.8014),
        ]
    ]
    + [
        # Regular Test Cases: diff = -30, margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "satterthwaite"
        TestCase(
            diff=-30,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="lower",
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="satterthwaite",
        )
        for margin, treatment_size, reference_size, actual_power in [
            (-20, 379, 190, 0.8010),
            (-19, 313, 157, 0.8005),
            (-18, 263, 132, 0.8002),
            (-17, 225, 113, 0.8014),
            (-16, 195, 98, 0.8031),
            (-15, 169, 85, 0.8007),
            (-14, 149, 75, 0.8015),
            (-13, 133, 67, 0.8041),
            (-12, 119, 60, 0.8048),
            (-11, 107, 54, 0.8051),
            (-10, 97, 49, 0.8063),
        ]
    ]
    + [
        # Regular Test Cases: diff = 30, margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "satterthwaite"
        TestCase(
            diff=30,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="upper",
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="satterthwaite",
        )
        for margin, treatment_size, reference_size, actual_power in [
            (10, 49, 98, 0.8076),
            (11, 54, 108, 0.8062),
            (12, 60, 120, 0.8059),
            (13, 67, 134, 0.8050),
            (14, 75, 150, 0.8024),
            (15, 85, 170, 0.8014),
            (16, 98, 196, 0.8037),
            (17, 113, 226, 0.8020),
            (18, 132, 264, 0.8007),
            (19, 157, 314, 0.8009),
            (20, 190, 380, 0.8014),
        ]
    ]
    + [
        # Regular Test Cases: diff = -30, margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "z", equal_var = True
        TestCase(
            diff=-30,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="lower",
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=True,
        )
        for margin, treatment_size, reference_size, actual_power in [
            (-20, 378, 189, 0.8013),
            (-19, 312, 156, 0.8008),
            (-18, 262, 131, 0.8006),
            (-17, 224, 112, 0.8019),
            (-16, 194, 97, 0.8036),
            (-15, 168, 84, 0.8013),
            (-14, 148, 74, 0.8022),
            (-13, 132, 66, 0.8049),
            (-12, 118, 59, 0.8057),
            (-11, 106, 53, 0.8061),
            (-10, 96, 48, 0.8074),
        ]
    ]
    + [
        # Regular Test Cases: diff = 30, margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "z", equal_var = True
        TestCase(
            diff=30,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="upper",
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=True,
        )
        for margin, treatment_size, reference_size, actual_power in [
            (10, 48, 96, 0.8074),
            (11, 53, 106, 0.8061),
            (12, 59, 118, 0.8057),
            (13, 66, 132, 0.8049),
            (14, 74, 148, 0.8022),
            (15, 84, 168, 0.8013),
            (16, 97, 194, 0.8036),
            (17, 112, 224, 0.8019),
            (18, 131, 262, 0.8006),
            (19, 156, 312, 0.8008),
            (20, 189, 378, 0.8013),
        ]
    ]
    + [
        # Regular Test Cases: diff = -30, margin = -20 to -10 by 1, treatment_std = 40, reference_std = 30, Ratio = 2, alpha = 0.025, power = 0.80, method = "z", equal_var = False
        TestCase(
            diff=-30,
            margin=margin,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="lower",
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=False,
        )
        for margin, treatment_size, reference_size, actual_power in [
            (-20, 268, 134, 0.8017),
            (-19, 222, 111, 0.8026),
            (-18, 186, 93, 0.8014),
            (-17, 158, 80, 0.8028),
            (-16, 138, 69, 0.8053),
            (-15, 120, 60, 0.8046),
            (-14, 106, 53, 0.8065),
            (-13, 94, 47, 0.8069),
            (-12, 84, 42, 0.8077),
            (-11, 74, 37, 0.8004),
            (-10, 68, 34, 0.8074),
        ]
    ]
    + [
        # Regular Test Cases: diff = 30, margin = 10 to 20 by 1, treatment_std = 40, reference_std = 30, Ratio = 2, alpha = 0.025, power = 0.80, method = "z", equal_var = False
        TestCase(
            diff=30,
            margin=margin,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="upper",
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=False,
        )
        for margin, treatment_size, reference_size, actual_power in [
            (10, 41, 82, 0.8074),
            (11, 45, 90, 0.8037),
            (12, 50, 100, 0.8027),
            (13, 56, 112, 0.8023),
            (14, 63, 126, 0.8009),
            (15, 72, 144, 0.8027),
            (16, 83, 166, 0.8043),
            (17, 96, 192, 0.8032),
            (18, 112, 224, 0.8009),
            (19, 133, 266, 0.8001),
            (20, 161, 322, 0.8002),
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
                case.alternative,
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
    if case == TestCase(
        diff=30,
        margin=13,
        treatment_std=40,
        reference_std=40,
        treatment_size=67,
        reference_size=134,
        alternative="upper",
        alpha=0.025,
        power=0.8,
        actual_power=0.8051,
        method="t",
        equal_var=False,
        df_adjust="welch",
    ):
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    ratio = case.treatment_size / case.reference_size
    assert solve_size(
        case.diff,
        case.margin,
        case.treatment_std,
        case.reference_std,
        ratio,
        case.alternative,
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


def test_solve_diff(case: TestCase) -> None:
    if case == TestCase(
        diff=30,
        margin=16,
        treatment_std=40,
        reference_std=40,
        treatment_size=98,
        reference_size=196,
        alternative="upper",
        alpha=0.025,
        power=0.8,
        actual_power=0.8037,
        method="t",
        equal_var=False,
        df_adjust="satterthwaite",
    ):
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    assert (
        round(
            solve_diff(
                case.margin,
                case.treatment_std,
                case.reference_std,
                case.treatment_size,
                case.reference_size,
                case.alternative,
                case.alpha,
                case.actual_power,
                case.method,
                case.equal_var,
                case.df_adjust,
            ),
            0,
        )
        == case.diff
    )

    with pytest.raises(ValueError):
        solve_diff(margin=10, treatment_std=10, reference_std=20, treatment_size=20, reference_size=20, method="z", equal_var=True)


def test_solve_margin(case: TestCase) -> None:
    assert (
        round(
            solve_margin(
                case.diff,
                case.treatment_std,
                case.reference_std,
                case.treatment_size,
                case.reference_size,
                case.alternative,
                case.alpha,
                case.actual_power,
                case.method,
                case.equal_var,
                case.df_adjust,
            ),
            0,
        )
        == case.margin
    )

    with pytest.raises(ValueError):
        solve_margin(diff=0, treatment_std=10, reference_std=20, treatment_size=20, reference_size=20, method="z", equal_var=True)


def test_solve_treatment_std(case: TestCase) -> None:
    assert (
        round(
            solve_treatment_std(
                case.diff,
                case.margin,
                case.treatment_size,
                case.reference_size,
                case.alternative,
                case.alpha,
                case.actual_power,
                case.method,
                case.equal_var,
                case.reference_std,
                case.df_adjust,
            ),
            0,
        )
        == case.treatment_std
    )

    with pytest.raises(ValueError):
        solve_treatment_std(diff=0, margin=10, treatment_size=20, reference_size=20, equal_var=False)


def test_solve_reference_std(case: TestCase) -> None:
    assert (
        round(
            solve_reference_std(
                case.diff,
                case.margin,
                case.treatment_size,
                case.reference_size,
                case.alternative,
                case.alpha,
                case.actual_power,
                case.method,
                case.equal_var,
                case.treatment_std,
                case.df_adjust,
            ),
            0,
        )
        == case.reference_std
    )

    with pytest.raises(ValueError):
        solve_reference_std(diff=0, margin=10, treatment_size=20, reference_size=20, equal_var=False)
