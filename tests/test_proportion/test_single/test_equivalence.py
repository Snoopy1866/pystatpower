# Validation Software: PASS 15
# Module: Equivalence Tests for One Proportion

from dataclasses import dataclass

from pystatpower.proportion.single.equivalence import solve_power, solve_size, solve_null_proportion, solve_proportion

from tests.models import BaseTestCase


@dataclass
class TestCase(BaseTestCase):
    null_proportion: float
    proportion: float
    margin_lower: float
    margin_upper: float
    size: int
    alpha: float
    power: float
    phat: bool
    continuity_correction: bool
    actual_power: float


case_group = (
    [
        # Regular Cases: null_proportion = 0.80, proportion = 0.71 to 0.89 by 0.01, margin_lower = -0.10, margin_upper = 0.10, alpha = 0.025, power = 0.80, phat = False, continuity_correction = False
        TestCase(null_proportion=0.80, proportion=proportion, margin_lower=-0.10, margin_upper=0.10, size=size, alpha=0.025, power=0.80, phat=False, continuity_correction=False, actual_power=actual_power)
        for proportion, actual_power, size in [
            (0.71, 0.800008645, 16386),
            (0.72, 0.800020228, 4071),
            (0.73, 0.800170764, 1798),
            (0.74, 0.800067735, 1004),
            (0.75, 0.800214634, 638),
            (0.76, 0.800628722, 440),
            (0.77, 0.801179861, 321),
            (0.78, 0.800959648, 244),
            (0.79, 0.800726425, 195),
            (0.80, 0.801789107, 168),
            (0.81, 0.801493296, 156),
            (0.82, 0.802101987, 157),
            (0.83, 0.801542134, 175),
            (0.84, 0.800570668, 224),
            (0.85, 0.800243662, 316),
            (0.86, 0.800715517, 485),
            (0.87, 0.800003797, 843),
            (0.88, 0.800122869, 1856),
            (0.89, 0.800025059, 7248),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.80, proportion = 0.71 to 0.89 by 0.01, margin_lower = -0.10, margin_upper = 0.10, alpha = 0.025, power = 0.80, phat = False, continuity_correction = True
        TestCase(null_proportion=0.80, proportion=proportion, margin_lower=-0.10, margin_upper=0.10, size=size, alpha=0.025, power=0.80, phat=False, continuity_correction=True, actual_power=actual_power)
        for proportion, actual_power, size in [
            (0.71, 0.800012300, 16486),
            (0.72, 0.800035048, 4121),
            (0.73, 0.800130265, 1831),
            (0.74, 0.800128889, 1029),
            (0.75, 0.800311804, 658),
            (0.76, 0.800146911, 456),
            (0.77, 0.801010771, 335),
            (0.78, 0.800466128, 256),
            (0.79, 0.801312828, 206),
            (0.80, 0.802230800, 178),
            (0.81, 0.802350624, 166),
            (0.82, 0.800337918, 167),
            (0.83, 0.801996006, 188),
            (0.84, 0.800175658, 240),
            (0.85, 0.800571559, 336),
            (0.86, 0.800208240, 509),
            (0.87, 0.800426339, 877),
            (0.88, 0.800188410, 1906),
            (0.89, 0.800042936, 7348),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.80, proportion = 0.71 to 0.89 by 0.01, margin_lower = -0.10, margin_upper = 0.10, alpha = 0.025, power = 0.80, phat = True, continuity_correction = False
        TestCase(null_proportion=0.80, proportion=proportion, margin_lower=-0.10, margin_upper=0.10, size=size, alpha=0.025, power=0.80, phat=True, continuity_correction=False, actual_power=actual_power)
        for proportion, actual_power, size in [
            (0.71, 0.800003801, 16161),
            (0.72, 0.800016319, 3956),
            (0.73, 0.800021750, 1719),
            (0.74, 0.800071545, 944),
            (0.75, 0.800222418, 589),
            (0.76, 0.800316402, 398),
            (0.77, 0.801249565, 285),
            (0.78, 0.801375954, 217),
            (0.79, 0.800223275, 182),
            (0.80, 0.802961846, 169),
            (0.81, 0.800738510, 169),
            (0.82, 0.802204172, 187),
            (0.83, 0.801133297, 227),
            (0.84, 0.801299217, 294),
            (0.85, 0.800691755, 401),
            (0.86, 0.800246739, 591),
            (0.87, 0.800261254, 987),
            (0.88, 0.800169469, 2073),
            (0.89, 0.800048313, 7685),
        ]
    ]
    + [
        # Regular Cases: null_proportion = 0.80, proportion = 0.71 to 0.89 by 0.01, margin_lower = -0.10, margin_upper = 0.10, alpha = 0.025, power = 0.80, phat = True, continuity_correction = True
        TestCase(null_proportion=0.80, proportion=proportion, margin_lower=-0.10, margin_upper=0.10, size=size, alpha=0.025, power=0.80, phat=True, continuity_correction=True, actual_power=actual_power)
        for proportion, actual_power, size in [
            (0.71, 0.800007531, 16261),
            (0.72, 0.800031784, 4006),
            (0.73, 0.800209910, 1753),
            (0.74, 0.800138515, 969),
            (0.75, 0.800331680, 609),
            (0.76, 0.800809692, 415),
            (0.77, 0.801196838, 299),
            (0.78, 0.801771186, 229),
            (0.79, 0.802231738, 193),
            (0.80, 0.800073350, 178),
            (0.81, 0.802924842, 180),
            (0.82, 0.800353268, 198),
            (0.83, 0.801135120, 241),
            (0.84, 0.800710197, 310),
            (0.85, 0.800923659, 421),
            (0.86, 0.800414922, 616),
            (0.87, 0.800237025, 1020),
            (0.88, 0.800036010, 2122),
            (0.89, 0.800013673, 7784),
        ]
    ]
)


def test_size_solve_power(case: TestCase) -> None:
    assert round(
        solve_power(
            null_proportion=case.null_proportion,
            proportion=case.proportion,
            margin_lower=case.margin_lower,
            margin_upper=case.margin_upper,
            size=case.size,
            alpha=case.alpha,
            phat=case.phat,
            continuity_correction=case.continuity_correction,
        ),
        4,
    ) == round(case.actual_power, 4)


def test_solve_size(case: TestCase) -> None:
    assert (
        solve_size(
            null_proportion=case.null_proportion,
            proportion=case.proportion,
            margin_lower=case.margin_lower,
            margin_upper=case.margin_upper,
            alpha=case.alpha,
            power=case.power,
            phat=case.phat,
            continuity_correction=case.continuity_correction,
        )
        == case.size
    )


def test_size_solve_null_proportion(case: TestCase) -> None:
    assert any(
        [
            round(
                solve_null_proportion(
                    proportion=case.proportion,
                    margin_lower=case.margin_lower,
                    margin_upper=case.margin_upper,
                    size=case.size,
                    alpha=case.alpha,
                    power=case.actual_power,
                    phat=case.phat,
                    continuity_correction=case.continuity_correction,
                    search_direction=search_direction,
                ),
                2,
            )
            == case.null_proportion
            for search_direction in ["lower", "upper"]
        ]
    )


def test_size_solve_proportion(case: TestCase) -> None:
    assert any(
        [
            round(
                solve_proportion(
                    null_proportion=case.null_proportion,
                    margin_lower=case.margin_lower,
                    margin_upper=case.margin_upper,
                    size=case.size,
                    alpha=case.alpha,
                    power=case.actual_power,
                    phat=case.phat,
                    continuity_correction=case.continuity_correction,
                    search_direction=search_direction,
                ),
                2,
            )
            == case.proportion
            for search_direction in ["lower", "upper"]
        ]
    )


# def test_solve_margin(case: TestCase) -> None:
#     assert (
#         round(
#             solve_margin(
#                 null_proportion=case.null_proportion,
#                 proportion=case.proportion,
#                 size=case.size,
#                 alternative=case.alternative,
#                 alpha=case.alpha,
#                 power=case.actual_power,
#                 phat=case.phat,
#                 continuity_correction=case.continuity_correction,
#             ),
#             2,
#         )
#         == case.margin
#     )
