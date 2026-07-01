# Validation Software: PASS 15
# Module: Confidence Intervals for the Difference Between Two Proportions

from dataclasses import dataclass
from typing import Literal

from pystatpower.proportion.independent.ci import solve_distance, solve_size, solve_treatment_proportion, solve_reference_proportion
from pystatpower.exceptions import SolutionNotFoundError

from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    treatment_proportion: float
    reference_proportion: float
    treatment_size: int
    reference_size: int
    conf_level: float
    interval_type: Literal["two-sided", "lower", "upper"]
    method: Literal["chisq", "wilson", "farrington_manning", "fm", "miettinen_nurminen", "mn"]
    continuity_correction: bool | None = None
    direction: Literal["greater", "less"] | None = None
    distance: float
    actual_distance: float


case_group_chisq = (
    [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "two-sided", method = "chisq", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="two-sided",
            method="chisq",
            continuity_correction=False,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 841, 421, 0.10, 0.0999623604102685),
            (0.10, 0.50, 907, 454, 0.10, 0.0999304137946998),
            (0.15, 0.50, 965, 483, 0.10, 0.0999176257073741),
            (0.20, 0.50, 1015, 508, 0.10, 0.0999206057258476),
            (0.25, 0.50, 1057, 529, 0.10, 0.0999373030538815),
            (0.30, 0.50, 1091, 546, 0.10, 0.0999665728387672),
            (0.35, 0.50, 1118, 559, 0.10, 0.0999939406429146),
            (0.40, 0.50, 1137, 569, 0.10, 0.0999734655390569),
            (0.45, 0.50, 1149, 575, 0.10, 0.0999533445407366),
            (0.50, 0.50, 1153, 577, 0.10, 0.0999467283160465),
            (0.55, 0.50, 1149, 575, 0.10, 0.0999533445407366),
            (0.60, 0.50, 1137, 569, 0.10, 0.0999734655390569),
            (0.65, 0.50, 1118, 559, 0.10, 0.0999939406429146),
            (0.70, 0.50, 1091, 546, 0.10, 0.0999665728387672),
            (0.75, 0.50, 1057, 529, 0.10, 0.0999373030538815),
            (0.80, 0.50, 1015, 508, 0.10, 0.0999206057258476),
            (0.85, 0.50, 965, 483, 0.10, 0.0999176257073741),
            (0.90, 0.50, 907, 454, 0.10, 0.0999304137946998),
            (0.95, 0.50, 841, 421, 0.10, 0.0999623604102685),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "lower", method = "chisq", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="lower",
            method="chisq",
            continuity_correction=False,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 149, 75, 0.10, 0.0994031369938266),
            (0.10, 0.50, 159, 80, 0.10, 0.0999312913225417),
            (0.15, 0.50, 169, 85, 0.10, 0.0999932257100696),
            (0.20, 0.50, 179, 90, 0.10, 0.0996682564708424),
            (0.25, 0.50, 187, 94, 0.10, 0.0995408048021086),
            (0.30, 0.50, 193, 97, 0.10, 0.0995836618706983),
            (0.35, 0.50, 197, 99, 0.10, 0.0997827763151041),
            (0.40, 0.50, 201, 101, 0.10, 0.0996362854831719),
            (0.45, 0.50, 203, 102, 0.10, 0.0996487055731943),
            (0.50, 0.50, 203, 102, 0.10, 0.0998157503757825),
            (0.55, 0.50, 203, 102, 0.10, 0.0996487055731943),
            (0.60, 0.50, 201, 101, 0.10, 0.0996362854831719),
            (0.65, 0.50, 197, 99, 0.10, 0.0997827763151041),
            (0.70, 0.50, 193, 97, 0.10, 0.0995836618706983),
            (0.75, 0.50, 187, 94, 0.10, 0.0995408048021086),
            (0.80, 0.50, 179, 90, 0.10, 0.0996682564708423),
            (0.85, 0.50, 169, 85, 0.10, 0.0999932257100695),
            (0.90, 0.50, 159, 80, 0.10, 0.0999312913225419),
            (0.95, 0.50, 149, 75, 0.10, 0.0994031369938267),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "upper", method = "chisq", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="upper",
            method="chisq",
            continuity_correction=False,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 47, 94, 0.10, 0.0996489845628985),
            (0.10, 0.50, 59, 118, 0.10, 0.0992934226106608),
            (0.15, 0.50, 69, 138, 0.10, 0.0995023648530200),
            (0.20, 0.50, 78, 156, 0.10, 0.0994265535164114),
            (0.25, 0.50, 85, 170, 0.10, 0.0997339006282121),
            (0.30, 0.50, 91, 182, 0.10, 0.0997996375796283),
            (0.35, 0.50, 96, 192, 0.10, 0.0996715474488579),
            (0.40, 0.50, 99, 198, 0.10, 0.0998748388845343),
            (0.45, 0.50, 101, 202, 0.10, 0.0998917699800948),
            (0.50, 0.50, 102, 204, 0.10, 0.0997339006282121),
            (0.55, 0.50, 101, 202, 0.10, 0.0998917699800948),
            (0.60, 0.50, 99, 198, 0.10, 0.0998748388845342),
            (0.65, 0.50, 96, 192, 0.10, 0.0996715474488580),
            (0.70, 0.50, 91, 182, 0.10, 0.0997996375796283),
            (0.75, 0.50, 85, 170, 0.10, 0.0997339006282121),
            (0.80, 0.50, 78, 156, 0.10, 0.0994265535164114),
            (0.85, 0.50, 69, 138, 0.10, 0.0995023648530200),
            (0.90, 0.50, 59, 118, 0.10, 0.0992934226106608),
            (0.95, 0.50, 47, 94, 0.10, 0.0996489845628985),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.05, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "two-sided", method = "chisq", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="two-sided",
            method="chisq",
            continuity_correction=False,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.05, 110, 220, 0.10, 0.0997640746030822),
            (0.10, 0.05, 175, 350, 0.10, 0.0999389460336989),
            (0.15, 0.05, 233, 466, 0.10, 0.0998729361546123),
            (0.20, 0.05, 283, 566, 0.10, 0.0998846018502169),
            (0.25, 0.05, 325, 650, 0.10, 0.0999389460336989),
            (0.30, 0.05, 360, 720, 0.10, 0.0998855455778245),
            (0.35, 0.05, 387, 774, 0.10, 0.0998793343695620),
            (0.40, 0.05, 406, 812, 0.10, 0.0999105394920193),
            (0.45, 0.05, 417, 834, 0.10, 0.0999758102717780),
            (0.50, 0.05, 421, 842, 0.10, 0.0999572047250057),
            (0.55, 0.05, 417, 834, 0.10, 0.0999758102717780),
            (0.60, 0.05, 406, 812, 0.10, 0.0999105394920192),
            (0.65, 0.05, 387, 774, 0.10, 0.0998793343695619),
            (0.70, 0.05, 360, 720, 0.10, 0.0998855455778245),
            (0.75, 0.05, 325, 650, 0.10, 0.0999389460336990),
            (0.80, 0.05, 283, 566, 0.10, 0.0998846018502169),
            (0.85, 0.05, 233, 466, 0.10, 0.0998729361546122),
            (0.90, 0.05, 175, 350, 0.10, 0.0999389460336990),
            (0.95, 0.05, 110, 220, 0.10, 0.0997640746030823),
        ]
    ]
)

