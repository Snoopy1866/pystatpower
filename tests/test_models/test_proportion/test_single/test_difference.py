# Validation Software: PASS 15
# Module: Tests for One Proportions

import pytest

from pystatpower.models.proportion.single.difference import solve_power, solve_size, solve_null_proportion, solve_proportion


@pytest.fixture(
    params=[
        # null_proportion, proportion, size, alpha, power, phat, continuity_correction, actual_power
        # null_proportion = 0.65 to 0.79 by 0.01, proportion = 0.95, phat = True, continuity_correction = True
        (0.80, 0.65, 86, 0.05, 0.80, True, True, 0.8005),
        (0.80, 0.66, 97, 0.05, 0.80, True, True, 0.8006),
        (0.80, 0.67, 111, 0.05, 0.80, True, True, 0.8029),
        (0.80, 0.68, 127, 0.05, 0.80, True, True, 0.8007),
        (0.80, 0.69, 148, 0.05, 0.80, True, True, 0.8008),
        (0.80, 0.70, 175, 0.05, 0.80, True, True, 0.8008),
        (0.80, 0.71, 211, 0.05, 0.80, True, True, 0.8010),
        (0.80, 0.72, 260, 0.05, 0.80, True, True, 0.8007),
        (0.80, 0.73, 330, 0.05, 0.80, True, True, 0.8002),
        (0.80, 0.74, 436, 0.05, 0.80, True, True, 0.8000),
        (0.80, 0.75, 609, 0.05, 0.80, True, True, 0.8003),
        (0.80, 0.76, 920, 0.05, 0.80, True, True, 0.8002),
        (0.80, 0.77, 1578, 0.05, 0.80, True, True, 0.8001),
        (0.80, 0.78, 3417, 0.05, 0.80, True, True, 0.8000),
        (0.80, 0.79, 13122, 0.05, 0.80, True, True, 0.8000),
        # null_proportion = 0.81 to 0.95 by 0.01, proportion = 0.95, phat = True, continuity_correction = True
        (0.80, 0.81, 12180, 0.05, 0.80, True, True, 0.8000),
        (0.80, 0.82, 2947, 0.05, 0.80, True, True, 0.8001),
        (0.80, 0.83, 1264, 0.05, 0.80, True, True, 0.8001),
        (0.80, 0.84, 685, 0.05, 0.80, True, True, 0.8005),
        (0.80, 0.85, 421, 0.05, 0.80, True, True, 0.8009),
        (0.80, 0.86, 279, 0.05, 0.80, True, True, 0.8001),
        (0.80, 0.87, 196, 0.05, 0.80, True, True, 0.8017),
        (0.80, 0.88, 142, 0.05, 0.80, True, True, 0.8008),
        (0.80, 0.89, 106, 0.05, 0.80, True, True, 0.8013),
        (0.80, 0.90, 81, 0.05, 0.80, True, True, 0.8037),
        (0.80, 0.91, 62, 0.05, 0.80, True, True, 0.8009),
        (0.80, 0.92, 49, 0.05, 0.80, True, True, 0.8087),
        (0.80, 0.93, 38, 0.05, 0.80, True, True, 0.8059),
        (0.80, 0.94, 30, 0.05, 0.80, True, True, 0.8118),
        (0.80, 0.95, 23, 0.05, 0.80, True, True, 0.8058),
        # null_proportion = 0.65 to 0.79 by 0.01, proportion = 0.95, phat = True, continuity_correction = False
        (0.80, 0.65, 80, 0.05, 0.80, True, False, 0.8031),
        (0.80, 0.66, 90, 0.05, 0.80, True, False, 0.8006),
        (0.80, 0.67, 103, 0.05, 0.80, True, False, 0.8012),
        (0.80, 0.68, 119, 0.05, 0.80, True, False, 0.8013),
        (0.80, 0.69, 139, 0.05, 0.80, True, False, 0.8007),
        (0.80, 0.70, 165, 0.05, 0.80, True, False, 0.8004),
        (0.80, 0.71, 200, 0.05, 0.80, True, False, 0.8009),
        (0.80, 0.72, 248, 0.05, 0.80, True, False, 0.8012),
        (0.80, 0.73, 316, 0.05, 0.80, True, False, 0.8004),
        (0.80, 0.74, 420, 0.05, 0.80, True, False, 0.8005),
        (0.80, 0.75, 589, 0.05, 0.80, True, False, 0.8002),
        (0.80, 0.76, 895, 0.05, 0.80, True, False, 0.8001),
        (0.80, 0.77, 1545, 0.05, 0.80, True, False, 0.8001),
        (0.80, 0.78, 3368, 0.05, 0.80, True, False, 0.8001),
        (0.80, 0.79, 13022, 0.05, 0.80, True, False, 0.8000),
        # null_proportion = 0.81 to 0.95 by 0.01, proportion = 0.95, phat = True, continuity_correction = False
        (0.80, 0.81, 12080, 0.05, 0.80, True, False, 0.8000),
        (0.80, 0.82, 2897, 0.05, 0.80, True, False, 0.8001),
        (0.80, 0.83, 1231, 0.05, 0.80, True, False, 0.8002),
        (0.80, 0.84, 660, 0.05, 0.80, True, False, 0.8004),
        (0.80, 0.85, 401, 0.05, 0.80, True, False, 0.8007),
        (0.80, 0.86, 263, 0.05, 0.80, True, False, 0.8007),
        (0.80, 0.87, 182, 0.05, 0.80, True, False, 0.8018),
        (0.80, 0.88, 130, 0.05, 0.80, True, False, 0.8015),
        (0.80, 0.89, 95, 0.05, 0.80, True, False, 0.8006),
        (0.80, 0.90, 71, 0.05, 0.80, True, False, 0.8020),
        (0.80, 0.91, 54, 0.05, 0.80, True, False, 0.8064),
        (0.80, 0.92, 41, 0.05, 0.80, True, False, 0.8085),
        (0.80, 0.93, 31, 0.05, 0.80, True, False, 0.8097),
        (0.80, 0.94, 23, 0.05, 0.80, True, False, 0.8071),
        (0.80, 0.95, 17, 0.05, 0.80, True, False, 0.8100),
    ],
    ids=lambda p: f"{p[0]}, {p[1]}, {p[2]}, {p[3]}, {p[4]}, {p[5]}, {p[6]}, {p[7]}",
)
def case(request: pytest.FixtureRequest):
    return request.param


