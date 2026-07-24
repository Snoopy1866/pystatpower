# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Validation Software: PASS 2025
# Module: Equivalence Tests for One Proportion

from dataclasses import dataclass
from typing import Literal

from pystatpower.proportion.single.equivalence import solve_power
from pystatpower.proportion.single.equivalence import solve_size
from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    proportion: float
    null_proportion: float
    margin_lower: float
    margin_upper: float
    size: int
    alpha: float
    method: Literal["z-p0", "z-phat"]
    continuity_correction: bool
    power: float
    actual_power: float


case_group_z_p0 = [
    # proportion = 0.71 to 0.89 by 0.01, null_proportion = 0.80, margin_lower = -0.10, margin_upper = 0.10, alpha = 0.025, power = 0.80, method = "z-p0", continuity_correction = False
    TestCase(
        proportion=proportion,
        null_proportion=0.80,
        margin_lower=-0.10,
        margin_upper=0.10,
        size=size,
        alpha=0.025,
        power=0.80,
        method="z-p0",
        continuity_correction=False,
        actual_power=actual_power,
    )
    for proportion, size, actual_power in [
        (0.71, 16386, 0.800008645395320),
        (0.72, 4071, 0.800020228237472),
        (0.73, 1798, 0.800170764010163),
        (0.74, 1004, 0.800067735296659),
        (0.75, 638, 0.800214633755415),
        (0.76, 440, 0.800628721682362),
        (0.77, 321, 0.801179860895646),
        (0.78, 244, 0.800959648152263),
        (0.79, 195, 0.800726424606503),
        (0.80, 168, 0.801789107079452),
        (0.81, 156, 0.801493296253854),
        (0.82, 157, 0.802101987330091),
        (0.83, 175, 0.801542133869552),
        (0.84, 224, 0.800570667573584),
        (0.85, 316, 0.800243662399114),
        (0.86, 485, 0.800715516538510),
        (0.87, 843, 0.800003797491396),
        (0.88, 1856, 0.800122869124067),
        (0.89, 7248, 0.800025059163928),
    ]
]

case_group_z_p0_cc = [
    # proportion = 0.71 to 0.89 by 0.01, null_proportion = 0.80, margin_lower = -0.10, margin_upper = 0.10, alpha = 0.025, power = 0.80, method = "z-p0", continuity_correction = True
    TestCase(
        proportion=proportion,
        null_proportion=0.80,
        margin_lower=-0.10,
        margin_upper=0.10,
        size=size,
        alpha=0.025,
        power=0.80,
        method="z-p0",
        continuity_correction=True,
        actual_power=actual_power,
    )
    for proportion, size, actual_power in [
        (0.71, 16486, 0.800012299780784),
        (0.72, 4121, 0.800035047971845),
        (0.73, 1831, 0.800130265198342),
        (0.74, 1029, 0.800128888526456),
        (0.75, 658, 0.800311803767697),
        (0.76, 456, 0.800146910867358),
        (0.77, 335, 0.801010770820005),
        (0.78, 256, 0.800466127949615),
        (0.79, 206, 0.801312828015927),
        (0.80, 178, 0.802230800014678),
        (0.81, 166, 0.802350624361241),
        (0.82, 167, 0.800337918494614),
        (0.83, 188, 0.801996006026150),
        (0.84, 240, 0.800175657767678),
        (0.85, 336, 0.800571558656332),
        (0.86, 509, 0.800208239574793),
        (0.87, 877, 0.800426338593650),
        (0.88, 1906, 0.800188410060528),
        (0.89, 7348, 0.800042935968912),
    ]
]

case_group_z_phat = [
    # proportion = 0.71 to 0.89 by 0.01, null_proportion = 0.80, margin_lower = -0.10, margin_upper = 0.10, alpha = 0.025, power = 0.80, method = "z-phat", continuity_correction = False
    TestCase(
        proportion=proportion,
        null_proportion=0.80,
        margin_lower=-0.10,
        margin_upper=0.10,
        size=size,
        alpha=0.025,
        power=0.80,
        method="z-phat",
        continuity_correction=False,
        actual_power=actual_power,
    )
    for proportion, size, actual_power in [
        (0.71, 16161, 0.800003800757050),
        (0.72, 3956, 0.800016318697791),
        (0.73, 1719, 0.800021750404768),
        (0.74, 944, 0.800071544574412),
        (0.75, 589, 0.800222417640806),
        (0.76, 398, 0.800316401568403),
        (0.77, 285, 0.801249564933707),
        (0.78, 217, 0.801375954276119),
        (0.79, 182, 0.800223274815251),
        (0.80, 169, 0.802961846320122),
        (0.81, 169, 0.800738509804512),
        (0.82, 187, 0.802204172126832),
        (0.83, 227, 0.801133296831188),
        (0.84, 294, 0.801299217214459),
        (0.85, 401, 0.800691754951146),
        (0.86, 591, 0.800246739379968),
        (0.87, 987, 0.800261253764890),
        (0.88, 2073, 0.800169469068211),
        (0.89, 7685, 0.800048313460553),
    ]
]

case_group_z_phat_cc = [
    # proportion = 0.71 to 0.89 by 0.01, null_proportion = 0.80, margin_lower = -0.10, margin_upper = 0.10, alpha = 0.025, power = 0.80, method = "z-phat", continuity_correction = True
    TestCase(
        proportion=proportion,
        null_proportion=0.80,
        margin_lower=-0.10,
        margin_upper=0.10,
        size=size,
        alpha=0.025,
        power=0.80,
        method="z-phat",
        continuity_correction=True,
        actual_power=actual_power,
    )
    for proportion, size, actual_power in [
        (0.71, 16261, 0.800007531462899),
        (0.72, 4006, 0.800031784019027),
        (0.73, 1753, 0.800209909579564),
        (0.74, 969, 0.800138514675414),
        (0.75, 609, 0.800331680146841),
        (0.76, 415, 0.800809691940262),
        (0.77, 299, 0.801196837939170),
        (0.78, 229, 0.801771186082395),
        (0.79, 193, 0.802231737618877),
        (0.80, 178, 0.800073350151615),
        (0.81, 180, 0.802924842313689),
        (0.82, 198, 0.800353268485122),
        (0.83, 241, 0.801135120000960),
        (0.84, 310, 0.800710197383088),
        (0.85, 421, 0.800923658669870),
        (0.86, 616, 0.800414922435674),
        (0.87, 1020, 0.800237025247695),
        (0.88, 2122, 0.800036010477757),
        (0.89, 7784, 0.800013672909686),
    ]
]

case_group = case_group_z_p0 + case_group_z_p0_cc + case_group_z_phat + case_group_z_phat_cc


def test_size_solve_power(case: TestCase) -> None:
    assert round(
        solve_power(
            proportion=case.proportion,
            null_proportion=case.null_proportion,
            margin_lower=case.margin_lower,
            margin_upper=case.margin_upper,
            size=case.size,
            alpha=case.alpha,
            method=case.method,
            continuity_correction=case.continuity_correction,
        ),
        6,
    ) == round(case.actual_power, 6)


def test_solve_size(case: TestCase) -> None:
    assert (
        solve_size(
            proportion=case.proportion,
            null_proportion=case.null_proportion,
            margin_lower=case.margin_lower,
            margin_upper=case.margin_upper,
            alpha=case.alpha,
            power=case.power,
            method=case.method,
            continuity_correction=case.continuity_correction,
        )
        == case.size
    )
