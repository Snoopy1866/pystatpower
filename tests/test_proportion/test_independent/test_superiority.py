# Validation Software: PASS 15
# Module: Superiority by a Margin for the Difference Between Two Proportions

from dataclasses import dataclass

from pystatpower.proportion.independent.superiority import solve_power, solve_size, solve_treatment_proportion, solve_reference_proportion, solve_margin

from tests.models import BaseTestCase


@dataclass
class TestCase(BaseTestCase):
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


case_group = (
    [  # Regular Cases: ratio = 2, margin = 0, pooled = True, continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=True,
            actual_power=actual_power,
        )
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
    + [  # Regular Cases: ratio = 2, margin = 0, pooled = True, continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=False,
            actual_power=actual_power,
        )
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
    + [  # Regular Cases,: ratio = 2, margin = 0, pooled = False, continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=False,
            continuity_correction=True,
            actual_power=actual_power,
        )
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
    + [  # Regular Cases: ratio = 2, margin = 0, pooled = False, continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=False,
            continuity_correction=False,
            actual_power=actual_power,
        )
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
    + [  # Regular Cases: ratio = 0.5, margin = 0, pooled = True, continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.80, 0.70, 239, 478, 0.8015),
            (0.81, 0.71, 233, 466, 0.8012),
            (0.82, 0.72, 227, 454, 0.8015),
            (0.83, 0.73, 220, 440, 0.8002),
            (0.84, 0.74, 214, 428, 0.8014),
            (0.85, 0.75, 207, 414, 0.8011),
            (0.86, 0.76, 200, 400, 0.8012),
            (0.87, 0.77, 193, 386, 0.8020),
            (0.88, 0.78, 185, 370, 0.8009),
            (0.89, 0.79, 177, 354, 0.8004),
            (0.90, 0.80, 169, 338, 0.8005),
            (0.91, 0.81, 161, 322, 0.8012),
            (0.92, 0.82, 153, 306, 0.8029),
            (0.93, 0.83, 144, 288, 0.8023),
            (0.94, 0.84, 135, 270, 0.8024),
            (0.95, 0.85, 126, 252, 0.8036),
            (0.96, 0.86, 116, 232, 0.8019),
            (0.97, 0.87, 106, 212, 0.8010),
            (0.98, 0.88, 96, 192, 0.8015),
            (0.99, 0.89, 86, 172, 0.8042),
        ]
    ]
    + [  # Regular Cases: ratio = 0.5, margin = 0.02, 0.04, 0.06, 0.08, pooled = True, continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=margin,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, margin, treatment_size, reference_size, actual_power in [
            (0.80, 0.70, 0.02, 368, 736, 0.8004),
            (0.80, 0.70, 0.04, 646, 1292, 0.8004),
            (0.80, 0.70, 0.06, 1434, 2868, 0.8001),
            (0.80, 0.70, 0.08, 5661, 11322, 0.8000),
            (0.81, 0.71, 0.02, 359, 718, 0.8006),
            (0.81, 0.71, 0.04, 630, 1260, 0.8006),
            (0.81, 0.71, 0.06, 1398, 2796, 0.8003),
            (0.81, 0.71, 0.08, 5515, 11030, 0.8001),
            (0.82, 0.72, 0.02, 349, 698, 0.8001),
            (0.82, 0.72, 0.04, 613, 1226, 0.8006),
            (0.82, 0.72, 0.06, 1359, 2718, 0.8000),
            (0.82, 0.72, 0.08, 5362, 10724, 0.8000),
            (0.83, 0.73, 0.02, 340, 680, 0.8012),
            (0.83, 0.73, 0.04, 595, 1190, 0.8003),
            (0.83, 0.73, 0.06, 1320, 2640, 0.8002),
            (0.83, 0.73, 0.08, 5204, 10408, 0.8001),
            (0.84, 0.74, 0.02, 329, 658, 0.8003),
            (0.84, 0.74, 0.04, 577, 1154, 0.8005),
            (0.84, 0.74, 0.06, 1279, 2558, 0.8002),
            (0.84, 0.74, 0.08, 5040, 10080, 0.8001),
            (0.85, 0.75, 0.02, 319, 638, 0.8012),
            (0.85, 0.75, 0.04, 558, 1116, 0.8005),
            (0.85, 0.75, 0.06, 1236, 2472, 0.8001),
            (0.85, 0.75, 0.08, 4869, 9738, 0.8000),
            (0.86, 0.76, 0.02, 308, 616, 0.8013),
            (0.86, 0.76, 0.04, 538, 1076, 0.8001),
            (0.86, 0.76, 0.06, 1192, 2384, 0.8001),
            (0.86, 0.76, 0.08, 4693, 9386, 0.8000),
            (0.87, 0.77, 0.02, 296, 592, 0.8004),
            (0.87, 0.77, 0.04, 518, 1036, 0.8003),
            (0.87, 0.77, 0.06, 1147, 2294, 0.8003),
            (0.87, 0.77, 0.08, 4511, 9022, 0.8000),
            (0.88, 0.78, 0.02, 284, 568, 0.8001),
            (0.88, 0.78, 0.04, 497, 994, 0.8003),
            (0.88, 0.78, 0.06, 1100, 2200, 0.8003),
            (0.88, 0.78, 0.08, 4323, 8646, 0.8000),
            (0.89, 0.79, 0.02, 272, 544, 0.8003),
            (0.89, 0.79, 0.04, 476, 952, 0.8008),
            (0.89, 0.79, 0.06, 1051, 2102, 0.8001),
            (0.89, 0.79, 0.08, 4129, 8258, 0.8000),
        ]
    ]
    + [  # Regular Cases: ratio = 0.5, margin = -0.02, -0.04, -0.06, -0.08, pooled = True, continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=margin,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, margin, treatment_size, reference_size, actual_power in [
            (0.60, 0.70, -0.08, 6684, 13368, 0.8000),
            (0.60, 0.70, -0.06, 1690, 3380, 0.8001),
            (0.60, 0.70, -0.04, 760, 1520, 0.8005),
            (0.60, 0.70, -0.02, 432, 864, 0.8004),
            (0.61, 0.71, -0.08, 6589, 13178, 0.8000),
            (0.61, 0.71, -0.06, 1666, 3332, 0.8001),
            (0.61, 0.71, -0.04, 749, 1498, 0.8002),
            (0.61, 0.71, -0.02, 426, 852, 0.8003),
            (0.62, 0.72, -0.08, 6488, 12976, 0.8000),
            (0.62, 0.72, -0.06, 1641, 3282, 0.8001),
            (0.62, 0.72, -0.04, 738, 1476, 0.8004),
            (0.62, 0.72, -0.02, 420, 840, 0.8006),
            (0.63, 0.73, -0.08, 6381, 12762, 0.8000),
            (0.63, 0.73, -0.06, 1614, 3228, 0.8001),
            (0.63, 0.73, -0.04, 726, 1452, 0.8003),
            (0.63, 0.73, -0.02, 413, 826, 0.8004),
            (0.64, 0.74, -0.08, 6268, 12536, 0.8000),
            (0.64, 0.74, -0.06, 1586, 3172, 0.8001),
            (0.64, 0.74, -0.04, 713, 1426, 0.8001),
            (0.64, 0.74, -0.02, 406, 812, 0.8004),
            (0.65, 0.75, -0.08, 6149, 12298, 0.8000),
            (0.65, 0.75, -0.06, 1556, 3112, 0.8001),
            (0.65, 0.75, -0.04, 700, 1400, 0.8002),
            (0.65, 0.75, -0.02, 399, 798, 0.8009),
            (0.66, 0.76, -0.08, 6024, 12048, 0.8000),
            (0.66, 0.76, -0.06, 1525, 3050, 0.8001),
            (0.66, 0.76, -0.04, 686, 1372, 0.8001),
            (0.66, 0.76, -0.02, 391, 782, 0.8007),
            (0.67, 0.77, -0.08, 5894, 11788, 0.8000),
            (0.67, 0.77, -0.06, 1492, 2984, 0.8000),
            (0.67, 0.77, -0.04, 672, 1344, 0.8004),
            (0.67, 0.77, -0.02, 383, 766, 0.8009),
            (0.68, 0.78, -0.08, 5757, 11514, 0.8000),
            (0.68, 0.78, -0.06, 1458, 2916, 0.8001),
            (0.68, 0.78, -0.04, 657, 1314, 0.8005),
            (0.68, 0.78, -0.02, 374, 748, 0.8004),
            (0.69, 0.79, -0.08, 5615, 11230, 0.8000),
            (0.69, 0.79, -0.06, 1423, 2846, 0.8002),
            (0.69, 0.79, -0.04, 641, 1282, 0.8005),
            (0.69, 0.79, -0.02, 365, 730, 0.8003),
        ]
    ]
)


