# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Validation Software: PASS 2025
# Module: Tests for One Proportions
# For mathod = "exact", the max n for Binomial Enumeration is 20000

from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.proportion.single.inequality import solve_null_proportion
from pystatpower.proportion.single.inequality import solve_power
from pystatpower.proportion.single.inequality import solve_proportion
from pystatpower.proportion.single.inequality import solve_size
from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    proportion: float
    null_proportion: float
    size: int
    alternative: Literal["two-sided", "greater", "less"]
    alpha: float
    method: Literal["exact", "z-p0", "z-phat"]
    continuity_correction: bool | None = None
    power: float
    actual_power: float

    direction: Literal["greater", "less"] | None = None


case_group_exact = (
    [
        # null_proportion = 0.80, proportion = 0.65 to 0.95 by 0.01, alternative = "two-sided", alpha = 0.05, power = 0.80, method = "exact"
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="two-sided",
            alpha=0.05,
            power=0.80,
            method="exact",
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.65, 72, 0.819135301254731),
            (0.80, 0.66, 80, 0.807878014451981),
            (0.80, 0.67, 89, 0.807638012747759),
            (0.80, 0.68, 105, 0.803531754685669),
            (0.80, 0.69, 122, 0.800112018840346),
            (0.80, 0.70, 144, 0.802713330760977),
            (0.80, 0.71, 178, 0.800213215666391),
            (0.80, 0.72, 222, 0.800358041141018),
            (0.80, 0.73, 289, 0.805837176788970),
            (0.80, 0.74, 384, 0.802733217481613),
            (0.80, 0.75, 540, 0.800209359415236),
            (0.80, 0.76, 842, 0.802848150704484),
            (0.80, 0.77, 1466, 0.801628950741427),
            (0.80, 0.78, 3252, 0.800376315244901),
            (0.80, 0.79, 12768, 0.800105719765596),
            (0.80, 0.81, 12362, 0.800260819925483),
            (0.80, 0.82, 3048, 0.800529065652599),
            (0.80, 0.83, 1329, 0.801567855182316),
            (0.80, 0.84, 738, 0.801991669635496),
            (0.80, 0.85, 466, 0.805220853144157),
            (0.80, 0.86, 316, 0.804637729671247),
            (0.80, 0.87, 225, 0.802321463552064),
            (0.80, 0.88, 173, 0.811282940356863),
            (0.80, 0.89, 131, 0.808688918169614),
            (0.80, 0.90, 107, 0.819108271643123),
            (0.80, 0.91, 88, 0.833494128995576),
            (0.80, 0.92, 69, 0.814869150464013),
            (0.80, 0.93, 55, 0.814543788094879),
            (0.80, 0.94, 48, 0.840714535711805),
            (0.80, 0.95, 41, 0.852594507253420),
        ]
    ]
    + [
        # null_proportion = 0.80, proportion = 0.81 to 0.95 by 0.01, alternative = "greater", alpha = 0.05, power = 0.80, method = "exact"
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="greater",
            alpha=0.05,
            power=0.80,
            method="exact",
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.81, 9747, 0.800027630098403),
            (0.80, 0.82, 2398, 0.800852261897212),
            (0.80, 0.83, 1043, 0.800298043765811),
            (0.80, 0.84, 581, 0.804234526623940),
            (0.80, 0.85, 365, 0.801778627534206),
            (0.80, 0.86, 249, 0.803418437199858),
            (0.80, 0.87, 181, 0.811728602015956),
            (0.80, 0.88, 135, 0.811325124094171),
            (0.80, 0.89, 106, 0.813783118922670),
            (0.80, 0.90, 82, 0.805706395989952),
            (0.80, 0.91, 69, 0.834345812477074),
            (0.80, 0.92, 57, 0.831335165738529),
            (0.80, 0.93, 44, 0.807584196470843),
            (0.80, 0.94, 37, 0.820333086243616),
            (0.80, 0.95, 30, 0.812178813146965),
        ]
    ]
    + [
        # null_proportion = 0.80, proportion = 0.65 to 0.79 by 0.01, alternative = "less", alpha = 0.05, power = 0.80, method = "exact"
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="less",
            alpha=0.05,
            power=0.80,
            method="exact",
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.65, 56, 0.806415503536763),
            (0.80, 0.66, 61, 0.808429477025855),
            (0.80, 0.67, 73, 0.813433532153910),
            (0.80, 0.68, 85, 0.804148944447580),
            (0.80, 0.69, 98, 0.800497187659299),
            (0.80, 0.70, 116, 0.807275790447936),
            (0.80, 0.71, 138, 0.800716433009873),
            (0.80, 0.72, 177, 0.800540393112464),
            (0.80, 0.73, 227, 0.805857293927260),
            (0.80, 0.74, 304, 0.802984078542563),
            (0.80, 0.75, 433, 0.804476066202352),
            (0.80, 0.76, 662, 0.802749242395281),
            (0.80, 0.77, 1164, 0.802167701224689),
            (0.80, 0.78, 2560, 0.800446539149970),
            (0.80, 0.79, 10076, 0.800151453279983),
        ]
    ]
)

