# Validation Software: PASS 15
# Module: Tests for Two Proportions

from dataclasses import dataclass
from typing import Literal

from pystatpower.proportion.independent.inequality import solve_power, solve_size, solve_treatment_proportion, solve_reference_proportion

from tests.models import BaseTestCase


@dataclass
class TestCase(BaseTestCase):
    treatment_proportion: float
    reference_proportion: float
    treatment_size: int
    reference_size: int
    alternative: Literal["one-sided", "two-sided"]
    alpha: float
    power: float
    pooled: bool
    continuity_correction: bool
    actual_power: float


case_group_pooled = (
    [
        # treatment_proportion = 0.98, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 2, alternative = "two-sided", pooled = True, continuity_orrection = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="one-sided",
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.98, 0.80, 74, 37, 0.8022739482150650),
            (0.98, 0.81, 79, 40, 0.8003693203281330),
            (0.98, 0.82, 87, 44, 0.8059362278881300),
            (0.98, 0.83, 94, 47, 0.8007222907112260),
            (0.98, 0.84, 103, 52, 0.8018790123693330),
            (0.98, 0.85, 114, 57, 0.8007679098051310),
            (0.98, 0.86, 127, 64, 0.8018365170988300),
            (0.98, 0.87, 143, 72, 0.8015355588869760),
            (0.98, 0.88, 163, 82, 0.8011225957640860),
            (0.98, 0.89, 189, 95, 0.8013035578756430),
            (0.98, 0.90, 223, 112, 0.8006977932606080),
            (0.98, 0.91, 271, 136, 0.8016598149849190),
            (0.98, 0.92, 339, 170, 0.8007339396633520),
            (0.98, 0.93, 445, 223, 0.8000030088958710),
            (0.98, 0.94, 629, 315, 0.8003930065003960),
            (0.98, 0.95, 997, 499, 0.8002976757437660),
        ]
    ]
    + [
        # treatment_proportion = 0.98, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 2, alternative = "greater", pooled = True, continuity_orrection = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.98, 0.80, 62, 31, 0.8028177485169600),
            (0.98, 0.81, 67, 34, 0.8056171412864290),
            (0.98, 0.82, 72, 36, 0.8002400331894230),
            (0.98, 0.83, 79, 40, 0.8044037196094530),
            (0.98, 0.84, 87, 44, 0.8054992129578950),
            (0.98, 0.85, 95, 48, 0.8012865843966410),
            (0.98, 0.86, 107, 54, 0.8045874384350130),
            (0.98, 0.87, 119, 60, 0.8001542320296360),
            (0.98, 0.88, 137, 69, 0.8031698721317420),
            (0.98, 0.89, 158, 79, 0.8004856707145800),
            (0.98, 0.90, 187, 94, 0.8021432497300570),
            (0.98, 0.91, 226, 113, 0.8004640503309270),
            (0.98, 0.92, 283, 142, 0.8009158538979060),
            (0.98, 0.93, 371, 186, 0.8000085218549490),
            (0.98, 0.94, 524, 262, 0.8000193563830090),
            (0.98, 0.95, 829, 415, 0.8000476011450170),
        ]
    ]
    + [  # ratio = 0.5, alternative = "two-sided", pooled = True, continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.98, 0.80, 46, 92, 0.8024),
            (0.98, 0.81, 50, 100, 0.8066),
            (0.98, 0.82, 54, 108, 0.8050),
            (0.98, 0.83, 59, 118, 0.8068),
            (0.98, 0.84, 64, 128, 0.8017),
            (0.98, 0.85, 71, 142, 0.8048),
            (0.98, 0.86, 79, 158, 0.8052),
            (0.98, 0.87, 88, 176, 0.8011),
            (0.98, 0.88, 100, 200, 0.8013),
            (0.98, 0.89, 115, 230, 0.8001),
            (0.98, 0.90, 136, 272, 0.8038),
            (0.98, 0.91, 163, 326, 0.8021),
            (0.98, 0.92, 202, 404, 0.8011),
            (0.98, 0.93, 262, 524, 0.8004),
            (0.98, 0.94, 364, 728, 0.8002),
            (0.98, 0.95, 566, 1132, 0.8007),
        ]
    ]
)

