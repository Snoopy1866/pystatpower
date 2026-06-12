# Validation Software: PASS 15
# Module: Non-Inferiority Tests for the Difference Between Two Means

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.mean.independent.noninferiority import solve_power, solve_size, solve_diff, solve_margin, solve_treatment_std, solve_reference_std


@dataclass
class TestCase:
    __test__ = False

    treatment_mean: float
    reference_mean: float
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
        # Regular Cases: margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = True
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
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
        for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
            (10, 10, -20, 95, 48, 0.8007),
            (10, 10, -19, 105, 53, 0.8000),
            (10, 10, -18, 117, 59, 0.8003),
            (10, 10, -17, 131, 66, 0.8000),
            (10, 10, -16, 149, 75, 0.8032),
            (10, 10, -15, 169, 85, 0.8022),
            (10, 10, -14, 193, 97, 0.8003),
            (10, 10, -13, 225, 113, 0.8025),
            (10, 10, -12, 263, 132, 0.8011),
            (10, 10, -11, 313, 157, 0.8013),
            (10, 10, -10, 379, 190, 0.8017),
        ]
    ]
    + [
        # Regular Cases: margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, ratio = 0.5, alpha = 0.025, power = 0.80, method = "t", equal_var = True
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
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
        for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
            (30, 30, 10, 190, 380, 0.8020),
            (30, 30, 11, 157, 314, 0.8017),
            (30, 30, 12, 132, 264, 0.8016),
            (30, 30, 13, 113, 226, 0.8031),
            (30, 30, 14, 97, 194, 0.8010),
            (30, 30, 15, 85, 170, 0.8029),
            (30, 30, 16, 75, 150, 0.8041),
            (30, 30, 17, 66, 132, 0.8010),
            (30, 30, 18, 59, 118, 0.8014),
            (30, 30, 19, 53, 106, 0.8013),
            (30, 30, 20, 48, 96, 0.8021),
        ]
    ]
    + [
        # Regular Cases: margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "welch"
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
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
        for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
            (10, 10, -20, 97, 49, 0.8064),
            (10, 10, -19, 107, 54, 0.8052),
            (10, 10, -18, 119, 60, 0.8049),
            (10, 10, -17, 133, 67, 0.8041),  #
            (10, 10, -16, 149, 75, 0.8016),
            (10, 10, -15, 169, 85, 0.8007),
            (10, 10, -14, 195, 98, 0.8031),
            (10, 10, -13, 225, 113, 0.8014),
            (10, 10, -12, 263, 132, 0.8002),
            (10, 10, -11, 313, 157, 0.8005),
            (10, 10, -10, 379, 190, 0.8010),
        ]
    ]
    + [
        # Regular Cases: margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "welch"
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
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
        for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
            (30, 30, 10, 379, 190, 0.8010),
            (30, 30, 11, 313, 157, 0.8005),
            (30, 30, 12, 263, 132, 0.8002),
            (30, 30, 13, 225, 113, 0.8014),
            (30, 30, 14, 195, 98, 0.8031),
            (30, 30, 15, 169, 85, 0.8007),
            (30, 30, 16, 149, 75, 0.8016),
            (30, 30, 17, 133, 67, 0.8041),
            (30, 30, 18, 119, 60, 0.8049),
            (30, 30, 19, 107, 54, 0.8052),
            (30, 30, 20, 97, 49, 0.8064),
        ]
    ]
    + [
        # Regular Cases: margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "satterthwaite"
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
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
        for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
            (10, 10, -20, 97, 49, 0.8063),
            (10, 10, -19, 107, 54, 0.8051),
            (10, 10, -18, 119, 60, 0.8048),
            (10, 10, -17, 133, 67, 0.8041),
            (10, 10, -16, 149, 75, 0.8015),
            (10, 10, -15, 169, 85, 0.8007),
            (10, 10, -14, 195, 98, 0.8031),
            (10, 10, -13, 225, 113, 0.8014),
            (10, 10, -12, 263, 132, 0.8002),  #
            (10, 10, -11, 313, 157, 0.8005),
            (10, 10, -10, 379, 190, 0.8010),
        ]
    ]
    + [
        # Regular Cases: margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = False, df_adjust = "satterthwaite"
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
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
        for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
            (30, 30, 10, 379, 190, 0.8010),
            (30, 30, 11, 313, 157, 0.8005),
            (30, 30, 12, 263, 132, 0.8002),
            (30, 30, 13, 225, 113, 0.8014),
            (30, 30, 14, 195, 98, 0.8031),
            (30, 30, 15, 169, 85, 0.8007),
            (30, 30, 16, 149, 75, 0.8015),
            (30, 30, 17, 133, 67, 0.8041),
            (30, 30, 18, 119, 60, 0.8048),
            (30, 30, 19, 107, 54, 0.8051),
            (30, 30, 20, 97, 49, 0.8063),
        ]
    ]
    + [
        # Regular Cases: margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, method = "z", equal_var = True
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
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
        for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
            (10, 10, -20, 96, 48, 0.8074),
            (10, 10, -19, 106, 53, 0.8061),
            (10, 10, -18, 118, 59, 0.8057),
            (10, 10, -17, 132, 66, 0.8049),
            (10, 10, -16, 148, 74, 0.8022),
            (10, 10, -15, 168, 84, 0.8013),
            (10, 10, -14, 194, 97, 0.8036),
            (10, 10, -13, 224, 112, 0.8019),
            (10, 10, -12, 262, 131, 0.8006),
            (10, 10, -11, 312, 156, 0.8008),
            (10, 10, -10, 378, 189, 0.8013),
        ]
    ]
    + [
        # Regular Cases: margin = 10 to 20 by 1, treatment_std = 40, reference_std = 30, ratio = 2, alpha = 0.025, power = 0.80, method = "z", equal_var = False
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
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
        for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
            (30, 30, 10, 268, 134, 0.8017),
            (30, 30, 11, 222, 111, 0.8026),
            (30, 30, 12, 186, 93, 0.8014),
            (30, 30, 13, 158, 79, 0.8002),
            (30, 30, 14, 138, 69, 0.8053),
            (30, 30, 15, 120, 60, 0.8046),
            (30, 30, 16, 106, 53, 0.8065),
            (30, 30, 17, 94, 47, 0.8069),
            (30, 30, 18, 84, 42, 0.8077),
            (30, 30, 19, 74, 37, 0.8004),
            (30, 30, 20, 68, 34, 0.8074),
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
                treatment_mean=case.treatment_mean,
                reference_mean=case.reference_mean,
                margin=case.margin,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                method=case.method,
                equal_var=case.equal_var,
                df_adjust=case.df_adjust,
            ),
            4,
        )
        == case.actual_power
    )


