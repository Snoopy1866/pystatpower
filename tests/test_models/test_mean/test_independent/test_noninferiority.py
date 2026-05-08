# Validation Software: PASS 15
# Module: Non-Inferiority Tests for the Difference Between Two Means

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.models.mean.independent.noninferiority import solve_power


@dataclass
class TestCase:
    diff: float
    margin: float
    treatment_std: float
    reference_std: float
    treatment_size: int
    reference_size: int
    alpha: float
    power: float
    actual_power: float
    method: Literal["z", "t"]
    equal_var: bool
    df_adjust: Literal["welch", "satterthwaite"]


case_group = (
    [
        # Reference: Chow, S.C.; Shao, J.; Wang, H. 2003. Sample Size Calculations in Clinical Research. Marcel Dekker. New York.
        TestCase(
            diff=0,
            margin=-0.05,
            treatment_std=0.1,
            reference_std=0.1,
            treatment_size=51,
            reference_size=51,
            alpha=0.05,
            power=0.80,
            actual_power=0.8059,
            method="t",
            equal_var=True,
            df_adjust="welch",
        )
    ]
    + [
        # Reference: Julious, Steven A. 2004. 'Tutorial in Biostatistics. Sample sizes for clinical trials with Normal data.' Statistics in Medicine, 23:1921-1986.
        TestCase(
            diff=0,
            margin=-10,
            treatment_std=40,
            reference_std=40,
            treatment_size=337,
            reference_size=337,
            alpha=0.025,
            power=0.90,
            actual_power=0.8998,
            method="t",
            equal_var=True,
            df_adjust="welch",
        )
    ]
    + [
        # Regular Test Cases: margin = -20 to -10 by 1, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.025, power = 0.80, method = "t", equal_var = True, df_adjust = "welch"
        TestCase(
            diff=0,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=True,
            df_adjust="welch",
        )
        for margin, treatment_size, reference_size, actual_power in [
            (-20, 95, 48, 0.8007),
            (-19, 105, 53, 0.8000),
            (-18, 117, 59, 0.8003),
            (-17, 131, 66, 0.8000),
            (-16, 149, 75, 0.8032),
            (-15, 169, 85, 0.8022),
            (-14, 193, 97, 0.8003),
            (-13, 225, 113, 0.8025),
            (-12, 263, 132, 0.8011),
            (-11, 313, 157, 0.8013),
            (-10, 379, 190, 0.8017),
        ]
    ]
    + [
        # Regular Test Cases: margin = 10 to 20 by 1, treatment_std = 40, reference_std = 40, Ratio = 0.5, alpha = 0.025, power = 0.80, method = "t", equal_var = True, df_adjust = "welch"
        TestCase(
            diff=0,
            margin=margin,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=True,
            df_adjust="welch",
        )
        for margin, treatment_size, reference_size, actual_power in [
            (10, 190, 380, 0.8020),
            (11, 157, 314, 0.8017),
            (12, 132, 264, 0.8016),
            (13, 113, 226, 0.8031),
            (14, 97, 194, 0.8010),
            (15, 85, 170, 0.8029),
            (16, 75, 150, 0.8041),
            (17, 66, 132, 0.8010),
            (18, 59, 118, 0.8014),
            (19, 53, 106, 0.8013),
            (20, 48, 96, 0.8021),
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
                case.diff,
                case.margin,
                case.treatment_std,
                case.reference_std,
                case.treatment_size,
                case.reference_size,
                case.alpha,
                case.method,
                case.equal_var,
                case.df_adjust,
            ),
            4,
        )
        == case.actual_power
    )
