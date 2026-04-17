# Validation Software: PASS 15
# Module: Non-Inferiority Tests for the Difference Between Two Proportions

import pytest

from pystatpower.models.proportion.independent.noninferiority import solve_power, solve_size, solve_treatment_proportion, solve_reference_proportion, solve_margin


@pytest.fixture(
    params=[
        # alpha, power, actual_power, treatment_proportion, reference_proportion, margin, pooled, continuity_correction, treatment_size, reference_size
        # case series: alpha = 0.01 to 0.99 by 0.01, power = 0.80, treatment_proportion = 0.90, reference_proportion = 0.80, margin = -0.10, pooled = True, continuity_correction = False
        (0.01, 0.80, 0.8011, 0.90, 0.90, -0.10, True, False, 271, 136),
        (0.02, 0.80, 0.8024, 0.90, 0.90, -0.10, True, False, 227, 114),
        (0.03, 0.80, 0.8029, 0.90, 0.90, -0.10, True, False, 201, 101),
        (0.04, 0.80, 0.8004, 0.90, 0.90, -0.10, True, False, 181, 91),
        (0.05, 0.80, 0.8015, 0.90, 0.90, -0.10, True, False, 167, 84),
        (0.06, 0.80, 0.8013, 0.90, 0.90, -0.10, True, False, 155, 78),
        (0.07, 0.80, 0.8015, 0.90, 0.90, -0.10, True, False, 145, 73),
        (0.08, 0.80, 0.8032, 0.90, 0.90, -0.10, True, False, 137, 69),
        (0.09, 0.80, 0.8025, 0.90, 0.90, -0.10, True, False, 129, 65),
        (0.10, 0.80, 0.8007, 0.90, 0.90, -0.10, True, False, 122, 61),
        (0.11, 0.80, 0.8004, 0.90, 0.90, -0.10, True, False, 115, 58),
        (0.12, 0.80, 0.8005, 0.90, 0.90, -0.10, True, False, 110, 55),
        (0.13, 0.80, 0.8029, 0.90, 0.90, -0.10, True, False, 105, 53),
        (0.14, 0.80, 0.8007, 0.90, 0.90, -0.10, True, False, 100, 50),
        (0.15, 0.80, 0.8012, 0.90, 0.90, -0.10, True, False, 95, 48),
        (0.16, 0.80, 0.8018, 0.90, 0.90, -0.10, True, False, 91, 46),
        (0.17, 0.80, 0.8017, 0.90, 0.90, -0.10, True, False, 87, 44),
        (0.18, 0.80, 0.8009, 0.90, 0.90, -0.10, True, False, 83, 42),
        (0.19, 0.80, 0.8005, 0.90, 0.90, -0.10, True, False, 80, 40),
        (0.20, 0.80, 0.8036, 0.90, 0.90, -0.10, True, False, 77, 39),
        # case series: alpha = 0.05, power = 0.70 to 0.99 by 0.01, treatment_proportion = 0.90, reference_proportion = 0.80, margin = -0.10, pooled = True, continuity_correction = False
        (0.05, 0.70, 0.7087, 0.90, 0.80, -0.10, True, False, 43, 22),
        (0.05, 0.71, 0.7121, 0.90, 0.80, -0.10, True, False, 44, 22),
        (0.05, 0.72, 0.7246, 0.90, 0.80, -0.10, True, False, 45, 23),
        (0.05, 0.73, 0.7397, 0.90, 0.80, -0.10, True, False, 47, 24),
        (0.05, 0.74, 0.7426, 0.90, 0.80, -0.10, True, False, 48, 24),
        (0.05, 0.75, 0.7541, 0.90, 0.80, -0.10, True, False, 49, 25),
        (0.05, 0.76, 0.7677, 0.90, 0.80, -0.10, True, False, 51, 26),
        (0.05, 0.77, 0.7703, 0.90, 0.80, -0.10, True, False, 52, 26),
        (0.05, 0.78, 0.7807, 0.90, 0.80, -0.10, True, False, 53, 27),
        (0.05, 0.79, 0.7930, 0.90, 0.80, -0.10, True, False, 55, 28),
        (0.05, 0.80, 0.8047, 0.90, 0.80, -0.10, True, False, 57, 29),
        (0.05, 0.81, 0.8157, 0.90, 0.80, -0.10, True, False, 59, 30),
        (0.05, 0.82, 0.8262, 0.90, 0.80, -0.10, True, False, 61, 31),
        (0.05, 0.83, 0.8362, 0.90, 0.80, -0.10, True, False, 63, 32),
        (0.05, 0.84, 0.8456, 0.90, 0.80, -0.10, True, False, 65, 33),
        (0.05, 0.85, 0.8545, 0.90, 0.80, -0.10, True, False, 67, 34),
        (0.05, 0.86, 0.8630, 0.90, 0.80, -0.10, True, False, 69, 35),
        (0.05, 0.87, 0.8710, 0.90, 0.80, -0.10, True, False, 71, 36),
        (0.05, 0.88, 0.8857, 0.90, 0.80, -0.10, True, False, 75, 38),
        (0.05, 0.89, 0.8925, 0.90, 0.80, -0.10, True, False, 77, 39),
        (0.05, 0.90, 0.9049, 0.90, 0.80, -0.10, True, False, 81, 41),
        (0.05, 0.91, 0.9105, 0.90, 0.80, -0.10, True, False, 83, 42),
        (0.05, 0.92, 0.9210, 0.90, 0.80, -0.10, True, False, 87, 44),
        (0.05, 0.93, 0.9303, 0.90, 0.80, -0.10, True, False, 91, 46),
        (0.05, 0.94, 0.9423, 0.90, 0.80, -0.10, True, False, 97, 49),
        (0.05, 0.95, 0.9523, 0.90, 0.80, -0.10, True, False, 103, 52),
        (0.05, 0.96, 0.9607, 0.90, 0.80, -0.10, True, False, 109, 55),
        (0.05, 0.97, 0.9716, 0.90, 0.80, -0.10, True, False, 119, 60),
        (0.05, 0.98, 0.9809, 0.90, 0.80, -0.10, True, False, 131, 66),
        (0.05, 0.99, 0.9902, 0.90, 0.80, -0.10, True, False, 151, 76),
        # case series: alpha = 0.05, power = 0.80, treatment_proportion = 0.75 to 0.95 by 0.01, reference_proportion = 0.80, margin = -0.10, pooled = True, continuity_correction = False
        (0.05, 0.80, 0.8003, 0.75, 0.80, -0.10, True, False, 1303, 652),
        (0.05, 0.80, 0.8001, 0.76, 0.80, -0.10, True, False, 889, 445),
        (0.05, 0.80, 0.8000, 0.77, 0.80, -0.10, True, False, 642, 321),
        (0.05, 0.80, 0.8009, 0.78, 0.80, -0.10, True, False, 483, 242),
        (0.05, 0.80, 0.8001, 0.79, 0.80, -0.10, True, False, 374, 187),
        (0.05, 0.80, 0.8011, 0.80, 0.80, -0.10, True, False, 297, 149),
        (0.05, 0.80, 0.8022, 0.81, 0.80, -0.10, True, False, 241, 121),
        (0.05, 0.80, 0.8006, 0.82, 0.80, -0.10, True, False, 197, 99),
        (0.05, 0.80, 0.8029, 0.83, 0.80, -0.10, True, False, 165, 83),
        (0.05, 0.80, 0.8036, 0.84, 0.80, -0.10, True, False, 139, 70),
        (0.05, 0.80, 0.8009, 0.85, 0.80, -0.10, True, False, 117, 59),
        (0.05, 0.80, 0.8042, 0.86, 0.80, -0.10, True, False, 101, 51),
        (0.05, 0.80, 0.8047, 0.87, 0.80, -0.10, True, False, 87, 44),
        (0.05, 0.80, 0.8036, 0.88, 0.80, -0.10, True, False, 75, 38),
        (0.05, 0.80, 0.8028, 0.89, 0.80, -0.10, True, False, 65, 33),
        (0.05, 0.80, 0.8047, 0.90, 0.80, -0.10, True, False, 57, 29),
        (0.05, 0.80, 0.8017, 0.91, 0.80, -0.10, True, False, 50, 25),
        (0.05, 0.80, 0.8024, 0.92, 0.80, -0.10, True, False, 44, 22),
        (0.05, 0.80, 0.8096, 0.93, 0.80, -0.10, True, False, 39, 20),
        (0.05, 0.80, 0.8017, 0.94, 0.80, -0.10, True, False, 34, 17),
        (0.05, 0.80, 0.8020, 0.95, 0.80, -0.10, True, False, 30, 15),
        # case series: alpha = 0.05, power = 0.80, treatment_proportion = 0.90, reference_proportion = 0.70 to 0.75 by 0.01, margin = -0.10, pooled = True, continuity_correction = False
        (0.05, 0.80, 0.8090, 0.90, 0.70, -0.10, True, False, 31, 16),
        (0.05, 0.80, 0.8121, 0.90, 0.71, -0.10, True, False, 33, 17),
        (0.05, 0.80, 0.8136, 0.90, 0.72, -0.10, True, False, 35, 18),
        (0.05, 0.80, 0.8135, 0.90, 0.73, -0.10, True, False, 37, 19),
        (0.05, 0.80, 0.8118, 0.90, 0.74, -0.10, True, False, 39, 20),
        (0.05, 0.80, 0.8086, 0.90, 0.75, -0.10, True, False, 41, 21),
        # case series: alpha = 0.05, power = 0.80, treatment_proportion = 0.90, reference_proportion = 0.80, margin = -0.20 to -0.01 by 0.01, pooled = True, continuity_correction = False
        (0.05, 0.80, 0.8047, 0.90, 0.80, -0.20, True, False, 25, 13),
        (0.05, 0.80, 0.8071, 0.90, 0.80, -0.19, True, False, 27, 14),
        (0.05, 0.80, 0.8070, 0.90, 0.80, -0.18, True, False, 29, 15),
        (0.05, 0.80, 0.8046, 0.90, 0.80, -0.17, True, False, 31, 16),
        (0.05, 0.80, 0.8038, 0.90, 0.80, -0.16, True, False, 34, 17),
        (0.05, 0.80, 0.8111, 0.90, 0.80, -0.15, True, False, 37, 19),
        (0.05, 0.80, 0.8014, 0.90, 0.80, -0.14, True, False, 39, 20),
        (0.05, 0.80, 0.8050, 0.90, 0.80, -0.13, True, False, 43, 22),
        (0.05, 0.80, 0.8046, 0.90, 0.80, -0.12, True, False, 47, 24),
        (0.05, 0.80, 0.8006, 0.90, 0.80, -0.11, True, False, 51, 26),
        (0.05, 0.80, 0.8047, 0.90, 0.80, -0.10, True, False, 57, 29),
        (0.05, 0.80, 0.8035, 0.90, 0.80, -0.09, True, False, 63, 32),
        (0.05, 0.80, 0.8069, 0.90, 0.80, -0.08, True, False, 71, 36),
        (0.05, 0.80, 0.8041, 0.90, 0.80, -0.07, True, False, 79, 40),
        (0.05, 0.80, 0.8032, 0.90, 0.80, -0.06, True, False, 89, 45),
        (0.05, 0.80, 0.8020, 0.90, 0.80, -0.05, True, False, 101, 51),
        (0.05, 0.80, 0.8002, 0.90, 0.80, -0.04, True, False, 116, 58),
        (0.05, 0.80, 0.8028, 0.90, 0.80, -0.03, True, False, 135, 68),
        (0.05, 0.80, 0.8004, 0.90, 0.80, -0.02, True, False, 158, 79),
        (0.05, 0.80, 0.8004, 0.90, 0.80, -0.01, True, False, 188, 94),
        # case series: alpha = 0.05, power = 0.80, treatment_proportion = 0.90, reference_proportion = 0.80, margin = -0.10, pooled = True/False, continuity_correction = True/False, ratio ≈ 2
        # ratio = 2
        (0.05, 0.80, 0.8035, 0.90, 0.80, -0.10, True, True, 71, 36),
        (0.05, 0.80, 0.8047, 0.90, 0.80, -0.10, True, False, 57, 29),
        (0.05, 0.80, 0.8006, 0.90, 0.80, -0.10, False, True, 77, 39),
        (0.05, 0.80, 0.8022, 0.90, 0.80, -0.10, False, False, 63, 32),
        # ratio = 0.5
        (0.05, 0.80, 0.8090, 0.90, 0.80, -0.10, True, True, 38, 76),
        (0.05, 0.80, 0.8105, 0.90, 0.80, -0.10, True, False, 31, 62),
        (0.05, 0.80, 0.8083, 0.90, 0.80, -0.10, False, True, 34, 68),
        (0.05, 0.80, 0.8094, 0.90, 0.80, -0.10, False, False, 27, 54),
        # case: alpha = 0.05, power = 0.80, treatment_proportion = 0.90, reference_proportion = 0.80, margin = 0.15, pooled = True, continuity_correction = True
        (0.05, 0.80, 0.8003, 0.90, 0.80, 0.15, True, True, 512, 1024),
    ],
    ids=lambda p: f"{p[0]}, {p[1]}, {p[2]}, {p[3]}, {p[4]}, {p[5]}, {p[6]}, {p[7]}, {p[8]}, {p[9]}",
)
def case(request: pytest.FixtureRequest):
    return request.param


