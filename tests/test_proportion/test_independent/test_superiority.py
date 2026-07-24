# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Validation Software: PASS 2025
# Module: Superiority by a Margin for the Difference Between Two Proportions

from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.proportion.independent.superiority import solve_margin
from pystatpower.proportion.independent.superiority import solve_power
from pystatpower.proportion.independent.superiority import solve_reference_proportion
from pystatpower.proportion.independent.superiority import solve_size
from pystatpower.proportion.independent.superiority import solve_superiority_proportion
from pystatpower.proportion.independent.superiority import solve_treatment_proportion
from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    treatment_proportion: float
    reference_proportion: float
    margin: float | None = None
    superiority_proportion: float | None = None
    treatment_size: int
    reference_size: int
    alternative: Literal["greater", "less"]
    alpha: float
    method: Literal["z-pooled", "z-unpooled"]
    continuity_correction: bool
    power: float
    actual_power: float

    ratio: float | None = None

    def __post_init__(self) -> None:
        if self.ratio is None:
            self.ratio = self.treatment_size / self.reference_size

        if self.superiority_proportion is None:
            self.superiority_proportion = self.reference_proportion + self.margin


case_group_pooled = (
    [
        # treatment_proportion = 0.95, reference_proportion = 0.70 to 0.85 by 0.01, margin = 0.05, ratio = 0.5, alternative = "greater", method = "z-pooled", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0.05,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.95, 0.70, 75, 38, 0.803444603013955),
            (0.95, 0.71, 81, 41, 0.801365228735172),
            (0.95, 0.72, 89, 45, 0.803685869623629),
            (0.95, 0.73, 97, 49, 0.801313601199356),
            (0.95, 0.74, 107, 54, 0.801068168707404),
            (0.95, 0.75, 119, 60, 0.801300227267644),
            (0.95, 0.76, 133, 67, 0.800512338333167),
            (0.95, 0.77, 151, 76, 0.802044976303477),
            (0.95, 0.78, 173, 87, 0.803023540292531),
            (0.95, 0.79, 199, 100, 0.800972207636175),
            (0.95, 0.80, 234, 117, 0.800495131089949),
            (0.95, 0.81, 280, 140, 0.800544571701990),
            (0.95, 0.82, 343, 172, 0.801230771916748),
            (0.95, 0.83, 432, 216, 0.800073277552776),
            (0.95, 0.84, 567, 284, 0.800483947581391),
            (0.95, 0.85, 785, 393, 0.800122773773160),
        ]
    ]
    + [
        # treatment_proportion = 0.60, reference_proportion = 0.70 to 0.85 by 0.01, margin = -0.05, ratio = 2, alternative = "less", method = "z-pooled", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=-0.05,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="less",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.60, 0.70, 1058, 2116, 0.800199803328006),
            (0.60, 0.71, 728, 1456, 0.800104673864339),
            (0.60, 0.72, 530, 1060, 0.800212532833877),
            (0.60, 0.73, 402, 804, 0.800408308705910),
            (0.60, 0.74, 315, 630, 0.801191770768206),
            (0.60, 0.75, 252, 504, 0.800585799441923),
            (0.60, 0.76, 206, 412, 0.800748745912685),
            (0.60, 0.77, 171, 342, 0.800632153811169),
            (0.60, 0.78, 144, 288, 0.800886549058955),
            (0.60, 0.79, 123, 246, 0.802248817498394),
            (0.60, 0.80, 106, 212, 0.803314100007647),
            (0.60, 0.81, 92, 184, 0.803917783379996),
            (0.60, 0.82, 80, 160, 0.802519923455680),
            (0.60, 0.83, 70, 140, 0.801108774280558),
            (0.60, 0.84, 62, 124, 0.802211787192024),
            (0.60, 0.85, 55, 110, 0.802083037952487),
        ]
    ]
    + [
        # treatment_proportion = 0.90, reference_proportion = 0.70, margin = 0 to 0.15 by 0.01, ratio = 2, alternative = "greater", method = "z-pooled", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=margin,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, margin, treatment_size, reference_size, actual_power in [
            (0.90, 0.70, 0.00, 87, 44, 0.802108277112294),
            (0.90, 0.70, 0.01, 97, 49, 0.804129372456354),
            (0.90, 0.70, 0.02, 107, 54, 0.800275408845470),
            (0.90, 0.70, 0.03, 121, 61, 0.803208398674937),
            (0.90, 0.70, 0.04, 137, 69, 0.804079314332581),
            (0.90, 0.70, 0.05, 155, 78, 0.801851788416907),
            (0.90, 0.70, 0.06, 178, 89, 0.800643816525670),
            (0.90, 0.70, 0.07, 207, 104, 0.802643132805260),
            (0.90, 0.70, 0.08, 242, 121, 0.800224480122883),
            (0.90, 0.70, 0.09, 288, 144, 0.800224480122883),
            (0.90, 0.70, 0.10, 349, 175, 0.801367846217016),
            (0.90, 0.70, 0.11, 430, 215, 0.800035527154478),
            (0.90, 0.70, 0.12, 545, 273, 0.800943566533859),
            (0.90, 0.70, 0.13, 711, 356, 0.800424253323451),
            (0.90, 0.70, 0.14, 967, 484, 0.800062877390611),
            (0.90, 0.70, 0.15, 1393, 697, 0.800133288785701),
        ]
    ]
)

