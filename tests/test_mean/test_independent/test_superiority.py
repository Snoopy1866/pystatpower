# Validation Software: PASS 15
# Module: Superiority by a Margin Tests for the Difference Between Two Means

from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.mean.independent._verify import _verify_mean_and_get_diff, _verify_std_and_get_std
from pystatpower.mean.independent.superiority import solve_power, solve_size, solve_treatment_mean, solve_reference_mean, solve_diff, solve_margin, solve_treatment_std, solve_reference_std

from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    treatment_mean: float | None = None
    reference_mean: float | None = None
    diff: float | None = None
    margin: float
    treatment_std: float | None = None
    reference_std: float | None = None
    std: float | None = None
    treatment_size: int
    reference_size: int
    alternative: Literal["greater", "less"]
    alpha: float
    power: float
    actual_power: float
    dist: Literal["z", "t"]
    equal_var: bool
    approx_t_method: Literal["welch", "satterthwaite"] = "welch"

    def __post_init__(self) -> None:
        self.diff = _verify_mean_and_get_diff(self.treatment_mean, self.reference_mean, self.diff)
        self.std = _verify_std_and_get_std(self.treatment_std, self.reference_std, self.std, self.dist, self.equal_var)


# The superiority module of PASS 15 does not support z-test. The test cases here are verified by AI.
case_group_z_equal_var = [
    # treatment_mean = 10, reference_mean = 40, margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, dist = "z", equal_var = True
    TestCase(
        treatment_mean=10,
        reference_mean=40,
        margin=margin,
        treatment_std=40,
        reference_std=40,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="less",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="z",
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
] + [
    # treatment_mean = 40, reference_mean = 10, margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, dist = "z", equal_var = True
    TestCase(
        treatment_mean=40,
        reference_mean=10,
        margin=margin,
        treatment_std=40,
        reference_std=40,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="greater",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="z",
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

# The superiority module of PASS 15 does not support z-test. The test cases here are verified by AI.
case_group_z_unequal_var = [
    # treatment_mean = 10, reference_mean = 40, margin = -20 to -10 by 1, treatment_std = 40, reference_std = 30, ratio = 2, alpha = 0.025, power = 0.80, dist = "z", equal_var = False
    TestCase(
        treatment_mean=10,
        reference_mean=40,
        margin=margin,
        treatment_std=40,
        reference_std=30,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="less",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="z",
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
] + [
    # treatment_mean = 40, reference_mean = 10, margin = 10 to 20 by 1, treatment_std = 40, reference_std = 30, ratio = 2, alpha = 0.025, power = 0.80, dist = "z", equal_var = False
    TestCase(
        treatment_mean=40,
        reference_mean=10,
        margin=margin,
        treatment_std=40,
        reference_std=30,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="greater",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="z",
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

case_group_t_equal_var = [
    # treatment_mean = 10, reference_mean = 40, margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, dist = "t", equal_var = True
    TestCase(
        treatment_mean=10,
        reference_mean=40,
        margin=margin,
        treatment_std=40,
        reference_std=40,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="less",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="t",
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
] + [
    # treatment_mean = 40, reference_mean = 10, margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, ratio = 0.5, alpha = 0.025, power = 0.80, dist = "t", equal_var = True
    TestCase(
        treatment_mean=40,
        reference_mean=10,
        margin=margin,
        treatment_std=40,
        reference_std=40,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="greater",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="t",
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

case_group_t_unequal_var_welch = [
    # treatment_mean = 10, reference_mean = 40, margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, dist = "t", equal_var = False, approx_t_method = "welch"
    TestCase(
        treatment_mean=10,
        reference_mean=40,
        margin=margin,
        treatment_std=40,
        reference_std=40,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="less",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="t",
        equal_var=False,
        approx_t_method="welch",
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
] + [
    # treatment_mean = 40, reference_mean = 10, margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, dist = "t", equal_var = False, approx_t_method = "welch"
    TestCase(
        treatment_mean=40,
        reference_mean=10,
        margin=margin,
        treatment_std=40,
        reference_std=40,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="greater",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="t",
        equal_var=False,
        approx_t_method="welch",
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

case_group_t_unequal_var_satterthwaite = [
    # treatment_mean = 10, reference_mean = 40, margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, dist = "t", equal_var = False, approx_t_method = "satterthwaite"
    TestCase(
        treatment_mean=10,
        reference_mean=40,
        margin=margin,
        treatment_std=40,
        reference_std=40,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="less",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="t",
        equal_var=False,
        approx_t_method="satterthwaite",
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
] + [
    # treatment_mean = 40, reference_mean = 10, margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.025, power = 0.80, dist = "t", equal_var = False, approx_t_method = "satterthwaite"
    TestCase(
        treatment_mean=40,
        reference_mean=10,
        margin=margin,
        treatment_std=40,
        reference_std=40,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="greater",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="t",
        equal_var=False,
        approx_t_method="satterthwaite",
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

case_group = case_group_z_equal_var + case_group_z_unequal_var + case_group_t_equal_var + case_group_t_unequal_var_welch + case_group_t_unequal_var_satterthwaite


def test_solve_power(case: TestCase) -> None:
    assert round(
        solve_power(
            treatment_mean=case.treatment_mean,
            reference_mean=case.reference_mean,
            diff=case.diff,
            margin=case.margin,
            treatment_std=case.treatment_std,
            reference_std=case.reference_std,
            std=case.std,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            alternative=case.alternative,
            alpha=case.alpha,
            dist=case.dist,
            equal_var=case.equal_var,
            approx_t_method=case.approx_t_method,
        ),
        4,
    ) == round(case.actual_power, 4)


def test_solve_size(case: TestCase, request: pytest.FixtureRequest) -> None:
    if case in [
        TestCase(
            treatment_mean=40,
            reference_mean=10,
            margin=13,
            treatment_std=40,
            reference_std=40,
            treatment_size=67,
            reference_size=134,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8051,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
        TestCase(
            treatment_mean=40,
            reference_mean=10,
            margin=10,
            treatment_std=40,
            reference_std=40,
            treatment_size=49,
            reference_size=98,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8076,
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        ),
        TestCase(
            treatment_mean=40,
            reference_mean=10,
            margin=15,
            treatment_std=40,
            reference_std=40,
            treatment_size=85,
            reference_size=170,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8014,
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        ),
        TestCase(
            treatment_mean=40,
            reference_mean=10,
            margin=19,
            treatment_std=40,
            reference_std=40,
            treatment_size=157,
            reference_size=314,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8009,
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        ),
    ]:
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25106"))

    ratio = case.treatment_size / case.reference_size
    assert solve_size(
        treatment_mean=case.treatment_mean,
        reference_mean=case.reference_mean,
        diff=case.diff,
        margin=case.margin,
        treatment_std=case.treatment_std,
        reference_std=case.reference_std,
        std=case.std,
        ratio=ratio,
        alternative=case.alternative,
        alpha=case.alpha,
        power=case.power,
        dist=case.dist,
        equal_var=case.equal_var,
        approx_t_method=case.approx_t_method,
    ) == (case.treatment_size, case.reference_size)


def test_solve_treatment_mean(case: TestCase, request: pytest.FixtureRequest) -> None:
    if case in [
        TestCase(
            treatment_mean=40,
            reference_mean=10,
            margin=15,
            treatment_std=40,
            reference_std=40,
            treatment_size=85,
            reference_size=170,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8015,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
    ]:
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25106"))

    assert (
        round(
            solve_treatment_mean(
                reference_mean=case.reference_mean,
                margin=case.margin,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                std=case.std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                equal_var=case.equal_var,
                approx_t_method=case.approx_t_method,
            ),
            0,
        )
        == case.treatment_mean
    )


def test_solve_reference_mean(case: TestCase, request: pytest.FixtureRequest) -> None:
    if case in [
        TestCase(
            treatment_mean=40,
            reference_mean=10,
            margin=15,
            treatment_std=40,
            reference_std=40,
            treatment_size=85,
            reference_size=170,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8015,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
    ]:
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25106"))

    assert (
        round(
            solve_reference_mean(
                treatment_mean=case.treatment_mean,
                margin=case.margin,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                std=case.std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                equal_var=case.equal_var,
                approx_t_method=case.approx_t_method,
            ),
            0,
        )
        == case.reference_mean
    )


def test_solve_diff(case: TestCase, request: pytest.FixtureRequest) -> None:
    if case in [
        TestCase(
            treatment_mean=40,
            reference_mean=10,
            margin=15,
            treatment_std=40,
            reference_std=40,
            treatment_size=85,
            reference_size=170,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8015,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
        TestCase(
            treatment_mean=40,
            reference_mean=10,
            margin=16,
            treatment_std=40,
            reference_std=40,
            treatment_size=98,
            reference_size=196,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8038,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
        TestCase(
            treatment_mean=40,
            reference_mean=10,
            margin=16,
            treatment_std=40,
            reference_std=40,
            treatment_size=98,
            reference_size=196,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8037,
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        ),
    ]:
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25106"))

    assert (
        round(
            solve_diff(
                margin=case.margin,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                std=case.std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                equal_var=case.equal_var,
                approx_t_method=case.approx_t_method,
            ),
            0,
        )
        == case.diff
    )


def test_solve_margin(case: TestCase, request: pytest.FixtureRequest) -> None:
    if case in [
        TestCase(
            treatment_mean=40,
            reference_mean=10,
            margin=15,
            treatment_std=40,
            reference_std=40,
            treatment_size=85,
            reference_size=170,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8015,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
    ]:
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25106"))

    assert (
        round(
            solve_margin(
                treatment_mean=case.treatment_mean,
                reference_mean=case.reference_mean,
                diff=case.diff,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                std=case.std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                equal_var=case.equal_var,
                approx_t_method=case.approx_t_method,
            ),
            0,
        )
        == case.margin
    )


def test_solve_treatment_std(case: TestCase) -> None:
    assert (
        round(
            solve_treatment_std(
                treatment_mean=case.treatment_mean,
                reference_mean=case.reference_mean,
                diff=case.diff,
                margin=case.margin,
                reference_std=case.reference_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                equal_var=case.equal_var,
                approx_t_method=case.approx_t_method,
            ),
            0,
        )
        == case.treatment_std
    )

    if case.dist == "t" and case.equal_var:
        assert (
            round(
                solve_treatment_std(
                    treatment_mean=case.treatment_mean,
                    reference_mean=case.reference_mean,
                    diff=case.diff,
                    margin=case.margin,
                    treatment_size=case.treatment_size,
                    reference_size=case.reference_size,
                    alternative=case.alternative,
                    alpha=case.alpha,
                    power=case.actual_power,
                    dist=case.dist,
                    equal_var=case.equal_var,
                    approx_t_method=case.approx_t_method,
                ),
                0,
            )
            == case.treatment_std
        )


def test_solve_treatment_std_error() -> None:
    with pytest.raises(ValueError):
        solve_treatment_std(diff=0, margin=10, treatment_size=20, reference_size=20, alternative="greater", equal_var=False)


def test_solve_reference_std(case: TestCase) -> None:
    assert (
        round(
            solve_reference_std(
                treatment_mean=case.treatment_mean,
                reference_mean=case.reference_mean,
                diff=case.diff,
                margin=case.margin,
                treatment_std=case.treatment_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                equal_var=case.equal_var,
                approx_t_method=case.approx_t_method,
            ),
            0,
        )
        == case.reference_std
    )

    if case.dist == "t" and case.equal_var:
        assert (
            round(
                solve_reference_std(
                    treatment_mean=case.treatment_mean,
                    reference_mean=case.reference_mean,
                    diff=case.diff,
                    margin=case.margin,
                    treatment_size=case.treatment_size,
                    reference_size=case.reference_size,
                    alternative=case.alternative,
                    alpha=case.alpha,
                    power=case.actual_power,
                    dist=case.dist,
                    equal_var=case.equal_var,
                    approx_t_method=case.approx_t_method,
                ),
                0,
            )
            == case.reference_std
        )


def test_solve_reference_std_error() -> None:
    with pytest.raises(ValueError):
        solve_reference_std(diff=0, margin=10, treatment_size=20, reference_size=20, alternative="greater", equal_var=False)
