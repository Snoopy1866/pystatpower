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


case_group = (
    [
        # Reference: Chow, S.C.; Shao, J.; Wang, H. 2003. Sample Size Calculations in Clinical Research. Marcel Dekker. New York.
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
    + [
        # Reference: Julious, Steven A. 2004. 'Tutorial in Biostatistics. Sample sizes for clinical trials with Normal data.' Statistics in Medicine, 23:1921-1986.
        TestCase(
            treatment_mean=None,
            reference_mean=None,
            diff=0,
            margin=-10,
            treatment_std=40,
            reference_std=40,
            treatment_size=337,
            reference_size=337,
            alpha=0.025,
            power=0.90,
            actual_power=0.8998,
        )
    ]
    + [
        # Regular Test Cases: margin = -20 to 20 by 1 (exclude 0), treatment_std = 40, reference_std = 40, alpha = 0.025, power = 0.80
        TestCase(
            treatment_mean=None,
            reference_mean=None,
            diff=0,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
        )
        for margin, treatment_size, reference_size, actual_power in [
            (-20, 97, 49, 0.8063),
            (-19, 107, 54, 0.8051),
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