case_group_z_p0 = (
    [
        # null_proportion = 0.80, proportion = 0.65 to 0.95 by 0.01, alternative = "two-sided", alpha = 0.05, power = 0.80, method = "z-p0", continuity_correction = False
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="two-sided",
            alpha=0.05,
            power=0.80,
            method="z-p0",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.65, 63, 0.803040864950383),
            (0.80, 0.66, 72, 0.803115950394531),
            (0.80, 0.67, 83, 0.802759291914434),
            (0.80, 0.68, 97, 0.803166938896514),
            (0.80, 0.69, 114, 0.800766576638177),
            (0.80, 0.70, 137, 0.800501487734719),
            (0.80, 0.71, 168, 0.800410594875327),
            (0.80, 0.72, 211, 0.800128588585912),
            (0.80, 0.73, 274, 0.800683176428901),
            (0.80, 0.74, 370, 0.800625769091056),
            (0.80, 0.75, 528, 0.800323427024922),
            (0.80, 0.76, 818, 0.800396351461364),
            (0.80, 0.77, 1440, 0.800170588106992),
            (0.80, 0.78, 3208, 0.800110038623282),
            (0.80, 0.79, 12697, 0.800018403869863),
            (0.80, 0.81, 12414, 0.800019884892353),
            (0.80, 0.82, 3066, 0.800075870233685),
            (0.80, 0.83, 1345, 0.800075617171763),
            (0.80, 0.84, 747, 0.800551815376927),
            (0.80, 0.85, 471, 0.800487589670274),
            (0.80, 0.86, 322, 0.800519447080362),
            (0.80, 0.87, 233, 0.801228064327272),
            (0.80, 0.88, 175, 0.800706051157800),
            (0.80, 0.89, 136, 0.802008084164421),
            (0.80, 0.90, 108, 0.802564298471140),
            (0.80, 0.91, 87, 0.801142070865251),
            (0.80, 0.92, 72, 0.806055009458303),
            (0.80, 0.93, 60, 0.808931891240985),
            (0.80, 0.94, 50, 0.807101440204685),
            (0.80, 0.95, 42, 0.805980482858176),
        ]
    ]
    + [
        # null_proportion = 0.80, proportion = 0.81 to 0.95 by 0.01, alternative = "greater", alpha = 0.05, power = 0.80, method = "z-p0", continuity_correction = False
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="greater",
            alpha=0.05,
            power=0.80,
            method="z-p0",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.81, 9764, 0.800013789994728),
            (0.80, 0.82, 2408, 0.800106201345581),
            (0.80, 0.83, 1055, 0.800253989677130),
            (0.80, 0.84, 584, 0.800121236481480),
            (0.80, 0.85, 368, 0.800553050361994),
            (0.80, 0.86, 251, 0.800488315290235),
            (0.80, 0.87, 181, 0.800642145169928),
            (0.80, 0.88, 136, 0.801303781422184),
            (0.80, 0.89, 105, 0.800848451180299),
            (0.80, 0.90, 83, 0.800573927032559),
            (0.80, 0.91, 67, 0.801552493465908),
            (0.80, 0.92, 55, 0.803772052858985),
            (0.80, 0.93, 46, 0.809754034417974),
            (0.80, 0.94, 38, 0.806076352035532),
            (0.80, 0.95, 32, 0.809069284985241),
        ]
    ]
    + [
        # null_proportion = 0.80, proportion = 0.65 to 0.79 by 0.01, alternative = "less", alpha = 0.05, power = 0.80, method = "z-p0", continuity_correction = False
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="less",
            alpha=0.05,
            power=0.80,
            method="z-p0",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.65, 50, 0.800756888260664),
            (0.80, 0.66, 57, 0.800207972697630),
            (0.80, 0.67, 66, 0.801451089868895),
            (0.80, 0.68, 77, 0.801471953460059),
            (0.80, 0.69, 91, 0.801297431146030),
            (0.80, 0.70, 109, 0.800250324197502),
            (0.80, 0.71, 134, 0.801224349718141),
            (0.80, 0.72, 168, 0.800678987495538),
            (0.80, 0.73, 218, 0.801227687943674),
            (0.80, 0.74, 294, 0.801070766044885),
            (0.80, 0.75, 419, 0.800710657275667),
            (0.80, 0.76, 647, 0.800042020029968),
            (0.80, 0.77, 1139, 0.800232224300619),
            (0.80, 0.78, 2534, 0.800133180369081),
            (0.80, 0.79, 10015, 0.800006191027803),
        ]
    ]
)