case_group_chisq_cc = (
    [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "two-sided", method = "chisq", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="two-sided",
            method="chisq",
            continuity_correction=True,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 901, 451, 0.10, 0.0999073033276827),
            (0.10, 0.50, 965, 483, 0.10, 0.0999901700470706),
            (0.15, 0.50, 1023, 512, 0.10, 0.0999767447198968),
            (0.20, 0.50, 1073, 537, 0.10, 0.0999786557790135),
            (0.25, 0.50, 1115, 558, 0.10, 0.0999940408911913),
            (0.30, 0.50, 1151, 576, 0.10, 0.0999327003131095),
            (0.35, 0.50, 1177, 589, 0.10, 0.0999744769927094),
            (0.40, 0.50, 1197, 599, 0.10, 0.0999419744321274),
            (0.45, 0.50, 1208, 604, 0.10, 0.0999936820676184),
            (0.50, 0.50, 1212, 606, 0.10, 0.0999871003317755),
            (0.55, 0.50, 1208, 604, 0.10, 0.0999936820676184),
            (0.60, 0.50, 1197, 599, 0.10, 0.0999419744321274),
            (0.65, 0.50, 1177, 589, 0.10, 0.0999744769927094),
            (0.70, 0.50, 1151, 576, 0.10, 0.0999327003131095),
            (0.75, 0.50, 1115, 558, 0.10, 0.0999940408911913),
            (0.80, 0.50, 1073, 537, 0.10, 0.0999786557790135),
            (0.85, 0.50, 1023, 512, 0.10, 0.0999767447198968),
            (0.90, 0.50, 965, 483, 0.10, 0.0999901700470706),
            (0.95, 0.50, 901, 451, 0.10, 0.0999073033276827),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "lower", method = "chisq", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="lower",
            method="chisq",
            continuity_correction=True,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 177, 89, 0.10, 0.0996892339388344),
            (0.10, 0.50, 189, 95, 0.10, 0.0996049266639931),
            (0.15, 0.50, 199, 100, 0.10, 0.0996934168107554),
            (0.20, 0.50, 207, 104, 0.10, 0.0999321127516571),
            (0.25, 0.50, 215, 108, 0.10, 0.0998116466683702),
            (0.30, 0.50, 221, 111, 0.10, 0.0998499471089292),
            (0.35, 0.50, 226, 113, 0.10, 0.0999603496541272),
            (0.40, 0.50, 229, 115, 0.10, 0.0998967518613963),
            (0.45, 0.50, 231, 116, 0.10, 0.0999077596880224),
            (0.50, 0.50, 232, 116, 0.10, 0.0999875409854135),
            (0.55, 0.50, 231, 116, 0.10, 0.0999077596880224),
            (0.60, 0.50, 229, 115, 0.10, 0.0998967518613963),
            (0.65, 0.50, 226, 113, 0.10, 0.0999603496541272),
            (0.70, 0.50, 221, 111, 0.10, 0.0998499471089293),
            (0.75, 0.50, 215, 108, 0.10, 0.0998116466683702),
            (0.80, 0.50, 207, 104, 0.10, 0.0999321127516569),
            (0.85, 0.50, 199, 100, 0.10, 0.0996934168107554),
            (0.90, 0.50, 189, 95, 0.10, 0.0996049266639931),
            (0.95, 0.50, 177, 89, 0.10, 0.0996892339388342),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "upper", method = "chisq", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="upper",
            method="chisq",
            continuity_correction=True,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 61, 122, 0.10, 0.0997646313148303),
            (0.10, 0.50, 73, 146, 0.10, 0.0995397633972700),
            (0.15, 0.50, 83, 166, 0.10, 0.0997594577032753),
            (0.20, 0.50, 92, 184, 0.10, 0.0997016309937978),
            (0.25, 0.50, 99, 198, 0.10, 0.0999890983325918),
            (0.30, 0.50, 106, 212, 0.10, 0.0995445923548547),
            (0.35, 0.50, 110, 220, 0.10, 0.0999312151604391),
            (0.40, 0.50, 114, 228, 0.10, 0.0996514224664221),
            (0.45, 0.50, 116, 232, 0.10, 0.0996752796003288),
            (0.50, 0.50, 116, 232, 0.10, 0.0999875409854135),
            (0.55, 0.50, 116, 232, 0.10, 0.0996752796003288),
            (0.60, 0.50, 114, 228, 0.10, 0.0996514224664221),
            (0.65, 0.50, 110, 220, 0.10, 0.0999312151604391),
            (0.70, 0.50, 106, 212, 0.10, 0.0995445923548546),
            (0.75, 0.50, 99, 198, 0.10, 0.0999890983325918),
            (0.80, 0.50, 92, 184, 0.10, 0.0997016309937979),
            (0.85, 0.50, 83, 166, 0.10, 0.0997594577032753),
            (0.90, 0.50, 73, 146, 0.10, 0.0995397633972700),
            (0.95, 0.50, 61, 122, 0.10, 0.0997646313148303),
        ]
    ]
)