def test_solve_power(case) -> None:
    alpha, _, expected_power, treatment_proportion, reference_proportion, margin, pooled, continuity_correction, treatment_size, reference_size = case
    assert (
        round(
            solve_power(
                treatment_proportion,
                reference_proportion,
                margin,
                treatment_size,
                reference_size,
                alpha,
                pooled,
                continuity_correction,
            ),
            4,
        )
        == expected_power
    )


def test_solve_size(case) -> None:
    alpha, power, _, treatment_proportion, reference_proportion, margin, pooled, continuity_correction, expected_treatment_size, expected_reference_size = case
    ratio = expected_treatment_size / expected_reference_size
    assert solve_size(
        treatment_proportion,
        reference_proportion,
        margin,
        ratio,
        alpha,
        power,
        pooled,
        continuity_correction,
    ) == (expected_treatment_size, expected_reference_size)


def test_solve_treatment_proportion(case) -> None:
    alpha, _, actual_power, expected_treatment_proportion, reference_proportion, margin, pooled, continuity_correction, treatment_size, reference_size = case
    assert (
        round(
            solve_treatment_proportion(
                reference_proportion,
                margin,
                treatment_size,
                reference_size,
                alpha,
                actual_power,
                pooled,
                continuity_correction,
            ),
            2,
        )
        == expected_treatment_proportion
    )


