# Validation Software: PASS 15
# Module: Tests for Two Proportions

from dataclasses import dataclass
from typing import Literal

from pystatpower.proportion.independent.inequality import solve_power, solve_size, solve_treatment_proportion, solve_reference_proportion

from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    treatment_proportion: float
    reference_proportion: float
    treatment_size: int
    reference_size: int
    alternative: Literal["one-sided", "two-sided"]
    alpha: float
    method: Literal["z-pooled", "z-unpooled"]
    continuity_correction: bool
    power: float
    actual_power: float

    ratio: float | None = None

    def __post_init__(self) -> None:
        if self.ratio is None:
            self.ratio = self.treatment_size / self.reference_size


case_group_pooled = (
    [
        # treatment_proportion = 0.98, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 0.5, alternative = "two-sided", method = "z-pooled", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.98, 0.80, 46, 92, 0.8023671292122600),
            (0.98, 0.81, 50, 100, 0.8065989930742810),
            (0.98, 0.82, 54, 108, 0.8050093403205440),
            (0.98, 0.83, 59, 118, 0.8068356651299450),
            (0.98, 0.84, 64, 128, 0.8017362506122160),
            (0.98, 0.85, 71, 142, 0.8048357148847580),
            (0.98, 0.86, 79, 158, 0.8052019538317560),
            (0.98, 0.87, 88, 176, 0.8010972313493260),
            (0.98, 0.88, 100, 200, 0.8012534546867960),
            (0.98, 0.89, 115, 230, 0.8000525702219660),
            (0.98, 0.90, 136, 272, 0.8037552679278470),
            (0.98, 0.91, 163, 326, 0.8020906342439550),
            (0.98, 0.92, 202, 404, 0.8011181227229140),
            (0.98, 0.93, 262, 524, 0.8003649427583080),
            (0.98, 0.94, 364, 728, 0.8001650778789080),
            (0.98, 0.95, 566, 1132, 0.8007452499757070),
        ]
    ]
    + [
        # treatment_proportion = 0.98, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 2, alternative = "one-sided", method = "z-pooled", continuity_orrection = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="one-sided",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
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
    + [
        # treatment_proportion = 0.78, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 2, alternative = "one-sided", method = "z-pooled", continuity_orrection = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="one-sided",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.78, 0.80, 9809, 4905, 0.8000319036059040),
            (0.78, 0.81, 4293, 2147, 0.8001390799794710),
            (0.78, 0.82, 2375, 1188, 0.8000135158236820),
            (0.78, 0.83, 1495, 748, 0.8001788598068810),
            (0.78, 0.84, 1021, 511, 0.8005917317355860),
            (0.78, 0.85, 736, 368, 0.8000037747338040),
            (0.78, 0.86, 553, 277, 0.8005867774435390),
            (0.78, 0.87, 429, 215, 0.8013425070844380),
            (0.78, 0.88, 340, 170, 0.8002013100907780),
            (0.78, 0.89, 275, 138, 0.8012772590193300),
            (0.78, 0.90, 226, 113, 0.8003425148855670),
            (0.78, 0.91, 188, 94, 0.8001652200442540),
            (0.78, 0.92, 159, 80, 0.8044563933687560),
            (0.78, 0.93, 135, 68, 0.8050152271398630),
            (0.78, 0.94, 115, 58, 0.8037494967565390),
            (0.78, 0.95, 99, 50, 0.8043821469834260),
        ]
    ]
)

