# Validation Software: PASS 15
# Module: Tests for One Proportions

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.models.proportion.single.inequality import solve_power, solve_size, solve_null_proportion, solve_proportion


@dataclass
class TestCase:
    null_proportion: float
    proportion: float
    size: int
    alternative: Literal["one-sided", "two-sided"]
    alpha: float
    power: float
    phat: bool
    continuity_correction: bool
    actual_power: float
    proportion_selection: Literal["lower", "upper"] | None = None


# null_proportion, proportion, size, alternative, alpha, power, phat, continuity_correction, actual_power
case_group = (
    [
        TestCase(0.80, proportion, size, "two-sided", 0.05, 0.80, True, True, actual_power)
        for proportion, size, actual_power in [
            (0.65, 86, 0.8005),
            (0.66, 97, 0.8006),
            (0.67, 111, 0.8029),
            (0.68, 127, 0.8007),
            (0.69, 148, 0.8008),
            (0.70, 175, 0.8008),
            (0.71, 211, 0.8010),
            (0.72, 260, 0.8007),
            (0.73, 330, 0.8002),
            (0.74, 436, 0.8000),
            (0.75, 609, 0.8003),
            (0.76, 920, 0.8002),
            (0.77, 1578, 0.8001),
            (0.78, 3417, 0.8000),
            (0.79, 13122, 0.8000),
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
        TestCase(0.80, proportion, size, "one-sided", 0.05, 0.80, True, True, actual_power)
        for proportion, size, actual_power in [
            (0.65, 70, 0.8054),
            (0.66, 78, 0.8012),
            (0.67, 89, 0.8025),
            (0.68, 102, 0.8015),
            (0.69, 119, 0.8025),
            (0.70, 140, 0.8009),
            (0.71, 169, 0.8020),
            (0.72, 208, 0.8017),
            (0.73, 263, 0.8003),
            (0.74, 347, 0.8001),
            (0.75, 484, 0.8004),
            (0.76, 730, 0.8002),
            (0.77, 1250, 0.8001),
            (0.78, 2703, 0.8001),
            (0.79, 10357, 0.8000),
            (0.81, 9615, 0.8000),
            (0.82, 2332, 0.8001),
            (0.83, 1003, 0.8002),
            (0.84, 545, 0.8006),
            (0.85, 336, 0.8011),
            (0.86, 224, 0.8015),
            (0.87, 157, 0.8008),
            (0.88, 115, 0.8028),
            (0.89, 86, 0.8024),
            (0.90, 66, 0.8046),
            (0.91, 51, 0.8039),
            (0.92, 40, 0.8055),
            (0.93, 32, 0.8135),
            (0.94, 25, 0.8110),
            (0.95, 20, 0.8212),
        ]
    ]
    + [
        TestCase(0.80, proportion, size, "two-sided", 0.05, 0.80, True, False, actual_power)
        for proportion, size, actual_power in [
            (0.65, 80, 0.8031),
            (0.66, 90, 0.8006),
            (0.67, 103, 0.8012),
            (0.68, 119, 0.8013),
            (0.69, 139, 0.8007),
            (0.70, 165, 0.8004),
            (0.71, 200, 0.8009),
            (0.72, 248, 0.8012),
            (0.73, 316, 0.8004),
            (0.74, 420, 0.8005),
            (0.75, 589, 0.8002),
            (0.76, 895, 0.8001),
            (0.77, 1545, 0.8001),
            (0.78, 3368, 0.8001),
            (0.79, 13022, 0.8000),
            (0.81, 12080, 0.8000),
            (0.82, 2897, 0.8001),
            (0.83, 1231, 0.8002),
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
        TestCase(0.80, proportion, size, "one-sided", 0.05, 0.80, True, False, actual_power)
        for proportion, size, actual_power in [
            (0.65, 63, 0.8027),
            (0.66, 71, 0.8011),
            (0.67, 81, 0.8005),
            (0.68, 94, 0.8021),
            (0.69, 110, 0.8022),
            (0.70, 130, 0.8004),
            (0.71, 158, 0.8019),
            (0.72, 195, 0.8004),
            (0.73, 249, 0.8004),
            (0.74, 331, 0.8006),
            (0.75, 464, 0.8002),
            (0.76, 705, 0.8001),
            (0.77, 1217, 0.8001),
            (0.78, 2653, 0.8001),
            (0.79, 10257, 0.8000),
            (0.81, 9515, 0.8000),
            (0.82, 2282, 0.8001),
            (0.83, 970, 0.8003),
            (0.84, 520, 0.8004),
            (0.85, 316, 0.8008),
            (0.86, 207, 0.8004),
            (0.87, 143, 0.8007),
            (0.88, 103, 0.8033),
            (0.89, 75, 0.8013),
            (0.90, 56, 0.8022),
            (0.91, 42, 0.8013),
            (0.92, 32, 0.8044),
            (0.93, 24, 0.8027),
            (0.94, 18, 0.8041),
            (0.95, 14, 0.8239),
        ]
    ]
    + [
        TestCase(0.80, proportion, size, "two-sided", 0.05, 0.80, False, True, actual_power)
        for proportion, size, actual_power in [
            (0.65, 69, 0.8002),
            (0.66, 79, 0.8032),
            (0.67, 90, 0.8005),
            (0.68, 105, 0.8026),
            (0.69, 123, 0.8010),
            (0.70, 147, 0.8009),
            (0.71, 179, 0.8005),
            (0.72, 224, 0.8013),
            (0.73, 288, 0.8005),
            (0.74, 386, 0.8001),
            (0.75, 548, 0.8005),
            (0.76, 842, 0.8000),
            (0.77, 1473, 0.8001),
            (0.78, 3257, 0.8000),
            (0.79, 12797, 0.8000),
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
        TestCase(0.80, proportion, size, "one-sided", 0.05, 0.80, False, True, actual_power)
        for proportion, size, actual_power in [
            (0.65, 57, 0.8040),
            (0.66, 64, 0.8005),
            (0.67, 74, 0.8038),
            (0.68, 85, 0.8009),
            (0.69, 100, 0.8017),
            (0.70, 119, 0.8009),
            (0.71, 145, 0.8015),
            (0.72, 180, 0.8001),
            (0.73, 232, 0.8011),
            (0.74, 310, 0.8006),
            (0.75, 438, 0.8001),
            (0.76, 672, 0.8002),
            (0.77, 1172, 0.8002),
            (0.78, 2583, 0.8000),
            (0.79, 10115, 0.8000),
            (0.81, 9864, 0.8000),
            (0.82, 2458, 0.8001),
            (0.83, 1088, 0.8002),
            (0.84, 609, 0.8003),
            (0.85, 388, 0.8008),
            (0.86, 268, 0.8014),
            (0.87, 195, 0.8006),
            (0.88, 148, 0.8006),
            (0.89, 116, 0.8015),
            (0.90, 93, 0.8019),
            (0.91, 76, 0.8027),
            (0.92, 63, 0.8033),
            (0.93, 53, 0.8055),
            (0.94, 45, 0.8079),
            (0.95, 38, 0.8028),
        ]
    ]
    + [
        TestCase(0.80, proportion, size, "two-sided", 0.05, 0.80, False, False, actual_power)
        for proportion, size, actual_power in [
            (0.65, 63, 0.8030),
            (0.66, 72, 0.8031),
            (0.67, 83, 0.8028),
            (0.68, 97, 0.8032),
            (0.69, 114, 0.8008),
            (0.70, 137, 0.8005),
            (0.71, 168, 0.8004),
            (0.72, 211, 0.8001),
            (0.73, 274, 0.8007),
            (0.74, 370, 0.8006),
            (0.75, 528, 0.8003),
            (0.76, 818, 0.8004),
            (0.77, 1440, 0.8002),
            (0.78, 3208, 0.8001),
            (0.79, 12697, 0.8000),
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
        TestCase(0.80, proportion, size, "one-sided", 0.05, 0.80, False, False, actual_power)
        for proportion, size, actual_power in [
            (0.65, 50, 0.8008),
            (0.66, 57, 0.8002),
            (0.67, 66, 0.8015),
            (0.68, 77, 0.8015),
            (0.69, 91, 0.8013),
            (0.70, 109, 0.8003),
            (0.71, 134, 0.8012),
            (0.72, 168, 0.8007),
            (0.73, 218, 0.8012),
            (0.74, 294, 0.8011),
            (0.75, 419, 0.8007),
            (0.76, 647, 0.8000),
            (0.77, 1139, 0.8002),
            (0.78, 2534, 0.8001),
            (0.79, 10015, 0.8000),
            (0.81, 9764, 0.8000),
            (0.82, 2408, 0.8001),
            (0.83, 1055, 0.8003),
            (0.84, 584, 0.8001),
            (0.85, 368, 0.8006),
            (0.86, 251, 0.8005),
            (0.87, 181, 0.8006),
            (0.88, 136, 0.8013),
            (0.89, 105, 0.8008),
            (0.90, 83, 0.8006),
            (0.91, 67, 0.8016),
            (0.92, 55, 0.8038),
            (0.93, 46, 0.8098),
            (0.94, 38, 0.8061),
            (0.95, 32, 0.8091),
        ]
    ]
    + [
        TestCase(0.98, 0.90, 37, "one-sided", 0.05, 0.80, False, False, 0.8036),
        TestCase(0.98, 0.90, 43, "two-sided", 0.05, 0.80, False, False, 0.8017),
    ]
)


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


def test_size_solve_power(case: TestCase) -> None:
    assert (
        round(
            solve_power(
                case.null_proportion,
                case.proportion,
                case.size,
                case.alternative,
                case.alpha,
                case.phat,
                case.continuity_correction,
            ),
            4,
        )
        == case.actual_power
    )


def test_solve_size(case: TestCase) -> None:
    assert (
        solve_size(
            case.null_proportion,
            case.proportion,
            case.alternative,
            case.alpha,
            case.power,
            case.phat,
            case.continuity_correction,
        )
        == case.size
    )


def test_size_solve_null_proportion(case: TestCase) -> None:
    case.proportion_selection = "lower" if case.null_proportion < case.proportion else "upper"
    assert (
        round(
            solve_null_proportion(
                case.proportion,
                case.size,
                case.alternative,
                case.alpha,
                case.actual_power,
                case.phat,
                case.continuity_correction,
                case.proportion_selection,
            ),
            2,
        )
        == case.null_proportion
    )


def test_size_solve_proportion(case: TestCase) -> None:
    case.proportion_selection = "lower" if case.proportion < case.null_proportion else "upper"
    assert (
        round(
            solve_proportion(
                case.null_proportion,
                case.size,
                case.alternative,
                case.alpha,
                case.actual_power,
                case.phat,
                case.continuity_correction,
                case.proportion_selection,
            ),
            2,
        )
        == case.proportion
    )
