# Validation Software: PASS 15
# Module: Superiority by a Margin for the Difference Between Two Proportions

from dataclasses import dataclass, asdict

import pytest

from pystatpower.models.proportion.independent.superiority import solve_power, solve_size


@dataclass
class TestCase:
    treatment_proportion: float
    reference_proportion: float
    margin: float
    treatment_size: int
    reference_size: int
    alpha: float
    power: float
    pooled: bool
    continuity_correction: bool
    actual_power: float


# treatment_proportion, reference_proportion, margin, treatment_size, reference_size, alpha, power, pooled, continuity_correction, actual_power
case_group = (
    [
        TestCase(treatment_proportion, reference_proportion, 0, treatment_size, reference_size, 0.025, 0.80, True, True, actual_power)
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.80, 0.70, 461, 231, 0.8007),
            (0.81, 0.71, 449, 225, 0.8011),
            (0.82, 0.72, 435, 218, 0.8000),
            (0.83, 0.73, 423, 212, 0.8013),
            (0.84, 0.74, 409, 205, 0.8011),
            (0.85, 0.75, 395, 198, 0.8014),
            (0.86, 0.76, 379, 190, 0.8001),
            (0.87, 0.77, 365, 183, 0.8014),
            (0.88, 0.78, 349, 175, 0.8011),
            (0.89, 0.79, 333, 167, 0.8013),
            (0.90, 0.80, 316, 158, 0.8002),
            (0.91, 0.81, 299, 150, 0.8012),
            (0.92, 0.82, 281, 141, 0.8007),
            (0.93, 0.83, 263, 132, 0.8009),
            (0.94, 0.84, 245, 123, 0.8019),
            (0.95, 0.85, 225, 113, 0.8005),
            (0.96, 0.86, 206, 103, 0.8006),
            (0.97, 0.87, 186, 93, 0.8010),
            (0.98, 0.88, 165, 83, 0.8017),
            (0.99, 0.89, 144, 72, 0.8013),
        ]
    ]
    + [
        TestCase(treatment_proportion, reference_proportion, 0, treatment_size, reference_size, 0.025, 0.80, True, False, actual_power)
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.80, 0.70, 431, 216, 0.8003),
            (0.81, 0.71, 419, 210, 0.8006),
            (0.82, 0.72, 407, 204, 0.8014),
            (0.83, 0.73, 393, 197, 0.8007),
            (0.84, 0.74, 379, 190, 0.8005),
            (0.85, 0.75, 365, 183, 0.8008),
            (0.86, 0.76, 351, 176, 0.8016),
            (0.87, 0.77, 335, 168, 0.8007),
            (0.88, 0.78, 319, 160, 0.8003),
            (0.89, 0.79, 303, 152, 0.8005),
            (0.90, 0.80, 287, 144, 0.8013),
            (0.91, 0.81, 269, 135, 0.8001),
            (0.92, 0.82, 252, 126, 0.8001),
            (0.93, 0.83, 234, 117, 0.8002),
            (0.94, 0.84, 215, 108, 0.8004),
            (0.95, 0.85, 197, 99, 0.8022),
            (0.96, 0.86, 177, 89, 0.8015),
            (0.97, 0.87, 157, 79, 0.8017),
            (0.98, 0.88, 137, 69, 0.8032),
            (0.99, 0.89, 115, 58, 0.8010),
        ]
    ]
    + [
        TestCase(treatment_proportion, reference_proportion, 0, treatment_size, reference_size, 0.025, 0.80, False, True, actual_power)
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.80, 0.70, 485, 243, 0.8008),
            (0.81, 0.71, 473, 237, 0.8002),
            (0.82, 0.72, 462, 231, 0.8002),
            (0.83, 0.73, 449, 225, 0.8001),
            (0.84, 0.74, 437, 219, 0.8007),
            (0.85, 0.75, 424, 212, 0.8001),
            (0.86, 0.76, 411, 206, 0.8015),
            (0.87, 0.77, 397, 199, 0.8016),
            (0.88, 0.78, 381, 191, 0.8001),
            (0.89, 0.79, 367, 184, 0.8013),
            (0.90, 0.80, 351, 176, 0.8007),
            (0.91, 0.81, 335, 168, 0.8007),
            (0.92, 0.82, 319, 160, 0.8014),
            (0.93, 0.83, 302, 151, 0.8002),
            (0.94, 0.84, 285, 143, 0.8021),
            (0.95, 0.85, 267, 134, 0.8020),
            (0.96, 0.86, 249, 125, 0.8028),
            (0.97, 0.87, 229, 115, 0.8009),
            (0.98, 0.88, 211, 106, 0.8038),
            (0.99, 0.89, 191, 96, 0.8039),
        ]
    ]
    + [
        TestCase(treatment_proportion, reference_proportion, 0, treatment_size, reference_size, 0.025, 0.80, False, False, actual_power)
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.80, 0.70, 455, 228, 0.8004),
            (0.81, 0.71, 445, 223, 0.8015),
            (0.82, 0.72, 433, 217, 0.8013),
            (0.83, 0.73, 421, 211, 0.8015),
            (0.84, 0.74, 407, 204, 0.8002),
            (0.85, 0.75, 395, 198, 0.8013),
            (0.86, 0.76, 381, 191, 0.8009),
            (0.87, 0.77, 367, 184, 0.8010),
            (0.88, 0.78, 353, 177, 0.8017),
            (0.89, 0.79, 337, 169, 0.8006),
            (0.90, 0.80, 322, 161, 0.8002),
            (0.91, 0.81, 306, 153, 0.8002),
            (0.92, 0.82, 289, 145, 0.8005),
            (0.93, 0.83, 273, 137, 0.8017),
            (0.94, 0.84, 255, 128, 0.8009),
            (0.95, 0.85, 237, 119, 0.8007),
            (0.96, 0.86, 219, 110, 0.8013),
            (0.97, 0.87, 201, 101, 0.8029),
            (0.98, 0.88, 181, 91, 0.8016),
            (0.99, 0.89, 161, 81, 0.8012),
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
    assert (
        round(
            solve_power(
                case.treatment_proportion,
                case.reference_proportion,
                case.margin,
                case.treatment_size,
                case.reference_size,
                case.alpha,
                case.pooled,
                case.continuity_correction,
            ),
            4,
        )
        == case.actual_power
    )


def test_solve_size(case: TestCase) -> None:
    ratio = case.treatment_size / case.reference_size
    assert solve_size(
        case.treatment_proportion,
        case.reference_proportion,
        case.margin,
        ratio,
        case.alpha,
        case.power,
        case.pooled,
        case.continuity_correction,
    ) == (case.treatment_size, case.reference_size)
