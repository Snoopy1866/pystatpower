# Validation Software: PASS 15
# Module: Confidence Intervals for the Difference Between Two Means

from dataclasses import dataclass
from typing import Literal

import pytest

from tests.models import BaseTestCase


@dataclass
class TestCase(BaseTestCase):
    treatment_std: float
    reference_std: float
    treatment_size: int
    reference_size: int
    interval_type: Literal["two-sided", "lower", "upper"]
    conf_level: float
    equal_var: bool
    precision: float
    actual_precision: float


case_group_equal_var = [
    # treatment_std = 5 to 95 by 5, reference_std = treatment_std, interval_type = "two-sided", conf_level = 0.95, equal_var = True
    TestCase(
        treatment_std=treatment_std,
        reference_std=reference_std,
        treatment_size=treatment_size,
        reference_size=reference_size,
        interval_type="two-sided",
        conf_level=0.95,
        equal_var=True,
        precision=precision,
        actual_precision=actual_precision,
    )
    for treatment_std, reference_std, treatment_size, reference_size, precision, actual_precision in [
        (5, 5, 13, 7, 5, 4.924637221),
        (10, 10, 48, 24, 5, 4.986092779),
        (15, 15, 105, 53, 5, 4.992493813),
        (20, 20, 187, 94, 5, 4.977766659),
        (25, 25, 290, 145, 5, 4.997644398),
        (30, 30, 415, 208, 5, 4.995254886),
        (35, 35, 565, 283, 5, 4.995703100),
        (40, 40, 737, 369, 5, 4.999639825),
        (45, 45, 933, 467, 5, 4.999486045),
        (50, 50, 1153, 577, 5, 4.997336416),
        (55, 55, 1395, 698, 5, 4.997819642),
        (60, 60, 1659, 830, 5, 4.999764522),
        (65, 65, 1947, 974, 5, 4.999939760),
        (70, 70, 2259, 1130, 5, 4.999016593),
        (75, 75, 2593, 1297, 5, 4.999342705),
        (80, 80, 2951, 1476, 5, 4.998791878),
        (85, 85, 3331, 1666, 5, 4.999158157),
        (90, 90, 3734, 1867, 5, 4.999931691),
        (95, 95, 4161, 2081, 5, 4.999178921),
    ]
]

case_group_unequal_var = [
    # treatment_std = 5 to 95 by 5, reference_std = treatment_std, interval_type = "two-sided", conf_level = 0.95, equal_var = True
    TestCase(
        treatment_std=treatment_std,
        reference_std=reference_std,
        treatment_size=treatment_size,
        reference_size=reference_size,
        interval_type="two-sided",
        conf_level=0.95,
        equal_var=True,
        precision=precision,
        actual_precision=actual_precision,
    )
    for treatment_std, reference_std, treatment_size, reference_size, precision, actual_precision in [
        (5, 5, 15, 8, 5, 4.682452713),
        (10, 10, 49, 25, 5, 4.940610507),
        (15, 15, 107, 54, 5, 4.963970980),
        (20, 20, 187, 94, 5, 4.988555116),
        (25, 25, 291, 146, 5, 4.990216430),
        (30, 30, 417, 209, 5, 4.997805644),
        (35, 35, 567, 284, 5, 4.997573217),
        (40, 40, 737, 369, 5, 4.999639825),
        (45, 45, 933, 467, 5, 4.999486045),
        (50, 50, 1153, 577, 5, 4.997336416),
        (55, 55, 1395, 698, 5, 4.997819642),
        (60, 60, 1659, 830, 5, 4.999764522),
        (65, 65, 1947, 974, 5, 4.999939760),
        (70, 70, 2259, 1130, 5, 4.999016593),
        (75, 75, 2593, 1297, 5, 4.999342705),
        (80, 80, 2951, 1476, 5, 4.998791878),
        (85, 85, 3331, 1666, 5, 4.999158157),
        (90, 90, 3734, 1867, 5, 4.999931691),
        (95, 95, 4161, 2081, 5, 4.999178921),
    ]
]

case_group = case_group_equal_var + case_group_unequal_var


def test_solve_distance(case: TestCase) -> None:
    pytest.skip(reason="There may be issues with the PASS calculation results, so the test is temporarily skipped")

    # assert (
    #     round(
    #         solve_precision(
    #             treatment_std=case.treatment_std,
    #             reference_std=case.reference_std,
    #             treatment_size=case.treatment_size,
    #             reference_size=case.reference_size,
    #             conf_level=case.conf_level,
    #             interval_type=case.interval_type,
    #             equal_var=case.equal_var,
    #         ),
    #         9,
    #     )
    #     == case.actual_precision
    # )


def test_solve_size(case: TestCase) -> None:
    pytest.skip(reason="There may be issues with the PASS calculation results, so the test is temporarily skipped")

    # ratio = case.treatment_size / case.reference_size
    # assert solve_size(
    #     treatment_std=case.treatment_std,
    #     reference_std=case.reference_std,
    #     precision=case.precision,
    #     ratio=ratio,
    #     conf_level=case.conf_level,
    #     interval_type=case.interval_type,
    #     equal_var=case.equal_var,
    # ) == (case.treatment_size, case.reference_size)
