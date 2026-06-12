from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.correlation.ci import solve_distance, solve_size, solve_correlation
from pystatpower.exceptions import SolutionNotFoundError


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
            (0.05, 1530, 0.10, 0.099979332),
            (0.10, 1507, 0.10, 0.099984091),
            (0.15, 1469, 0.10, 0.099994088),
            (0.20, 1417, 0.10, 0.099995093),
            (0.25, 1352, 0.10, 0.099978952),
            (0.30, 1274, 0.10, 0.099983282),
            (0.35, 1185, 0.10, 0.099981330),
            (0.40, 1086, 0.10, 0.099994484),
            (0.45, 980, 0.10, 0.099962668),
            (0.50, 867, 0.10, 0.099981828),
            (0.55, 751, 0.10, 0.099954382),
            (0.60, 633, 0.10, 0.099967040),
            (0.65, 517, 0.10, 0.099916027),
            (0.70, 404, 0.10, 0.099982215),
            (0.75, 299, 0.10, 0.099975088),
            (0.80, 205, 0.10, 0.099865422),
            (0.85, 125, 0.10, 0.099683160),
            (0.90, 62, 0.10, 0.099963173),
            (0.95, 22, 0.10, 0.097922665),
        ]
    ]
    + [
        # correlation = 0.05 to 0.95 by 0.05, conf_level = 0.95, alternative = "upper", bias_adj = False
        TestCase(correlation=correlation, size=size, conf_level=0.95, interval_type="upper", bias_adj=False, distance=distance, actual_distance=actual_distance)
        for correlation, size, distance, actual_distance in [
            (0.05, 268, 0.10, 0.099945111),
            (0.10, 262, 0.10, 0.099816657),
            (0.15, 252, 0.10, 0.099968113),
            (0.20, 241, 0.10, 0.099847999),
            (0.25, 227, 0.10, 0.099886326),
            (0.30, 211, 0.10, 0.099933430),
            (0.35, 194, 0.10, 0.099809303),
            (0.40, 175, 0.10, 0.099821253),
            (0.45, 155, 0.10, 0.099814585),
            (0.50, 134, 0.10, 0.099917109),
            (0.55, 113, 0.10, 0.099949897),
            (0.60, 93, 0.10, 0.099606807),
            (0.65, 73, 0.10, 0.099536426),
            (0.70, 54, 0.10, 0.099644694),
            (0.75, 37, 0.10, 0.099692333),
            (0.80, 23, 0.10, 0.098890934),
            (0.85, 12, 0.10, 0.097263613),
            (0.90, 4, 0.10, 0.096085072),
            (0.95, 4, 0.10, 0.048090811),
        ]
    ]
    + [
        # correlation = 0.05 to 0.95 by 0.05, conf_level = 0.95, alternative = "lower", bias_adj = False
        TestCase(correlation=correlation, size=size, conf_level=0.95, interval_type="lower", bias_adj=False, distance=distance, actual_distance=actual_distance)
        for correlation, size, distance, actual_distance in [
            (0.05, 274, 0.10, 0.099834696),
            (0.10, 272, 0.10, 0.099953148),
            (0.15, 268, 0.10, 0.099943989),
            (0.20, 262, 0.10, 0.099810938),
            (0.25, 252, 0.10, 0.099966753),
            (0.30, 241, 0.10, 0.099839661),
            (0.35, 227, 0.10, 0.099878563),
            (0.40, 211, 0.10, 0.099927887),
            (0.45, 194, 0.10, 0.099790214),
            (0.50, 175, 0.10, 0.099799846),
            (0.55, 155, 0.10, 0.099788059),
            (0.60, 134, 0.10, 0.099902876),
            (0.65, 113, 0.10, 0.099939493),
            (0.70, 93, 0.10, 0.099507075),
            (0.75, 73, 0.10, 0.099388989),
            (0.80, 54, 0.10, 0.099497394),
            (0.85, 37, 0.10, 0.099515798),
            (0.90, 23, 0.10, 0.097919260),
            (0.95, 12, 0.10, 0.092586343),
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
            9,
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


def test_solve_correlation(case: TestCase) -> None:
    res = solve_correlation(
        distance=case.actual_distance,
        size=case.size,
        conf_level=case.conf_level,
        interval_type=case.interval_type,
        bias_adj=case.bias_adj,
    )

    if isinstance(res, float):
        assert round(res, 2) == case.correlation
    elif isinstance(res, tuple):
        assert round(res[0], 2) == case.correlation or round(res[1], 2) == case.correlation
    else:
        assert False


def test_solve_correlation_exception() -> None:
    with pytest.raises(SolutionNotFoundError):
        solve_correlation(distance=0.1, size=274, conf_level=0.95, interval_type="lower", bias_adj=False)
