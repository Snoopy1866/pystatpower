# Validation Software: PASS 15
# Module: Two-Sample Z-Tests Assuming Equal Variance
#         Two-Sample Z-Tests Allowing Unequal Variance
#         Two-Sample T-Tests Assuming Equal Variance
#         Two-Sample T-Tests Assuming Unequal Variance
# Two-Sample T-Test Assuming Unequal Variance with Degree of Freedom Adjusted by Welch's Methos is not available in PASS.

from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.mean.independent.inequality import solve_power, solve_size, solve_diff, solve_treatment_mean, solve_reference_mean, solve_treatment_std, solve_reference_std

from tests.models import BaseTestCase


@dataclass
class TestCase(BaseTestCase):
    treatment_mean: float | None
    reference_mean: float | None
    diff: float | None
    treatment_std: float
    reference_std: float
    treatment_size: int
    reference_size: int
    alternative: Literal["two-sided", "less", "greater"]
    alpha: float
    power: float
    actual_power: float
    method: Literal["z", "t"]
    equal_var: bool
    df_adjust: Literal["welch", "satterthwaite"] | None = None

    def __post_init__(self):
        if self.treatment_mean is not None and self.reference_mean is not None:
            self.diff = self.treatment_mean - self.reference_mean


case_group = (
    [
        # Regular Test Cases: treatment_mean = 0 to 20 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.05, power = 0.80, alternative = "less", method = "z", equal_var = True
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="less",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (0, 30, 33, 17, 0.8071),
            (1, 30, 35, 18, 0.8037),
            (2, 30, 38, 19, 0.8014),
            (3, 30, 41, 21, 0.8080),
            (4, 30, 44, 22, 0.8008),
            (5, 30, 47, 24, 0.8013),
            (6, 30, 51, 26, 0.8010),
            (7, 30, 57, 29, 0.8095),
            (8, 30, 61, 31, 0.8020),
            (9, 30, 67, 34, 0.8019),
            (10, 30, 75, 38, 0.8068),
            (11, 30, 83, 42, 0.8061),
            (12, 30, 91, 46, 0.8003),
            (13, 30, 103, 52, 0.8033),
            (14, 30, 116, 58, 0.8002),
            (15, 30, 132, 66, 0.8003),
            (16, 30, 151, 76, 0.8006),
            (17, 30, 175, 88, 0.8001),
            (18, 30, 207, 104, 0.8027),
            (19, 30, 245, 123, 0.8006),
            (20, 30, 297, 149, 0.8011),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.05, power = 0.80, alternative = "greater", method = "z", equal_var = True
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 297, 149, 0.8011),
            (41, 30, 245, 123, 0.8006),
            (42, 30, 207, 104, 0.8027),
            (43, 30, 175, 88, 0.8001),
            (44, 30, 151, 76, 0.8006),
            (45, 30, 132, 66, 0.8003),
            (46, 30, 116, 58, 0.8002),
            (47, 30, 103, 52, 0.8033),
            (48, 30, 91, 46, 0.8003),
            (49, 30, 83, 42, 0.8061),
            (50, 30, 75, 38, 0.8068),
            (51, 30, 67, 34, 0.8019),
            (52, 30, 61, 31, 0.8020),
            (53, 30, 57, 29, 0.8095),
            (54, 30, 51, 26, 0.8010),
            (55, 30, 47, 24, 0.8013),
            (56, 30, 44, 22, 0.8008),
            (57, 30, 41, 21, 0.8080),
            (58, 30, 38, 19, 0.8014),
            (59, 30, 35, 18, 0.8037),
            (60, 30, 33, 17, 0.8071),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.05, power = 0.80, alternative = "two-sided", method = "z", equal_var = True
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 377, 189, 0.8010),
            (41, 30, 311, 156, 0.8004),
            (42, 30, 261, 131, 0.8001),
            (43, 30, 223, 112, 0.8013),
            (44, 30, 193, 97, 0.8029),
            (45, 30, 167, 84, 0.8005),
            (46, 30, 147, 74, 0.8013),
            (47, 30, 131, 66, 0.8039),
            (48, 30, 117, 59, 0.8046),
            (49, 30, 105, 53, 0.8048),
            (50, 30, 95, 48, 0.8061),
            (51, 30, 85, 43, 0.8011),
            (52, 30, 78, 39, 0.8008),
            (53, 30, 71, 36, 0.8024),
            (54, 30, 65, 33, 0.8015),
            (55, 30, 61, 31, 0.8088),
            (56, 30, 56, 28, 0.8019),
            (57, 30, 52, 26, 0.8024),
            (58, 30, 49, 25, 0.8128),
            (59, 30, 45, 23, 0.8074),
            (60, 30, 42, 21, 0.8013),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 0 to 20 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, Ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "less", method = "z", equal_var = False
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="less",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=False,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (0, 30, 15, 30, 0.8216),
            (1, 30, 16, 32, 0.8205),
            (2, 30, 17, 34, 0.8173),
            (3, 30, 18, 36, 0.8120),
            (4, 30, 19, 38, 0.8046),
            (5, 30, 21, 42, 0.8120),
            (6, 30, 23, 46, 0.8152),
            (7, 30, 24, 48, 0.8006),
            (8, 30, 27, 54, 0.8106),
            (9, 30, 29, 58, 0.8031),
            (10, 30, 32, 64, 0.8034),
            (11, 30, 36, 72, 0.8087),
            (12, 30, 40, 80, 0.8077),
            (13, 30, 44, 88, 0.8011),
            (14, 30, 50, 100, 0.8034),
            (15, 30, 57, 114, 0.8041),
            (16, 30, 65, 130, 0.8018),
            (17, 30, 75, 150, 0.8000),
            (18, 30, 89, 178, 0.8039),
            (19, 30, 105, 210, 0.8008),
            (20, 30, 127, 254, 0.8007),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, Ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "greater", method = "z", equal_var = False
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=False,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 127, 254, 0.8007),
            (41, 30, 105, 210, 0.8008),
            (42, 30, 89, 178, 0.8039),
            (43, 30, 75, 150, 0.8000),
            (44, 30, 65, 130, 0.8018),
            (45, 30, 57, 114, 0.8041),
            (46, 30, 50, 100, 0.8034),
            (47, 30, 44, 88, 0.8011),
            (48, 30, 40, 80, 0.8077),
            (49, 30, 36, 72, 0.8087),
            (50, 30, 32, 64, 0.8034),
            (51, 30, 29, 58, 0.8031),
            (52, 30, 27, 54, 0.8106),
            (53, 30, 24, 48, 0.8006),
            (54, 30, 23, 46, 0.8152),
            (55, 30, 21, 42, 0.8120),
            (56, 30, 19, 38, 0.8046),
            (57, 30, 18, 36, 0.8120),
            (58, 30, 17, 34, 0.8173),
            (59, 30, 16, 32, 0.8205),
            (60, 30, 15, 30, 0.8216),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, Ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "two-sided", method = "z", equal_var = False
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="z",
            equal_var=False,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 161, 322, 0.8002),
            (41, 30, 133, 266, 0.8001),
            (42, 30, 112, 224, 0.8009),
            (43, 30, 96, 192, 0.8032),
            (44, 30, 83, 166, 0.8043),
            (45, 30, 72, 144, 0.8027),
            (46, 30, 63, 126, 0.8009),
            (47, 30, 56, 112, 0.8023),
            (48, 30, 50, 100, 0.8027),
            (49, 30, 45, 90, 0.8037),
            (50, 30, 41, 82, 0.8074),
            (51, 30, 37, 74, 0.8055),
            (52, 30, 34, 68, 0.8087),
            (53, 30, 31, 62, 0.8074),
            (54, 30, 28, 56, 0.8009),
            (55, 30, 26, 52, 0.8039),
            (56, 30, 24, 48, 0.8032),
            (57, 30, 23, 46, 0.8159),
            (58, 30, 21, 42, 0.8089),
            (59, 30, 20, 40, 0.8171),
            (60, 30, 18, 36, 0.8027),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 0 to 20 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.05, power = 0.80, alternative = "less", method = "t", equal_var = True
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="less",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (0, 30, 34, 17, 0.8009),
            (1, 30, 37, 19, 0.8137),
            (2, 30, 39, 20, 0.8078),
            (3, 30, 41, 21, 0.8001),
            (4, 30, 45, 23, 0.8065),
            (5, 30, 49, 25, 0.8090),
            (6, 30, 53, 27, 0.8080),
            (7, 30, 57, 29, 0.8039),
            (8, 30, 63, 32, 0.8079),
            (9, 30, 69, 35, 0.8074),
            (10, 30, 75, 38, 0.8026),
            (11, 30, 83, 42, 0.8023),
            (12, 30, 93, 47, 0.8043),
            (13, 30, 103, 52, 0.8002),
            (14, 30, 117, 59, 0.8025),
            (15, 30, 133, 67, 0.8023),
            (16, 30, 153, 77, 0.8031),
            (17, 30, 177, 89, 0.8023),
            (18, 30, 207, 104, 0.8011),
            (19, 30, 247, 124, 0.8021),
            (20, 30, 298, 149, 0.8004),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.05, power = 0.80, alternative = "greater", method = "t", equal_var = True
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 298, 149, 0.8004),
            (41, 30, 247, 124, 0.8021),
            (42, 30, 207, 104, 0.8011),
            (43, 30, 177, 89, 0.8023),
            (44, 30, 153, 77, 0.8031),
            (45, 30, 133, 67, 0.8023),
            (46, 30, 117, 59, 0.8025),
            (47, 30, 103, 52, 0.8002),
            (48, 30, 93, 47, 0.8043),
            (49, 30, 83, 42, 0.8023),
            (50, 30, 75, 38, 0.8026),
            (51, 30, 69, 35, 0.8074),
            (52, 30, 63, 32, 0.8079),
            (53, 30, 57, 29, 0.8039),
            (54, 30, 53, 27, 0.8080),
            (55, 30, 49, 25, 0.8090),
            (56, 30, 45, 23, 0.8065),
            (57, 30, 41, 21, 0.8001),
            (58, 30, 39, 20, 0.8078),
            (59, 30, 37, 19, 0.8137),
            (60, 30, 34, 17, 0.8009),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, Ratio = 2, alpha = 0.05, power = 0.80, alternative = "two-sided", method = "t", equal_var = True
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=40,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 379, 190, 0.8017),
            (41, 30, 313, 157, 0.8013),
            (42, 30, 263, 132, 0.8011),
            (43, 30, 225, 113, 0.8025),
            (44, 30, 193, 97, 0.8003),
            (45, 30, 169, 85, 0.8022),
            (46, 30, 149, 75, 0.8032),
            (47, 30, 131, 66, 0.8000),
            (48, 30, 117, 59, 0.8003),
            (49, 30, 105, 53, 0.8000),
            (50, 30, 95, 48, 0.8007),
            (51, 30, 87, 44, 0.8042),
            (52, 30, 79, 40, 0.8026),
            (53, 30, 73, 37, 0.8062),
            (54, 30, 67, 34, 0.8056),
            (55, 30, 61, 31, 0.8005),
            (56, 30, 57, 29, 0.8043),
            (57, 30, 53, 27, 0.8050),
            (58, 30, 49, 25, 0.8023),
            (59, 30, 47, 24, 0.8131),
            (60, 30, 43, 22, 0.8044),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 0 to 20 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, Ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "less", method = "t", equal_var = False, df_adjust="satterthwaite",
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="less",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="satterthwaite",
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (0, 30, 15, 30, 0.8000),
            (1, 30, 16, 32, 0.8004),
            (2, 30, 18, 36, 0.8191),
            (3, 30, 19, 38, 0.8138),
            (4, 30, 20, 40, 0.8064),
            (5, 30, 22, 44, 0.8137),
            (6, 30, 23, 46, 0.8016),
            (7, 30, 25, 50, 0.8022),
            (8, 30, 28, 56, 0.8120),
            (9, 30, 30, 60, 0.8045),
            (10, 30, 33, 66, 0.8047),
            (11, 30, 36, 72, 0.8001),
            (12, 30, 40, 80, 0.8000),
            (13, 30, 45, 90, 0.8021),
            (14, 30, 51, 102, 0.8043),
            (15, 30, 58, 116, 0.8049),
            (16, 30, 66, 132, 0.8025),
            (17, 30, 76, 152, 0.8006),
            (18, 30, 89, 178, 0.8005),
            (19, 30, 106, 212, 0.8013),
            (20, 30, 128, 256, 0.8011),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, Ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "greater", method = "t", equal_var = False, df_adjust="satterthwaite",
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="satterthwaite",
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 128, 256, 0.8011),
            (41, 30, 106, 212, 0.8013),
            (42, 30, 89, 178, 0.8005),
            (43, 30, 76, 152, 0.8006),
            (44, 30, 66, 132, 0.8025),
            (45, 30, 58, 116, 0.8049),
            (46, 30, 51, 102, 0.8043),
            (47, 30, 45, 90, 0.8021),
            (48, 30, 40, 80, 0.8000),
            (49, 30, 36, 72, 0.8001),
            (50, 30, 33, 66, 0.8047),
            (51, 30, 30, 60, 0.8045),
            (52, 30, 28, 56, 0.8120),
            (53, 30, 25, 50, 0.8022),
            (54, 30, 23, 46, 0.8016),
            (55, 30, 22, 44, 0.8137),
            (56, 30, 20, 40, 0.8064),
            (57, 30, 19, 38, 0.8138),
            (58, 30, 18, 36, 0.8191),
            (59, 30, 16, 32, 0.8004),
            (60, 30, 15, 30, 0.8000),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, Ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "two-sided", method = "t", equal_var = False, df_adjust="satterthwaite",
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="satterthwaite",
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 163, 326, 0.8021),
            (41, 30, 135, 270, 0.8023),
            (42, 30, 113, 226, 0.8001),
            (43, 30, 97, 194, 0.8023),
            (44, 30, 84, 168, 0.8032),
            (45, 30, 73, 146, 0.8014),
            (46, 30, 65, 130, 0.8056),
            (47, 30, 57, 114, 0.8006),
            (48, 30, 51, 102, 0.8008),
            (49, 30, 46, 92, 0.8017),
            (50, 30, 42, 84, 0.8051),
            (51, 30, 38, 76, 0.8029),
            (52, 30, 35, 70, 0.8059),
            (53, 30, 32, 64, 0.8042),
            (54, 30, 30, 60, 0.8111),
            (55, 30, 28, 56, 0.8147),
            (56, 30, 26, 52, 0.8149),
            (57, 30, 24, 48, 0.8115),
            (58, 30, 22, 44, 0.8040),
            (59, 30, 21, 42, 0.8119),
            (60, 30, 20, 40, 0.8179),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 0 to 20 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, Ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "less", method = "t", equal_var = False, df_adjust="welch",
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="less",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="welch",
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (0, 30, 15, 30, 0.8011),
            (1, 30, 16, 32, 0.8013),
            (2, 30, 18, 36, 0.8198),
            (3, 30, 19, 38, 0.8144),
            (4, 30, 20, 40, 0.8070),
            (5, 30, 22, 44, 0.8142),
            (6, 30, 23, 46, 0.8020),
            (7, 30, 25, 50, 0.8025),
            (8, 30, 28, 56, 0.8122),
            (9, 30, 30, 60, 0.8047),
            (10, 30, 33, 66, 0.8049),
            (11, 30, 36, 72, 0.8003),
            (12, 30, 40, 80, 0.8002),
            (13, 30, 45, 90, 0.8022),
            (14, 30, 51, 102, 0.8044),
            (15, 30, 58, 116, 0.8049),
            (16, 30, 66, 132, 0.8025),
            (17, 30, 76, 152, 0.8007),
            (18, 30, 89, 178, 0.8005),
            (19, 30, 106, 212, 0.8013),
            (20, 30, 128, 256, 0.8011),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, Ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "greater", method = "t", equal_var = False, df_adjust="welch",
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="welch",
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 128, 256, 0.8011),
            (41, 30, 106, 212, 0.8013),
            (42, 30, 89, 178, 0.8005),
            (43, 30, 76, 152, 0.8007),
            (44, 30, 66, 132, 0.8025),
            (45, 30, 58, 116, 0.8049),
            (46, 30, 51, 102, 0.8044),
            (47, 30, 45, 90, 0.8022),
            (48, 30, 40, 80, 0.8002),
            (49, 30, 36, 72, 0.8003),
            (50, 30, 33, 66, 0.8049),
            (51, 30, 30, 60, 0.8047),
            (52, 30, 28, 56, 0.8122),
            (53, 30, 25, 50, 0.8025),
            (54, 30, 23, 46, 0.8020),
            (55, 30, 22, 44, 0.8142),
            (56, 30, 20, 40, 0.8070),
            (57, 30, 19, 38, 0.8144),
            (58, 30, 18, 36, 0.8198),
            (59, 30, 16, 32, 0.8013),
            (60, 30, 15, 30, 0.8011),
        ]
    ]
    + [
        # Regular Test Cases: treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, Ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "two-sided", method = "t", equal_var = False, df_adjust="welch",
        TestCase(
            treatment_mean=treatment_mean,
            reference_mean=reference_mean,
            diff=None,
            treatment_std=40,
            reference_std=30,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.05,
            power=0.80,
            actual_power=actual_power,
            method="t",
            equal_var=False,
            df_adjust="welch",
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 163, 326, 0.8021),
            (41, 30, 135, 270, 0.8024),
            (42, 30, 113, 226, 0.8002),
            (43, 30, 97, 194, 0.8023),
            (44, 30, 84, 168, 0.8033),
            (45, 30, 73, 146, 0.8015),
            (46, 30, 65, 130, 0.8057),
            (47, 30, 57, 114, 0.8007),
            (48, 30, 51, 102, 0.8009),
            (49, 30, 46, 92, 0.8018),
            (50, 30, 42, 84, 0.8053),
            (51, 30, 38, 76, 0.8031),
            (52, 30, 35, 70, 0.8062),
            (53, 30, 32, 64, 0.8046),
            (54, 30, 30, 60, 0.8115),
            (55, 30, 28, 56, 0.8152),
            (56, 30, 26, 52, 0.8155),
            (57, 30, 24, 48, 0.8121),
            (58, 30, 22, 44, 0.8047),
            (59, 30, 21, 42, 0.8127),
            (60, 30, 20, 40, 0.8188),
        ]
    ]
)