case_group_wilson = (
    [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "two-sided", method = "wilson", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="two-sided",
            method="wilson",
            continuity_correction=False,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 837, 419, 0.10, 0.0999260433718746),
            (0.10, 0.50, 901, 451, 0.10, 0.0999768209355942),
            (0.15, 0.50, 959, 480, 0.10, 0.0999412624864418),
            (0.20, 0.50, 1009, 505, 0.10, 0.0999293765478190),
            (0.25, 0.50, 1051, 526, 0.10, 0.0999361442992492),
            (0.30, 0.50, 1085, 543, 0.10, 0.0999587155660015),
            (0.35, 0.50, 1111, 556, 0.10, 0.0999955996540440),
            (0.40, 0.50, 1131, 566, 0.10, 0.0999582982231086),
            (0.45, 0.50, 1143, 572, 0.10, 0.0999366074352342),
            (0.50, 0.50, 1147, 574, 0.10, 0.0999294880969267),
            (0.55, 0.50, 1143, 572, 0.10, 0.0999366074352342),
            (0.60, 0.50, 1131, 566, 0.10, 0.0999582982231086),
            (0.65, 0.50, 1111, 556, 0.10, 0.0999955996540440),
            (0.70, 0.50, 1085, 543, 0.10, 0.0999587155660014),
            (0.75, 0.50, 1051, 526, 0.10, 0.0999361442992492),
            (0.80, 0.50, 1009, 505, 0.10, 0.0999293765478190),
            (0.85, 0.50, 959, 480, 0.10, 0.0999412624864418),
            (0.90, 0.50, 901, 451, 0.10, 0.0999768209355942),
            (0.95, 0.50, 837, 419, 0.10, 0.0999260433718746),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "lower", method = "wilson", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="lower",
            method="wilson",
            continuity_correction=False,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 137, 69, 0.10, 0.0997726775590791),
            (0.10, 0.50, 147, 74, 0.10, 0.0997827850553910),
            (0.15, 0.50, 157, 79, 0.10, 0.0997647470447195),
            (0.20, 0.50, 167, 84, 0.10, 0.0995602340878863),
            (0.25, 0.50, 175, 88, 0.10, 0.0996635453316536),
            (0.30, 0.50, 182, 91, 0.10, 0.0999300229803076),
            (0.35, 0.50, 188, 94, 0.10, 0.0999445908254750),
            (0.40, 0.50, 193, 97, 0.10, 0.0997308543777694),
            (0.45, 0.50, 197, 99, 0.10, 0.0996290278215731),
            (0.50, 0.50, 199, 100, 0.10, 0.0996945998420020),
            (0.55, 0.50, 199, 100, 0.10, 0.0999183129815431),
            (0.60, 0.50, 199, 100, 0.10, 0.0998034563523741),
            (0.65, 0.50, 197, 99, 0.10, 0.0998327224103704),
            (0.70, 0.50, 194, 97, 0.10, 0.0999171548383990),
            (0.75, 0.50, 189, 95, 0.10, 0.0997879363241898),
            (0.80, 0.50, 183, 92, 0.10, 0.0996744773012348),
            (0.85, 0.50, 175, 88, 0.10, 0.0996387229686190),
            (0.90, 0.50, 165, 83, 0.10, 0.0996292351235110),
            (0.95, 0.50, 153, 77, 0.10, 0.0994953284925036),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "upper", method = "wilson", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="upper",
            method="wilson",
            continuity_correction=False,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 62, 124, 0.10, 0.0992617900213629),
            (0.10, 0.50, 72, 144, 0.10, 0.0999809425221021),
            (0.15, 0.50, 81, 162, 0.10, 0.0997923174714839),
            (0.20, 0.50, 88, 176, 0.10, 0.0998207720094969),
            (0.25, 0.50, 94, 188, 0.10, 0.0995398098025460),
            (0.30, 0.50, 98, 196, 0.10, 0.0995629592500131),
            (0.35, 0.50, 100, 200, 0.10, 0.0998677804452224),
            (0.40, 0.50, 101, 202, 0.10, 0.0999609252348309),
            (0.45, 0.50, 101, 202, 0.10, 0.0998709720526048),
            (0.50, 0.50, 100, 200, 0.10, 0.0996115975166691),
            (0.55, 0.50, 97, 194, 0.10, 0.0996786839703007),
            (0.60, 0.50, 93, 186, 0.10, 0.0995942647840674),
            (0.65, 0.50, 87, 174, 0.10, 0.0998976833084366),
            (0.70, 0.50, 81, 162, 0.10, 0.0995460708948986),
            (0.75, 0.50, 73, 146, 0.10, 0.0996872917780802),
            (0.80, 0.50, 64, 128, 0.10, 0.0998892094465562),
            (0.85, 0.50, 55, 110, 0.10, 0.0996180821195150),
            (0.90, 0.50, 46, 92, 0.10, 0.0991724825072867),
            (0.95, 0.50, 37, 74, 0.10, 0.0998580177167584),
        ]
    ]
    + [
        # treatment_proportion = 0.10, reference_proportion = 0.05 to 0.95 by 0.05, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "lower", method = "wilson", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="lower",
            method="wilson",
            continuity_correction=False,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.10, 0.05, 25, 50, 0.10, 0.0996510349111803),
            (0.10, 0.10, 31, 62, 0.10, 0.0995045902468680),
            (0.10, 0.15, 36, 72, 0.10, 0.0992118074383943),
            (0.10, 0.20, 40, 80, 0.10, 0.0990406644626776),
            (0.10, 0.25, 43, 86, 0.10, 0.0990413786948773),
            (0.10, 0.30, 45, 90, 0.10, 0.0992258924120226),
            (0.10, 0.35, 46, 92, 0.10, 0.0996043575653431),
            (0.10, 0.40, 47, 94, 0.10, 0.0992169219274573),
            (0.10, 0.45, 47, 94, 0.10, 0.0990765106237289),
            (0.10, 0.50, 46, 92, 0.10, 0.0991724825072869),
            (0.10, 0.55, 44, 88, 0.10, 0.0995168371481482),
            (0.10, 0.60, 42, 84, 0.10, 0.0991275282907580),
            (0.10, 0.65, 39, 78, 0.10, 0.0989682251891008),
            (0.10, 0.70, 35, 70, 0.10, 0.0990553619362583),
            (0.10, 0.75, 30, 60, 0.10, 0.0994366070158341),
            (0.10, 0.80, 25, 50, 0.10, 0.0988052811182918),
            (0.10, 0.85, 18, 36, 0.10, 0.0998861989601409),
            (0.10, 0.90, 11, 22, 0.10, 0.0997862261117957),
            (0.10, 0.95, 4, 8, 0.10, 0.0987669543429515),
        ]
    ]
    + [
        # treatment_proportion = 0.90, reference_proportion = 0.05 to 0.95 by 0.05, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "upper", method = "wilson", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="upper",
            method="wilson",
            continuity_correction=False,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.90, 0.05, 4, 8, 0.10, 0.0987669543429515),
            (0.90, 0.10, 11, 22, 0.10, 0.0997862261117957),
            (0.90, 0.15, 18, 36, 0.10, 0.0998861989601409),
            (0.90, 0.20, 25, 50, 0.10, 0.0988052811182920),
            (0.90, 0.25, 30, 60, 0.10, 0.0994366070158341),
            (0.90, 0.30, 35, 70, 0.10, 0.0990553619362577),
            (0.90, 0.35, 39, 78, 0.10, 0.0989682251891003),
            (0.90, 0.40, 42, 84, 0.10, 0.0991275282907581),
            (0.90, 0.45, 44, 88, 0.10, 0.0995168371481478),
            (0.90, 0.50, 46, 92, 0.10, 0.0991724825072867),
            (0.90, 0.55, 47, 94, 0.10, 0.0990765106237286),
            (0.90, 0.60, 47, 94, 0.10, 0.0992169219274571),
            (0.90, 0.65, 46, 92, 0.10, 0.0996043575653428),
            (0.90, 0.70, 45, 90, 0.10, 0.0992258924120225),
            (0.90, 0.75, 43, 86, 0.10, 0.0990413786948769),
            (0.90, 0.80, 40, 80, 0.10, 0.0990406644626772),
            (0.90, 0.85, 36, 72, 0.10, 0.0992118074383938),
            (0.90, 0.90, 31, 62, 0.10, 0.0995045902468680),
            (0.90, 0.95, 25, 50, 0.10, 0.0996510349111806),
        ]
    ]
)


