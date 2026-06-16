# Validation Software: PASS 15
# Module: Non-Inferiority Tests for One Proportion

from dataclasses import dataclass
from typing import Literal

from pystatpower.proportion.single.noninferiority import solve_power, solve_size, solve_null_proportion, solve_proportion, solve_margin

from tests.models import BaseTestCase


@dataclass
class TestCase(BaseTestCase):
    null_proportion: float
    proportion: float
    margin: float
    size: int
    alternative: Literal["lower", "upper"]
    alpha: float
    power: float
    phat: bool
    continuity_correction: bool
    actual_power: float


case_group = (
    [
        # Regular Cases: null_proportion = 0.85, proportion = 0.80 to 0.95 by 0.01, margin = -0.10, alternative = "upper", alpha = 0.025, power = 0.80, phat = False, continuity_correction = False
        TestCase(null_proportion=0.85, proportion=proportion, margin=-0.10, size=size, alternative="upper", alpha=0.025, power=0.80, phat=False, continuity_correction=False, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.80, 563, 0.8007),
            (0.81, 387, 0.8011),
            (0.82, 281, 0.8010),
            (0.83, 213, 0.8020),
            (0.84, 166, 0.8018),
            (0.85, 133, 0.8032),
            (0.86, 108, 0.8020),
            (0.87, 89, 0.8003),
            (0.88, 75, 0.8031),
            (0.89, 64, 0.8071),
            (0.90, 54, 0.8010),
            (0.91, 47, 0.8071),
            (0.92, 41, 0.8117),
            (0.93, 35, 0.8016),
            (0.94, 31, 0.8108),
            (0.95, 27, 0.8090),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.75, proportion = 0.65 to 0.80 by 0.01, margin = 0.10, alternative = "lower", alpha = 0.025, power = 0.80, phat = False, continuity_correction = False
        TestCase(null_proportion=0.75, proportion=proportion, margin=0.10, size=size, alternative="lower", alpha=0.025, power=0.80, phat=False, continuity_correction=False, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.65, 31, 0.8071),
            (0.66, 34, 0.8055),
            (0.67, 38, 0.8082),
            (0.68, 42, 0.8055),
            (0.69, 47, 0.8047),
            (0.70, 53, 0.8039),
            (0.71, 60, 0.8017),
            (0.72, 69, 0.8013),
            (0.73, 81, 0.8041),
            (0.74, 95, 0.8020),
            (0.75, 114, 0.8022),
            (0.76, 139, 0.8012),
            (0.77, 174, 0.8008),
            (0.78, 225, 0.8010),
            (0.79, 302, 0.8000),
            (0.80, 430, 0.8002),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.85, proportion = 0.80 to 0.95 by 0.01, margin = -0.10, alternative = "upper", alpha = 0.025, power = 0.80, phat = False, continuity_correction = True
        TestCase(null_proportion=0.85, proportion=proportion, margin=-0.10, size=size, alternative="upper", alpha=0.025, power=0.80, phat=False, continuity_correction=True, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.80, 582, 0.8001),
            (0.81, 403, 0.8005),
            (0.82, 295, 0.8008),
            (0.83, 225, 0.8014),
            (0.84, 177, 0.8019),
            (0.85, 142, 0.8004),
            (0.86, 117, 0.8023),
            (0.87, 98, 0.8047),
            (0.88, 83, 0.8062),
            (0.89, 71, 0.8073),
            (0.90, 61, 0.8059),
            (0.91, 53, 0.8064),
            (0.92, 46, 0.8023),
            (0.93, 41, 0.8119),
            (0.94, 36, 0.8094),
            (0.95, 32, 0.8137),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.75, proportion = 0.65 to 0.80 by 0.01, margin = 0.10, alternative = "lower", alpha = 0.025, power = 0.80, phat = False, continuity_correction = True
        TestCase(null_proportion=0.75, proportion=proportion, margin=0.10, size=size, alternative="lower", alpha=0.025, power=0.80, phat=False, continuity_correction=True, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.65, 36, 0.8089),
            (0.66, 39, 0.8047),
            (0.67, 43, 0.8050),
            (0.68, 47, 0.8001),
            (0.69, 53, 0.8042),
            (0.70, 59, 0.8009),
            (0.71, 67, 0.8019),
            (0.72, 77, 0.8037),
            (0.73, 89, 0.8035),
            (0.74, 104, 0.8024),
            (0.75, 124, 0.8028),
            (0.76, 150, 0.8014),
            (0.77, 186, 0.8002),
            (0.78, 239, 0.8009),
            (0.79, 319, 0.8007),
            (0.80, 450, 0.8004),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.85, proportion = 0.80 to 0.95 by 0.01, margin = -0.10, alternative = "upper", alpha = 0.025, power = 0.80, phat = True, continuity_correction = False
        TestCase(null_proportion=0.85, proportion=proportion, margin=-0.10, size=size, alternative="upper", alpha=0.025, power=0.80, phat=True, continuity_correction=False, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.80, 503, 0.8005),
            (0.81, 336, 0.8005),
            (0.82, 237, 0.8009),
            (0.83, 174, 0.8022),
            (0.84, 131, 0.8023),
            (0.85, 101, 0.8036),
            (0.86, 79, 0.8045),
            (0.87, 62, 0.8022),
            (0.88, 50, 0.8075),
            (0.89, 40, 0.8078),
            (0.90, 32, 0.8074),
            (0.91, 26, 0.8135),
            (0.92, 20, 0.8002),
            (0.93, 16, 0.8056),
            (0.94, 13, 0.8224),
            (0.95, 10, 0.8269),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.75, proportion = 0.65 to 0.80 by 0.01, margin = 0.10, alternative = "lower", alpha = 0.025, power = 0.80, phat = True, continuity_correction = False
        TestCase(null_proportion=0.75, proportion=proportion, margin=0.10, size=size, alternative="lower", alpha=0.025, power=0.80, phat=True, continuity_correction=False, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.65, 45, 0.8031),
            (0.66, 49, 0.8017),
            (0.67, 54, 0.8032),
            (0.68, 60, 0.8059),
            (0.69, 66, 0.8025),
            (0.70, 74, 0.8039),
            (0.71, 83, 0.8026),
            (0.72, 94, 0.8015),
            (0.73, 108, 0.8021),
            (0.74, 125, 0.8006),
            (0.75, 148, 0.8022),
            (0.76, 177, 0.8006),
            (0.77, 218, 0.8015),
            (0.78, 275, 0.8002),
            (0.79, 362, 0.8003),
            (0.80, 503, 0.8005),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.85, proportion = 0.80 to 0.95 by 0.01, margin = -0.10, alternative = "upper", alpha = 0.025, power = 0.80, phat = True, continuity_correction = True
        TestCase(null_proportion=0.85, proportion=proportion, margin=-0.10, size=size, alternative="upper", alpha=0.025, power=0.80, phat=True, continuity_correction=True, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.80, 523, 0.8007),
            (0.81, 353, 0.8012),
            (0.82, 251, 0.8008),
            (0.83, 186, 0.8015),
            (0.84, 142, 0.8026),
            (0.85, 110, 0.8006),
            (0.86, 87, 0.8002),
            (0.87, 70, 0.8017),
            (0.88, 57, 0.8041),
            (0.89, 47, 0.8091),
            (0.90, 38, 0.8029),
            (0.91, 32, 0.8143),
            (0.92, 26, 0.8089),
            (0.93, 21, 0.8010),
            (0.94, 18, 0.8259),
            (0.95, 14, 0.8052),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.75, proportion = 0.65 to 0.80 by 0.01, margin = 0.10, alternative = "lower", alpha = 0.025, power = 0.80, phat = True, continuity_correction = True
        TestCase(null_proportion=0.75, proportion=proportion, margin=0.10, size=size, alternative="lower", alpha=0.025, power=0.80, phat=True, continuity_correction=True, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.65, 50, 0.8042),
            (0.66, 54, 0.8006),
            (0.67, 59, 0.8001),
            (0.68, 65, 0.8010),
            (0.69, 72, 0.8018),
            (0.70, 80, 0.8012),
            (0.71, 90, 0.8026),
            (0.72, 102, 0.8034),
            (0.73, 116, 0.8014),
            (0.74, 134, 0.8008),
            (0.75, 158, 0.8026),
            (0.76, 188, 0.8007),
            (0.77, 230, 0.8009),
            (0.78, 289, 0.8000),
            (0.79, 379, 0.8009),
            (0.80, 523, 0.8007),
        ]
    ]
)


def test_size_solve_power(case: TestCase) -> None:
    assert (
        round(
            solve_power(
                null_proportion=case.null_proportion,
                proportion=case.proportion,
                margin=case.margin,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                phat=case.phat,
                continuity_correction=case.continuity_correction,
            ),
            4,
        )
        == case.actual_power
    )


def test_solve_size(case: TestCase) -> None:
    assert (
        solve_size(
            null_proportion=case.null_proportion,
            proportion=case.proportion,
            margin=case.margin,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.power,
            phat=case.phat,
            continuity_correction=case.continuity_correction,
        )
        == case.size
    )


def test_size_solve_null_proportion(case: TestCase) -> None:
    assert (
        round(
            solve_null_proportion(
                proportion=case.proportion,
                margin=case.margin,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                phat=case.phat,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.null_proportion
    )


def test_size_solve_proportion(case: TestCase) -> None:
    assert (
        round(
            solve_proportion(
                null_proportion=case.null_proportion,
                margin=case.margin,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                phat=case.phat,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.proportion
    )


def test_solve_margin(case: TestCase) -> None:
    assert (
        round(
            solve_margin(
                null_proportion=case.null_proportion,
                proportion=case.proportion,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                phat=case.phat,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.margin
    )
