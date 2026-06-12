# Validation Software: PASS 15
# Module: Non-Inferiority Tests for One Proportion

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.proportion.single.superiority import solve_power, solve_size, solve_null_proportion, solve_proportion, solve_margin


@dataclass
class TestCase:
    __test__ = False

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
        # Regular Cases: null_proportion = 0.75, proportion = 0.81 to 0.95 by 0.01, margin = 0.05, alternative = "upper", alpha = 0.025, power = 0.80, phat = False, continuity_correction = False
        TestCase(null_proportion=0.75, proportion=proportion, margin=0.05, size=size, alternative="upper", alpha=0.025, power=0.80, phat=False, continuity_correction=False, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.81, 12414, 0.8000),
            (0.82, 3066, 0.8001),
            (0.83, 1345, 0.8001),
            (0.84, 747, 0.8006),
            (0.85, 471, 0.8005),
            (0.86, 322, 0.8005),
            (0.87, 233, 0.8012),
            (0.88, 175, 0.8007),
            (0.89, 136, 0.8020),
            (0.90, 108, 0.8026),
            (0.91, 87, 0.8011),
            (0.92, 72, 0.8061),
            (0.93, 60, 0.8089),
            (0.94, 50, 0.8071),
            (0.95, 42, 0.8060),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.75, proportion = 0.55 to 0.69 by 0.01, margin = -0.05, alternative = "lower", alpha = 0.025, power = 0.80, phat = False, continuity_correction = False
        TestCase(null_proportion=0.75, proportion=proportion, margin=-0.05, size=size, alternative="lower", alpha=0.025, power=0.80, phat=False, continuity_correction=False, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.55, 78, 0.8044),
            (0.56, 89, 0.8027),
            (0.57, 103, 0.8025),
            (0.58, 120, 0.8006),
            (0.59, 143, 0.8019),
            (0.60, 172, 0.8006),
            (0.61, 212, 0.8010),
            (0.62, 267, 0.8003),
            (0.63, 348, 0.8008),
            (0.64, 471, 0.8000),
            (0.65, 676, 0.8002),
            (0.66, 1052, 0.8003),
            (0.67, 1861, 0.8002),
            (0.68, 4166, 0.8001),
            (0.69, 16575, 0.8000),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.75, proportion = 0.81 to 0.95 by 0.01, margin = 0.05, alternative = "upper", alpha = 0.025, power = 0.80, phat = False, continuity_correction = True
        TestCase(null_proportion=0.75, proportion=proportion, margin=0.05, size=size, alternative="upper", alpha=0.025, power=0.80, phat=False, continuity_correction=True, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.81, 12514, 0.8000),
            (0.82, 3116, 0.8001),
            (0.83, 1378, 0.8000),
            (0.84, 771, 0.8001),
            (0.85, 491, 0.8007),
            (0.86, 339, 0.8012),
            (0.87, 247, 0.8011),
            (0.88, 188, 0.8025),
            (0.89, 147, 0.8023),
            (0.90, 118, 0.8035),
            (0.91, 96, 0.8019),
            (0.92, 80, 0.8052),
            (0.93, 67, 0.8047),
            (0.94, 57, 0.8080),
            (0.95, 49, 0.8140),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.75, proportion = 0.55 to 0.69 by 0.01, margin = -0.05, alternative = "lower", alpha = 0.025, power = 0.80, phat = False, continuity_correction = True
        TestCase(null_proportion=0.75, proportion=proportion, margin=-0.05, size=size, alternative="lower", alpha=0.025, power=0.80, phat=False, continuity_correction=True, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.55, 84, 0.8019),
            (0.56, 96, 0.8027),
            (0.57, 110, 0.8005),
            (0.58, 129, 0.8030),
            (0.59, 152, 0.8020),
            (0.60, 182, 0.8009),
            (0.61, 223, 0.8011),
            (0.62, 280, 0.8012),
            (0.63, 362, 0.8006),
            (0.64, 488, 0.8004),
            (0.65, 696, 0.8003),
            (0.66, 1076, 0.8000),
            (0.67, 1894, 0.8001),
            (0.68, 4216, 0.8001),
            (0.69, 16675, 0.8000),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.75, proportion = 0.81 to 0.95 by 0.01, margin = 0.05, alternative = "upper", alpha = 0.025, power = 0.80, phat = True, continuity_correction = False
        TestCase(null_proportion=0.75, proportion=proportion, margin=0.05, size=size, alternative="upper", alpha=0.025, power=0.80, phat=True, continuity_correction=False, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.81, 12080, 0.8000),
            (0.82, 2897, 0.8001),
            (0.83, 1231, 0.8001),
            (0.84, 660, 0.8004),
            (0.85, 401, 0.8007),
            (0.86, 263, 0.8007),
            (0.87, 182, 0.8018),
            (0.88, 130, 0.8015),
            (0.89, 95, 0.8006),
            (0.90, 71, 0.8020),
            (0.91, 54, 0.8064),
            (0.92, 41, 0.8085),
            (0.93, 31, 0.8097),
            (0.94, 23, 0.8071),
            (0.95, 17, 0.8100),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.75, proportion = 0.55 to 0.69 by 0.01, margin = -0.05, alternative = "lower", alpha = 0.025, power = 0.80, phat = True, continuity_correction = False
        TestCase(null_proportion=0.75, proportion=proportion, margin=-0.05, size=size, alternative="lower", alpha=0.025, power=0.80, phat=True, continuity_correction=False, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.55, 87, 0.8030),
            (0.56, 99, 0.8013),
            (0.57, 114, 0.8006),
            (0.58, 133, 0.8007),
            (0.59, 157, 0.8002),
            (0.60, 189, 0.8013),
            (0.61, 231, 0.8008),
            (0.62, 289, 0.8001),
            (0.63, 374, 0.8006),
            (0.64, 503, 0.8005),
            (0.65, 715, 0.8004),
            (0.66, 1101, 0.8001),
            (0.67, 1929, 0.8002),
            (0.68, 4270, 0.8000),
            (0.69, 16789, 0.8000),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.75, proportion = 0.81 to 0.95 by 0.01, margin = 0.05, alternative = "upper", alpha = 0.025, power = 0.80, phat = True, continuity_correction = True
        TestCase(null_proportion=0.75, proportion=proportion, margin=0.05, size=size, alternative="upper", alpha=0.025, power=0.80, phat=True, continuity_correction=True, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.81, 12180, 0.8000),
            (0.82, 2947, 0.8001),
            (0.83, 1264, 0.8001),
            (0.84, 685, 0.8005),
            (0.85, 421, 0.8009),
            (0.86, 279, 0.8001),
            (0.87, 196, 0.8017),
            (0.88, 142, 0.8008),
            (0.89, 106, 0.8013),
            (0.90, 81, 0.8037),
            (0.91, 62, 0.8009),
            (0.92, 49, 0.8087),
            (0.93, 38, 0.8059),
            (0.94, 30, 0.8118),
            (0.95, 23, 0.8058),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.75, proportion = 0.55 to 0.69 by 0.01, margin = -0.05, alternative = "lower", alpha = 0.025, power = 0.80, phat = True, continuity_correction = True
        TestCase(null_proportion=0.75, proportion=proportion, margin=-0.05, size=size, alternative="lower", alpha=0.025, power=0.80, phat=True, continuity_correction=True, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.55, 93, 0.8005),
            (0.56, 106, 0.8012),
            (0.57, 122, 0.8020),
            (0.58, 141, 0.8000),
            (0.59, 166, 0.8003),
            (0.60, 199, 0.8016),
            (0.61, 242, 0.8008),
            (0.62, 302, 0.8009),
            (0.63, 388, 0.8005),
            (0.64, 519, 0.8001),
            (0.65, 735, 0.8005),
            (0.66, 1126, 0.8001),
            (0.67, 1962, 0.8001),
            (0.68, 4320, 0.8000),
            (0.69, 16889, 0.8000),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.80, proportion = 0.81 to 0.95 by 0.01, margin = 0, alternative = "upper", alpha = 0.025, power = 0.80, phat = True, continuity_correction = True
        TestCase(null_proportion=0.80, proportion=proportion, margin=0, size=size, alternative="upper", alpha=0.025, power=0.80, phat=True, continuity_correction=True, actual_power=actual_power)
        for proportion, size, actual_power in [
            (0.81, 12180, 0.800025301),
            (0.82, 2947, 0.800132046),
            (0.83, 1264, 0.800113590),
            (0.84, 685, 0.800547902),
            (0.85, 421, 0.800923659),
            (0.86, 279, 0.800120705),
            (0.87, 196, 0.801746057),
            (0.88, 142, 0.800811870),
            (0.89, 106, 0.801299421),
            (0.90, 81, 0.803683133),
            (0.91, 62, 0.800858016),
            (0.92, 49, 0.808676061),
            (0.93, 38, 0.805922940),
            (0.94, 30, 0.811788772),
            (0.95, 23, 0.805763190),
        ]
    ]
)


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


def test_size_solve_power(case: TestCase) -> None:
    assert round(
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
    ) == round(case.actual_power, 4)


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
