# Validation Software: PASS 2025
# Module: Two-Sample Z-Tests Assuming Equal Variance
#         Two-Sample Z-Tests Allowing Unequal Variance
#         Two-Sample T-Tests Assuming Equal Variance
#         Two-Sample T-Tests Assuming Unequal Variance
# Two-Sample T-Test Assuming Unequal Variance with Degree of Freedom Adjusted by Welch's Methos is not available in PASS.

from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.mean.independent.inequality import _verify_mean_and_get_diff, _verify_std_and_get_std, solve_power, solve_size, solve_diff, solve_treatment_mean, solve_reference_mean, solve_treatment_std, solve_reference_std

from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    treatment_mean: float | None = None
    reference_mean: float | None = None
    diff: float | None
    treatment_std: float | None = None
    reference_std: float | None = None
    std: float | None = None
    treatment_size: int
    reference_size: int
    alternative: Literal["two-sided", "less", "greater"]
    alpha: float
    power: float
    actual_power: float
    dist: Literal["z", "t"]
    equal_var: bool
    approx_t_method: Literal["welch", "satterthwaite"] | None = None

    direction: Literal["greater", "less"] | None = None

    def __post_init__(self):
        self.diff = _verify_mean_and_get_diff(self.treatment_mean, self.reference_mean, self.diff)
        self.std = _verify_std_and_get_std(self.treatment_std, self.reference_std, self.std, self.dist, self.equal_var)


case_group_z_equal_var = (
    [
        # treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.05, power = 0.80, alternative = "two-sided", dist = "z", equal_var = True
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
            dist="z",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 377, 189, 0.800956488931548),
            (41, 30, 311, 156, 0.800385341930126),
            (42, 30, 261, 131, 0.800055652573404),
            (43, 30, 223, 112, 0.801297203015291),
            (44, 30, 193, 97, 0.802936652062447),
            (45, 30, 167, 84, 0.800521655011479),
            (46, 30, 147, 74, 0.801325999098933),
            (47, 30, 131, 66, 0.803887830163156),
            (48, 30, 117, 59, 0.804625729911788),
            (49, 30, 105, 53, 0.804845167679882),
            (50, 30, 95, 48, 0.806073400959281),
            (51, 30, 85, 43, 0.801073019251286),
            (52, 30, 78, 39, 0.800805007022753),
            (53, 30, 71, 36, 0.802438419244675),
            (54, 30, 65, 33, 0.801530429361688),
            (55, 30, 61, 31, 0.808830702230739),
            (56, 30, 56, 28, 0.801881333593783),
            (57, 30, 52, 26, 0.802417625002170),
            (58, 30, 49, 25, 0.812758131855559),
            (59, 30, 45, 23, 0.807445978139098),
            (60, 30, 42, 21, 0.801302394090672),
        ]
    ]
    + [
        # treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.05, power = 0.80, alternative = "greater", dist = "z", equal_var = True
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
            dist="z",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 297, 149, 0.801056798810986),
            (41, 30, 245, 123, 0.800577267977837),
            (42, 30, 207, 104, 0.802653297040860),
            (43, 30, 175, 88, 0.800131060509146),
            (44, 30, 151, 76, 0.800586881429283),
            (45, 30, 132, 66, 0.800278090826272),
            (46, 30, 116, 58, 0.800231229783017),
            (47, 30, 103, 52, 0.803292142983297),
            (48, 30, 91, 46, 0.800268856211136),
            (49, 30, 83, 42, 0.806090165365316),
            (50, 30, 75, 38, 0.806805354392018),
            (51, 30, 67, 34, 0.801906788051731),
            (52, 30, 61, 31, 0.801969209910793),
            (53, 30, 57, 29, 0.809496684723749),
            (54, 30, 51, 26, 0.800950715423805),
            (55, 30, 47, 24, 0.801315104961945),
            (56, 30, 44, 22, 0.800792917916097),
            (57, 30, 41, 21, 0.808002926950256),
            (58, 30, 38, 19, 0.801353201873151),
            (59, 30, 35, 18, 0.803653943837461),
            (60, 30, 33, 17, 0.807129386379525),
        ]
    ]
    + [
        # treatment_mean = 0 to 20 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.05, power = 0.80, alternative = "less", dist = "z", equal_var = True
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
            dist="z",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (0, 30, 33, 17, 0.807129386379525),
            (1, 30, 35, 18, 0.803653943837461),
            (2, 30, 38, 19, 0.801353201873150),
            (3, 30, 41, 21, 0.808002926950255),
            (4, 30, 44, 22, 0.800792917916096),
            (5, 30, 47, 24, 0.801315104961944),
            (6, 30, 51, 26, 0.800950715423804),
            (7, 30, 57, 29, 0.809496684723749),
            (8, 30, 61, 31, 0.801969209910793),
            (9, 30, 67, 34, 0.801906788051731),
            (10, 30, 75, 38, 0.806805354392018),
            (11, 30, 83, 42, 0.806090165365316),
            (12, 30, 91, 46, 0.800268856211135),
            (13, 30, 103, 52, 0.803292142983296),
            (14, 30, 116, 58, 0.800231229783016),
            (15, 30, 132, 66, 0.800278090826271),
            (16, 30, 151, 76, 0.800586881429282),
            (17, 30, 175, 88, 0.800131060509146),
            (18, 30, 207, 104, 0.802653297040859),
            (19, 30, 245, 123, 0.800577267977836),
            (20, 30, 297, 149, 0.801056798810986),
        ]
    ]
)