case_group_z_p0_cc = (
    [
        # null_proportion = 0.80, proportion = 0.65 to 0.95 by 0.01, alternative = "two-sided", alpha = 0.05, power = 0.80, method = "z-p0", continuity_correction = True
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="two-sided",
            alpha=0.05,
            power=0.80,
            method="z-p0",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.65, 69, 0.800233135363792),
            (0.80, 0.66, 79, 0.803195440665644),
            (0.80, 0.67, 90, 0.800515253590740),
            (0.80, 0.68, 105, 0.802550135259552),
            (0.80, 0.69, 123, 0.800999469597177),
            (0.80, 0.70, 147, 0.800938599699220),
            (0.80, 0.71, 179, 0.800537167846699),
            (0.80, 0.72, 224, 0.801279451098839),
            (0.80, 0.73, 288, 0.800535898566648),
            (0.80, 0.74, 386, 0.800139561858438),
            (0.80, 0.75, 548, 0.800450127892657),
            (0.80, 0.76, 842, 0.800022161680960),
            (0.80, 0.77, 1473, 0.800131907487621),
            (0.80, 0.78, 3257, 0.800013283457466),
            (0.80, 0.79, 12797, 0.800024224798706),
            (0.80, 0.81, 12514, 0.800026211299798),
            (0.80, 0.82, 3116, 0.800102168802803),
            (0.80, 0.83, 1378, 0.800035377475483),
            (0.80, 0.84, 771, 0.800106509037517),
            (0.80, 0.85, 491, 0.800671154300968),
            (0.80, 0.86, 339, 0.801243148660685),
            (0.80, 0.87, 247, 0.801077476309997),
            (0.80, 0.88, 188, 0.802538928347337),
            (0.80, 0.89, 147, 0.802347067116994),
            (0.80, 0.90, 118, 0.803506347215552),
            (0.80, 0.91, 96, 0.801855659112001),
            (0.80, 0.92, 80, 0.805220447050618),
            (0.80, 0.93, 67, 0.804672131776765),
            (0.80, 0.94, 57, 0.808023550868064),
            (0.80, 0.95, 49, 0.814023491861191),
        ]
    ]
    + [
        # null_proportion = 0.80, proportion = 0.81 to 0.95 by 0.01, alternative = "greater", alpha = 0.05, power = 0.80, method = "z-p0", continuity_correction = True
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="greater",
            alpha=0.05,
            power=0.80,
            method="z-p0",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.81, 9864, 0.800022941571350),
            (0.80, 0.82, 2458, 0.800143945599966),
            (0.80, 0.83, 1088, 0.800227153780476),
            (0.80, 0.84, 609, 0.800283273288190),
            (0.80, 0.85, 388, 0.800815808629405),
            (0.80, 0.86, 268, 0.801390380543520),
            (0.80, 0.87, 195, 0.800590109422099),
            (0.80, 0.88, 148, 0.800607918513419),
            (0.80, 0.89, 116, 0.801455010839620),
            (0.80, 0.90, 93, 0.801944373252918),
            (0.80, 0.91, 76, 0.802733421021959),
            (0.80, 0.92, 63, 0.803294854229333),
            (0.80, 0.93, 53, 0.805500728213517),
            (0.80, 0.94, 45, 0.807916464074823),
            (0.80, 0.95, 38, 0.802792148124594),
        ]
    ]
    + [
        # null_proportion = 0.80, proportion = 0.65 to 0.79 by 0.01, alternative = "less", alpha = 0.05, power = 0.80, method = "z-p0", continuity_correction = True
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="less",
            alpha=0.05,
            power=0.80,
            method="z-p0",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.65, 57, 0.804013355348628),
            (0.80, 0.66, 64, 0.800516834407625),
            (0.80, 0.67, 74, 0.803845164881508),
            (0.80, 0.68, 85, 0.800943935064697),
            (0.80, 0.69, 100, 0.801699289738159),
            (0.80, 0.70, 119, 0.800863663970307),
            (0.80, 0.71, 145, 0.801467344879083),
            (0.80, 0.72, 180, 0.800134892249319),
            (0.80, 0.73, 232, 0.801129671194229),
            (0.80, 0.74, 310, 0.800577488874412),
            (0.80, 0.75, 438, 0.800101761879361),
            (0.80, 0.76, 672, 0.800161816224641),
            (0.80, 0.77, 1172, 0.800203762195588),
            (0.80, 0.78, 2583, 0.800031426650430),
            (0.80, 0.79, 10115, 0.800014678495153),
        ]
    ]
)