def test_solve_power(case: TestCase) -> None:
    assert (
        round(
            solve_power(
                treatment_mean=case.treatment_mean,
                reference_mean=case.reference_mean,
                diff=case.diff,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                method=case.method,
                equal_var=case.equal_var,
                df_adjust=case.df_adjust,
            ),
            4,
        )
        == case.actual_power
    )


def test_solve_power_errors() -> None:
    with pytest.raises(ValueError):
        solve_power(treatment_mean=None, reference_mean=30, treatment_std=40, reference_std=40, treatment_size=100, reference_size=100)
    with pytest.raises(ValueError):
        solve_power(treatment_mean=40, reference_mean=30, diff=None, treatment_std=40, reference_std=30, treatment_size=100, reference_size=100, method="z", equal_var=True)


def test_solve_size(case: TestCase) -> None:
    if (
        case
        in [
            TestCase(treatment_mean=42, reference_mean=30, diff=12, treatment_std=40, reference_std=40, treatment_size=207, reference_size=104, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8011, method="t", equal_var=True),
            TestCase(treatment_mean=47, reference_mean=30, diff=17, treatment_std=40, reference_std=40, treatment_size=103, reference_size=52, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8002, method="t", equal_var=True),
            TestCase(treatment_mean=54, reference_mean=30, diff=24, treatment_std=40, reference_std=40, treatment_size=53, reference_size=27, alternative="greater", alpha=0.05, power=0.8, actual_power=0.808, method="t", equal_var=True),
            TestCase(
                treatment_mean=52,
                reference_mean=30,
                diff=22,
                treatment_std=40,
                reference_std=30,
                treatment_size=28,
                reference_size=56,
                alternative="greater",
                alpha=0.05,
                power=0.8,
                actual_power=0.812,
                method="t",
                equal_var=False,
                df_adjust="satterthwaite",
            ),
        ]
        or (case.treatment_mean in range(40, 61) and case.alternative == "two-sided" and case.method == "t" and case.equal_var)
        or (case.treatment_mean in range(40, 61) and case.alternative == "two-sided" and case.method == "t" and not case.equal_var)
    ):
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    ratio = case.treatment_size / case.reference_size
    assert solve_size(
        treatment_mean=case.treatment_mean,
        reference_mean=case.reference_mean,
        diff=case.diff,
        treatment_std=case.treatment_std,
        reference_std=case.reference_std,
        ratio=ratio,
        alternative=case.alternative,
        alpha=case.alpha,
        power=case.power,
        method=case.method,
        equal_var=case.equal_var,
        df_adjust=case.df_adjust,
    ) == (case.treatment_size, case.reference_size)


