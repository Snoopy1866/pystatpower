from dataclasses import dataclass
from typing import Literal

import pytest

from pystatpower.correlation.ci import solve_distance, solve_size

from tests.models import BaseTestCase


@dataclass(kw_only=True)
class TestCase(BaseTestCase):
    correlation: float
    size: int
    conf_level: float
    interval_type: Literal["two-sided", "lower", "upper"]
    bias_adj: bool
    distance: float
    actual_distance: float


case_group_not_bias_adj = (
    [
        # correlation = 0.05 to 0.95 by 0.05, conf_level = 0.95, alternative = "two-sided", distance = 0.10, bias_adj = False
        TestCase(correlation=correlation, size=size, conf_level=0.95, interval_type="two-sided", bias_adj=False, distance=0.10, actual_distance=actual_distance)
        for correlation, size, actual_distance in [
            (0.05, 1530, 0.099979331717472),
            (0.10, 1507, 0.099984091436488),
            (0.15, 1469, 0.099994087978655),
            (0.20, 1417, 0.099995092984861),
            (0.25, 1352, 0.099978951865763),
            (0.30, 1274, 0.099983282146451),
            (0.35, 1185, 0.099981330392455),
            (0.40, 1086, 0.099994483830285),
            (0.45, 980, 0.099962668234808),
            (0.50, 867, 0.099981828376062),
            (0.55, 751, 0.099954381700265),
            (0.60, 633, 0.099967040247887),
            (0.65, 517, 0.099916027104486),
            (0.70, 404, 0.099982215320462),
            (0.75, 299, 0.099975087516713),
            (0.80, 205, 0.099865422390227),
            (0.85, 125, 0.099683159562744),
            (0.90, 62, 0.099963172662623),
            (0.95, 22, 0.097922665356393),
        ]
    ]
    + [
        # correlation = 0.05 to 0.95 by 0.05, conf_level = 0.95, alternative = "upper", distance = 0.10, bias_adj = False
        TestCase(correlation=correlation, size=size, conf_level=0.95, interval_type="upper", bias_adj=False, distance=0.10, actual_distance=actual_distance)
        for correlation, size, actual_distance in [
            (0.05, 268, 0.099945111385950),
            (0.10, 262, 0.099816657006419),
            (0.15, 252, 0.099968112777152),
            (0.20, 241, 0.099847999108691),
            (0.25, 227, 0.099886326471037),
            (0.30, 211, 0.099933430170927),
            (0.35, 194, 0.099809302872852),
            (0.40, 175, 0.099821253045578),
            (0.45, 155, 0.099814585407058),
            (0.50, 134, 0.099917108711245),
            (0.55, 113, 0.099949897421270),
            (0.60, 93, 0.099606806897013),
            (0.65, 73, 0.099536425872647),
            (0.70, 54, 0.099644693746844),
            (0.75, 37, 0.099692332674108),
            (0.80, 23, 0.098890934167862),
            (0.85, 12, 0.097263612520933),
            (0.90, 4, 0.096085072368805),
            (0.95, 4, 0.048090811067751),
        ]
    ]
    + [
        # correlation = 0.05 to 0.95 by 0.05, conf_level = 0.95, alternative = "lower", distance = 0.10, bias_adj = False
        TestCase(correlation=correlation, size=size, conf_level=0.95, interval_type="lower", bias_adj=False, distance=0.10, actual_distance=actual_distance)
        for correlation, size, actual_distance in [
            (0.05, 274, 0.099834696441772),
            (0.10, 272, 0.099953147908188),
            (0.15, 268, 0.099943988974280),
            (0.20, 262, 0.099810938370096),
            (0.25, 252, 0.099966752707981),
            (0.30, 241, 0.099839660802411),
            (0.35, 227, 0.099878563360771),
            (0.40, 211, 0.099927886685647),
            (0.45, 194, 0.099790213511564),
            (0.50, 175, 0.099799846343275),
            (0.55, 155, 0.099788059009436),
            (0.60, 134, 0.099902875608244),
            (0.65, 113, 0.099939492795180),
            (0.70, 93, 0.099507075241349),
            (0.75, 73, 0.099388988549015),
            (0.80, 54, 0.099497393554749),
            (0.85, 37, 0.099515797845095),
            (0.90, 23, 0.097919259752027),
            (0.95, 12, 0.092586342812536),
        ]
    ]
)