case_group_pooled_cc = (
    [
        # treatment_proportion = 0.98, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 0.5, alternative = "two-sided", method = "z-pooled", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
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
    + [
        # treatment_proportion = 0.98, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 2, alternative = "one-sided", method = "z-pooled", continuity_orrection = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="one-sided",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.98, 0.80, 77, 39, 0.8013493076015370),
            (0.98, 0.81, 83, 42, 0.8022126910009500),
            (0.98, 0.82, 90, 45, 0.8013025643517770),
            (0.98, 0.83, 97, 49, 0.8003876058627560),
            (0.98, 0.84, 107, 54, 0.8042398201040090),
            (0.98, 0.85, 117, 59, 0.8016039576871890),
            (0.98, 0.86, 130, 65, 0.8005302909928110),
            (0.98, 0.87, 145, 73, 0.8002556648080750),
            (0.98, 0.88, 165, 83, 0.8016557347415190),
            (0.98, 0.89, 190, 95, 0.8007629269440840),
            (0.98, 0.90, 223, 112, 0.8023196943428530),
            (0.98, 0.91, 267, 134, 0.8010707710135000),
            (0.98, 0.92, 331, 166, 0.8007992869225470),
            (0.98, 0.93, 429, 215, 0.8001131585861340),
            (0.98, 0.94, 597, 299, 0.8006391586573570),
            (0.98, 0.95, 927, 464, 0.8003508167163740),
        ]
    ]
    + [
        # treatment_proportion = 0.78, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 2, alternative = "one-sided", method = "z-pooled", continuity_orrection = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="one-sided",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.78, 0.80, 9959, 4980, 0.8000546656671780),
            (0.78, 0.81, 4391, 2196, 0.8000066492343880),
            (0.78, 0.82, 2451, 1226, 0.8002778737294480),
            (0.78, 0.83, 1555, 778, 0.8003339855431180),
            (0.78, 0.84, 1069, 535, 0.8000311939913820),
            (0.78, 0.85, 779, 390, 0.8007873713433710),
            (0.78, 0.86, 590, 295, 0.8001451744075990),
            (0.78, 0.87, 461, 231, 0.8006374108503390),
            (0.78, 0.88, 369, 185, 0.8005754722424370),
            (0.78, 0.89, 301, 151, 0.8002702890075350),
            (0.78, 0.90, 251, 126, 0.8028200290640030),
            (0.78, 0.91, 211, 106, 0.8030269694909870),
            (0.78, 0.92, 179, 90, 0.8022942868295720),
            (0.78, 0.93, 153, 77, 0.8005992230654660),
            (0.78, 0.94, 133, 67, 0.8033653265275570),
            (0.78, 0.95, 116, 58, 0.8011849189998360),
        ]
    ]
)

case_group_unpooled = (
    [
        # treatment_proportion = 0.98, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 0.5, alternative = "two-sided", method = "z-unpooled", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.98, 0.80, 30, 60, 0.8112583887383420),
            (0.98, 0.81, 32, 64, 0.8033105199318620),
            (0.98, 0.82, 35, 70, 0.8039674074153470),
            (0.98, 0.83, 39, 78, 0.8101631273574280),
            (0.98, 0.84, 43, 86, 0.8091131751395700),
            (0.98, 0.85, 47, 94, 0.8011169775610330),
            (0.98, 0.86, 53, 106, 0.8026582615981410),
            (0.98, 0.87, 60, 120, 0.8013031325187410),
            (0.98, 0.88, 69, 138, 0.8011482793041890),
            (0.98, 0.89, 81, 162, 0.8029815988176530),
            (0.98, 0.90, 96, 192, 0.8002632102161500),
            (0.98, 0.91, 118, 236, 0.8019938502967920),
            (0.98, 0.92, 149, 298, 0.8002542474042400),
            (0.98, 0.93, 199, 398, 0.8015727586721130),
            (0.98, 0.94, 284, 568, 0.8000563176754960),
            (0.98, 0.95, 458, 916, 0.8001640734234750),
        ]
    ]
    + [
        # treatment_proportion = 0.98, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 2, alternative = "one-sided", method = "z-unpooled", continuity_orrection = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="one-sided",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.98, 0.80, 83, 42, 0.8078434869319800),
            (0.98, 0.81, 89, 45, 0.8044630880911500),
            (0.98, 0.82, 97, 49, 0.8057006767816140),
            (0.98, 0.83, 105, 53, 0.8024265781239410),
            (0.98, 0.84, 115, 58, 0.8014921233712060),
            (0.98, 0.85, 127, 64, 0.8012127633464930),
            (0.98, 0.86, 142, 71, 0.8001825417690700),
            (0.98, 0.87, 159, 80, 0.8011709506158960),
            (0.98, 0.88, 181, 91, 0.8016448905131630),
            (0.98, 0.89, 209, 105, 0.8022187965816410),
            (0.98, 0.90, 245, 123, 0.8017787162215530),
            (0.98, 0.91, 293, 147, 0.8001607360265670),
            (0.98, 0.92, 363, 182, 0.8002343731107060),
            (0.98, 0.93, 471, 236, 0.8013005578354100),
            (0.98, 0.94, 649, 325, 0.8002154419101310),
            (0.98, 0.95, 999, 500, 0.8001587908208420),
        ]
    ]
    + [
        # treatment_proportion = 0.78, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 2, alternative = "one-sided", method = "z-unpooled", continuity_orrection = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="one-sided",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.78, 0.80, 9647, 4824, 0.8000560043292710),
            (0.78, 0.81, 4181, 2091, 0.8000755347578280),
            (0.78, 0.82, 2290, 1145, 0.8000152993659500),
            (0.78, 0.83, 1425, 713, 0.8002456889809310),
            (0.78, 0.84, 961, 481, 0.8005835267231750),
            (0.78, 0.85, 683, 342, 0.8001516438601670),
            (0.78, 0.86, 506, 253, 0.8001843270044550),
            (0.78, 0.87, 385, 193, 0.8001025159758080),
            (0.78, 0.88, 301, 151, 0.8014259021270660),
            (0.78, 0.89, 239, 120, 0.8019848732916940),
            (0.78, 0.90, 192, 96, 0.8007284238417560),
            (0.78, 0.91, 156, 78, 0.8005781457185360),
            (0.78, 0.92, 128, 64, 0.8010285503687910),
            (0.78, 0.93, 105, 53, 0.8005560327340640),
            (0.78, 0.94, 87, 44, 0.8008876726012490),
            (0.78, 0.95, 73, 37, 0.8050784404642460),
        ]
    ]
)

