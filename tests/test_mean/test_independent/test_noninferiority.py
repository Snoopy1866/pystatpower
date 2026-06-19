# Validation Software: PASS 15
# Module: Non-Inferiority Tests for the Difference Between Two Means

from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.mean.independent._verify import _verify_mean_and_get_diff, _verify_std_and_get_std
from pystatpower.mean.independent.noninferiority import solve_power, solve_size, solve_treatment_mean, solve_reference_mean, solve_diff, solve_margin, solve_treatment_std, solve_reference_std

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


# The non-inferior module of pass 15 does not support z-test. The test cases here are verified by AI.
case_group_z_equal_var = [
    # margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alternative = "greater", alpha = 0.025, power = 0.80, dist = "z", equal_var = True
    TestCase(
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
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
    for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
        (10, 10, -20, 96, 48, 0.807429578813821),
        (10, 10, -19, 106, 53, 0.8060752332852876),
        (10, 10, -18, 118, 59, 0.805730294056761),
        (10, 10, -17, 132, 66, 0.8048758305866315),
        (10, 10, -16, 148, 74, 0.802210583017446),
        (10, 10, -15, 168, 84, 0.801301455473719),
        (10, 10, -14, 194, 97, 0.8036085823531398),
        (10, 10, -13, 224, 112, 0.801880404604405),
        (10, 10, -12, 262, 131, 0.8005549626280719),
        (10, 10, -11, 312, 156, 0.8008040600716062),
        (10, 10, -10, 378, 189, 0.801301455473719),
    ]
] + [
    # margin = 10 to 20 by 1, treatment_std = 30, reference_std = 30, ratio = 2, alternative = "less", alpha = 0.025, power = 0.80, dist = "z", equal_var = True
    TestCase(
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
        margin=margin,
        treatment_std=30,
        reference_std=30,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="less",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="z",
        equal_var=True,
    )
    for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
        (30, 30, 10, 212, 106, 0.8001484543921606),
        (30, 30, 11, 176, 88, 0.8019171144127961),
        (30, 30, 12, 148, 74, 0.802210583017446),
        (30, 30, 13, 126, 63, 0.8018804046044048),
        (30, 30, 14, 110, 55, 0.8067118710583674),
        (30, 30, 15, 96, 48, 0.8074295788138209),
        (30, 30, 16, 84, 42, 0.8057032177180496),
        (30, 30, 17, 74, 37, 0.8035630304505966),
        (30, 30, 18, 66, 33, 0.8035265824012886),
        (30, 30, 19, 60, 30, 0.808501842220624),
        (30, 30, 20, 54, 27, 0.8074295788138209),
    ]
]

# The non-inferior module of pass 15 does not support z-test. The test cases here are verified by AI.
case_group_z_unequal_var = [
    # margin = -20 to 10 by 1, treatment_std = 30, reference_std = 40, ratio = 2, alternative = "greater", alpha = 0.025, power = 0.80, dist = "z", equal_var = False
    TestCase(
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
        margin=margin,
        treatment_std=30,
        reference_std=40,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="greater",
        alpha=0.025,
        power=0.80,
        actual_power=actual_power,
        dist="z",
        equal_var=False,
    )
    for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
        (30, 30, -20, 82, 41, 0.807429578813821),
        (30, 30, -19, 90, 45, 0.8037425190673304),
        (30, 30, -18, 100, 50, 0.8026607960592239),
        (30, 30, -17, 112, 56, 0.8022749530372595),
        (30, 30, -16, 126, 63, 0.8009194050738209),
        (30, 30, -15, 144, 72, 0.8026607960592239),
        (30, 30, -14, 166, 83, 0.8042934320783515),
        (30, 30, -13, 192, 96, 0.8032383497485462),
        (30, 30, -12, 224, 112, 0.8009194050738206),
        (30, 30, -11, 266, 133, 0.8000681505950427),
        (30, 30, -10, 322, 161, 0.8002386504248025),
    ]
] + [
    # margin = 10 to 20 by 1, treatment_std = 40, reference_std = 30, ratio = 2, alternative = "less", alpha = 0.025, power = 0.80, dist = "z", equal_var = False
    TestCase(
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
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
    for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
        (30, 30, 10, 268, 134, 0.8016665080686909),
        (30, 30, 11, 222, 111, 0.802569358646247),
        (30, 30, 12, 186, 93, 0.8014329406863088),
        (30, 30, 13, 158, 79, 0.8002322052181623),
        (30, 30, 14, 138, 69, 0.8052567878041874),
        (30, 30, 15, 120, 60, 0.8045662820153905),
        (30, 30, 16, 106, 53, 0.8065172728953574),
        (30, 30, 17, 94, 47, 0.8069453779356434),
        (30, 30, 18, 84, 42, 0.8076570764100186),
        (30, 30, 19, 74, 37, 0.800408310122521),
        (30, 30, 20, 68, 34, 0.8074295788138209),
    ]
]