case_group_wilson_cc = (
    [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "two-sided", method = "wilson", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="two-sided",
            method="wilson",
            continuity_correction=True,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 881, 441, 0.10, 0.0999012407337210),
            (0.10, 0.50, 945, 473, 0.10, 0.0999803215207654),
            (0.15, 0.50, 1003, 502, 0.10, 0.0999514227585547),
            (0.20, 0.50, 1053, 527, 0.10, 0.0999381500362536),
            (0.25, 0.50, 1095, 548, 0.10, 0.0999408805835880),
            (0.30, 0.50, 1129, 565, 0.10, 0.0999588518213822),
            (0.35, 0.50, 1155, 578, 0.10, 0.0999914355359657),
            (0.40, 0.50, 1175, 588, 0.10, 0.0999521845293668),
            (0.45, 0.50, 1187, 594, 0.10, 0.0999292671620007),
            (0.50, 0.50, 1190, 595, 0.10, 0.0999926887617467),
            (0.55, 0.50, 1187, 594, 0.10, 0.0999292671619999),
            (0.60, 0.50, 1175, 588, 0.10, 0.0999521845293675),
            (0.65, 0.50, 1155, 578, 0.10, 0.0999914355359655),
            (0.70, 0.50, 1129, 565, 0.10, 0.0999588518213833),
            (0.75, 0.50, 1095, 548, 0.10, 0.0999408805835884),
            (0.80, 0.50, 1053, 527, 0.10, 0.0999381500362552),
            (0.85, 0.50, 1003, 502, 0.10, 0.0999514227585546),
            (0.90, 0.50, 945, 473, 0.10, 0.0999803215207645),
            (0.95, 0.50, 881, 441, 0.10, 0.0999012407337218),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "lower", method = "wilson", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="lower",
            method="wilson",
            continuity_correction=True,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 159, 80, 0.10, 0.0993960076793748),
            (0.10, 0.50, 169, 85, 0.10, 0.0996069701608713),
            (0.15, 0.50, 179, 90, 0.10, 0.0996704963260702),
            (0.20, 0.50, 188, 94, 0.10, 0.0999886065925256),
            (0.25, 0.50, 197, 99, 0.10, 0.0996101774362115),
            (0.30, 0.50, 203, 102, 0.10, 0.0999239653766411),
            (0.35, 0.50, 209, 105, 0.10, 0.0999337049327459),
            (0.40, 0.50, 215, 108, 0.10, 0.0996504837335163),
            (0.45, 0.50, 218, 109, 0.10, 0.0999371677717659),
            (0.50, 0.50, 220, 110, 0.10, 0.0999871987690875),
            (0.55, 0.50, 221, 111, 0.10, 0.0998048150238618),
            (0.60, 0.50, 221, 111, 0.10, 0.0996924675327923),
            (0.65, 0.50, 219, 110, 0.10, 0.0997187010783577),
            (0.70, 0.50, 215, 108, 0.10, 0.0998805230381572),
            (0.75, 0.50, 211, 106, 0.10, 0.0996816266870509),
            (0.80, 0.50, 205, 103, 0.10, 0.0995819911212780),
            (0.85, 0.50, 197, 99, 0.10, 0.0995586887804044),
            (0.90, 0.50, 187, 94, 0.10, 0.0995622692157384),
            (0.95, 0.50, 175, 88, 0.10, 0.0994482472166248),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "upper", method = "wilson", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="upper",
            method="wilson",
            continuity_correction=True,
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 72, 144, 0.10, 0.0998670172789121),
            (0.10, 0.50, 83, 166, 0.10, 0.0997597375410162),
            (0.15, 0.50, 92, 184, 0.10, 0.0996395367759446),
            (0.20, 0.50, 99, 198, 0.10, 0.0996995392634417),
            (0.25, 0.50, 104, 208, 0.10, 0.0999762667406588),
            (0.30, 0.50, 108, 216, 0.10, 0.0999828529204739),
            (0.35, 0.50, 111, 222, 0.10, 0.0997819977650716),
            (0.40, 0.50, 112, 224, 0.10, 0.0998702672394812),
            (0.45, 0.50, 112, 224, 0.10, 0.0997799796341910),
            (0.50, 0.50, 110, 220, 0.10, 0.0999871987690875),
            (0.55, 0.50, 108, 216, 0.10, 0.0995671382819680),
            (0.60, 0.50, 103, 206, 0.10, 0.0999415804305930),
            (0.65, 0.50, 98, 196, 0.10, 0.0996902244754653),
            (0.70, 0.50, 91, 182, 0.10, 0.0998148829057031),
            (0.75, 0.50, 83, 166, 0.10, 0.0998483241498126),
            (0.80, 0.50, 74, 148, 0.10, 0.0998345879924479),
            (0.85, 0.50, 64, 128, 0.10, 0.0998986965097310),
            (0.90, 0.50, 54, 108, 0.10, 0.0995471443790187),
            (0.95, 0.50, 44, 88, 0.10, 0.0994759319428284),
        ]
    ]
)