def test_size_solve_power(case: TestCase) -> None:
    assert (
        round(
            solve_power(
                treatment_proportion=case.treatment_proportion,
                reference_proportion=case.reference_proportion,
                margin=case.margin,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                pooled=case.pooled,
                continuity_correction=case.continuity_correction,
            ),
            4,
        )
        == case.actual_power
    )


def test_solve_size(case: TestCase) -> None:
    ratio = case.treatment_size / case.reference_size
    assert solve_size(
        treatment_proportion=case.treatment_proportion,
        reference_proportion=case.reference_proportion,
        margin=case.margin,
        ratio=ratio,
        alpha=case.alpha,
        power=case.power,
        pooled=case.pooled,
        continuity_correction=case.continuity_correction,
    ) == (case.treatment_size, case.reference_size)


def test_solve_treatment_proportion(case: TestCase) -> None:
    assert (
        round(
            solve_treatment_proportion(
                reference_proportion=case.reference_proportion,
                margin=case.margin,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                power=case.actual_power,
                pooled=case.pooled,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.treatment_proportion
    )


def test_solve_reference_proportion(case: TestCase) -> None:
    assert (
        round(
            solve_reference_proportion(
                treatment_proportion=case.treatment_proportion,
                margin=case.margin,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                power=case.actual_power,
                pooled=case.pooled,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.reference_proportion
    )


def test_solve_margin(case: TestCase) -> None:
    assert (
        round(
            solve_margin(
                treatment_proportion=case.treatment_proportion,
                reference_proportion=case.reference_proportion,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                power=case.actual_power,
                pooled=case.pooled,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.margin
    )