case_group_z_phat = (
    [
        # null_proportion = 0.80, proportion = 0.65 to 0.95 by 0.01, alternative = "two-sided", alpha = 0.05, power = 0.80, method = "z-phat", continuity_correction = False
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="two-sided",
            alpha=0.05,
            power=0.80,
            method="z-phat",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.65, 80, 0.803137815396495),
            (0.80, 0.66, 90, 0.800603888281721),
            (0.80, 0.67, 103, 0.801198438091526),
            (0.80, 0.68, 119, 0.801302394090672),
            (0.80, 0.69, 139, 0.800706403107222),
            (0.80, 0.70, 165, 0.800413455028457),
            (0.80, 0.71, 200, 0.800949211542050),
            (0.80, 0.72, 248, 0.801203790889264),
            (0.80, 0.73, 316, 0.800351992353098),
            (0.80, 0.74, 420, 0.800487508908569),
            (0.80, 0.75, 589, 0.800223374483033),
            (0.80, 0.76, 895, 0.800100740378140),
            (0.80, 0.77, 1545, 0.800131659704370),
            (0.80, 0.78, 3368, 0.800097676763455),
            (0.80, 0.79, 13022, 0.800022298073926),
            (0.80, 0.81, 12080, 0.800019597757468),
            (0.80, 0.82, 2897, 0.800104302091012),
            (0.80, 0.83, 1231, 0.800150723076412),
            (0.80, 0.84, 660, 0.800413455028455),
            (0.80, 0.85, 401, 0.800692703861456),
            (0.80, 0.86, 263, 0.800744620193754),
            (0.80, 0.87, 182, 0.801801565925393),
            (0.80, 0.88, 130, 0.801490520197571),
            (0.80, 0.89, 95, 0.800558968626207),
            (0.80, 0.90, 71, 0.801991443704329),
            (0.80, 0.91, 54, 0.806364880555749),
            (0.80, 0.92, 41, 0.808479411558247),
            (0.80, 0.93, 31, 0.809721796442213),
            (0.80, 0.94, 23, 0.807087127639565),
            (0.80, 0.95, 17, 0.809961622848752),
        ]
    ]
    + [
        # null_proportion = 0.80, proportion = 0.81 to 0.95 by 0.01, alternative = "greater", alpha = 0.05, power = 0.80, method = "z-phat", continuity_correction = False
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="greater",
            alpha=0.05,
            power=0.80,
            method="z-phat",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.81, 9515, 0.800001624875980),
            (0.80, 0.82, 2282, 0.800097069388382),
            (0.80, 0.83, 970, 0.800255674466015),
            (0.80, 0.84, 520, 0.800445371961439),
            (0.80, 0.85, 316, 0.800759916334469),
            (0.80, 0.86, 207, 0.800383142369419),
            (0.80, 0.87, 143, 0.800721977479288),
            (0.80, 0.88, 103, 0.803345195831333),
            (0.80, 0.89, 75, 0.801277358582647),
            (0.80, 0.90, 56, 0.802221970153586),
            (0.80, 0.91, 42, 0.801267095627245),
            (0.80, 0.92, 32, 0.804365788992018),
            (0.80, 0.93, 24, 0.802678157850165),
            (0.80, 0.94, 18, 0.804059177390613),
            (0.80, 0.95, 14, 0.823900289011093),
        ]
    ]
    + [
        # null_proportion = 0.80, proportion = 0.65 to 0.79 by 0.01, alternative = "less", alpha = 0.05, power = 0.80, method = "z-phat", continuity_correction = False
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="less",
            alpha=0.05,
            power=0.80,
            method="z-phat",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.65, 63, 0.802697875598726),
            (0.80, 0.66, 71, 0.801059752072343),
            (0.80, 0.67, 81, 0.800492560384414),
            (0.80, 0.68, 94, 0.802130872070228),
            (0.80, 0.69, 110, 0.802239342269499),
            (0.80, 0.70, 130, 0.800445371961442),
            (0.80, 0.71, 158, 0.801854695429420),
            (0.80, 0.72, 195, 0.800445371961442),
            (0.80, 0.73, 249, 0.800433154726167),
            (0.80, 0.74, 331, 0.800606622868151),
            (0.80, 0.75, 464, 0.800231229783018),
            (0.80, 0.76, 705, 0.800093056182264),
            (0.80, 0.77, 1217, 0.800117304283512),
            (0.80, 0.78, 2653, 0.800089604206439),
            (0.80, 0.79, 10257, 0.800004667672462),
        ]
    ]
)

