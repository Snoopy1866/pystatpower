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
    method: Literal["chisq", "chisq_cc", "newcombe_wilson"]
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


case_group_newcombe_wilson = (
    [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "two-sided", method = "newcombe_wilson"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="two-sided",
            method="newcombe_wilson",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 837, 419, 0.10, 0.099926),
            (0.10, 0.50, 901, 451, 0.10, 0.099977),
            (0.15, 0.50, 959, 480, 0.10, 0.099941),
            (0.20, 0.50, 1009, 505, 0.10, 0.099929),
            (0.25, 0.50, 1051, 526, 0.10, 0.099936),
            (0.30, 0.50, 1085, 543, 0.10, 0.099959),
            (0.35, 0.50, 1111, 556, 0.10, 0.099996),
            (0.40, 0.50, 1131, 566, 0.10, 0.099958),
            (0.45, 0.50, 1143, 572, 0.10, 0.099937),
            (0.50, 0.50, 1147, 574, 0.10, 0.099929),
            (0.55, 0.50, 1143, 572, 0.10, 0.099937),
            (0.60, 0.50, 1131, 566, 0.10, 0.099958),
            (0.65, 0.50, 1111, 556, 0.10, 0.099996),
            (0.70, 0.50, 1085, 543, 0.10, 0.099959),
            (0.75, 0.50, 1051, 526, 0.10, 0.099936),
            (0.80, 0.50, 1009, 505, 0.10, 0.099929),
            (0.85, 0.50, 959, 480, 0.10, 0.099941),
            (0.90, 0.50, 901, 451, 0.10, 0.099977),
            (0.95, 0.50, 837, 419, 0.10, 0.099926),
        ]
    ]
    + [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "lower one-sided", method = "newcombe_wilson"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="lower one-sided",
            method="newcombe_wilson",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 137, 69, 0.10, 0.099773),
            (0.10, 0.50, 147, 74, 0.10, 0.099783),
            (0.15, 0.50, 157, 79, 0.10, 0.099765),
            (0.20, 0.50, 167, 84, 0.10, 0.099560),
            (0.25, 0.50, 175, 88, 0.10, 0.099664),
            (0.30, 0.50, 182, 91, 0.10, 0.099930),
            (0.35, 0.50, 188, 94, 0.10, 0.099945),
            (0.40, 0.50, 193, 97, 0.10, 0.099731),
            (0.45, 0.50, 197, 99, 0.10, 0.099629),
            (0.50, 0.50, 199, 100, 0.10, 0.099695),
            (0.55, 0.50, 199, 100, 0.10, 0.099918),
            (0.60, 0.50, 199, 100, 0.10, 0.099803),
            (0.65, 0.50, 197, 99, 0.10, 0.099833),
            (0.70, 0.50, 194, 97, 0.10, 0.099917),
            (0.75, 0.50, 189, 95, 0.10, 0.099788),
            (0.80, 0.50, 183, 92, 0.10, 0.099674),
            (0.85, 0.50, 175, 88, 0.10, 0.099639),
            (0.90, 0.50, 165, 83, 0.10, 0.099629),
            (0.95, 0.50, 153, 77, 0.10, 0.099495),
        ]
    ]
    + [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "upper one-sided", method = "newcombe_wilson"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="upper one-sided",
            method="newcombe_wilson",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 62, 124, 0.10, 0.099262),
            (0.10, 0.50, 72, 144, 0.10, 0.099981),
            (0.15, 0.50, 81, 162, 0.10, 0.099792),
            (0.20, 0.50, 88, 176, 0.10, 0.099821),
            (0.25, 0.50, 94, 188, 0.10, 0.099540),
            (0.30, 0.50, 98, 196, 0.10, 0.099563),
            (0.35, 0.50, 100, 200, 0.10, 0.099868),
            (0.40, 0.50, 101, 202, 0.10, 0.099961),
            (0.45, 0.50, 101, 202, 0.10, 0.099871),
            (0.50, 0.50, 100, 200, 0.10, 0.099612),
            (0.55, 0.50, 97, 194, 0.10, 0.099679),
            (0.60, 0.50, 93, 186, 0.10, 0.099594),
            (0.65, 0.50, 87, 174, 0.10, 0.099898),
            (0.70, 0.50, 81, 162, 0.10, 0.099546),
            (0.75, 0.50, 73, 146, 0.10, 0.099687),
            (0.80, 0.50, 64, 128, 0.10, 0.099889),
            (0.85, 0.50, 55, 110, 0.10, 0.099618),
            (0.90, 0.50, 46, 92, 0.10, 0.099172),
            (0.95, 0.50, 37, 74, 0.10, 0.099858),
        ]
    ]
)


