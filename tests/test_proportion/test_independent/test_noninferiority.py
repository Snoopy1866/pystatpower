# Validation Software: PASS 15
# Module: Non-Inferiority Tests for the Difference Between Two Proportions

from dataclasses import dataclass
from typing import Literal

from pystatpower.proportion.independent.noninferiority import solve_margin, solve_power, solve_reference_proportion, solve_size, solve_treatment_proportion

from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    treatment_proportion: float
    reference_proportion: float
    margin: float
    treatment_size: int
    reference_size: int
    alternative: Literal["greater", "less"]
    alpha: float
    method: Literal["z-pooled", "z-unpooled"]
    continuity_correction: bool
    power: float
    actual_power: float

    ratio: float | None = None

    def __post_init__(self) -> None:
        if self.ratio is None:
            self.ratio = self.treatment_size / self.reference_size


case_group_pooled = [
    # treatment_proportion = 0.90, reference_proportion = 0.80 to 0.95 by 0.01, margin = -0.10, ratio = 0.5, alternative = "greater", method = "z-pooled", continuity_correction = False
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        margin=-0.10,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="greater",
        alpha=0.025,
        power=0.8,
        method="z-pooled",
        continuity_correction=False,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.90, 0.80, 39, 78, 0.8049820843998110),
        (0.90, 0.81, 42, 84, 0.8050564038595800),
        (0.90, 0.82, 45, 90, 0.8013456759505820),
        (0.90, 0.83, 49, 98, 0.8024754302919810),
        (0.90, 0.84, 54, 108, 0.8063898455208470),
        (0.90, 0.85, 59, 118, 0.8043732381388180),
        (0.90, 0.86, 65, 130, 0.8029848255672580),
        (0.90, 0.87, 72, 144, 0.8006156286270200),
        (0.90, 0.88, 81, 162, 0.8007523186008060),
        (0.90, 0.89, 92, 184, 0.8002747336803840),
        (0.90, 0.90, 106, 212, 0.8001484543772640),
        (0.90, 0.91, 125, 250, 0.8026068195174530),
        (0.90, 0.92, 149, 298, 0.8011561265689470),
        (0.90, 0.93, 183, 366, 0.8008686167146070),
        (0.90, 0.94, 233, 466, 0.8006111957874470),
        (0.90, 0.95, 312, 624, 0.8004520221918940),
    ]
] + [
    # treatment_proportion = 0.85, reference_proportion = 0.80 to 0.95 by 0.01, margin = 0.10, ratio = 2, alternative = "less", method = "z-pooled", continuity_correction = False
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        margin=0.10,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="less",
        alpha=0.025,
        power=0.8,
        method="z-pooled",
        continuity_correction=False,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.85, 0.80, 1337, 669, 0.8002232390669280),
        (0.85, 0.81, 911, 456, 0.8005910236723990),
        (0.85, 0.82, 655, 328, 0.8002918967544500),
        (0.85, 0.83, 491, 246, 0.8005315294668470),
        (0.85, 0.84, 379, 190, 0.8002936509587790),
        (0.85, 0.85, 301, 151, 0.8018816085955260),
        (0.85, 0.86, 243, 122, 0.8024633130131380),
        (0.85, 0.87, 199, 100, 0.8026160671010640),
        (0.85, 0.88, 165, 83, 0.8026725051995730),
        (0.85, 0.89, 138, 69, 0.8000018241051730),
        (0.85, 0.90, 117, 59, 0.8033087703682490),
        (0.85, 0.91, 99, 50, 0.8008626197825510),
        (0.85, 0.92, 85, 43, 0.8019092817547240),
        (0.85, 0.93, 73, 37, 0.8010256795952380),
        (0.85, 0.94, 63, 32, 0.8004991063097440),
        (0.85, 0.95, 55, 28, 0.8036124868815580),
    ]
]