case_group_pooled_cc = (
    [
        # treatment_proportion = 0.95, reference_proportion = 0.70 to 0.85 by 0.01, margin = 0.05, ratio = 0.5, alternative = "greater", method = "z-pooled", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0.05,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.95, 0.70, 89, 45, 0.801816236673023),
            (0.95, 0.71, 97, 49, 0.805121043389059),
            (0.95, 0.72, 105, 53, 0.803740570772765),
            (0.95, 0.73, 115, 58, 0.805074737910681),
            (0.95, 0.74, 125, 63, 0.800973096733623),
            (0.95, 0.75, 139, 70, 0.803459905502484),
            (0.95, 0.76, 155, 78, 0.803991827444517),
            (0.95, 0.77, 173, 87, 0.801365847775097),
            (0.95, 0.78, 197, 99, 0.802633159984426),
            (0.95, 0.79, 225, 113, 0.800206130429461),
            (0.95, 0.80, 263, 132, 0.801104185625244),
            (0.95, 0.81, 313, 157, 0.801936074070607),
            (0.95, 0.82, 379, 190, 0.800651494895980),
            (0.95, 0.83, 474, 237, 0.800164866414633),
            (0.95, 0.84, 616, 308, 0.800144528917762),
            (0.95, 0.85, 845, 423, 0.800608658016376),
        ]
    ]
    + [
        # treatment_proportion = 0.60, reference_proportion = 0.70 to 0.85 by 0.01, margin = -0.05, ratio = 2, alternative = "less", method = "z-pooled", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=-0.05,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="less",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.60, 0.70, 1088, 2176, 0.800275505518563),
            (0.60, 0.71, 753, 1506, 0.800214910127597),
            (0.60, 0.72, 551, 1102, 0.800052012949071),
            (0.60, 0.73, 421, 842, 0.800847729190607),
            (0.60, 0.74, 331, 662, 0.800633806123860),
            (0.60, 0.75, 267, 534, 0.800906575305311),
            (0.60, 0.76, 220, 440, 0.801815644134529),
            (0.60, 0.77, 184, 368, 0.802219923815940),
            (0.60, 0.78, 155, 310, 0.800027180621703),
            (0.60, 0.79, 133, 266, 0.800704108317292),
            (0.60, 0.80, 115, 230, 0.800503709036977),
            (0.60, 0.81, 101, 202, 0.803271578670369),
            (0.60, 0.82, 89, 178, 0.804374856443181),
            (0.60, 0.83, 78, 156, 0.800511462782597),
            (0.60, 0.84, 70, 140, 0.804187853706354),
            (0.60, 0.85, 62, 124, 0.800216020645640),
        ]
    ]
    + [
        # treatment_proportion = 0.90, reference_proportion = 0.70, margin = 0 to 0.15 by 0.01, ratio = 2, alternative = "greater", method = "z-pooled", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=margin,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            method="z-pooled",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, margin, treatment_size, reference_size, actual_power in [
            (0.90, 0.70, 0.00, 101, 51, 0.800296136980926),
            (0.90, 0.70, 0.01, 112, 56, 0.801113529422866),
            (0.90, 0.70, 0.02, 124, 62, 0.801370077061472),
            (0.90, 0.70, 0.03, 138, 69, 0.801240494433846),
            (0.90, 0.70, 0.04, 155, 78, 0.803618018736799),
            (0.90, 0.70, 0.05, 175, 88, 0.803207725049118),
            (0.90, 0.70, 0.06, 199, 100, 0.802133971286543),
            (0.90, 0.70, 0.07, 229, 115, 0.801784846213773),
            (0.90, 0.70, 0.08, 267, 134, 0.801977518277513),
            (0.90, 0.70, 0.09, 315, 158, 0.801359983989459),
            (0.90, 0.70, 0.10, 378, 189, 0.800345367996964),
            (0.90, 0.70, 0.11, 463, 232, 0.800752944206074),
            (0.90, 0.70, 0.12, 581, 291, 0.800347111381320),
            (0.90, 0.70, 0.13, 753, 377, 0.800299577179967),
            (0.90, 0.70, 0.14, 1017, 509, 0.800296676165602),
            (0.90, 0.70, 0.15, 1453, 727, 0.800296731863563),
        ]
    ]
)