case_group_newcombe_wilson_cc = (
    [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "two-sided", method = "newcombe_wilson_cc"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="two-sided",
            method="newcombe_wilson_cc",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 881, 441, 0.10, 0.099901),
            (0.10, 0.50, 945, 473, 0.10, 0.099980),
            (0.15, 0.50, 1003, 502, 0.10, 0.099951),
            (0.20, 0.50, 1053, 527, 0.10, 0.099938),
            (0.25, 0.50, 1095, 548, 0.10, 0.099941),
            (0.30, 0.50, 1129, 565, 0.10, 0.099959),
            (0.35, 0.50, 1155, 578, 0.10, 0.099991),
            (0.40, 0.50, 1175, 588, 0.10, 0.099952),
            (0.45, 0.50, 1187, 594, 0.10, 0.099929),
            (0.50, 0.50, 1190, 595, 0.10, 0.099993),
            (0.55, 0.50, 1187, 594, 0.10, 0.099929),
            (0.60, 0.50, 1175, 588, 0.10, 0.099952),
            (0.65, 0.50, 1155, 578, 0.10, 0.099991),
            (0.70, 0.50, 1129, 565, 0.10, 0.099959),
            (0.75, 0.50, 1095, 548, 0.10, 0.099941),
            (0.80, 0.50, 1053, 527, 0.10, 0.099938),
            (0.85, 0.50, 1003, 502, 0.10, 0.099951),
            (0.90, 0.50, 945, 473, 0.10, 0.099980),
            (0.95, 0.50, 881, 441, 0.10, 0.099901),
        ]
    ]
    + [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "lower one-sided", method = "newcombe_wilson_cc"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="lower one-sided",
            method="newcombe_wilson_cc",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 159, 80, 0.10, 0.099396),
            (0.10, 0.50, 169, 85, 0.10, 0.099607),
            (0.15, 0.50, 179, 90, 0.10, 0.099670),
            (0.20, 0.50, 188, 94, 0.10, 0.099989),
            (0.25, 0.50, 197, 99, 0.10, 0.099610),
            (0.30, 0.50, 203, 102, 0.10, 0.099924),
            (0.35, 0.50, 209, 105, 0.10, 0.099934),
            (0.40, 0.50, 215, 108, 0.10, 0.099650),
            (0.45, 0.50, 218, 109, 0.10, 0.099937),
            (0.50, 0.50, 220, 110, 0.10, 0.099987),
            (0.55, 0.50, 221, 111, 0.10, 0.099805),
            (0.60, 0.50, 221, 111, 0.10, 0.099692),
            (0.65, 0.50, 219, 110, 0.10, 0.099719),
            (0.70, 0.50, 215, 108, 0.10, 0.099881),
            (0.75, 0.50, 211, 106, 0.10, 0.099682),
            (0.80, 0.50, 205, 103, 0.10, 0.099582),
            (0.85, 0.50, 197, 99, 0.10, 0.099559),
            (0.90, 0.50, 187, 94, 0.10, 0.099562),
            (0.95, 0.50, 175, 88, 0.10, 0.099448),
        ]
    ]
    + [
        # Regular Cases: treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "upper one-sided", method = "newcombe_wilson_cc"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="upper one-sided",
            method="newcombe_wilson_cc",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 72, 144, 0.10, 0.099867),
            (0.10, 0.50, 83, 166, 0.10, 0.099760),
            (0.15, 0.50, 92, 184, 0.10, 0.099640),
            (0.20, 0.50, 99, 198, 0.10, 0.099700),
            (0.25, 0.50, 104, 208, 0.10, 0.099976),
            (0.30, 0.50, 108, 216, 0.10, 0.099983),
            (0.35, 0.50, 111, 222, 0.10, 0.099782),
            (0.40, 0.50, 112, 224, 0.10, 0.099870),
            (0.45, 0.50, 112, 224, 0.10, 0.099780),
            (0.50, 0.50, 110, 220, 0.10, 0.099987),
            (0.55, 0.50, 108, 216, 0.10, 0.099567),
            (0.60, 0.50, 103, 206, 0.10, 0.099942),
            (0.65, 0.50, 98, 196, 0.10, 0.099690),
            (0.70, 0.50, 91, 182, 0.10, 0.099815),
            (0.75, 0.50, 83, 166, 0.10, 0.099848),
            (0.80, 0.50, 74, 148, 0.10, 0.099835),
            (0.85, 0.50, 64, 128, 0.10, 0.099899),
            (0.90, 0.50, 54, 108, 0.10, 0.099547),
            (0.95, 0.50, 44, 88, 0.10, 0.099476),
        ]
    ]
)


case_group = case_group_chisq + case_group_chisq_cc + case_group_newcombe_wilson + case_group_newcombe_wilson_cc


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
