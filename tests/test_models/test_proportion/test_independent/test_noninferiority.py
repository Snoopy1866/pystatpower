# Validation Software: PASS 15
# Module: Non-Inferiority Tests for the Difference Between Two Proportions

from dataclasses import dataclass, asdict

import pytest

from pystatpower.models.proportion.independent.noninferiority import solve_margin, solve_power, solve_reference_proportion, solve_size, solve_treatment_proportion


@dataclass
class TestCase:
    __test__ = False

    treatment_proportion: float
    reference_proportion: float
    margin: float
    treatment_size: int
    reference_size: int
    alpha: float
    power: float
    pooled: bool
    continuity_correction: bool
    actual_power: float


case_group = (
    [  # Regular Cases: ratio = 2, margin = -0.10, pooled = True, continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=-0.10,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.80, 0.80, 407, 204, 0.8015),
            (0.81, 0.81, 392, 196, 0.8002),
            (0.82, 0.82, 377, 189, 0.8008),
            (0.83, 0.83, 361, 181, 0.8001),
            (0.84, 0.84, 346, 173, 0.8002),
            (0.85, 0.85, 329, 165, 0.8002),
            (0.86, 0.86, 313, 157, 0.8012),
            (0.87, 0.87, 295, 148, 0.8002),
            (0.88, 0.88, 278, 139, 0.8002),
            (0.89, 0.89, 259, 130, 0.8000),
            (0.90, 0.90, 241, 121, 0.8012),
            (0.91, 0.91, 222, 111, 0.8003),
            (0.92, 0.92, 203, 102, 0.8033),
            (0.93, 0.93, 183, 92, 0.8041),
            (0.94, 0.94, 161, 81, 0.8007),
            (0.95, 0.95, 141, 71, 0.8049),
        ]
    ]
    + [  # Regular Cases: ratio = 2, margin = -0.10, pooled = True, continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=-0.10,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.80, 0.80, 377, 189, 0.8010),
            (0.81, 0.81, 363, 182, 0.8014),
            (0.82, 0.82, 347, 174, 0.8001),
            (0.83, 0.83, 333, 167, 0.8017),
            (0.84, 0.84, 317, 159, 0.8015),
            (0.85, 0.85, 301, 151, 0.8019),
            (0.86, 0.86, 283, 142, 0.8002),
            (0.87, 0.87, 267, 134, 0.8020),
            (0.88, 0.88, 249, 125, 0.8016),
            (0.89, 0.89, 231, 116, 0.8019),
            (0.90, 0.90, 212, 106, 0.8001),
            (0.91, 0.91, 193, 97, 0.8017),
            (0.92, 0.92, 173, 87, 0.8008),
            (0.93, 0.93, 153, 77, 0.8010),
            (0.94, 0.94, 133, 67, 0.8025),
            (0.95, 0.95, 112, 56, 0.8005),
        ]
    ]
    + [  # Regular Cases: ratio = 2, margin = -0.10, pooled = False, continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=-0.10,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=False,
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.80, 0.80, 407, 204, 0.8015),
            (0.81, 0.81, 392, 196, 0.8002),
            (0.82, 0.82, 377, 189, 0.8008),
            (0.83, 0.83, 361, 181, 0.8001),
            (0.84, 0.84, 346, 173, 0.8002),
            (0.85, 0.85, 329, 165, 0.8002),
            (0.86, 0.86, 313, 157, 0.8012),
            (0.87, 0.87, 295, 148, 0.8002),
            (0.88, 0.88, 278, 139, 0.8002),
            (0.89, 0.89, 259, 130, 0.8000),
            (0.90, 0.90, 241, 121, 0.8012),
            (0.91, 0.91, 222, 111, 0.8003),
            (0.92, 0.92, 203, 102, 0.8033),
            (0.93, 0.93, 183, 92, 0.8041),
            (0.94, 0.94, 161, 81, 0.8007),
            (0.95, 0.95, 141, 71, 0.8049),
        ]
    ]
    + [  # Regular Cases: ratio = 2, margin = -0.10, pooled = False, continuity_correction = False
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=-0.10,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=False,
            continuity_correction=False,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.80, 0.80, 377, 189, 0.8010),
            (0.81, 0.81, 363, 182, 0.8014),
            (0.82, 0.82, 347, 174, 0.8001),
            (0.83, 0.83, 333, 167, 0.8017),
            (0.84, 0.84, 317, 159, 0.8015),
            (0.85, 0.85, 301, 151, 0.8019),
            (0.86, 0.86, 283, 142, 0.8002),
            (0.87, 0.87, 267, 134, 0.8020),
            (0.88, 0.88, 249, 125, 0.8016),
            (0.89, 0.89, 231, 116, 0.8019),
            (0.90, 0.90, 212, 106, 0.8001),
            (0.91, 0.91, 193, 97, 0.8017),
            (0.92, 0.92, 173, 87, 0.8008),
            (0.93, 0.93, 153, 77, 0.8010),
            (0.94, 0.94, 133, 67, 0.8025),
            (0.95, 0.95, 112, 56, 0.8005),
        ]
    ]
    + [  # Regular Cases: ratio = 0.5, margin = -0.10, pooled = True, continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=-0.10,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.80, 0.80, 204, 408, 0.8019),
            (0.81, 0.81, 196, 392, 0.8002),
            (0.82, 0.82, 189, 378, 0.8012),
            (0.83, 0.83, 181, 362, 0.8004),
            (0.84, 0.84, 173, 346, 0.8002),
            (0.85, 0.85, 165, 330, 0.8006),
            (0.86, 0.86, 157, 314, 0.8017),
            (0.87, 0.87, 148, 296, 0.8007),
            (0.88, 0.88, 139, 278, 0.8002),
            (0.89, 0.89, 130, 260, 0.8006),
            (0.90, 0.90, 121, 242, 0.8019),
            (0.91, 0.91, 111, 222, 0.8003),
            (0.92, 0.92, 102, 204, 0.8040),
            (0.93, 0.93, 92, 184, 0.8049),
            (0.94, 0.94, 81, 162, 0.8017),
            (0.95, 0.95, 71, 142, 0.8060),
        ]
    ]
    + [  # Regular Cases: ratio = 0.5, margin = 0.10, pooled = True, continuity_correction = True
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0.10,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.70, 0.70, 263, 526, 0.8015),
            (0.71, 0.71, 258, 516, 0.8013),
            (0.72, 0.72, 253, 506, 0.8014),
            (0.73, 0.73, 247, 494, 0.8003),
            (0.74, 0.74, 242, 484, 0.8012),
            (0.75, 0.75, 236, 472, 0.8009),
            (0.76, 0.76, 230, 460, 0.8009),
            (0.77, 0.77, 224, 448, 0.8014),
            (0.78, 0.78, 217, 434, 0.8004),
            (0.79, 0.79, 211, 422, 0.8019),
            (0.80, 0.80, 204, 408, 0.8019),
            (0.81, 0.81, 196, 392, 0.8002),
            (0.82, 0.82, 189, 378, 0.8012),
            (0.83, 0.83, 181, 362, 0.8004),
            (0.84, 0.84, 173, 346, 0.8002),
            (0.85, 0.85, 165, 330, 0.8006),
        ]
    ]
    + [  # Regular Cases: ratio = 0.5, margin = 0.10, pooled = True, continuity_correction = True, treatment_proportion > reference_proportion
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0.10,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.72, 0.70, 399, 798, 0.8008),
            (0.73, 0.71, 391, 782, 0.8006),
            (0.74, 0.72, 383, 766, 0.8009),
            (0.75, 0.73, 374, 748, 0.8005),
            (0.76, 0.74, 365, 730, 0.8005),
            (0.77, 0.75, 356, 712, 0.8009),
            (0.78, 0.76, 346, 692, 0.8006),
            (0.79, 0.77, 336, 672, 0.8007),
            (0.80, 0.78, 326, 652, 0.8013),
            (0.81, 0.79, 315, 630, 0.8011),
            (0.82, 0.80, 304, 608, 0.8014),
            (0.83, 0.81, 292, 584, 0.8008),
            (0.84, 0.82, 280, 560, 0.8007),
            (0.85, 0.83, 268, 536, 0.8012),
            (0.86, 0.84, 255, 510, 0.8007),
            (0.87, 0.85, 242, 484, 0.8008),
        ]
    ]
    + [  # Regular Cases: ratio = 0.5, margin = 0.10, pooled = True, continuity_correction = True, treatment_proportion < reference_proportion
        TestCase(
            treatment_proportion=treatment_proportion,
            reference_proportion=reference_proportion,
            margin=0.10,
            treatment_size=treatment_size,
            reference_size=reference_size,
            alpha=0.025,
            power=0.80,
            pooled=True,
            continuity_correction=True,
            actual_power=actual_power,
        )
        for treatment_proportion, reference_proportion, treatment_size, reference_size, actual_power in [
            (0.68, 0.70, 187, 374, 0.8006),
            (0.69, 0.71, 184, 368, 0.8011),
            (0.70, 0.72, 181, 362, 0.8020),
            (0.71, 0.73, 177, 354, 0.8010),
            (0.72, 0.74, 173, 346, 0.8003),
            (0.73, 0.75, 170, 340, 0.8024),
            (0.74, 0.76, 165, 330, 0.8000),
            (0.75, 0.77, 161, 322, 0.8006),
            (0.76, 0.78, 157, 314, 0.8015),
            (0.77, 0.79, 152, 304, 0.8003),
            (0.78, 0.80, 148, 296, 0.8023),
            (0.79, 0.81, 143, 286, 0.8019),
            (0.80, 0.82, 138, 276, 0.8021),
            (0.81, 0.83, 133, 266, 0.8027),
            (0.82, 0.84, 127, 254, 0.8007),
            (0.83, 0.85, 122, 244, 0.8025),
        ]
    ]
)