case_group_unpooled = (
    [
        # treatment_proportion = 0.95, reference_proportion = 0.70 to 0.85 by 0.01, margin = 0.05, ratio = 0.5, alternative = "greater", method = "z-unpooled", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0.05,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.95, 0.70, 91, 46, 0.800698406059017),
            (0.95, 0.71, 99, 50, 0.800135111308754),
            (0.95, 0.72, 109, 55, 0.802543284457485),
            (0.95, 0.73, 120, 60, 0.800130031067646),
            (0.95, 0.74, 133, 67, 0.803953312385551),
            (0.95, 0.75, 147, 74, 0.801332929427480),
            (0.95, 0.76, 165, 83, 0.801839189497708),
            (0.95, 0.77, 187, 94, 0.802756988713212),
            (0.95, 0.78, 213, 107, 0.801692762655827),
            (0.95, 0.79, 247, 124, 0.802906040164145),
            (0.95, 0.80, 289, 145, 0.801928085959101),
            (0.95, 0.81, 345, 173, 0.801794143264181),
            (0.95, 0.82, 421, 211, 0.801467926965203),
            (0.95, 0.83, 529, 265, 0.801287200661768),
            (0.95, 0.84, 689, 345, 0.800135503697114),
            (0.95, 0.85, 949, 475, 0.800053009587000),
        ]
    ]
    + [
        # treatment_proportion = 0.60, reference_proportion = 0.70 to 0.85 by 0.01, margin = -0.05, ratio = 2, alternative = "less", method = "z-unpooled", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=-0.05,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="less",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.60, 0.70, 1084, 2168, 0.800309214291297),
            (0.60, 0.71, 748, 1496, 0.800149532885380),
            (0.60, 0.72, 546, 1092, 0.800073555655052),
            (0.60, 0.73, 416, 832, 0.800760558045954),
            (0.60, 0.74, 326, 652, 0.800268341473862),
            (0.60, 0.75, 262, 524, 0.800065321549853),
            (0.60, 0.76, 215, 430, 0.800294147755183),
            (0.60, 0.77, 180, 360, 0.802006431574506),
            (0.60, 0.78, 152, 304, 0.801777545514943),
            (0.60, 0.79, 130, 260, 0.802033974041354),
            (0.60, 0.80, 112, 224, 0.801301455458812),
            (0.60, 0.81, 98, 196, 0.803302281147728),
            (0.60, 0.82, 86, 172, 0.803542890643851),
            (0.60, 0.83, 76, 152, 0.803976790477263),
            (0.60, 0.84, 67, 134, 0.801220571758194),
            (0.60, 0.85, 60, 120, 0.802601294534439),
        ]
    ]
    + [
        # treatment_proportion = 0.90, reference_proportion = 0.70, margin = 0 to 0.15 by 0.01, ratio = 2, alternative = "greater", method = "z-unpooled", continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=margin,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, margin, treatment_size, reference_size, actual_power in [
            (0.90, 0.70, 0.00, 101, 51, 0.806753661118245),
            (0.90, 0.70, 0.01, 111, 56, 0.803293177434991),
            (0.90, 0.70, 0.02, 123, 62, 0.800871819787434),
            (0.90, 0.70, 0.03, 139, 70, 0.803687643225655),
            (0.90, 0.70, 0.04, 157, 79, 0.803628709572349),
            (0.90, 0.70, 0.05, 178, 89, 0.800202841452828),
            (0.90, 0.70, 0.06, 205, 103, 0.803036604663570),
            (0.90, 0.70, 0.07, 237, 119, 0.801589387938936),
            (0.90, 0.70, 0.08, 278, 139, 0.800026581322715),
            (0.90, 0.70, 0.09, 331, 166, 0.801185432953401),
            (0.90, 0.70, 0.10, 401, 201, 0.801494437629848),
            (0.90, 0.70, 0.11, 495, 248, 0.801293487101545),
            (0.90, 0.70, 0.12, 625, 313, 0.800229180955586),
            (0.90, 0.70, 0.13, 817, 409, 0.800431235311240),
            (0.90, 0.70, 0.14, 1112, 556, 0.800026581322715),
            (0.90, 0.70, 0.15, 1601, 801, 0.800159630537390),
        ]
    ]
)