case_group_farrington_manning = (
    [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "two-sided", method = "farrington_manning"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="two-sided",
            method="farrington_manning",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 835, 418, 0.10, 0.0999653833199517),
            (0.10, 0.50, 901, 451, 0.10, 0.0999844856171526),
            (0.15, 0.50, 959, 480, 0.10, 0.0999953650370744),
            (0.20, 0.50, 1010, 505, 0.10, 0.0999969769855610),
            (0.25, 0.50, 1053, 527, 0.10, 0.0999357421133943),
            (0.30, 0.50, 1087, 544, 0.10, 0.0999695049935674),
            (0.35, 0.50, 1114, 557, 0.10, 0.0999991288004462),
            (0.40, 0.50, 1133, 567, 0.10, 0.0999799665245749),
            (0.45, 0.50, 1145, 573, 0.10, 0.0999603963214137),
            (0.50, 0.50, 1149, 575, 0.10, 0.0999539383555871),
            (0.55, 0.50, 1145, 573, 0.10, 0.0999603963214137),
            (0.60, 0.50, 1133, 567, 0.10, 0.0999799665245749),
            (0.65, 0.50, 1114, 557, 0.10, 0.0999991288004462),
            (0.70, 0.50, 1087, 544, 0.10, 0.0999695049935674),
            (0.75, 0.50, 1053, 527, 0.10, 0.0999357421133943),
            (0.80, 0.50, 1010, 505, 0.10, 0.0999969769855610),
            (0.85, 0.50, 959, 480, 0.10, 0.0999953650370744),
            (0.90, 0.50, 901, 451, 0.10, 0.0999844856171526),
            (0.95, 0.50, 835, 418, 0.10, 0.0999653833199517),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "lower", method = "farrington_manning"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="lower",
            method="farrington_manning",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 141, 71, 0.10, 0.0998962116132077),
            (0.10, 0.50, 153, 77, 0.10, 0.0995849278417688),
            (0.15, 0.50, 163, 82, 0.10, 0.0996188408152449),
            (0.20, 0.50, 171, 86, 0.10, 0.0999164244141125),
            (0.25, 0.50, 179, 90, 0.10, 0.0998874186279859),
            (0.30, 0.50, 187, 94, 0.10, 0.0995555982876445),
            (0.35, 0.50, 191, 96, 0.10, 0.0999459253924408),
            (0.40, 0.50, 196, 98, 0.10, 0.0999247933823534),
            (0.45, 0.50, 199, 100, 0.10, 0.0997435665958891),
            (0.50, 0.50, 201, 101, 0.10, 0.0996492868272697),
            (0.55, 0.50, 201, 101, 0.10, 0.0997083507956864),
            (0.60, 0.50, 199, 100, 0.10, 0.0999142759014823),
            (0.65, 0.50, 197, 99, 0.10, 0.0997620704172411),
            (0.70, 0.50, 193, 97, 0.10, 0.0997327456413639),
            (0.75, 0.50, 187, 94, 0.10, 0.0998168684782387),
            (0.80, 0.50, 180, 90, 0.10, 0.0999233916695102),
            (0.85, 0.50, 171, 86, 0.10, 0.0996924807490623),
            (0.90, 0.50, 159, 80, 0.10, 0.0999626461078095),
            (0.95, 0.50, 147, 74, 0.10, 0.0994856649817564),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "upper", method = "farrington_manning"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="upper",
            method="farrington_manning",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 56, 112, 0.10, 0.0994730872135303),
            (0.10, 0.50, 69, 138, 0.10, 0.0993299296715353),
            (0.15, 0.50, 78, 156, 0.10, 0.0999809367160575),
            (0.20, 0.50, 86, 172, 0.10, 0.0998605928795459),
            (0.25, 0.50, 92, 184, 0.10, 0.0999176339600715),
            (0.30, 0.50, 97, 194, 0.10, 0.0996655930349130),
            (0.35, 0.50, 100, 200, 0.10, 0.0996951779394590),
            (0.40, 0.50, 102, 204, 0.10, 0.0995097901269606),
            (0.45, 0.50, 102, 204, 0.10, 0.0996246817715474),
            (0.50, 0.50, 101, 202, 0.10, 0.0995657095308883),
            (0.55, 0.50, 98, 196, 0.10, 0.0998427932682601),
            (0.60, 0.50, 94, 188, 0.10, 0.0999946929523506),
            (0.65, 0.50, 90, 180, 0.10, 0.0995057168519942),
            (0.70, 0.50, 84, 168, 0.10, 0.0994389557111998),
            (0.75, 0.50, 76, 152, 0.10, 0.0999347702097918),
            (0.80, 0.50, 68, 136, 0.10, 0.0999051361242086),
            (0.85, 0.50, 60, 120, 0.10, 0.0993197131931522),
            (0.90, 0.50, 51, 102, 0.10, 0.0990859104634182),
            (0.95, 0.50, 41, 82, 0.10, 0.0999275440326930),
        ]
    ]
)