case_group_pooled_cc = [  # ratio = 2, alternative = "one-sided", pooled = True, continuity_orrection = True
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="one-sided",
        alpha=0.025,
        power=0.80,
        pooled=True,
        continuity_correction=True,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.98, 0.80, 77, 39, 0.8013),
        (0.98, 0.81, 83, 42, 0.8022),
        (0.98, 0.82, 90, 45, 0.8013),
        (0.98, 0.83, 97, 49, 0.8004),
        (0.98, 0.84, 107, 54, 0.8042),
        (0.98, 0.85, 117, 59, 0.8016),
        (0.98, 0.86, 130, 65, 0.8005),
        (0.98, 0.87, 145, 73, 0.8003),
        (0.98, 0.88, 165, 83, 0.8017),
        (0.98, 0.89, 190, 95, 0.8008),
        (0.98, 0.90, 223, 112, 0.8023),
        (0.98, 0.91, 267, 134, 0.8011),
        (0.98, 0.92, 331, 166, 0.8008),
        (0.98, 0.93, 429, 215, 0.8001),
        (0.98, 0.94, 597, 299, 0.8006),
        (0.98, 0.95, 927, 464, 0.8004),
    ]
] + [  # ratio = 0.5, alternative = "two-sided", pooled = True, continuity_correction = True
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="two-sided",
        alpha=0.025,
        power=0.80,
        pooled=True,
        continuity_correction=True,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.98, 0.80, 54, 108, 0.8022288149272370),
        (0.98, 0.81, 58, 116, 0.8013653564643120),
        (0.98, 0.82, 63, 126, 0.8047516222661600),
        (0.98, 0.83, 68, 136, 0.8011329404521930),
        (0.98, 0.84, 75, 150, 0.8072036851158960),
        (0.98, 0.85, 82, 164, 0.8038567293891170),
        (0.98, 0.86, 91, 182, 0.8047357216103030),
        (0.98, 0.87, 101, 202, 0.8000510992671330),
        (0.98, 0.88, 115, 230, 0.8037756430764090),
        (0.98, 0.89, 132, 264, 0.8038787548095800),
        (0.98, 0.90, 154, 308, 0.8030847181326950),
        (0.98, 0.91, 184, 368, 0.8026952504843390),
        (0.98, 0.92, 226, 452, 0.8003515656224490),
        (0.98, 0.93, 292, 584, 0.8018180909465790),
        (0.98, 0.94, 401, 802, 0.8006699924225260),
        (0.98, 0.95, 615, 1230, 0.8007590030620840),
    ]
]

case_group_unpooled = (
    [  # ratio = 2, alternative = "one-sided", pooled = False, continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="one-sided",
            alpha=0.025,
            power=0.80,
            pooled=False,
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.98, 0.80, 83, 42, 0.8078),
            (0.98, 0.81, 89, 45, 0.8045),
            (0.98, 0.82, 97, 49, 0.8057),
            (0.98, 0.83, 105, 53, 0.8024),
            (0.98, 0.84, 115, 58, 0.8015),
            (0.98, 0.85, 127, 64, 0.8012),
            (0.98, 0.86, 142, 71, 0.8002),
            (0.98, 0.87, 159, 80, 0.8012),
            (0.98, 0.88, 181, 91, 0.8016),
            (0.98, 0.89, 209, 105, 0.8022),
            (0.98, 0.90, 245, 123, 0.8018),
            (0.98, 0.91, 293, 147, 0.8002),
            (0.98, 0.92, 363, 182, 0.8002),
            (0.98, 0.93, 471, 236, 0.8013),
            (0.98, 0.94, 649, 325, 0.8002),
            (0.98, 0.95, 999, 500, 0.8002),
        ]
    ]
    + [  # ratio = 0.5, alternative = "two-sided", pooled = False, continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.025,
            power=0.80,
            pooled=False,
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.98, 0.80, 30, 60, 0.8113),
            (0.98, 0.81, 32, 64, 0.8033),
            (0.98, 0.82, 35, 70, 0.8040),
            (0.98, 0.83, 39, 78, 0.8102),
            (0.98, 0.84, 43, 86, 0.8091),
            (0.98, 0.85, 47, 94, 0.8011),
            (0.98, 0.86, 53, 106, 0.8027),
            (0.98, 0.87, 60, 120, 0.8013),
            (0.98, 0.88, 69, 138, 0.8011),
            (0.98, 0.89, 81, 162, 0.8030),
            (0.98, 0.90, 96, 192, 0.8003),
            (0.98, 0.91, 118, 236, 0.8020),
            (0.98, 0.92, 149, 298, 0.8003),
            (0.98, 0.93, 199, 398, 0.8016),
            (0.98, 0.94, 284, 568, 0.8001),
            (0.98, 0.95, 458, 916, 0.8002),
        ]
    ]
    + [  # Specific Cases: Treatment Proportion < Reference Proportion
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.025,
            power=0.80,
            pooled=False,
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.80, 0.98, 50, 100, 0.8016),
            (0.81, 0.98, 54, 108, 0.8013),
            (0.82, 0.98, 59, 118, 0.8041),
            (0.83, 0.98, 64, 128, 0.8017),
            (0.84, 0.98, 70, 140, 0.8004),
            (0.85, 0.98, 78, 156, 0.8043),
            (0.86, 0.98, 86, 172, 0.8003),
            (0.87, 0.98, 97, 194, 0.8020),
            (0.88, 0.98, 110, 220, 0.8012),
            (0.89, 0.98, 127, 254, 0.8021),
            (0.90, 0.98, 149, 298, 0.8023),
            (0.91, 0.98, 178, 356, 0.8003),
            (0.92, 0.98, 221, 442, 0.8016),
            (0.93, 0.98, 285, 570, 0.8003),
            (0.94, 0.98, 394, 788, 0.8008),
            (0.95, 0.98, 606, 1212, 0.8006),
        ]
    ]
)