case_group_unpooled_cc = (
    [
        # treatment_proportion = 0.95, reference_proportion = 0.70 to 0.85 by 0.01, margin = 0.05, ratio = 0.5, alternative = "greater", method = "z-unpooled", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0.05,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.95, 0.70, 107, 54, 0.806968395255717),
            (0.95, 0.71, 115, 58, 0.802940277110016),
            (0.95, 0.72, 125, 63, 0.802033618555018),
            (0.95, 0.73, 137, 69, 0.802671488796340),
            (0.95, 0.74, 151, 76, 0.803378784127848),
            (0.95, 0.75, 167, 84, 0.802838310259286),
            (0.95, 0.76, 186, 93, 0.800194259968393),
            (0.95, 0.77, 209, 105, 0.801789143054007),
            (0.95, 0.78, 237, 119, 0.801025881090687),
            (0.95, 0.79, 273, 137, 0.801938377248403),
            (0.95, 0.80, 317, 159, 0.800154268270877),
            (0.95, 0.81, 377, 189, 0.801097893286785),
            (0.95, 0.82, 457, 229, 0.800773816716364),
            (0.95, 0.83, 571, 286, 0.801237108367839),
            (0.95, 0.84, 739, 370, 0.800608350772512),
            (0.95, 0.85, 1009, 505, 0.800416464775318),
        ]
    ]
    + [
        # treatment_proportion = 0.60, reference_proportion = 0.70 to 0.85 by 0.01, margin = -0.05, ratio = 2, alternative = "less", method = "z-unpooled", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=-0.05,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="less",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.60, 0.70, 1113, 2226, 0.800020547330437),
            (0.60, 0.71, 773, 1546, 0.800255458413284),
            (0.60, 0.72, 568, 1136, 0.800628420998836),
            (0.60, 0.73, 434, 868, 0.800244545549955),
            (0.60, 0.74, 343, 686, 0.800911698671728),
            (0.60, 0.75, 277, 554, 0.800369047912521),
            (0.60, 0.76, 229, 458, 0.801324907019065),
            (0.60, 0.77, 192, 384, 0.801361702926306),
            (0.60, 0.78, 163, 326, 0.800916199866685),
            (0.60, 0.79, 140, 280, 0.800497979784794),
            (0.60, 0.80, 122, 244, 0.802016245928679),
            (0.60, 0.81, 107, 214, 0.802626345805253),
            (0.60, 0.82, 94, 188, 0.800732175043039),
            (0.60, 0.83, 84, 168, 0.803326907626960),
            (0.60, 0.84, 75, 150, 0.803041670796890),
            (0.60, 0.85, 67, 134, 0.800705973718494),
        ]
    ]
    + [
        # treatment_proportion = 0.90, reference_proportion = 0.70, margin = 0 to 0.15 by 0.01, ratio = 2, alternative = "greater", method = "z-unpooled", continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=margin,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alternative="greater",
            alpha=0.025,
            power=0.8,
            method="z-unpooled",
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, margin, treatment_size, reference_size, actual_power in [
            (0.90, 0.70, 0.00, 115, 58, 0.804715379731597),
            (0.90, 0.70, 0.01, 127, 64, 0.805652028808185),
            (0.90, 0.70, 0.02, 139, 70, 0.800278007713332),
            (0.90, 0.70, 0.03, 155, 78, 0.800420641997346),
            (0.90, 0.70, 0.04, 175, 88, 0.802971221706705),
            (0.90, 0.70, 0.05, 197, 99, 0.800891596223787),
            (0.90, 0.70, 0.06, 225, 113, 0.801258915502807),
            (0.90, 0.70, 0.07, 259, 130, 0.800637277975028),
            (0.90, 0.70, 0.08, 303, 152, 0.801888076825968),
            (0.90, 0.70, 0.09, 357, 179, 0.800281958758666),
            (0.90, 0.70, 0.10, 429, 215, 0.800042332307117),
            (0.90, 0.70, 0.11, 527, 264, 0.800648121478010),
            (0.90, 0.70, 0.12, 663, 332, 0.800867852289888),
            (0.90, 0.70, 0.13, 859, 430, 0.800272711034650),
            (0.90, 0.70, 0.14, 1161, 581, 0.800151649004693),
            (0.90, 0.70, 0.15, 1661, 831, 0.800290787630421),
        ]
    ]
)