case_group_miettinen_nurminen = (
    [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "two-sided", method = "miettinen_nurminen"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="two-sided",
            method="miettinen_nurminen",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 836, 418, 0.10, 0.0999996228567564),
            (0.10, 0.50, 903, 452, 0.10, 0.0999110832770129),
            (0.15, 0.50, 961, 481, 0.10, 0.0999263197149514),
            (0.20, 0.50, 1011, 506, 0.10, 0.0999434357678580),
            (0.25, 0.50, 1053, 527, 0.10, 0.0999672619762495),
            (0.30, 0.50, 1088, 544, 0.10, 0.0999863553704662),
            (0.35, 0.50, 1115, 558, 0.10, 0.0999536417821418),
            (0.40, 0.50, 1134, 567, 0.10, 0.0999949025235256),
            (0.45, 0.50, 1145, 573, 0.10, 0.0999894040437367),
            (0.50, 0.50, 1149, 575, 0.10, 0.0999828436494676),
            (0.55, 0.50, 1145, 573, 0.10, 0.0999894040437367),
            (0.60, 0.50, 1134, 567, 0.10, 0.0999949025235256),
            (0.65, 0.50, 1115, 558, 0.10, 0.0999536417821418),
            (0.70, 0.50, 1088, 544, 0.10, 0.0999863553704662),
            (0.75, 0.50, 1053, 527, 0.10, 0.0999672619762495),
            (0.80, 0.50, 1011, 506, 0.10, 0.0999434357678579),
            (0.85, 0.50, 961, 481, 0.10, 0.0999263197149514),
            (0.90, 0.50, 903, 452, 0.10, 0.0999110832770130),
            (0.95, 0.50, 836, 418, 0.10, 0.0999996228567563),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 2, distance = 0.1, conf_level = 0.95, interval_type = "lower", method = "miettinen_nurminen"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="lower",
            method="miettinen_nurminen",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 143, 72, 0.10, 0.0994485213455888),
            (0.10, 0.50, 153, 77, 0.10, 0.0997945799420560),
            (0.15, 0.50, 163, 82, 0.10, 0.0998162378239202),
            (0.20, 0.50, 173, 87, 0.10, 0.0995426080219532),
            (0.25, 0.50, 180, 90, 0.10, 0.0999986761924429),
            (0.30, 0.50, 187, 94, 0.10, 0.0997290286491775),
            (0.35, 0.50, 193, 97, 0.10, 0.0996076540248368),
            (0.40, 0.50, 197, 99, 0.10, 0.0996731238050746),
            (0.45, 0.50, 199, 100, 0.10, 0.0999081726990137),
            (0.50, 0.50, 201, 101, 0.10, 0.0998125170827397),
            (0.55, 0.50, 201, 101, 0.10, 0.0998720666230723),
            (0.60, 0.50, 200, 100, 0.10, 0.0999937916885641),
            (0.65, 0.50, 197, 99, 0.10, 0.0999299018822514),
            (0.70, 0.50, 193, 97, 0.10, 0.0999042871198930),
            (0.75, 0.50, 187, 94, 0.10, 0.0999942606253977),
            (0.80, 0.50, 181, 91, 0.10, 0.0996366434809437),
            (0.85, 0.50, 171, 86, 0.10, 0.0998860755223686),
            (0.90, 0.50, 161, 81, 0.10, 0.0995522851783059),
            (0.95, 0.50, 147, 74, 0.10, 0.0997075509932679),
        ]
    ]
    + [
        # treatment_proportion = 0.05 to 0.95 by 0.05, reference_proportion = 0.50, ratio = 0.5, distance = 0.1, conf_level = 0.95, interval_type = "upper", method = "miettinen_nurminen"
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            conf_level=0.95,
            interval_type="upper",
            method="miettinen_nurminen",
            distance=distance,
            actual_distance=actual_distance,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, distance, actual_distance in [
            (0.05, 0.50, 56, 112, 0.10, 0.0998032921106434),
            (0.10, 0.50, 69, 138, 0.10, 0.0995911007629445),
            (0.15, 0.50, 79, 158, 0.10, 0.0995289096386237),
            (0.20, 0.50, 87, 174, 0.10, 0.0994569602938349),
            (0.25, 0.50, 93, 186, 0.10, 0.0995447046356399),
            (0.30, 0.50, 97, 194, 0.10, 0.0998414653609541),
            (0.35, 0.50, 100, 200, 0.10, 0.0998640989425020),
            (0.40, 0.50, 102, 204, 0.10, 0.0996735380850119),
            (0.45, 0.50, 102, 204, 0.10, 0.0997871499241058),
            (0.50, 0.50, 101, 202, 0.10, 0.0997282599637136),
            (0.55, 0.50, 99, 198, 0.10, 0.0995122337747879),
            (0.60, 0.50, 95, 190, 0.10, 0.0996526729064826),
            (0.65, 0.50, 90, 180, 0.10, 0.0996832943338271),
            (0.70, 0.50, 84, 168, 0.10, 0.0996274114497600),
            (0.75, 0.50, 77, 154, 0.10, 0.0995237428472630),
            (0.80, 0.50, 69, 138, 0.10, 0.0994498853685351),
            (0.85, 0.50, 60, 120, 0.10, 0.0995776579692114),
            (0.90, 0.50, 51, 102, 0.10, 0.0993887850868388),
            (0.95, 0.50, 42, 84, 0.10, 0.0991736299735178),
        ]
    ]
)