def test_solve_reference_proportion(case) -> None:
    alpha, _, actual_power, treatment_proportion, expected_reference_proportion, margin, pooled, continuity_correction, treatment_size, reference_size = case
    assert (
        round(
            solve_reference_proportion(
                treatment_proportion,
                margin,
                treatment_size,
                reference_size,
                alpha,
                actual_power,
                pooled,
                continuity_correction,
            ),
            2,
        )
        == expected_reference_proportion
    )


def test_solve_margin(case) -> None:
    alpha, _, actual_power, treatment_proportion, reference_proportion, expected_margin, pooled, continuity_correction, treatment_size, reference_size = case
    assert (
        round(
            solve_margin(
                treatment_proportion,
                reference_proportion,
                treatment_size,
                reference_size,
                alpha,
                actual_power,
                pooled,
                continuity_correction,
            ),
            2,
        )
        == expected_margin
    )


if __name__ == "__main__":
    margin_list = [x / 100 for x in range(-80, -5)]
    power_list = [
        solve_power(
            treatment_proportion=0.75,
            reference_proportion=0.80,
            margin=margin,
            treatment_size=1303,
            reference_size=652,
            pooled=True,
            continuity_correction=False,
        )
        for margin in margin_list
    ]

    for i, tp in enumerate(zip(margin_list, power_list)):
        print(tp)