case_group = case_group_pooled + case_group_pooled_cc + case_group_unpooled + case_group_unpooled_cc


def test_solve_power(case: TestCase) -> None:
    assert round(
        solve_power(
            treatment_proportion=case.treatment_proportion,
            reference_proportion=case.reference_proportion,
            margin=case.margin,
            superiority_proportion=case.superiority_proportion,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            alternative=case.alternative,
            alpha=case.alpha,
            method=case.method,
            continuity_correction=case.continuity_correction,
        ),
        6,
    ) == round(case.actual_power, 6)

    assert round(
        solve_power(
            treatment_proportion=case.treatment_proportion,
            reference_proportion=case.reference_proportion,
            margin=case.margin,
            superiority_proportion=None,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            alternative=case.alternative,
            alpha=case.alpha,
            method=case.method,
            continuity_correction=case.continuity_correction,
        ),
        6,
    ) == round(case.actual_power, 6)


def test_solve_power_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_power(
            treatment_proportion=0.95,
            reference_proportion=0.70,
            margin=None,
            superiority_proportion=None,
            treatment_size=100,
            reference_size=100,
            alternative="greater",
            alpha=0.025,
            method="z-pooled",
            continuity_correction=False,
        )


def test_solve_size(case: TestCase) -> None:
    assert solve_size(
        treatment_proportion=case.treatment_proportion,
        reference_proportion=case.reference_proportion,
        margin=case.margin,
        superiority_proportion=case.superiority_proportion,
        alternative=case.alternative,
        ratio=case.ratio,
        alpha=case.alpha,
        power=case.power,
        method=case.method,
        continuity_correction=case.continuity_correction,
    ) == (case.treatment_size, case.reference_size)

    assert solve_size(
        treatment_proportion=case.treatment_proportion,
        reference_proportion=case.reference_proportion,
        margin=case.margin,
        superiority_proportion=None,
        alternative=case.alternative,
        ratio=case.ratio,
        alpha=case.alpha,
        power=case.power,
        method=case.method,
        continuity_correction=case.continuity_correction,
    ) == (case.treatment_size, case.reference_size)


def test_solve_size_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_size(
            treatment_proportion=0.95,
            reference_proportion=0.70,
            margin=None,
            superiority_proportion=None,
            alternative="greater",
            ratio=1,
            alpha=0.025,
            method="z-pooled",
            continuity_correction=False,
        )


def test_solve_treatment_proportion(case: TestCase) -> None:
    assert (
        round(
            solve_treatment_proportion(
                reference_proportion=case.reference_proportion,
                margin=case.margin,
                superiority_proportion=case.superiority_proportion,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.treatment_proportion
    )

    assert (
        round(
            solve_treatment_proportion(
                reference_proportion=case.reference_proportion,
                margin=case.margin,
                superiority_proportion=None,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.treatment_proportion
    )


def test_solve_treatment_proportion_raise_error() -> None:
    with pytest.raises(ValueError):
        solve_treatment_proportion(
            reference_proportion=0.70,
            margin=None,
            superiority_proportion=None,
            treatment_size=100,
            reference_size=100,
            alternative="greater",
            alpha=0.025,
            method="z-pooled",
            continuity_correction=False,
        )


def test_solve_reference_proportion(case: TestCase) -> None:
    assert (
        round(
            solve_reference_proportion(
                treatment_proportion=case.treatment_proportion,
                margin=case.margin,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.reference_proportion
    )


def test_solve_superiority_proportion(case: TestCase) -> None:
    assert round(
        solve_superiority_proportion(
            treatment_proportion=case.treatment_proportion,
            reference_proportion=case.reference_proportion,
            treatment_size=case.treatment_size,
            reference_size=case.reference_size,
            alternative=case.alternative,
            alpha=case.alpha,
            power=case.actual_power,
            method=case.method,
            continuity_correction=case.continuity_correction,
        ),
        2,
    ) == round(case.superiority_proportion, 2)


def test_solve_margin(case: TestCase) -> None:
    assert (
        round(
            solve_margin(
                treatment_proportion=case.treatment_proportion,
                reference_proportion=case.reference_proportion,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alternative=case.alternative,
                alpha=case.alpha,
                power=case.actual_power,
                method=case.method,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.margin
    )
