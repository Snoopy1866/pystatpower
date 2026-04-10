# Validation Software: PASS 15
# Module: Confidence Interval for One Proportion


from math import ceil

import pytest

from pystatpower.models.proportion.single.ci import solve_size


@pytest.fixture(
    params=[
        # alpha = 0.05, proportion = 0.90, ci_width = 0.01 to 0.10 by 0.01, method = "clopper_pearson"
        (0.05, 0.90, 0.01, 14029, "clopper_pearson", False),
        (0.05, 0.90, 0.02, 3557, "clopper_pearson", False),
        (0.05, 0.90, 0.03, 1603, "clopper_pearson", False),
        (0.05, 0.90, 0.04, 914, "clopper_pearson", False),
        (0.05, 0.90, 0.05, 593, "clopper_pearson", False),
        (0.05, 0.90, 0.06, 417, "clopper_pearson", False),
        (0.05, 0.90, 0.07, 310, "clopper_pearson", False),
        (0.05, 0.90, 0.08, 241, "clopper_pearson", False),
        (0.05, 0.90, 0.09, 192, "clopper_pearson", False),
        (0.05, 0.90, 0.10, 158, "clopper_pearson", False),
        # alpha = 0.05, proportion = 0.90, ci_width = 0.01 to 0.10 by 0.01, method = "wald", continuity_correction = False
        (0.05, 0.90, 0.01, 13830, "wald", False),
        (0.05, 0.90, 0.02, 3458, "wald", False),
        (0.05, 0.90, 0.03, 1537, "wald", False),
        (0.05, 0.90, 0.04, 865, "wald", False),
        (0.05, 0.90, 0.05, 554, "wald", False),
        (0.05, 0.90, 0.06, 385, "wald", False),
        (0.05, 0.90, 0.07, 283, "wald", False),
        (0.05, 0.90, 0.08, 217, "wald", False),
        (0.05, 0.90, 0.09, 171, "wald", False),
        (0.05, 0.90, 0.10, 139, "wald", False),
        # alpha = 0.05, proportion = 0.90, ci_width = 0.01 to 0.10 by 0.01, method = "wald", continuity_correction = True
        (0.05, 0.90, 0.01, 14029, "wald", True),
        (0.05, 0.90, 0.02, 3557, "wald", True),
        (0.05, 0.90, 0.03, 1603, "wald", True),
        (0.05, 0.90, 0.04, 914, "wald", True),
        (0.05, 0.90, 0.05, 593, "wald", True),
        (0.05, 0.90, 0.06, 417, "wald", True),
        (0.05, 0.90, 0.07, 311, "wald", True),
        (0.05, 0.90, 0.08, 241, "wald", True),
        (0.05, 0.90, 0.09, 193, "wald", True),
        (0.05, 0.90, 0.10, 158, "wald", True),
        # alpha = 0.05, proportion = 0.90, ci_width = 0.01 to 0.10 by 0.01, method = "wilson", continuity_correction = False
        (0.05, 0.90, 0.01, 13833, "wilson", False),
        (0.05, 0.90, 0.02, 3461, "wilson", False),
        (0.05, 0.90, 0.03, 1540, "wilson", False),
        (0.05, 0.90, 0.04, 868, "wilson", False),
        (0.05, 0.90, 0.05, 557, "wilson", False),
        (0.05, 0.90, 0.06, 388, "wilson", False),
        (0.05, 0.90, 0.07, 286, "wilson", False),
        (0.05, 0.90, 0.08, 219, "wilson", False),
        (0.05, 0.90, 0.09, 174, "wilson", False),
        (0.05, 0.90, 0.10, 141, "wilson", False),
        # alpha = 0.05, proportion = 0.90, ci_width = 0.01 to 0.10 by 0.01, method = "wilson", continuity_correction = True
        (0.05, 0.90, 0.01, 14032, "wilson", True),
        (0.05, 0.90, 0.02, 3560, "wilson", True),
        (0.05, 0.90, 0.03, 1606, "wilson", True),
        (0.05, 0.90, 0.04, 917, "wilson", True),
        (0.05, 0.90, 0.05, 595, "wilson", True),
        (0.05, 0.90, 0.06, 420, "wilson", True),
        (0.05, 0.90, 0.07, 313, "wilson", True),
        (0.05, 0.90, 0.08, 243, "wilson", True),
        (0.05, 0.90, 0.09, 195, "wilson", True),
        (0.05, 0.90, 0.10, 160, "wilson", True),
    ],
    ids=lambda p: f"{p[0]}, {p[1]}, {p[2]}, {p[3]}, {p[4]}, {p[5]}",
)
def case(request: pytest.FixtureRequest):
    return request.param


def test_solve_size(case) -> None:
    alpha, proportion, ci_width, expected_size, method, continuity_correction = case
    assert ceil(solve_size(proportion, ci_width, alpha, method, continuity_correction)) == expected_size


def test_solve_wilson_cc_no_solution() -> None:
    with pytest.raises(ValueError):
        assert solve_size(0.90, 0.99, 0.05, method="wilson", continuity_correction=True)
