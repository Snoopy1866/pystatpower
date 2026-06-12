# Validation Software: PASS 15
# Module: Confidence Interval for One Proportion

from dataclasses import dataclass, asdict
from typing import Literal

import pytest

from pystatpower.proportion.single.ci import solve_distance, solve_proportion, solve_size


@dataclass
class TestCase:
    __test__ = False

    proportion: float
    size: int
    distance: float
    actual_distance: float
    conf_level: float
    interval_type: Literal["two-sided", "lower one-sided", "upper one-sided"]
    method: Literal["clopper-pearson", "wald", "wilson"]
    continuity_correction: bool | None = None


case_group = (
    [
        # Regular Cases: proportion = 0.90, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "two-sided", method = "clopper-pearson"
        TestCase(proportion=0.90, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="two-sided", method="clopper-pearson")
        for size, distance, actual_distance in [
            (14029, 0.01, 0.0100),
            (3557, 0.02, 0.0200),
            (1603, 0.03, 0.0300),
            (914, 0.04, 0.0400),
            (593, 0.05, 0.0500),
            (417, 0.06, 0.0600),
            (310, 0.07, 0.0700),
            (241, 0.08, 0.0798),
            (192, 0.09, 0.0900),
            (158, 0.10, 0.0997),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.90, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "lower one-sided", method = "clopper-pearson"
        TestCase(proportion=0.90, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="lower one-sided", method="clopper-pearson")
        for size, distance, actual_distance in [
            (2704, 0.01, 0.0100),
            (742, 0.02, 0.0200),
            (359, 0.03, 0.0300),
            (218, 0.04, 0.0399),
            (150, 0.05, 0.0498),
            (111, 0.06, 0.0598),
            (86, 0.07, 0.0700),
            (70, 0.08, 0.0796),
            (58, 0.09, 0.0898),
            (50, 0.10, 0.0988),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.80, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "upper one-sided", method = "clopper-pearson"
        TestCase(proportion=0.80, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="upper one-sided", method="clopper-pearson")
        for size, distance, actual_distance in [
            (4298, 0.01, 0.0100),
            (1065, 0.02, 0.0200),
            (469, 0.03, 0.0300),
            (261, 0.04, 0.0399),
            (165, 0.05, 0.0499),
            (113, 0.06, 0.0598),
            (81, 0.07, 0.0699),
            (61, 0.08, 0.0797),
            (47, 0.09, 0.0897),
            (37, 0.10, 0.0997),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.90, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "two-sided", method = "wald", continuity_correction = False
        TestCase(proportion=0.90, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="two-sided", method="wald", continuity_correction=False)
        for size, distance, actual_distance in [
            (13830, 0.01, 0.0100),
            (3458, 0.02, 0.0200),
            (1537, 0.03, 0.0300),
            (865, 0.04, 0.0400),
            (554, 0.05, 0.0500),
            (385, 0.06, 0.0599),
            (283, 0.07, 0.0699),
            (217, 0.08, 0.0798),
            (171, 0.09, 0.0899),
            (139, 0.10, 0.0997),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.90, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "lower one-sided", method = "wald", continuity_correction = False
        TestCase(proportion=0.90, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="lower one-sided", method="wald", continuity_correction=False)
        for size, distance, actual_distance in [
            (2435, 0.01, 0.0100),
            (609, 0.02, 0.0200),
            (271, 0.03, 0.0300),
            (153, 0.04, 0.0399),
            (98, 0.05, 0.0498),
            (68, 0.06, 0.0598),
            (50, 0.07, 0.0698),
            (39, 0.08, 0.0790),
            (31, 0.09, 0.0886),
            (25, 0.10, 0.0987),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.80, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "upper one-sided", method = "wald", continuity_correction = False
        TestCase(proportion=0.80, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="upper one-sided", method="wald", continuity_correction=False)
        for size, distance, actual_distance in [
            (4329, 0.01, 0.0100),
            (1083, 0.02, 0.0200),
            (481, 0.03, 0.0300),
            (271, 0.04, 0.0400),
            (174, 0.05, 0.0499),
            (121, 0.06, 0.0598),
            (89, 0.07, 0.0697),
            (68, 0.08, 0.0798),
            (54, 0.09, 0.0895),
            (44, 0.10, 0.0992),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.90, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "two-sided", method = "wald", continuity_correction = True
        TestCase(proportion=0.90, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="two-sided", method="wald", continuity_correction=True)
        for size, distance, actual_distance in [
            (14029, 0.01, 0.0100),
            (3557, 0.02, 0.0200),
            (1603, 0.03, 0.0300),
            (914, 0.04, 0.0400),
            (593, 0.05, 0.0500),
            (417, 0.06, 0.0600),
            (311, 0.07, 0.0699),
            (241, 0.08, 0.0799),
            (193, 0.09, 0.0898),
            (158, 0.10, 0.0999),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.90, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "lower one-sided", method = "wald", continuity_correction = True
        TestCase(proportion=0.90, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="lower one-sided", method="wald", continuity_correction=True)
        for size, distance, actual_distance in [
            (2535, 0.01, 0.0100),
            (658, 0.02, 0.0200),
            (303, 0.03, 0.0300),
            (177, 0.04, 0.0399),
            (117, 0.05, 0.0499),
            (84, 0.06, 0.0598),
            (64, 0.07, 0.0695),
            (50, 0.08, 0.0798),
            (41, 0.09, 0.0893),
            (34, 0.10, 0.0993),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.80, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "upper one-sided", method = "wald", continuity_correction = True
        TestCase(proportion=0.80, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="upper one-sided", method="wald", continuity_correction=True)
        for size, distance, actual_distance in [
            (4429, 0.01, 0.0100),
            (1132, 0.02, 0.0200),
            (514, 0.03, 0.0300),
            (296, 0.04, 0.0399),
            (193, 0.05, 0.0500),
            (137, 0.06, 0.0599),
            (103, 0.07, 0.0697),
            (80, 0.08, 0.0798),
            (65, 0.09, 0.0893),
            (53, 0.10, 0.0998),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.90, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "two-sided", method = "wilson", continuity_correction = False
        TestCase(proportion=0.90, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="two-sided", method="wilson", continuity_correction=False)
        for size, distance, actual_distance in [
            (13833, 0.01, 0.0100),
            (3461, 0.02, 0.0200),
            (1540, 0.03, 0.0300),
            (868, 0.04, 0.0400),
            (557, 0.05, 0.0500),
            (388, 0.06, 0.0599),
            (286, 0.07, 0.0699),
            (219, 0.08, 0.0800),
            (174, 0.09, 0.0899),
            (141, 0.10, 0.1000),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.90, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "lower one-sided", method = "wilson", continuity_correction = False
        TestCase(proportion=0.90, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="lower one-sided", method="wilson", continuity_correction=False)
        for size, distance, actual_distance in [
            (2649, 0.01, 0.0100),
            (715, 0.02, 0.0200),
            (340, 0.03, 0.0300),
            (204, 0.04, 0.0400),
            (138, 0.05, 0.0500),
            (102, 0.06, 0.0597),
            (78, 0.07, 0.0700),
            (63, 0.08, 0.0795),
            (52, 0.09, 0.0894),
            (44, 0.10, 0.0990),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.80, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "upper one-sided", method = "wilson", continuity_correction = False
        TestCase(proportion=0.80, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="upper one-sided", method="wilson", continuity_correction=False)
        for size, distance, actual_distance in [
            (4164, 0.01, 0.0100),
            (999, 0.02, 0.0200),
            (425, 0.03, 0.0300),
            (228, 0.04, 0.0399),
            (138, 0.05, 0.0500),
            (91, 0.06, 0.0599),
            (63, 0.07, 0.0697),
            (45, 0.08, 0.0798),
            (33, 0.09, 0.0897),
            (25, 0.10, 0.0991),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.90, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "two-sided", method = "wilson", continuity_correction = True
        TestCase(proportion=0.90, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="two-sided", method="wilson", continuity_correction=True)
        for size, distance, actual_distance in [
            (14032, 0.01, 0.0100),
            (3560, 0.02, 0.0200),
            (1606, 0.03, 0.0300),
            (917, 0.04, 0.0400),
            (595, 0.05, 0.0500),
            (420, 0.06, 0.0599),
            (313, 0.07, 0.0699),
            (243, 0.08, 0.0799),
            (195, 0.09, 0.0898),
            (160, 0.10, 0.0999),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.90, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "lower one-sided", method = "wilson", continuity_correction = True
        TestCase(proportion=0.90, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="lower one-sided", method="wilson", continuity_correction=True)
        for size, distance, actual_distance in [
            (2748, 0.01, 0.0100),
            (764, 0.02, 0.0200),
            (373, 0.03, 0.0300),
            (228, 0.04, 0.0400),
            (158, 0.05, 0.0499),
            (118, 0.06, 0.0597),
            (92, 0.07, 0.0698),
            (75, 0.08, 0.0796),
            (63, 0.09, 0.0891),
            (53, 0.10, 0.0998),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.80, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "upper one-sided", method = "wilson", continuity_correction = True
        TestCase(proportion=0.80, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="upper one-sided", method="wilson", continuity_correction=True)
        for size, distance, actual_distance in [
            (4264, 0.01, 0.0100),
            (1048, 0.02, 0.0200),
            (457, 0.03, 0.0300),
            (252, 0.04, 0.0400),
            (158, 0.05, 0.0499),
            (107, 0.06, 0.0599),
            (77, 0.07, 0.0696),
            (57, 0.08, 0.0797),
            (44, 0.09, 0.0892),
            (34, 0.10, 0.0995),
        ]
    ]
    + [
        # Regular Cases: proportion = 0.10, distance = 0.01 to 0.10 by 0.01, conf_level = 0.95, interval_type = "two-sided", method = "wilson", continuity_correction = True
        TestCase(proportion=0.10, size=size, distance=distance, actual_distance=actual_distance, conf_level=0.95, interval_type="two-sided", method="wilson", continuity_correction=True)
        for size, distance, actual_distance in [
            (14032, 0.01, 0.0100),
            (3560, 0.02, 0.0200),
            (1606, 0.03, 0.0300),
            (917, 0.04, 0.0400),
            (595, 0.05, 0.0500),
            (420, 0.06, 0.0599),
            (313, 0.07, 0.0699),
            (243, 0.08, 0.0799),
            (195, 0.09, 0.0898),
            (160, 0.10, 0.0999),
        ]
    ]
)


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


def test_solve_size(case: TestCase) -> None:
    assert (
        solve_size(
            proportion=case.proportion,
            distance=case.distance,
            conf_level=case.conf_level,
            interval_type=case.interval_type,
            method=case.method,
            continuity_correction=case.continuity_correction,
        )
        == case.size
    )


def test_solve_size_no_solution() -> None:
    with pytest.raises(ValueError):
        assert solve_size(proportion=0.90, distance=0.99, conf_level=0.95, method="wilson", continuity_correction=True)


def test_solve_distance(case: TestCase) -> None:
    assert (
        round(
            solve_distance(
                proportion=case.proportion,
                size=case.size,
                conf_level=case.conf_level,
                interval_type=case.interval_type,
                method=case.method,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.distance
    )


def test_solve_proportion(case: TestCase) -> None:
    side = "below" if case.proportion < 0.5 else "above"
    assert (
        round(
            solve_proportion(
                size=case.size,
                distance=case.actual_distance,
                conf_level=case.conf_level,
                interval_type=case.interval_type,
                method=case.method,
                continuity_correction=case.continuity_correction,
                search_direction=side,
            ),
            2,
        )
        == case.proportion
    )