case_group_z_phat_cc = (
    [
        # null_proportion = 0.80, proportion = 0.65 to 0.95 by 0.01, alternative = "two-sided", alpha = 0.05, power = 0.80, method = "z-phat", continuity_correction = True
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="two-sided",
            alpha=0.05,
            power=0.80,
            method="z-phat",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.65, 86, 0.800502011961338),
            (0.80, 0.66, 97, 0.800553800125984),
            (0.80, 0.67, 111, 0.802867230926064),
            (0.80, 0.68, 127, 0.800654379565129),
            (0.80, 0.69, 148, 0.800843012947857),
            (0.80, 0.70, 175, 0.800751964337301),
            (0.80, 0.71, 211, 0.801017535174508),
            (0.80, 0.72, 260, 0.800650742889036),
            (0.80, 0.73, 330, 0.800188885039840),
            (0.80, 0.74, 436, 0.800013263149384),
            (0.80, 0.75, 609, 0.800332278125249),
            (0.80, 0.76, 920, 0.800174826740080),
            (0.80, 0.77, 1578, 0.800091490677477),
            (0.80, 0.78, 3417, 0.800002354753752),
            (0.80, 0.79, 13122, 0.800027938408605),
            (0.80, 0.81, 12180, 0.800026156701902),
            (0.80, 0.82, 2947, 0.800132800556450),
            (0.80, 0.83, 1264, 0.800114249665817),
            (0.80, 0.84, 685, 0.800548466706908),
            (0.80, 0.85, 421, 0.800924134607493),
            (0.80, 0.86, 279, 0.800121106893743),
            (0.80, 0.87, 196, 0.801746374568586),
            (0.80, 0.88, 142, 0.800812124699786),
            (0.80, 0.89, 106, 0.801299612678994),
            (0.80, 0.90, 81, 0.803683266579139),
            (0.80, 0.91, 62, 0.800858111368021),
            (0.80, 0.92, 49, 0.808676113200957),
            (0.80, 0.93, 38, 0.805922969536309),
            (0.80, 0.94, 30, 0.811788784606714),
            (0.80, 0.95, 23, 0.805763194978974),
        ]
    ]
    + [
        # null_proportion = 0.80, proportion = 0.81 to 0.95 by 0.01, alternative = "greater", alpha = 0.05, power = 0.80, method = "z-phat", continuity_correction = True
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="greater",
            alpha=0.05,
            power=0.80,
            method="z-phat",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.81, 9615, 0.800011135843201),
            (0.80, 0.82, 2332, 0.800137937371904),
            (0.80, 0.83, 1003, 0.800235448903217),
            (0.80, 0.84, 545, 0.800637054840603),
            (0.80, 0.85, 336, 0.801087098047704),
            (0.80, 0.86, 224, 0.801461655017176),
            (0.80, 0.87, 157, 0.800817397914614),
            (0.80, 0.88, 115, 0.802805658998171),
            (0.80, 0.89, 86, 0.802421966288643),
            (0.80, 0.90, 66, 0.804555615226538),
            (0.80, 0.91, 51, 0.803850732015736),
            (0.80, 0.92, 40, 0.805450654751697),
            (0.80, 0.93, 32, 0.813521976457858),
            (0.80, 0.94, 25, 0.811004000244895),
            (0.80, 0.95, 20, 0.821237723868612),
        ]
    ]
    + [
        # null_proportion = 0.80, proportion = 0.65 to 0.79 by 0.01, alternative = "less", alpha = 0.05, power = 0.80, method = "z-phat", continuity_correction = True
        TestCase(
            null_proportion=null_proportion,
            proportion=proportion,
            size=size,
            alternative="less",
            alpha=0.05,
            power=0.80,
            method="z-phat",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for null_proportion, proportion, size, actual_power in [
            (0.80, 0.65, 70, 0.805388256208087),
            (0.80, 0.66, 78, 0.801160888064395),
            (0.80, 0.67, 89, 0.802518162361294),
            (0.80, 0.68, 102, 0.801528083693417),
            (0.80, 0.69, 119, 0.802499979913094),
            (0.80, 0.70, 140, 0.800922632131082),
            (0.80, 0.71, 169, 0.802011722609028),
            (0.80, 0.72, 208, 0.801668832957221),
            (0.80, 0.73, 263, 0.800304996301893),
            (0.80, 0.74, 347, 0.800115972743007),
            (0.80, 0.75, 484, 0.800386105094612),
            (0.80, 0.76, 730, 0.800198688214723),
            (0.80, 0.77, 1250, 0.800085530378012),
            (0.80, 0.78, 2703, 0.800119933295769),
            (0.80, 0.79, 10357, 0.800012858497205),
        ]
    ]
)


