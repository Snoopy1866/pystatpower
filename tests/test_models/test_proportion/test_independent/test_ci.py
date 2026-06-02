# Validation Software: PASS 15
# Module: Confidence Intervals for the Difference Between Two Proportions

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.models.proportion.independent.ci import solve_distance


@dataclass
class TestCase:
    __test__ = False

    treatment_proportion: float
    reference_proportion: float
    treatment_size: int
    reference_size: int
    conf_level: float
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"]
    method: Literal["chisq", "chisq_cc"]
    distance: float
    actual_distance: float


case_group_chisq = (
    [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "two-sided", method = "chisq"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="two-sided",
            method="chisq",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 841, 421, 0.10, 0.099962),
            (0.10, 0.50, 907, 454, 0.10, 0.099930),
            (0.15, 0.50, 965, 483, 0.10, 0.099918),
            (0.20, 0.50, 1015, 508, 0.10, 0.099921),
            (0.25, 0.50, 1057, 529, 0.10, 0.099937),
            (0.30, 0.50, 1091, 546, 0.10, 0.099967),
            (0.35, 0.50, 1118, 559, 0.10, 0.099994),
            (0.40, 0.50, 1137, 569, 0.10, 0.099973),
            (0.45, 0.50, 1149, 575, 0.10, 0.099953),
            (0.50, 0.50, 1153, 577, 0.10, 0.099947),
            (0.55, 0.50, 1149, 575, 0.10, 0.099953),
            (0.60, 0.50, 1137, 569, 0.10, 0.099973),
            (0.65, 0.50, 1118, 559, 0.10, 0.099994),
            (0.70, 0.50, 1091, 546, 0.10, 0.099967),
            (0.75, 0.50, 1057, 529, 0.10, 0.099937),
            (0.80, 0.50, 1015, 508, 0.10, 0.099921),
            (0.85, 0.50, 965, 483, 0.10, 0.099918),
            (0.90, 0.50, 907, 454, 0.10, 0.099930),
            (0.95, 0.50, 841, 421, 0.10, 0.099962),
        ]
    ]
    + [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "lower one-sided", method = "chisq"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="lower one-sided",
            method="chisq",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 149, 75, 0.10, 0.099403),
            (0.10, 0.50, 159, 80, 0.10, 0.099931),
            (0.15, 0.50, 169, 85, 0.10, 0.099993),
            (0.20, 0.50, 179, 90, 0.10, 0.099668),
            (0.25, 0.50, 187, 94, 0.10, 0.099541),
            (0.30, 0.50, 193, 97, 0.10, 0.099584),
            (0.35, 0.50, 197, 99, 0.10, 0.099783),
            (0.40, 0.50, 201, 101, 0.10, 0.099636),
            (0.45, 0.50, 203, 102, 0.10, 0.099649),
            (0.50, 0.50, 203, 102, 0.10, 0.099816),
            (0.55, 0.50, 203, 102, 0.10, 0.099649),
            (0.60, 0.50, 201, 101, 0.10, 0.099636),
            (0.65, 0.50, 197, 99, 0.10, 0.099783),
            (0.70, 0.50, 193, 97, 0.10, 0.099584),
            (0.75, 0.50, 187, 94, 0.10, 0.099541),
            (0.80, 0.50, 179, 90, 0.10, 0.099668),
            (0.85, 0.50, 169, 85, 0.10, 0.099993),
            (0.90, 0.50, 159, 80, 0.10, 0.099931),
            (0.95, 0.50, 149, 75, 0.10, 0.099403),
        ]
    ]
    + [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "upper one-sided", method = "chisq"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="upper one-sided",
            method="chisq",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 47, 94, 0.10, 0.099649),
            (0.10, 0.50, 59, 118, 0.10, 0.099293),
            (0.15, 0.50, 69, 138, 0.10, 0.099502),
            (0.20, 0.50, 78, 156, 0.10, 0.099427),
            (0.25, 0.50, 85, 170, 0.10, 0.099734),
            (0.30, 0.50, 91, 182, 0.10, 0.099800),
            (0.35, 0.50, 96, 192, 0.10, 0.099672),
            (0.40, 0.50, 99, 198, 0.10, 0.099875),
            (0.45, 0.50, 101, 202, 0.10, 0.099892),
            (0.50, 0.50, 102, 204, 0.10, 0.099734),
            (0.55, 0.50, 101, 202, 0.10, 0.099892),
            (0.60, 0.50, 99, 198, 0.10, 0.099875),
            (0.65, 0.50, 96, 192, 0.10, 0.099672),
            (0.70, 0.50, 91, 182, 0.10, 0.099800),
            (0.75, 0.50, 85, 170, 0.10, 0.099734),
            (0.80, 0.50, 78, 156, 0.10, 0.099427),
            (0.85, 0.50, 69, 138, 0.10, 0.099502),
            (0.90, 0.50, 59, 118, 0.10, 0.099293),
            (0.95, 0.50, 47, 94, 0.10, 0.099649),
        ]
    ]
)