case_group_z_unequal_var = (
    [
        # treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "two-sided", dist = "z", equal_var = False
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
            dist="z",
            equal_var=False,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 161, 322, 0.800239606920691),
            (41, 30, 133, 266, 0.800069109984034),
            (42, 30, 112, 224, 0.800920350087096),
            (43, 30, 96, 192, 0.803239256461936),
            (44, 30, 83, 166, 0.804294321776750),
            (45, 30, 72, 144, 0.802661712194769),
            (46, 30, 63, 126, 0.800920350087096),
            (47, 30, 56, 112, 0.802275875510353),
            (48, 30, 50, 100, 0.802661712194769),
            (49, 30, 45, 90, 0.803743417618413),
            (50, 30, 41, 82, 0.807430419417483),
            (51, 30, 37, 74, 0.805463561597174),
            (52, 30, 34, 68, 0.808747773575592),
            (53, 30, 31, 62, 0.807406824477827),
            (54, 30, 28, 56, 0.800920350087096),
            (55, 30, 26, 52, 0.803863292473643),
            (56, 30, 24, 48, 0.803239256461936),
            (57, 30, 23, 46, 0.815923398689011),
            (58, 30, 21, 42, 0.808935332465637),
            (59, 30, 20, 40, 0.817122773503530),
            (60, 30, 18, 36, 0.802661712194769),
        ]
    ]
    + [
        # treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "greater", dist = "z", equal_var = False
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
            dist="z",
            equal_var=False,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 127, 254, 0.800706244851413),
            (41, 30, 105, 210, 0.800843081743926),
            (42, 30, 89, 178, 0.803859425853916),
            (43, 30, 75, 150, 0.800020806228989),
            (44, 30, 65, 130, 0.801798603733634),
            (45, 30, 57, 114, 0.804102203568099),
            (46, 30, 50, 100, 0.803427159812370),
            (47, 30, 44, 88, 0.801143828981854),
            (48, 30, 40, 80, 0.807711898822810),
            (49, 30, 36, 72, 0.808664418805339),
            (50, 30, 32, 64, 0.803427159812370),
            (51, 30, 29, 58, 0.803129485388852),
            (52, 30, 27, 54, 0.810556844186746),
            (53, 30, 24, 48, 0.800596715177956),
            (54, 30, 23, 46, 0.815215008698224),
            (55, 30, 21, 42, 0.812043149704281),
            (56, 30, 19, 38, 0.804613856120709),
            (57, 30, 18, 36, 0.811965183424669),
            (58, 30, 17, 34, 0.817252237345353),
            (59, 30, 16, 32, 0.820470015919712),
            (60, 30, 15, 30, 0.821564347968964),
        ]
    ]
    + [
        # treatment_mean = 0 to 20 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "less", dist = "z", equal_var = False
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
            dist="z",
            equal_var=False,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (0, 30, 15, 30, 0.821564347968964),
            (1, 30, 16, 32, 0.820470015919711),
            (2, 30, 17, 34, 0.817252237345353),
            (3, 30, 18, 36, 0.811965183424669),
            (4, 30, 19, 38, 0.804613856120709),
            (5, 30, 21, 42, 0.812043149704280),
            (6, 30, 23, 46, 0.815215008698224),
            (7, 30, 24, 48, 0.800596715177955),
            (8, 30, 27, 54, 0.810556844186745),
            (9, 30, 29, 58, 0.803129485388852),
            (10, 30, 32, 64, 0.803427159812369),
            (11, 30, 36, 72, 0.808664418805338),
            (12, 30, 40, 80, 0.807711898822810),
            (13, 30, 44, 88, 0.801143828981853),
            (14, 30, 50, 100, 0.803427159812369),
            (15, 30, 57, 114, 0.804102203568099),
            (16, 30, 65, 130, 0.801798603733633),
            (17, 30, 75, 150, 0.800020806228988),
            (18, 30, 89, 178, 0.803859425853915),
            (19, 30, 105, 210, 0.800843081743926),
            (20, 30, 127, 254, 0.800706244851412),
        ]
    ]
)