case_group_unpooled_cc = (
    [
        # treatment_proportion = 0.98, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 0.5, alternative = "two-sided", method = "z-unpooled", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="two-sided",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
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
    + [
        # treatment_proportion = 0.98, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 2, alternative = "one-sided", method = "z-unpooled", continuity_orrection = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="one-sided",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.98, 0.80, 99, 50, 0.8077780117995080),
            (0.98, 0.81, 105, 53, 0.8002978427665710),
            (0.98, 0.82, 115, 58, 0.8055721603540280),
            (0.98, 0.83, 125, 63, 0.8051916569613080),
            (0.98, 0.84, 137, 69, 0.8060537341668410),
            (0.98, 0.85, 149, 75, 0.8005195387480430),
            (0.98, 0.86, 166, 83, 0.8000203254647120),
            (0.98, 0.87, 185, 93, 0.8004181124580120),
            (0.98, 0.88, 211, 106, 0.8038462870045620),
            (0.98, 0.89, 241, 121, 0.8018160876850860),
            (0.98, 0.90, 281, 141, 0.8013297416840050),
            (0.98, 0.91, 335, 168, 0.8008039637080280),
            (0.98, 0.92, 413, 207, 0.8018293056226130),
            (0.98, 0.93, 529, 265, 0.8010324830004510),
            (0.98, 0.94, 723, 362, 0.8007724969438890),
            (0.98, 0.95, 1097, 549, 0.8002619429416010),
        ]
    ]
    + [
        # treatment_proportion = 0.78, reference_proportion = 0.80 to 0.95 by 0.01, ratio = 2, alternative = "one-sided", method = "z-unpooled", continuity_orrection = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="one-sided",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.78, 0.80, 9796, 4898, 0.8000122376306930),
            (0.78, 0.81, 4281, 2141, 0.8001303335769720),
            (0.78, 0.82, 2365, 1183, 0.8002254652420710),
            (0.78, 0.83, 1485, 743, 0.8004126966755080),
            (0.78, 0.84, 1009, 505, 0.8000213473638650),
            (0.78, 0.85, 725, 363, 0.8000252398524380),
            (0.78, 0.86, 543, 272, 0.8007536563066810),
            (0.78, 0.87, 419, 210, 0.8014574572840100),
            (0.78, 0.88, 330, 165, 0.8002957149950980),
            (0.78, 0.89, 265, 133, 0.8010705467442460),
            (0.78, 0.90, 216, 108, 0.8001634445721430),
            (0.78, 0.91, 179, 90, 0.8035060646017460),
            (0.78, 0.92, 149, 75, 0.8035435464734160),
            (0.78, 0.93, 125, 63, 0.8036278320445790),
            (0.78, 0.94, 105, 53, 0.8014607929519660),
            (0.78, 0.95, 89, 45, 0.8012309098740600),
        ]
    ]
)

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
            method=case.method,
            continuity_correction=case.continuity_correction,
        ),
        6,
    ) == round(case.actual_power, 6)


def test_solve_size(case: TestCase) -> None:
    assert solve_size(
        treatment_proportion=case.treatment_proportion,
        reference_proportion=case.reference_proportion,
        alternative=case.alternative,
        ratio=case.ratio,
        alpha=case.alpha,
        power=case.power,
        method=case.method,
        continuity_correction=case.continuity_correction,
    ) == (case.treatment_size, case.reference_size)


def test_solve_treatment_proportion(case: TestCase) -> None:
    direction = "greater" if case.treatment_proportion > case.reference_proportion else "less"
    assert (
        round(
            solve_treatment_proportion(
                reference_proportion=case.reference_proportion,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                continuity_correction=case.continuity_correction,
                direction=direction,
            ),
            2,
        )
        == case.treatment_proportion
    )


def test_solve_reference_proportion(case: TestCase) -> None:
    direction = "greater" if case.reference_proportion > case.treatment_proportion else "less"
    assert (
        round(
            solve_reference_proportion(
                treatment_proportion=case.treatment_proportion,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                continuity_correction=case.continuity_correction,
                direction=direction,
            ),
            2,
        )
        == case.reference_proportion
    )
