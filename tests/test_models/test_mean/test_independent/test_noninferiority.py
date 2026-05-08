# Validation Software: PASS 15
# Module: Non-Inferiority Tests for the Difference Between Two Means

from dataclasses import dataclass, asdict

import pytest

from pystatpower.models.mean.independent.noninferiority import solve_power


@dataclass
class TestCase:
    treatment_mean: float | None
    reference_mean: float | None
    diff: float | None
    margin: float
    treatment_std: float
    reference_std: float
    treatment_size: int
    reference_size: int
    alpha: float
    power: float
    actual_power: float


case_group = [
    # Regular Test Cases, Ratio = 2, Margin = -0.10, Pooled = True, Continuity Correction = True
    TestCase(
        treatment_mean=None,
        reference_mean=None,
        diff=0,
        margin=-0.05,
        treatment_std=0.1,
        reference_std=0.1,
        treatment_size=51,
        reference_size=51,
        alpha=0.05,
        power=0.80,
        actual_power=0.8059,
    )
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
                diff=case.diff,
                margin=case.margin,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
            ),
            4,
        )
        == case.actual_power
    )