case_group_t_equal_var = (
    [
        # treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.05, power = 0.80, alternative = "two-sided", dist = "t", equal_var = True
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
            dist="t",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 379, 190, 0.801695621293806),
            (41, 30, 313, 157, 0.801280169896146),
            (42, 30, 263, 132, 0.801119839498282),
            (43, 30, 225, 113, 0.802536707019970),
            (44, 30, 193, 97, 0.800321025139564),
            (45, 30, 169, 85, 0.802168948353301),
            (46, 30, 149, 75, 0.803188563334180),
            (47, 30, 131, 66, 0.800021604132335),
            (48, 30, 117, 59, 0.800294519935256),
            (49, 30, 105, 53, 0.800011252761740),
            (50, 30, 95, 48, 0.800731473604127),
            (51, 30, 87, 44, 0.804231438352434),
            (52, 30, 79, 40, 0.802592423442305),
            (53, 30, 73, 37, 0.806175115579405),
            (54, 30, 67, 34, 0.805597462456100),
            (55, 30, 61, 31, 0.800452419055767),
            (56, 30, 57, 29, 0.804284796796349),
            (57, 30, 53, 27, 0.804979692174247),
            (58, 30, 49, 25, 0.802317015564749),
            (59, 30, 47, 24, 0.813097856503667),
            (60, 30, 43, 22, 0.804383572625028),
        ]
    ]
    + [
        # treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.05, power = 0.80, alternative = "greater", dist = "t", equal_var = True
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
            dist="t",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 298, 149, 0.800388222080177),
            (41, 30, 247, 124, 0.802117660107207),
            (42, 30, 207, 104, 0.801130622587925),
            (43, 30, 177, 89, 0.802279050667971),
            (44, 30, 153, 77, 0.803067997347360),
            (45, 30, 133, 67, 0.802250443947344),
            (46, 30, 117, 59, 0.802469050797567),
            (47, 30, 103, 52, 0.800209094742798),
            (48, 30, 93, 47, 0.804337074993792),
            (49, 30, 83, 42, 0.802265939253365),
            (50, 30, 75, 38, 0.802568640325396),
            (51, 30, 69, 35, 0.807356512142458),
            (52, 30, 63, 32, 0.807929689296780),
            (53, 30, 57, 29, 0.803905661930996),
            (54, 30, 53, 27, 0.808028103369108),
            (55, 30, 49, 25, 0.808954618135864),
            (56, 30, 45, 23, 0.806451475187205),
            (57, 30, 41, 21, 0.800114852223148),
            (58, 30, 39, 20, 0.807831122941065),
            (59, 30, 37, 19, 0.813668062197955),
            (60, 30, 34, 17, 0.800919479188958),
        ]
    ]
    + [
        # treatment_mean = 0 to 20 by 1, reference_mean = 30, treatment_std = 40, reference_std = 40, ratio = 2, alpha = 0.05, power = 0.80, alternative = "less", dist = "t", equal_var = True
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
            dist="t",
            equal_var=True,
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (0, 30, 34, 17, 0.800919479188958),
            (1, 30, 37, 19, 0.813668062197955),
            (2, 30, 39, 20, 0.807831122941065),
            (3, 30, 41, 21, 0.800114852223148),
            (4, 30, 45, 23, 0.806451475187205),
            (5, 30, 49, 25, 0.808954618135864),
            (6, 30, 53, 27, 0.808028103369108),
            (7, 30, 57, 29, 0.803905661930996),
            (8, 30, 63, 32, 0.807929689296780),
            (9, 30, 69, 35, 0.807356512142458),
            (10, 30, 75, 38, 0.802568640325396),
            (11, 30, 83, 42, 0.802265939253365),
            (12, 30, 93, 47, 0.804337074993792),
            (13, 30, 103, 52, 0.800209094742798),
            (14, 30, 117, 59, 0.802469050797567),
            (15, 30, 133, 67, 0.802250443947344),
            (16, 30, 153, 77, 0.803067997347360),
            (17, 30, 177, 89, 0.802279050667971),
            (18, 30, 207, 104, 0.801130622587925),
            (19, 30, 247, 124, 0.802117660107207),
            (20, 30, 298, 149, 0.800388222080177),
        ]
    ]
)