case_group_bias_adj = (
    [
        # correlation = 0.05 to 0.95 by 0.05, conf_level = 0.95, alternative = "two-sided", distance = 0.10, bias_adj = True
        TestCase(correlation=correlation, size=size, conf_level=0.95, interval_type="two-sided", bias_adj=True, distance=0.10, actual_distance=actual_distance)
        for correlation, size, actual_distance in [
            (0.05, 1530, 0.099979332),
            (0.10, 1507, 0.099984091),
            (0.15, 1469, 0.099994088),
            (0.20, 1417, 0.099995093),
            (0.25, 1352, 0.099978952),
            (0.30, 1274, 0.099983282),
            (0.35, 1185, 0.099981330),
            (0.40, 1086, 0.099994484),
            (0.45, 980, 0.099962668),
            (0.50, 867, 0.099981828),
            (0.55, 751, 0.099954382),
            (0.60, 633, 0.099967040),
            (0.65, 517, 0.099916027),
            (0.70, 404, 0.099982215),
            (0.75, 299, 0.099975088),
            (0.80, 205, 0.099865422),
            (0.85, 125, 0.099683160),
            (0.90, 62, 0.099963173),
            (0.95, 22, 0.097922665),
        ]
    ]
    + [
        # correlation = 0.05 to 0.95 by 0.05, conf_level = 0.95, alternative = "upper", distance = 0.10, bias_adj = True
        TestCase(correlation=correlation, size=size, conf_level=0.95, interval_type="upper", bias_adj=True, distance=0.10, actual_distance=actual_distance)
        for correlation, size, actual_distance in [
            (0.05, 268, 0.099945111),
            (0.10, 262, 0.099816657),
            (0.15, 252, 0.099968113),
            (0.20, 241, 0.099847999),
            (0.25, 227, 0.099886326),
            (0.30, 211, 0.099933430),
            (0.35, 194, 0.099809303),
            (0.40, 175, 0.099821253),
            (0.45, 155, 0.099814585),
            (0.50, 134, 0.099917109),
            (0.55, 113, 0.099949897),
            (0.60, 93, 0.099606807),
            (0.65, 73, 0.099536426),
            (0.70, 54, 0.099644694),
            (0.75, 37, 0.099692333),
            (0.80, 23, 0.098890934),
            (0.85, 12, 0.097263613),
            (0.90, 4, 0.096085072),
            (0.95, 4, 0.048090811),
        ]
    ]
    + [
        # correlation = 0.05 to 0.95 by 0.05, conf_level = 0.95, alternative = "lower", distance = 0.10, bias_adj = True
        TestCase(correlation=correlation, size=size, conf_level=0.95, interval_type="lower", bias_adj=True, distance=0.10, actual_distance=actual_distance)
        for correlation, size, actual_distance in [
            (0.05, 274, 0.099834696),
            (0.10, 272, 0.099953148),
            (0.15, 268, 0.099943989),
            (0.20, 262, 0.099810938),
            (0.25, 252, 0.099966753),
            (0.30, 241, 0.099839661),
            (0.35, 227, 0.099878563),
            (0.40, 211, 0.099927887),
            (0.45, 194, 0.099790214),
            (0.50, 175, 0.099799846),
            (0.55, 155, 0.099788059),
            (0.60, 134, 0.099902876),
            (0.65, 113, 0.099939493),
            (0.70, 93, 0.099507075),
            (0.75, 73, 0.099388989),
            (0.80, 54, 0.099497394),
            (0.85, 37, 0.099515798),
            (0.90, 23, 0.097919260),
            (0.95, 12, 0.092586343),
        ]
    ]
)


case_group = case_group_not_bias_adj + case_group_bias_adj


def test_solve_distance(case: TestCase) -> None:

    if case.bias_adj:
        pytest.skip(reason="Both SAS and PASS do not support the bias adjustment, skipping the 'bias_adj = True' test cases.")

    assert round(
        solve_distance(
            correlation=case.correlation,
            size=case.size,
            conf_level=case.conf_level,
            interval_type=case.interval_type,
            bias_adj=case.bias_adj,
        ),
        6,
    ) == round(case.actual_distance, 6)


def test_solve_size(case: TestCase) -> None:

    if case.bias_adj:
        pytest.skip(reason="Both SAS and PASS do not support the bias adjustment, skipping the 'bias_adj = True' test cases.")

    assert (
        solve_size(
            correlation=case.correlation,
            distance=case.distance,
            conf_level=case.conf_level,
            interval_type=case.interval_type,
            bias_adj=case.bias_adj,
        )
        == case.size
    )