def test_solve_power_error() -> None:
    with pytest.raises(ValueError):
        solve_power(diff=0, margin=10, treatment_std=20, reference_std=30, treatment_size=20, reference_size=20, method="z", equal_var=True)
    with pytest.raises(ValueError):
        solve_power(treatment_mean=10, margin=10, treatment_std=20, reference_std=30, treatment_size=20, reference_size=20, method="z")


def test_solve_size(case: TestCase) -> None:
    if (
        case
        == TestCase(
            treatment_mean=10,
            reference_mean=10,
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
            treatment_mean=10,
            reference_mean=10,
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
            treatment_mean=10,
            reference_mean=10,
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
            treatment_mean=10,
            reference_mean=10,
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
        or case
        == TestCase(
            treatment_mean=10,
            reference_mean=10,
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
            treatment_mean=30,
            reference_mean=30,
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
        treatment_mean=case.treatment_mean,
        reference_mean=case.reference_mean,
        margin=case.margin,
        treatment_std=case.treatment_std,
        reference_std=case.reference_std,
        ratio=ratio,
        alpha=case.alpha,
        power=case.power,
        method=case.method,
        equal_var=case.equal_var,
        df_adjust=case.df_adjust,
    ) == (case.treatment_size, case.reference_size)


def test_solve_size_error() -> None:
    with pytest.raises(ValueError):
        solve_size(diff=0, margin=10, treatment_std=30, reference_std=20, ratio=1, alpha=0.05, power=0.80, method="z", equal_var=True)


def test_solve_diff(case: TestCase) -> None:
    if case == TestCase(
        treatment_mean=10,
        reference_mean=10,
        margin=-14,
        treatment_std=40,
        reference_std=40,
        treatment_size=193,
        reference_size=97,
        alpha=0.025,
        power=0.8,
        actual_power=0.8003,
        method="t",
        equal_var=True,
    ) or case == TestCase(
        treatment_mean=10,
        reference_mean=10,
        margin=-14,
        treatment_std=40,
        reference_std=40,
        treatment_size=195,
        reference_size=98,
        alpha=0.025,
        power=0.8,
        actual_power=0.8031,
        method="t",
        equal_var=False,
        df_adjust="satterthwaite",
    ):
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    diff = case.treatment_mean - case.reference_mean
    assert (
        round(
            solve_diff(
                margin=case.margin,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                equal_var=case.equal_var,
                df_adjust=case.df_adjust,
            ),
            0,
        )
        == diff
    )


def test_solve_diff_error() -> None:
    with pytest.raises(ValueError):
        solve_diff(margin=10, treatment_std=10, reference_std=20, treatment_size=20, reference_size=20, method="z", equal_var=True)


def test_solve_margin(case: TestCase) -> None:
    if (
        case
        == TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-14,
            treatment_std=40,
            reference_std=40,
            treatment_size=193,
            reference_size=97,
            alpha=0.025,
            power=0.8,
            actual_power=0.8003,
            method="t",
            equal_var=True,
        )
        or case
        == TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-14,
            treatment_std=40,
            reference_std=40,
            treatment_size=195,
            reference_size=98,
            alpha=0.025,
            power=0.8,
            actual_power=0.8031,
            method="t",
            equal_var=False,
            df_adjust="welch",
        )
        or case
        == TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-14,
            treatment_std=40,
            reference_std=40,
            treatment_size=195,
            reference_size=98,
            alpha=0.025,
            power=0.8,
            actual_power=0.8031,
            method="t",
            equal_var=False,
            df_adjust="satterthwaite",
        )
    ):
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    diff = case.treatment_mean - case.reference_mean
    margin_selection = "negative" if case.margin < 0 else "positive"

    assert (
        round(
            solve_margin(
                diff=diff,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                equal_var=case.equal_var,
                df_adjust=case.df_adjust,
                margin_selection=margin_selection,
            ),
            0,
        )
        == case.margin
    )