case_group_t_equal_var = [
    # margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alternative = "greater", alpha = 0.025, power = 0.80, dist = "t", equal_var = True
    TestCase(
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
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
] + [
    # margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, ratio = 0.5, alternative = "less", alpha = 0.025, power = 0.80, dist = "t", equal_var = True
    TestCase(
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
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

# The non-inferior module of pass 15 does not support Welch's approx t-test. The test cases here are verified by AI.
case_group_t_unequal_var_welch = [
    # margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alternative = "greater", alpha = 0.025, power = 0.80, dist = "t", equal_var = False, approx_t_method = "welch"
    TestCase(
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
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
    for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
        (10, 10, -20, 97, 49, 0.8064474375940522),
        (10, 10, -19, 107, 54, 0.8051800073169824),
        (10, 10, -18, 119, 60, 0.8049224505515407),
        (10, 10, -17, 133, 67, 0.8041499210960346),
        (10, 10, -16, 149, 75, 0.8015579748384355),
        (10, 10, -15, 169, 85, 0.8007237508501055),
        (10, 10, -14, 195, 98, 0.8031086712596027),
        (10, 10, -13, 225, 113, 0.8014449273348606),
        (10, 10, -12, 263, 132, 0.800180818740927),
        (10, 10, -11, 313, 157, 0.8004892311377916),
        (10, 10, -10, 379, 190, 0.8010412332082162),
    ]
] + [
    # margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alternative = "less", alpha = 0.025, power = 0.80, dist = "t", equal_var = False, approx_t_method = "welch"
    TestCase(
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
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
    for treatment_mean, reference_mean, margin, treatment_size, reference_size, actual_power in [
        (30, 30, 10, 379, 190, 0.8010412332082162),
        (30, 30, 11, 313, 157, 0.8004892311377914),
        (30, 30, 12, 263, 132, 0.800180818740927),
        (30, 30, 13, 225, 113, 0.8014449273348604),
        (30, 30, 14, 195, 98, 0.8031086712596027),
        (30, 30, 15, 169, 85, 0.8007237508501055),
        (30, 30, 16, 149, 75, 0.8015579748384355),
        (30, 30, 17, 133, 67, 0.8041499210960347),
        (30, 30, 18, 119, 60, 0.8049224505515405),
        (30, 30, 19, 107, 54, 0.8051800073169819),
        (30, 30, 20, 97, 49, 0.806447437594052),
    ]
]

case_group_t_unequal_var_satterthwaite = [
    # margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alternative = "greater", alpha = 0.025, power = 0.80, dist = "t", equal_var = False, approx_t_method = "satterthwaite"
    TestCase(
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
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
] + [
    # margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, ratio = 2, alternative = "less", alpha = 0.025, power = 0.80, dist = "t", equal_var = False, approx_t_method = "satterthwaite"
    TestCase(
        treatment_mean=treatment_mean,
        reference_mean=reference_mean,
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


case_group = case_group_z_equal_var + case_group_z_unequal_var + case_group_t_equal_var + case_group_t_unequal_var_welch + case_group_t_unequal_var_satterthwaite


def test_verify_mean_and_get_diff() -> None:
    with pytest.raises(ValueError):
        _verify_mean_and_get_diff(diff=None, treatment_mean=None, reference_mean=None)

    _verify_mean_and_get_diff(diff=None, treatment_mean=20, reference_mean=10)


def test_verify_std_and_get_std() -> None:
    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=None, dist="z", equal_var=True)
    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=10, reference_std=20, dist="z", equal_var=True)

    _verify_std_and_get_std(std=None, treatment_std=10, reference_std=None, dist="z", equal_var=True)
    _verify_std_and_get_std(std=None, treatment_std=None, reference_std=20, dist="z", equal_var=True)

    # dist = "z" and equal_var = False
    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=None, dist="z", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=10, reference_std=None, dist="z", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=10, dist="z", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=10, treatment_std=None, reference_std=None, dist="z", equal_var=False)

    # dist = "t" and equal_var = True
    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=None, dist="t", equal_var=True)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=10, reference_std=None, dist="t", equal_var=True)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=10, dist="t", equal_var=True)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=10, treatment_std=None, reference_std=None, dist="t", equal_var=True)

    # dist = "t" and equal_var = False
    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=None, dist="t", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=10, reference_std=None, dist="t", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=10, dist="t", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=10, treatment_std=None, reference_std=None, dist="t", equal_var=False)