case_group_t_unequal_var_welch = []

case_group_t_unequal_var_satterthwaite = (
    [
        # treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "two-sided", dist = "t", equal_var = False, approx_t_method="satterthwaite",
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
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 163, 326, 0.802123480788046),
            (41, 30, 135, 270, 0.802344176119546),
            (42, 30, 113, 226, 0.800128467354919),
            (43, 30, 97, 194, 0.802312170106138),
            (44, 30, 84, 168, 0.803215247484982),
            (45, 30, 73, 146, 0.801402820098010),
            (46, 30, 65, 130, 0.805635204914526),
            (47, 30, 57, 114, 0.800624598020793),
            (48, 30, 51, 102, 0.800794377786510),
            (49, 30, 46, 92, 0.801650420608002),
            (50, 30, 42, 84, 0.805124445248507),
            (51, 30, 38, 76, 0.802867813798303),
            (52, 30, 35, 70, 0.805908101536807),
            (53, 30, 32, 64, 0.804244270021829),
            (54, 30, 30, 60, 0.811117453410171),
            (55, 30, 28, 56, 0.814724360111304),
            (56, 30, 26, 52, 0.814945917214449),
            (57, 30, 24, 48, 0.811512006713500),
            (58, 30, 22, 44, 0.803955742926776),
            (59, 30, 21, 42, 0.811918013735676),
            (60, 30, 20, 40, 0.817874109579663),
        ]
    ]
    + [
        # treatment_mean = 40 to 60 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "greater", dist = "t", equal_var = False, approx_t_method="satterthwaite",
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
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (40, 30, 128, 256, 0.801079918266573),
            (41, 30, 106, 212, 0.801290209782415),
            (42, 30, 89, 178, 0.800466396873862),
            (43, 30, 76, 152, 0.800632317932014),
            (44, 30, 66, 132, 0.802492658376903),
            (45, 30, 58, 116, 0.804879249562874),
            (46, 30, 51, 102, 0.804299346326872),
            (47, 30, 45, 90, 0.802120294751663),
            (48, 30, 40, 80, 0.800030724467211),
            (49, 30, 36, 72, 0.800102020866036),
            (50, 30, 33, 66, 0.804685379882172),
            (51, 30, 30, 60, 0.804485598028449),
            (52, 30, 28, 56, 0.811965375296716),
            (53, 30, 25, 50, 0.802154225298166),
            (54, 30, 23, 46, 0.801588746121388),
            (55, 30, 22, 44, 0.813701802636139),
            (56, 30, 20, 40, 0.806397610053575),
            (57, 30, 19, 38, 0.813772769961607),
            (58, 30, 18, 36, 0.819088554824873),
            (59, 30, 16, 32, 0.800380162664402),
            (60, 30, 15, 30, 0.800011510251783),
        ]
    ]
    + [
        # treatment_mean = 0 to 20 by 1, reference_mean = 30, treatment_std = 40, reference_std = 30, ratio = 0.5, alpha = 0.05, power = 0.80, alternative = "less", dist = "t", equal_var = False, approx_t_method="satterthwaite",
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
            dist="t",
            equal_var=False,
            approx_t_method="satterthwaite",
        )
        for treatment_mean, reference_mean, treatment_size, reference_size, actual_power in [
            (0, 30, 15, 30, 0.800011510251783),
            (1, 30, 16, 32, 0.800380162664402),
            (2, 30, 18, 36, 0.819088554824873),
            (3, 30, 19, 38, 0.813772769961607),
            (4, 30, 20, 40, 0.806397610053575),
            (5, 30, 22, 44, 0.813701802636139),
            (6, 30, 23, 46, 0.801588746121388),
            (7, 30, 25, 50, 0.802154225298166),
            (8, 30, 28, 56, 0.811965375296716),
            (9, 30, 30, 60, 0.804485598028449),
            (10, 30, 33, 66, 0.804685379882172),
            (11, 30, 36, 72, 0.800102020866036),
            (12, 30, 40, 80, 0.800030724467211),
            (13, 30, 45, 90, 0.802120294751663),
            (14, 30, 51, 102, 0.804299346326872),
            (15, 30, 58, 116, 0.804879249562874),
            (16, 30, 66, 132, 0.802492658376903),
            (17, 30, 76, 152, 0.800632317932014),
            (18, 30, 89, 178, 0.800466396873862),
            (19, 30, 106, 212, 0.801290209782415),
            (20, 30, 128, 256, 0.801079918266573),
        ]
    ]
)