def test_solve_margin_error() -> None:
    with pytest.raises(ValueError):
        solve_margin(diff=0, treatment_std=10, reference_std=20, treatment_size=20, reference_size=20, method="z", equal_var=True)


def test_solve_treatment_std(case: TestCase) -> None:
    diff = case.treatment_mean - case.reference_mean
    assert (
        round(
            solve_treatment_std(
                diff=diff,
                margin=case.margin,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                equal_var=case.equal_var,
                reference_std=case.reference_std,
                df_adjust=case.df_adjust,
            ),
            0,
        )
        == case.treatment_std
    )


def test_solve_treatment_std_error() -> None:
    with pytest.raises(ValueError):
        solve_treatment_std(diff=0, margin=10, treatment_size=20, reference_size=20, equal_var=False)


def test_solve_reference_std(case: TestCase) -> None:
    diff = case.treatment_mean - case.reference_mean
    assert (
        round(
            solve_reference_std(
                diff=diff,
                margin=case.margin,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                equal_var=case.equal_var,
                treatment_std=case.treatment_std,
                df_adjust=case.df_adjust,
            ),
            0,
        )
        == case.reference_std
    )


def test_solve_reference_std_error() -> None:
    with pytest.raises(ValueError):
        solve_reference_std(diff=0, margin=10, treatment_size=20, reference_size=20, equal_var=False)