case_group_chisq_cc = (
    [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "two-sided", method = "chisq_cc"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="two-sided",
            method="chisq_cc",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 901, 451, 0.10, 0.099907),
            (0.10, 0.50, 965, 483, 0.10, 0.099990),
            (0.15, 0.50, 1023, 512, 0.10, 0.099977),
            (0.20, 0.50, 1073, 537, 0.10, 0.099979),
            (0.25, 0.50, 1115, 558, 0.10, 0.099994),
            (0.30, 0.50, 1151, 576, 0.10, 0.099933),
            (0.35, 0.50, 1177, 589, 0.10, 0.099974),
            (0.40, 0.50, 1197, 599, 0.10, 0.099942),
            (0.45, 0.50, 1208, 604, 0.10, 0.099994),
            (0.50, 0.50, 1212, 606, 0.10, 0.099987),
            (0.55, 0.50, 1208, 604, 0.10, 0.099994),
            (0.60, 0.50, 1197, 599, 0.10, 0.099942),
            (0.65, 0.50, 1177, 589, 0.10, 0.099974),
            (0.70, 0.50, 1151, 576, 0.10, 0.099933),
            (0.75, 0.50, 1115, 558, 0.10, 0.099994),
            (0.80, 0.50, 1073, 537, 0.10, 0.099979),
            (0.85, 0.50, 1023, 512, 0.10, 0.099977),
            (0.90, 0.50, 965, 483, 0.10, 0.099990),
            (0.95, 0.50, 901, 451, 0.10, 0.099907),
        ]
    ]
    + [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "lower one-sided", method = "chisq_cc"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="lower one-sided",
            method="chisq_cc",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 177, 89, 0.10, 0.099689),
            (0.10, 0.50, 189, 95, 0.10, 0.099605),
            (0.15, 0.50, 199, 100, 0.10, 0.099693),
            (0.20, 0.50, 207, 104, 0.10, 0.099932),
            (0.25, 0.50, 215, 108, 0.10, 0.099812),
            (0.30, 0.50, 221, 111, 0.10, 0.099850),
            (0.35, 0.50, 226, 113, 0.10, 0.099960),
            (0.40, 0.50, 229, 115, 0.10, 0.099897),
            (0.45, 0.50, 231, 116, 0.10, 0.099908),
            (0.50, 0.50, 232, 116, 0.10, 0.099988),
            (0.55, 0.50, 231, 116, 0.10, 0.099908),
            (0.60, 0.50, 229, 115, 0.10, 0.099897),
            (0.65, 0.50, 226, 113, 0.10, 0.099960),
            (0.70, 0.50, 221, 111, 0.10, 0.099850),
            (0.75, 0.50, 215, 108, 0.10, 0.099812),
            (0.80, 0.50, 207, 104, 0.10, 0.099932),
            (0.85, 0.50, 199, 100, 0.10, 0.099693),
            (0.90, 0.50, 189, 95, 0.10, 0.099605),
            (0.95, 0.50, 177, 89, 0.10, 0.099689),
        ]
    ]
    + [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "upper one-sided", method = "chisq_cc"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="upper one-sided",
            method="chisq_cc",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 61, 122, 0.10, 0.099765),
            (0.10, 0.50, 73, 146, 0.10, 0.099540),
            (0.15, 0.50, 83, 166, 0.10, 0.099759),
            (0.20, 0.50, 92, 184, 0.10, 0.099702),
            (0.25, 0.50, 99, 198, 0.10, 0.099989),
            (0.30, 0.50, 106, 212, 0.10, 0.099545),
            (0.35, 0.50, 110, 220, 0.10, 0.099931),
            (0.40, 0.50, 114, 228, 0.10, 0.099651),
            (0.45, 0.50, 116, 232, 0.10, 0.099675),
            (0.50, 0.50, 116, 232, 0.10, 0.099988),
            (0.55, 0.50, 116, 232, 0.10, 0.099675),
            (0.60, 0.50, 114, 228, 0.10, 0.099651),
            (0.65, 0.50, 110, 220, 0.10, 0.099931),
            (0.70, 0.50, 106, 212, 0.10, 0.099545),
            (0.75, 0.50, 99, 198, 0.10, 0.099989),
            (0.80, 0.50, 92, 184, 0.10, 0.099702),
            (0.85, 0.50, 83, 166, 0.10, 0.099759),
            (0.90, 0.50, 73, 146, 0.10, 0.099540),
            (0.95, 0.50, 61, 122, 0.10, 0.099765),
        ]
    ]
)


case_group = case_group_chisq + case_group_chisq_cc


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


def test_size_solve_distance(case: TestCase) -> None:
    assert (
        round(
            solve_distance(
                treatment_proportion=case.treatment_proportion,
                reference_proportion=case.reference_proportion,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                conf_level=case.conf_level,
                interval_type=case.interval_type,
                method=case.method,
            ),
            6,
        )
        == case.actual_distance
    )