case_group = case_group_z_equal_var + case_group_z_unequal_var + case_group_t_equal_var + case_group_t_unequal_var_welch + case_group_t_unequal_var_satterthwaite


def test_verify_mean_and_get_diff() -> None:
    with pytest.raises(ValueError):
        _verify_mean_and_get_diff(diff=None, treatment_mean=None, reference_mean=None)

    _verify_mean_and_get_diff(diff=None, treatment_mean=20, reference_mean=10)


def test_verify_std_and_get_std() -> None:
    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=None, dist="z", equal_var=True)
    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=10, reference_std=20, dist="z", equal_var=True)

    _verify_std_and_get_std(std=None, treatment_std=10, reference_std=None, dist="z", equal_var=True)
    _verify_std_and_get_std(std=None, treatment_std=None, reference_std=20, dist="z", equal_var=True)

    # dist = "z" and equal_var = False
    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=None, dist="z", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=10, reference_std=None, dist="z", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=10, dist="z", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=10, treatment_std=None, reference_std=None, dist="z", equal_var=False)

    # dist = "t" and equal_var = True
    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=None, dist="t", equal_var=True)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=10, reference_std=None, dist="t", equal_var=True)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=10, dist="t", equal_var=True)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=10, treatment_std=None, reference_std=None, dist="t", equal_var=True)

    # dist = "t" and equal_var = False
    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=None, dist="t", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=10, reference_std=None, dist="t", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=None, treatment_std=None, reference_std=10, dist="t", equal_var=False)

    with pytest.raises(ValueError):
        _verify_std_and_get_std(std=10, treatment_std=None, reference_std=None, dist="t", equal_var=False)


def test_solve_power(case: TestCase) -> None:
    assert round(
        solve_power(
            treatment_mean=case.treatment_mean,
            reference_mean=case.reference_mean,
            diff=case.diff,
            treatment_std=case.treatment_std,
            reference_std=case.reference_std,
            std=case.std,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            alternative=case.alternative,
            alpha=case.alpha,
            dist=case.dist,
            equal_var=case.equal_var,
            approx_t_method=case.approx_t_method,
        ),
        6,
    ) == round(case.actual_power, 6)