case_group_pooled_cc = [
    # treatment_proportion = 0.90, reference_proportion = 0.80 to 0.95 by 0.01, margin = -0.10, ratio = 0.5, alternative = "greater", method = "z-pooled", continuity_correction = True
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        margin=-0.10,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="greater",
        alpha=0.025,
        power=0.8,
        method="z-pooled",
        continuity_correction=True,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.90, 0.80, 46, 92, 0.8028921855482220),
        (0.90, 0.81, 50, 100, 0.8091427679513060),
        (0.90, 0.82, 53, 106, 0.8012923822190090),
        (0.90, 0.83, 58, 116, 0.8067477538619360),
        (0.90, 0.84, 63, 126, 0.8061920693770740),
        (0.90, 0.85, 69, 138, 0.8068521955417800),
        (0.90, 0.86, 75, 150, 0.8009144376861430),
        (0.90, 0.87, 84, 168, 0.8053633042548020),
        (0.90, 0.88, 93, 186, 0.8003578898271080),
        (0.90, 0.89, 106, 212, 0.8037012732678170),
        (0.90, 0.90, 121, 242, 0.8018615923454540),
        (0.90, 0.91, 141, 282, 0.8020681682044450),
        (0.90, 0.92, 167, 334, 0.8005810646019530),
        (0.90, 0.93, 204, 408, 0.8011453033897280),
        (0.90, 0.94, 258, 516, 0.8015766185154820),
        (0.90, 0.95, 341, 682, 0.8000525576497800),
    ]
] + [
    # treatment_proportion = 0.85, reference_proportion = 0.80 to 0.95 by 0.01, margin = 0.10, ratio = 2, alternative = "less", method = "z-pooled", continuity_correction = True
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        margin=0.10,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="less",
        alpha=0.025,
        power=0.8,
        method="z-pooled",
        continuity_correction=True,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.85, 0.80, 1397, 699, 0.8004075246986670),
        (0.85, 0.81, 959, 480, 0.8000230747151290),
        (0.85, 0.82, 697, 349, 0.8001753541426380),
        (0.85, 0.83, 528, 264, 0.8001443815201760),
        (0.85, 0.84, 413, 207, 0.8016632500612320),
        (0.85, 0.85, 329, 165, 0.8001682538929360),
        (0.85, 0.86, 269, 135, 0.8015199572519210),
        (0.85, 0.87, 223, 112, 0.8020157112299060),
        (0.85, 0.88, 187, 94, 0.8017813955517890),
        (0.85, 0.89, 159, 80, 0.8028416348528750),
        (0.85, 0.90, 137, 69, 0.8057924774091910),
        (0.85, 0.91, 117, 59, 0.8008306220758370),
        (0.85, 0.92, 103, 52, 0.8071989876506560),
        (0.85, 0.93, 89, 45, 0.8016027062009700),
        (0.85, 0.94, 79, 40, 0.8070738020252170),
        (0.85, 0.95, 69, 35, 0.8020112843072910),
    ]
]

case_group_unpooled = [
    # treatment_proportion = 0.90, reference_proportion = 0.80 to 0.95 by 0.01, margin = -0.10, ratio = 0.5, alternative = "greater", method = "z-unpooled", continuity_correction = False
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        margin=-0.10,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="greater",
        alpha=0.025,
        power=0.8,
        method="z-unpooled",
        continuity_correction=False,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.90, 0.80, 34, 68, 0.8074295787987470),
        (0.90, 0.81, 37, 74, 0.8074585483639640),
        (0.90, 0.82, 40, 80, 0.8031369070188060),
        (0.90, 0.83, 44, 88, 0.8035400680462760),
        (0.90, 0.84, 49, 98, 0.8064428251067260),
        (0.90, 0.85, 54, 108, 0.8026607960442980),
        (0.90, 0.86, 61, 122, 0.8054890887434440),
        (0.90, 0.87, 69, 138, 0.8053406314850040),
        (0.90, 0.88, 78, 156, 0.8008312562282790),
        (0.90, 0.89, 91, 182, 0.8037446332933180),
        (0.90, 0.90, 106, 212, 0.8001484543772630),
        (0.90, 0.91, 127, 254, 0.8003390338429590),
        (0.90, 0.92, 156, 312, 0.8012426708629400),
        (0.90, 0.93, 197, 394, 0.8013901278008480),
        (0.90, 0.94, 258, 516, 0.8004486673638550),
        (0.90, 0.95, 358, 716, 0.8009599523381190),
    ]
] + [
    # treatment_proportion = 0.85, reference_proportion = 0.80 to 0.95 by 0.01, margin = 0.10, ratio = 2, alternative = "less", method = "z-unpooled", continuity_correction = False
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        margin=0.10,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="less",
        alpha=0.025,
        power=0.8,
        method="z-unpooled",
        continuity_correction=False,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.85, 0.80, 1405, 703, 0.8002135696554090),
        (0.85, 0.81, 949, 475, 0.8002669949404440),
        (0.85, 0.82, 677, 339, 0.8003542270776100),
        (0.85, 0.83, 503, 252, 0.8009638323369970),
        (0.85, 0.84, 385, 193, 0.8016931646543130),
        (0.85, 0.85, 301, 151, 0.8018816085955260),
        (0.85, 0.86, 239, 120, 0.8012255195919340),
        (0.85, 0.87, 193, 97, 0.8017231298457590),
        (0.85, 0.88, 157, 79, 0.8007948670054670),
        (0.85, 0.89, 129, 65, 0.8004155672886720),
        (0.85, 0.90, 107, 54, 0.8011490973487050),
        (0.85, 0.91, 89, 45, 0.8010859474720350),
        (0.85, 0.92, 75, 38, 0.8048246762506180),
        (0.85, 0.93, 63, 32, 0.8066478341502140),
        (0.85, 0.94, 53, 27, 0.8089696599028970),
        (0.85, 0.95, 44, 22, 0.8030395064186200),
    ]
]