case_group_unpooled_cc = [  # ratio = 2, alternative = "one-sided", pooled = False, continuity_correction = True
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="one-sided",
        alpha=0.025,
        power=0.80,
        pooled=False,
        continuity_correction=True,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.98, 0.80, 99, 50, 0.8078),
        (0.98, 0.81, 105, 53, 0.8003),
        (0.98, 0.82, 115, 58, 0.8056),
        (0.98, 0.83, 125, 63, 0.8052),
        (0.98, 0.84, 137, 69, 0.8061),
        (0.98, 0.85, 149, 75, 0.8005),
        (0.98, 0.86, 166, 83, 0.8000),
        (0.98, 0.87, 185, 93, 0.8004),
        (0.98, 0.88, 211, 106, 0.8038),
        (0.98, 0.89, 241, 121, 0.8018),
        (0.98, 0.90, 281, 141, 0.8013),
        (0.98, 0.91, 335, 168, 0.8008),
        (0.98, 0.92, 413, 207, 0.8018),
        (0.98, 0.93, 529, 265, 0.8010),
        (0.98, 0.94, 723, 362, 0.8008),
        (0.98, 0.95, 1097, 549, 0.8003),
    ]
] + [  # ratio = 0.5, alternative = "two-sided", pooled = False, continuity_correction = True
    TestCase(
        treatment_proportion=treatment_proportion,
        reference_proportion=reference_proportion,
        treatment_size=treatment_size,
        reference_size=reference_size,
        alternative="two-sided",
        alpha=0.025,
        power=0.80,
        pooled=False,
        continuity_correction=True,
        actual_power=actual_power,
    )
    for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
        (0.98, 0.80, 38, 76, 0.8129899608739270),
        (0.98, 0.81, 41, 82, 0.8118778019766200),
        (0.98, 0.82, 44, 88, 0.8054846310721070),
        (0.98, 0.83, 48, 96, 0.8049048076866920),
        (0.98, 0.84, 53, 106, 0.8074028914061020),
        (0.98, 0.85, 58, 116, 0.8014410938016210),
        (0.98, 0.86, 65, 130, 0.8034748180302020),
        (0.98, 0.87, 73, 146, 0.8013063336920820),
        (0.98, 0.88, 84, 168, 0.8052911406956490),
        (0.98, 0.89, 97, 194, 0.8032423747023240),
        (0.98, 0.90, 114, 228, 0.8003573691860350),
        (0.98, 0.91, 139, 278, 0.8034370459974150),
        (0.98, 0.92, 174, 348, 0.8028398546281730),
        (0.98, 0.93, 228, 456, 0.8015442603682950),
        (0.98, 0.94, 321, 642, 0.8009589541200160),
        (0.98, 0.95, 507, 1014, 0.8003831724761880),
    ]
]

case_group = case_group_pooled + case_group_pooled_cc + case_group_unpooled + case_group_unpooled_cc


def test_size_solve_power(case: TestCase) -> None:
    assert round(
        solve_power(
            treatment_proportion=case.treatment_proportion,
            reference_proportion=case.reference_proportion,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            alternative=case.alternative,
            alpha=case.alpha,
            pooled=case.pooled,
            continuity_correction=case.continuity_correction,
        ),
        6,
    ) == round(case.actual_power, 6)


def test_solve_size(case: TestCase) -> None:
    ratio = case.treatment_size / case.reference_size
    assert solve_size(
        treatment_proportion=case.treatment_proportion,
        reference_proportion=case.reference_proportion,
        alternative=case.alternative,
        ratio=ratio,
        alpha=case.alpha,
        power=case.power,
        pooled=case.pooled,
        continuity_correction=case.continuity_correction,
    ) == (case.treatment_size, case.reference_size)


def test_solve_treatment_proportion(case: TestCase) -> None:
    search_direction = "lower" if case.treatment_proportion < case.reference_proportion else "upper"
    assert (
        round(
            solve_treatment_proportion(
                reference_proportion=case.reference_proportion,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                pooled=case.pooled,
                continuity_correction=case.continuity_correction,
                search_direction=search_direction,
            ),
            2,
        )
        == case.treatment_proportion
    )


def test_solve_reference_proportion(case: TestCase) -> None:
    search_direction = "lower" if case.reference_proportion < case.treatment_proportion else "upper"
    assert (
        round(
            solve_reference_proportion(
                treatment_proportion=case.treatment_proportion,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                pooled=case.pooled,
                continuity_correction=case.continuity_correction,
                search_direction=search_direction,
            ),
            2,
        )
        == case.reference_proportion
    )