def test_solve_diff(case: TestCase) -> None:
    if (
        case == TestCase(treatment_mean=56, reference_mean=30, diff=26, treatment_std=40, reference_std=40, treatment_size=45, reference_size=23, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8065, method="t", equal_var=True)
        or (case.treatment_mean in range(40, 61) and case.alternative == "two-sided" and case.method == "t" and case.equal_var)
        or (case.treatment_mean in range(40, 61) and case.alternative == "two-sided" and case.method == "t" and not case.equal_var)
    ):
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    search_direction = "above" if case.diff > 0 else "below"
    assert (
        round(
            solve_diff(
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                search_direction=search_direction,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                equal_var=case.equal_var,
                df_adjust=case.df_adjust,
            ),
            0,
        )
        == case.diff
    )


def test_solve_treatment_mean(case: TestCase) -> None:
    if (
        case == TestCase(treatment_mean=56, reference_mean=30, diff=26, treatment_std=40, reference_std=40, treatment_size=45, reference_size=23, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8065, method="t", equal_var=True)
        or (case.treatment_mean in range(40, 61) and case.alternative == "two-sided" and case.method == "t" and case.equal_var)
        or (case.treatment_mean in range(40, 61) and case.alternative == "two-sided" and case.method == "t" and not case.equal_var)
    ):
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    search_direction = "above" if case.treatment_mean > case.reference_mean else "below"
    assert (
        round(
            solve_treatment_mean(
                reference_mean=case.reference_mean,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                search_direction=search_direction,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                equal_var=case.equal_var,
                df_adjust=case.df_adjust,
            ),
            0,
        )
        == case.treatment_mean
    )