case_group = case_group_chisq + case_group_chisq_cc + case_group_wilson + case_group_wilson_cc + case_group_farrington_manning + case_group_miettinen_nurminen


def test_size_solve_distance(case: TestCase) -> None:
    assert round(
        solve_distance(
            treatment_proportion=case.treatment_proportion,
            reference_proportion=case.reference_proportion,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            conf_level=case.conf_level,
            interval_type=case.interval_type,
            method=case.method,
            continuity_correction=case.continuity_correction,
        ),
        6,
    ) == round(case.actual_distance, 6)


def test_solve_size(case: TestCase) -> None:
    ratio = case.treatment_size / case.reference_size
    assert solve_size(
        treatment_proportion=case.treatment_proportion,
        reference_proportion=case.reference_proportion,
        distance=case.distance,
        ratio=ratio,
        conf_level=case.conf_level,
        interval_type=case.interval_type,
        method=case.method,
        continuity_correction=case.continuity_correction,
    ) == (case.treatment_size, case.reference_size)


def test_solve_treatment_proportion(case: TestCase) -> None:
    treatment_proportion_solutions = []
    try:
        res = solve_treatment_proportion(
            reference_proportion=case.reference_proportion,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            distance=case.actual_distance,
            conf_level=case.conf_level,
            interval_type=case.interval_type,
            method=case.method,
            continuity_correction=case.continuity_correction,
            direction="greater",
        )
        treatment_proportion_solutions.append(res)
    except SolutionNotFoundError:
        pass

    try:
        res = solve_treatment_proportion(
            reference_proportion=case.reference_proportion,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            distance=case.actual_distance,
            conf_level=case.conf_level,
            interval_type=case.interval_type,
            method=case.method,
            continuity_correction=case.continuity_correction,
            direction="less",
        )
        treatment_proportion_solutions.append(res)
    except SolutionNotFoundError:
        pass

    assert case.treatment_proportion in [round(x, 2) for x in treatment_proportion_solutions]


def test_solve_reference_proportion(case: TestCase) -> None:
    reference_proportion_solutions = []
    try:
        res = solve_reference_proportion(
            treatment_proportion=case.treatment_proportion,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            distance=case.actual_distance,
            conf_level=case.conf_level,
            interval_type=case.interval_type,
            method=case.method,
            continuity_correction=case.continuity_correction,
            direction="greater",
        )
        reference_proportion_solutions.append(res)
    except SolutionNotFoundError:
        pass

    try:
        res = solve_reference_proportion(
            treatment_proportion=case.treatment_proportion,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            distance=case.actual_distance,
            conf_level=case.conf_level,
            interval_type=case.interval_type,
            method=case.method,
            continuity_correction=case.continuity_correction,
            direction="less",
        )
        reference_proportion_solutions.append(res)
    except SolutionNotFoundError:
        pass

    assert case.reference_proportion in [round(x, 2) for x in reference_proportion_solutions]
