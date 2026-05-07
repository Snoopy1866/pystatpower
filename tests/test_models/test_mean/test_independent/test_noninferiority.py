# Validation Software: PASS 15
# Module: Non-Inferiority Tests for the Difference Between Two Means

from dataclasses import dataclass, asdict

import pytest

from pystatpower.models.mean.independent.noninferiority import solve_power


@dataclass
class TestCase:
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


case_group = [  # Regular Test Cases, Ratio = 2, Margin = -0.10, Pooled = True, Continuity Correction = True
    TestCase(treatment_mean, reference_mean, margin, treatment_std, reference_std, treatment_size, reference_size, 0.025, 0.80, actual_power)
    for treatment_mean, reference_mean, margin, treatment_std, reference_std, treatment_size, reference_size, actual_power in [
        (2, 2, -0.1, 1, 1, 2355, 1178, 0.8001),
        (2, 2, -1, 1, 1, 25, 13, 0.8121),
        (2, 2, -1, 1, 2, 73, 37, 0.8007),
    ]
]


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
                case.treatment_mean,
                case.reference_mean,
                case.margin,
                case.treatment_std,
                case.reference_std,
                case.treatment_size,
                case.reference_size,
                case.alpha,
            ),
            4,
        )
        == case.actual_power
    )