def get_id(case: TestCase) -> str:
    parts = [f"{k}={v}" for k, v in asdict(case).items() if v is not None]
    return ", ".join(parts)


@pytest.fixture(params=case_group, ids=get_id)
def case(request: pytest.FixtureRequest) -> TestCase:
    return request.param


def test_solve_power(case: TestCase) -> None:
    assert (
        round(
            solve_power(
                treatment_proportion=case.treatment_proportion,
                reference_proportion=case.reference_proportion,
                margin=case.margin,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                pooled=case.pooled,
                continuity_correction=case.continuity_correction,
            ),
            4,
        )
        == case.actual_power
    )


def test_solve_size(case: TestCase) -> None:
    ratio = case.treatment_size / case.reference_size
    assert solve_size(
        treatment_proportion=case.treatment_proportion,
        reference_proportion=case.reference_proportion,
        margin=case.margin,
        ratio=ratio,
        alpha=case.alpha,
        power=case.power,
        pooled=case.pooled,
        continuity_correction=case.continuity_correction,
    ) == (case.treatment_size, case.reference_size)


def test_solve_treatment_proportion(case: TestCase) -> None:
    assert (
        round(
            solve_treatment_proportion(
                reference_proportion=case.reference_proportion,
                margin=case.margin,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                power=case.actual_power,
                pooled=case.pooled,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.treatment_proportion
    )


def test_solve_reference_proportion(case: TestCase) -> None:
    assert (
        round(
            solve_reference_proportion(
                treatment_proportion=case.treatment_proportion,
                margin=case.margin,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                power=case.actual_power,
                pooled=case.pooled,
                continuity_correction=case.continuity_correction,
            ),
            2,
        )
        == case.reference_proportion
    )


def test_solve_margin(case: TestCase) -> None:
    margin_selection = "negative" if case.margin < 0 else "positive"
    assert (
        round(
            solve_margin(
                treatment_proportion=case.treatment_proportion,
                reference_proportion=case.reference_proportion,
                treatment_size=case.treatment_size,
                reference_size=case.reference_size,
                alpha=case.alpha,
                power=case.actual_power,
                pooled=case.pooled,
                continuity_correction=case.continuity_correction,
                margin_selection=margin_selection,
            ),
            2,
        )
        == case.margin
    )