def test_solve_size(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case in [
        TestCase(treatment_mean=42, reference_mean=30, diff=17, treatment_std=40, reference_std=40, treatment_size=103, reference_size=52, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8002, dist="t", equal_var=True),
        TestCase(treatment_mean=47, reference_mean=30, diff=17, treatment_std=40, reference_std=40, treatment_size=103, reference_size=52, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8002, dist="t", equal_var=True),
        TestCase(treatment_mean=54, reference_mean=30, diff=17, treatment_std=40, reference_std=40, treatment_size=103, reference_size=52, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8002, dist="t", equal_var=True),
        TestCase(treatment_mean=41, reference_mean=30, diff=22, treatment_std=40, reference_std=30, treatment_size=28, reference_size=56, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8120, dist="t", equal_var=False, approx_t_method="satterthwaite"),
        TestCase(treatment_mean=46, reference_mean=30, diff=22, treatment_std=40, reference_std=30, treatment_size=28, reference_size=56, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8120, dist="t", equal_var=False, approx_t_method="satterthwaite"),
        TestCase(treatment_mean=52, reference_mean=30, diff=22, treatment_std=40, reference_std=30, treatment_size=28, reference_size=56, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8120, dist="t", equal_var=False, approx_t_method="satterthwaite"),
        TestCase(treatment_mean=53, reference_mean=30, diff=22, treatment_std=40, reference_std=30, treatment_size=28, reference_size=56, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8120, dist="t", equal_var=False, approx_t_method="satterthwaite"),
        TestCase(treatment_mean=41, reference_mean=30, diff=11, treatment_std=40, reference_std=30, treatment_size=106, reference_size=212, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8013, dist="t", equal_var=False, approx_t_method="welch"),
    ]:
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if case.treatment_mean in range(40, 61) and (
        (case.alternative == "two-sided" and case.dist == "t" and case.equal_var)
        or (case.alternative == "two-sided" and case.dist == "t" and not case.equal_var and case.approx_t_method == "satterthwaite")
        or (case.alternative == "two-sided" and case.dist == "t" and not case.equal_var and case.approx_t_method == "welch")
    ):
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    ratio = case.treatment_size / case.reference_size
    assert solve_size(
        treatment_mean=case.treatment_mean,
        reference_mean=case.reference_mean,
        diff=case.diff,
        treatment_std=case.treatment_std,
        reference_std=case.reference_std,
        std=case.std,
        ratio=ratio,
        alternative=case.alternative,
        alpha=case.alpha,
        power=case.power,
        dist=case.dist,
        equal_var=case.equal_var,
        approx_t_method=case.approx_t_method,
    ) == (case.treatment_size, case.reference_size)


def test_solve_diff(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case in [
        TestCase(treatment_mean=56, reference_mean=30, diff=26, treatment_std=40, reference_std=40, treatment_size=45, reference_size=23, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8065, dist="t", equal_var=True),
    ]:
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if case.treatment_mean in range(40, 61) and (
        (case.alternative == "two-sided" and case.dist == "t" and case.equal_var)
        or (case.alternative == "two-sided" and case.dist == "t" and not case.equal_var and case.approx_t_method == "satterthwaite")
        or (case.alternative == "two-sided" and case.dist == "t" and not case.equal_var and case.approx_t_method == "welch")
    ):
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    case.direction = "greater" if case.diff > 0 else "less"
    assert (
        round(
            solve_diff(
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                direction=case.direction,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                equal_var=case.equal_var,
                approx_t_method=case.approx_t_method,
            ),
            0,
        )
        == case.diff
    )


def test_solve_diff_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_diff(std=30, treatment_size=20, reference_size=30, alternative="two-sided")


def test_solve_treatment_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case in [
        TestCase(treatment_mean=56, reference_mean=30, diff=26, treatment_std=40, reference_std=40, treatment_size=45, reference_size=23, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8065, dist="t", equal_var=True),
    ]:
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if case.treatment_mean in range(40, 61) and (
        (case.alternative == "two-sided" and case.dist == "t" and case.equal_var)
        or (case.alternative == "two-sided" and case.dist == "t" and not case.equal_var and case.approx_t_method == "satterthwaite")
        or (case.alternative == "two-sided" and case.dist == "t" and not case.equal_var and case.approx_t_method == "welch")
    ):
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    case.direction = "greater" if case.treatment_mean > case.reference_mean else "less"
    assert (
        round(
            solve_treatment_mean(
                reference_mean=case.reference_mean,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                std=case.std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                equal_var=case.equal_var,
                approx_t_method=case.approx_t_method,
                direction=case.direction,
            ),
            0,
        )
        == case.treatment_mean
    )


def test_solve_treatment_mean_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_treatment_mean(reference_mean=20, std=30, treatment_size=20, reference_size=30, alternative="two-sided")


def test_solve_reference_mean(case: TestCase, request: pytest.FixtureRequest) -> None:

    if case in [
        TestCase(treatment_mean=56, reference_mean=30, diff=26, treatment_std=40, reference_std=40, treatment_size=45, reference_size=23, alternative="greater", alpha=0.05, power=0.8, actual_power=0.8065, dist="t", equal_var=True),
    ]:
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    if case.treatment_mean in range(40, 61) and (
        (case.alternative == "two-sided" and case.dist == "t" and case.equal_var)
        or (case.alternative == "two-sided" and case.dist == "t" and not case.equal_var and case.approx_t_method == "satterthwaite")
        or (case.alternative == "two-sided" and case.dist == "t" and not case.equal_var and case.approx_t_method == "welch")
    ):
        request.node.add_marker(pytest.mark.xfail(reason="SciPy upstream bug: https://github.com/scipy/scipy/issues/25470"))

    case.direction = "greater" if case.reference_mean > case.treatment_mean else "less"
    assert (
        round(
            solve_reference_mean(
                treatment_mean=case.treatment_mean,
                treatment_std=case.treatment_std,
                reference_std=case.reference_std,
                std=case.std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                equal_var=case.equal_var,
                approx_t_method=case.approx_t_method,
                direction=case.direction,
            ),
            0,
        )
        == case.reference_mean
    )


def test_solve_reference_mean_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_reference_mean(treatment_mean=20, std=30, treatment_size=20, reference_size=30, alternative="two-sided")


def test_solve_treatment_std(case: TestCase) -> None:
    assert (
        round(
            solve_treatment_std(
                treatment_mean=case.treatment_mean,
                reference_mean=case.reference_mean,
                diff=case.diff,
                reference_std=case.reference_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                equal_var=case.equal_var,
                approx_t_method=case.approx_t_method,
            ),
            0,
        )
        == case.treatment_std
    )

    if case.equal_var and case.dist == "t":
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
                    dist=case.dist,
                    equal_var=case.equal_var,
                    approx_t_method=case.approx_t_method,
                ),
                0,
            )
            == case.treatment_std
        )


def test_solve_treatment_std_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_treatment_std(diff=30, treatment_size=20, reference_size=30, alternative="two-sided", dist="t", equal_var=False)


def test_solve_reference_std(case: TestCase) -> None:
    assert (
        round(
            solve_reference_std(
                treatment_mean=case.treatment_mean,
                reference_mean=case.reference_mean,
                diff=case.diff,
                treatment_std=case.treatment_std,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                dist=case.dist,
                equal_var=case.equal_var,
                approx_t_method=case.approx_t_method,
            ),
            0,
        )
        == case.reference_std
    )

    if case.equal_var and case.dist == "t":
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
                    dist=case.dist,
                    equal_var=case.equal_var,
                    approx_t_method=case.approx_t_method,
                ),
                0,
            )
            == case.reference_std
        )


def test_solve_reference_std_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_reference_std(diff=30, treatment_size=20, reference_size=30, alternative="two-sided", dist="t", equal_var=False)