def test_solve_power(case: TestCase) -> None:
    assert round(
        solve_power(
            treatment_mean=case.treatment_mean,
            reference_mean=case.reference_mean,
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


def test_solve_size(case: TestCase) -> None:
    if case in [
        TestCase(treatment_mean=10, reference_mean=10, margin=-17, treatment_std=40, reference_std=40, treatment_size=131, reference_size=66, alternative="greater", alpha=0.025, power=0.8, actual_power=0.8, dist="t", equal_var=True),
        TestCase(treatment_mean=10, reference_mean=10, margin=-12, treatment_std=40, reference_std=40, treatment_size=263, reference_size=132, alternative="greater", alpha=0.025, power=0.8, actual_power=0.8011, dist="t", equal_var=True),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-12,
            treatment_std=40,
            reference_std=40,
            treatment_size=263,
            reference_size=132,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8002,
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        ),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-12,
            treatment_std=40,
            reference_std=40,
            treatment_size=263,
            reference_size=132,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8002,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-17,
            treatment_std=40,
            reference_std=40,
            treatment_size=133,
            reference_size=67,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8041,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
        TestCase(
            treatment_mean=30,
            reference_mean=30,
            margin=-12,
            treatment_std=40,
            reference_std=40,
            treatment_size=263,
            reference_size=132,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8002,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    ratio = case.treatment_size / case.reference_size
    assert solve_size(
        treatment_mean=case.treatment_mean,
        reference_mean=case.reference_mean,
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


def test_solve_treatment_mean(case: TestCase) -> None:
    if case in [
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-15,
            treatment_std=40,
            reference_std=40,
            treatment_size=169,
            reference_size=85,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8007237508501055,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-15,
            treatment_std=40,
            reference_std=40,
            treatment_size=169,
            reference_size=85,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8007,
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        ),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

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


def test_solve_reference_mean(case: TestCase) -> None:
    if case in [
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-15,
            treatment_std=40,
            reference_std=40,
            treatment_size=169,
            reference_size=85,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8007237508501055,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-15,
            treatment_std=40,
            reference_std=40,
            treatment_size=169,
            reference_size=85,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8007,
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        ),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

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


def test_solve_diff(case: TestCase) -> None:
    if case in [
        TestCase(treatment_mean=10, reference_mean=10, margin=-14, treatment_std=40, reference_std=40, treatment_size=193, reference_size=97, alternative="greater", alpha=0.025, power=0.8, actual_power=0.8003, dist="t", equal_var=True),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-15,
            treatment_std=40,
            reference_std=40,
            treatment_size=169,
            reference_size=85,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8007237508501055,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-14,
            treatment_std=40,
            reference_std=40,
            treatment_size=195,
            reference_size=98,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8031,
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        ),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-15,
            treatment_std=40,
            reference_std=40,
            treatment_size=169,
            reference_size=85,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8007,
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        ),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

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


def test_solve_margin(case: TestCase) -> None:

    if case in [
        TestCase(treatment_mean=10, reference_mean=10, margin=-14, treatment_std=40, reference_std=40, treatment_size=193, reference_size=97, alternative="greater", alpha=0.025, power=0.8, actual_power=0.8003, dist="t", equal_var=True),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-15,
            treatment_std=40,
            reference_std=40,
            treatment_size=169,
            reference_size=85,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8007237508501055,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-14,
            treatment_std=40,
            reference_std=40,
            treatment_size=195,
            reference_size=98,
            alternative="less",
            alpha=0.025,
            power=0.8,
            actual_power=0.8031,
            dist="t",
            equal_var=False,
            approx_t_method="welch",
        ),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-15,
            treatment_std=40,
            reference_std=40,
            treatment_size=169,
            reference_size=85,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            actual_power=0.8007,
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        ),
        TestCase(
            treatment_mean=10,
            reference_mean=10,
            margin=-14,
            treatment_std=40,
            reference_std=40,
            treatment_size=195,
            reference_size=98,
            alternative="less",
            alpha=0.025,
            power=0.8,
            actual_power=0.8031,
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        ),
    ]:
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    assert (
        round(
            solve_margin(
                treatment_mean=case.treatment_mean,
                reference_mean=case.reference_mean,
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