case_group = case_group_exact + case_group_z_p0 + case_group_z_p0_cc + case_group_z_phat + case_group_z_phat_cc


def test_solve_power(case: TestCase) -> None:
    assert round(
        solve_power(
            proportion=case.proportion,
            null_proportion=case.null_proportion,
            size=case.size,
            alternative=case.alternative,
            alpha=case.alpha,
            method=case.method,
            continuity_correction=case.continuity_correction,
        ),
        6,
    ) == round(case.actual_power, 6)


def test_solve_size(case: TestCase) -> None:
    assert (
        solve_size(
            null_proportion=case.null_proportion,
            proportion=case.proportion,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.power,
            method=case.method,
            continuity_correction=case.continuity_correction,
        )
        == case.size
    )


def test_solve_proportion(case: TestCase) -> None:
    direction = "greater" if case.proportion > case.null_proportion else "less"
    assert (
        round(
            solve_proportion(
                null_proportion=case.null_proportion,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                continuity_correction=case.continuity_correction,
                direction=direction,
            ),
            2,
        )
        == case.proportion
    )


def test_solve_proportion_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_proportion(
            null_proportion=0.5,
            size=100,
            alternative="two-sided",
            alpha=0.05,
            power=0.8,
            method="z-p0",
            continuity_correction=True,
        )


def test_solve_null_proportion(case: TestCase) -> None:

    if case.method == "exact":
        return

    direction = "greater" if case.null_proportion > case.proportion else "less"
    assert (
        round(
            solve_null_proportion(
                proportion=case.proportion,
                size=case.size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                continuity_correction=case.continuity_correction,
                direction=direction,
            ),
            2,
        )
        == case.null_proportion
    )


def test_solve_null_proportion_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_null_proportion(
            proportion=0.5,
            size=100,
            alternative="two-sided",
            alpha=0.05,
            power=0.8,
            method="z-p0",
            continuity_correction=True,
        )
