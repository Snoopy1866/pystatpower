from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.models.correlation.ci import solve_distance, solve_size


@dataclass
class TestCase:
    __test__ = False

    correlation: float
    size: int
    conf_level: float
    interval_type: Literal["two-sided", "upper", "lower"]
    bias_adj: bool
    distance: float
    actual_distance: float


case_group_not_bias_adj = (
    [
        # correlation = 0.05 to 0.95 by 0.05, conf_level = 0.95, alternative = "two-sided", bias_adj = False
        TestCase(correlation=correlation, size=size, conf_level=0.95, interval_type="two-sided", bias_adj=False, distance=distance, actual_distance=actual_distance)
        for correlation, size, distance, actual_distance in [
            (0.05, 1530, 0.10, 0.099979),
            (0.10, 1507, 0.10, 0.099984),
            (0.15, 1469, 0.10, 0.099994),
            (0.20, 1417, 0.10, 0.099995),
            (0.25, 1352, 0.10, 0.099979),
            (0.30, 1274, 0.10, 0.099983),
            (0.35, 1185, 0.10, 0.099981),
            (0.40, 1086, 0.10, 0.099994),
            (0.45, 980, 0.10, 0.099963),
            (0.50, 867, 0.10, 0.099982),
            (0.55, 751, 0.10, 0.099954),
            (0.60, 633, 0.10, 0.099967),
            (0.65, 517, 0.10, 0.099916),
            (0.70, 404, 0.10, 0.099982),
            (0.75, 299, 0.10, 0.099975),
            (0.80, 205, 0.10, 0.099865),
            (0.85, 125, 0.10, 0.099683),
            (0.90, 62, 0.10, 0.099963),
            (0.95, 22, 0.10, 0.097923),
        ]
    ]
    + [
        # correlation = 0.05 to 0.95 by 0.05, conf_level = 0.95, alternative = "upper", bias_adj = False
        TestCase(correlation=correlation, size=size, conf_level=0.95, interval_type="upper", bias_adj=False, distance=distance, actual_distance=actual_distance)
        for correlation, size, distance, actual_distance in [
            (0.05, 268, 0.10, 0.099945),
            (0.10, 262, 0.10, 0.099817),
            (0.15, 252, 0.10, 0.099968),
            (0.20, 241, 0.10, 0.099848),
            (0.25, 227, 0.10, 0.099886),
            (0.30, 211, 0.10, 0.099933),
            (0.35, 194, 0.10, 0.099809),
            (0.40, 175, 0.10, 0.099821),
            (0.45, 155, 0.10, 0.099815),
            (0.50, 134, 0.10, 0.099917),
            (0.55, 113, 0.10, 0.099950),
            (0.60, 93, 0.10, 0.099607),
            (0.65, 73, 0.10, 0.099536),
            (0.70, 54, 0.10, 0.099645),
            (0.75, 37, 0.10, 0.099692),
            (0.80, 23, 0.10, 0.098891),
            (0.85, 12, 0.10, 0.097264),
            (0.90, 4, 0.10, 0.096085),
            (0.95, 4, 0.10, 0.048091),
        ]
    ]
    + [
        # correlation = 0.05 to 0.95 by 0.05, conf_level = 0.95, alternative = "lower", bias_adj = False
        TestCase(correlation=correlation, size=size, conf_level=0.95, interval_type="lower", bias_adj=False, distance=distance, actual_distance=actual_distance)
        for correlation, size, distance, actual_distance in [
            (0.05, 274, 0.10, 0.099835),
            (0.10, 272, 0.10, 0.099953),
            (0.15, 268, 0.10, 0.099944),
            (0.20, 262, 0.10, 0.099811),
            (0.25, 252, 0.10, 0.099967),
            (0.30, 241, 0.10, 0.099840),
            (0.35, 227, 0.10, 0.099879),
            (0.40, 211, 0.10, 0.099928),
            (0.45, 194, 0.10, 0.099790),
            (0.50, 175, 0.10, 0.099800),
            (0.55, 155, 0.10, 0.099788),
            (0.60, 134, 0.10, 0.099903),
            (0.65, 113, 0.10, 0.099939),
            (0.70, 93, 0.10, 0.099507),
            (0.75, 73, 0.10, 0.099389),
            (0.80, 54, 0.10, 0.099497),
            (0.85, 37, 0.10, 0.099516),
            (0.90, 23, 0.10, 0.097919),
            (0.95, 12, 0.10, 0.092586),
        ]
    ]
)

case_group_bias_adj = []


case_group = case_group_not_bias_adj + case_group_bias_adj


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


def test_solve_distance(case: TestCase) -> None:
    assert (
        round(
            solve_distance(
                correlation=case.correlation,
                size=case.size,
                conf_level=case.conf_level,
                interval_type=case.interval_type,
                bias_adj=case.bias_adj,
            ),
            6,
        )
        == case.actual_distance
    )


def test_solve_size(case: TestCase) -> None:
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