def test_solve_reference_mean(case: TestCase) -> None:
    if (
        case == TestCase(treatment_mean=56, reference_mean=30, diff=26, treatment_std=40, reference_std=40, treatment_size=45, reference_size=23, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8065, method="t", equal_var=True)
        or (case.treatment_mean in range(40, 61) and case.alternative == "two-sided" and case.method == "t" and case.equal_var)
        or (case.treatment_mean in range(40, 61) and case.alternative == "two-sided" and case.method == "t" and not case.equal_var)
    ):
        pytest.xfail("SciPy upstream bug: https://github.com/scipy/scipy/issues/25106")

    search_direction = "above" if case.reference_mean > case.treatment_mean else "below"
    assert (
        round(
            solve_reference_mean(
                treatment_mean=case.treatment_mean,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                search_direction=search_direction,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                equal_var=case.equal_var,
                df_adjust=case.df_adjust,
            ),
            0,
        )
        == case.reference_mean
    )


def test_solve_treatment_std(case: TestCase) -> None:
    assert (
        round(
            solve_treatment_std(
                treatment_mean=case.treatment_mean,
                reference_mean=case.reference_mean,
                diff=case.diff,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                equal_var=case.equal_var,
                reference_std=case.reference_std,
                df_adjust=case.df_adjust,
            ),
            0,
        )
        == case.treatment_std
    )


def test_solve_treatment_std_error() -> None:
    with pytest.raises(ValueError):
        solve_treatment_std(treatment_mean=40, reference_mean=30, treatment_size=100, reference_size=100, equal_var=False)


def test_solve_reference_std(case: TestCase) -> None:
    assert (
        round(
            solve_reference_std(
                treatment_mean=case.treatment_mean,
                reference_mean=case.reference_mean,
                diff=case.diff,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                equal_var=case.equal_var,
                treatment_std=case.treatment_std,
                df_adjust=case.df_adjust,
            ),
            0,
        )
        == case.reference_std
    )


def test_solve_reference_std_error() -> None:
    with pytest.raises(ValueError):
        solve_reference_std(treatment_mean=40, reference_mean=30, treatment_size=100, reference_size=100, equal_var=False)