def test_size_solve_power(case) -> None:
    null_proportion, proportion, size, alpha, _, phat, continuity_correction, expected_power = case
    assert (
        round(
            solve_power(
                null_proportion,
                proportion,
                size,
                alpha,
                phat,
                continuity_correction,
            ),
            4,
        )
        == expected_power
    )


def test_solve_size(case) -> None:
    null_proportion, proportion, expected_size, alpha, power, phat, continuity_correction, _ = case
    assert (
        solve_size(
            null_proportion,
            proportion,
            alpha,
            power,
            phat,
            continuity_correction,
        )
        == expected_size
    )


def test_size_solve_null_proportion(case) -> None:
    expected_null_proportion, proportion, size, alpha, _, phat, continuity_correction, power = case

    if expected_null_proportion < proportion:
        assert (
            round(
                solve_null_proportion(
                    proportion,
                    size,
                    alpha,
                    power,
                    phat,
                    continuity_correction,
                    proportion_selection="lower",
                ),
                2,
            )
            == expected_null_proportion
        )
    else:
        assert (
            round(
                solve_null_proportion(
                    proportion,
                    size,
                    alpha,
                    power,
                    phat,
                    continuity_correction,
                    proportion_selection="upper",
                ),
                2,
            )
            == expected_null_proportion
        )


def test_size_solve_proportion(case) -> None:
    null_proportion, expected_proportion, size, alpha, _, phat, continuity_correction, power = case

    if expected_proportion < null_proportion:
        assert (
            round(
                solve_proportion(
                    null_proportion,
                    size,
                    alpha,
                    power,
                    phat,
                    continuity_correction,
                    proportion_selection="lower",
                ),
                2,
            )
            == expected_proportion
        )
    else:
        assert (
            round(
                solve_proportion(
                    null_proportion,
                    size,
                    alpha,
                    power,
                    phat,
                    continuity_correction,
                    proportion_selection="upper",
                ),
                2,
            )
            == expected_proportion
        )