case_group_unpooled_cc = [
    # treatment_proportion = 0.90, reference_proportion = 0.80 to 0.95 by 0.01, margin = -0.10, ratio = 0.5, alternative = "greater", method = "z-unpooled", continuity_correction = True
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        margin=-0.10,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="greater",
        alpha=0.025,
        power=0.8,
        method="z-unpooled",
        continuity_correction=True,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.90, 0.80, 41, 82, 0.8056355321011060),
        (0.90, 0.81, 44, 88, 0.8017334350191030),
        (0.90, 0.82, 48, 96, 0.8034132209196180),
        (0.90, 0.83, 53, 106, 0.8083055027284310),
        (0.90, 0.84, 58, 116, 0.8064731940770030),
        (0.90, 0.85, 64, 128, 0.8054671530985140),
        (0.90, 0.86, 71, 142, 0.8035064443006650),
        (0.90, 0.87, 80, 160, 0.8046504448272710),
        (0.90, 0.88, 90, 180, 0.8004998041699690),
        (0.90, 0.89, 104, 208, 0.8029324937076820),
        (0.90, 0.90, 121, 242, 0.8018615923454540),
        (0.90, 0.91, 144, 288, 0.8028424832529980),
        (0.90, 0.92, 174, 348, 0.8006275814713440),
        (0.90, 0.93, 218, 436, 0.8015846928673590),
        (0.90, 0.94, 283, 566, 0.8012857472139540),
        (0.90, 0.95, 387, 774, 0.8005017091595150),
    ]
] + [
    # treatment_proportion = 0.85, reference_proportion = 0.80 to 0.95 by 0.01, margin = 0.10, ratio = 0.5, alternative = "less", method = "z-unpooled", continuity_correction = True
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        margin=0.10,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="less",
        alpha=0.025,
        power=0.8,
        method="z-unpooled",
        continuity_correction=True,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.85, 0.80, 1465, 733, 0.8003842082992640),
        (0.85, 0.81, 999, 500, 0.8005240849871690),
        (0.85, 0.82, 719, 360, 0.8002264207209840),
        (0.85, 0.83, 539, 270, 0.8003021663665260),
        (0.85, 0.84, 417, 209, 0.8010137916141240),
        (0.85, 0.85, 329, 165, 0.8001682538929360),
        (0.85, 0.86, 265, 133, 0.8002905857393580),
        (0.85, 0.87, 217, 109, 0.8011591105281060),
        (0.85, 0.88, 180, 90, 0.8008958506729710),
        (0.85, 0.89, 151, 76, 0.8044231633746520),
        (0.85, 0.90, 127, 64, 0.8040266086483350),
        (0.85, 0.91, 107, 54, 0.8014537385068210),
        (0.85, 0.92, 91, 46, 0.8008099650914480),
        (0.85, 0.93, 79, 40, 0.8080950259200550),
        (0.85, 0.94, 67, 34, 0.8029437201784100),
        (0.85, 0.95, 58, 29, 0.8027718620066030),
    ]
]


case_group = case_group_pooled + case_group_pooled_cc + case_group_unpooled + case_group_unpooled_cc


def test_solve_power(case: TestCase) -> None:
    assert round(
        solve_power(
            treatment_proportion=case.treatment_proportion,
            reference_proportion=case.reference_proportion,
            margin=case.margin,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            alternative=case.alternative,
            alpha=case.alpha,
            method=case.method,
            continuity_correction=case.continuity_correction,
        ),
        6,
    ) == round(case.actual_power, 6)


def test_solve_size(case: TestCase) -> None:
    assert solve_size(
        treatment_proportion=case.treatment_proportion,
        reference_proportion=case.reference_proportion,
        margin=case.margin,
        alternative=case.alternative,
        ratio=case.ratio,
        alpha=case.alpha,
        power=case.power,
        method=case.method,
        continuity_correction=case.continuity_correction,
    ) == (case.treatment_size, case.reference_size)


def test_solve_treatment_proportion(case: TestCase) -> None:
    assert (
        round(
            solve_treatment_proportion(
                reference_proportion=case.reference_proportion,
                margin=case.margin,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.treatment_proportion
    )


def test_solve_reference_proportion(case: TestCase) -> None:
    assert (
        round(
            solve_reference_proportion(
                treatment_proportion=case.treatment_proportion,
                margin=case.margin,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.reference_proportion
    )


def test_solve_margin(case: TestCase) -> None:
    assert (
        round(
            solve_margin(
                treatment_proportion=case.treatment_proportion,
                reference_proportion=case.reference_proportion,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.margin
    )
