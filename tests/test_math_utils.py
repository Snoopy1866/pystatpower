# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

from math import inf

from pystatpower._math_utils import _domain_square_root_of_quad


def test_domain_square_root_of_quad() -> None:
    assert _domain_square_root_of_quad(1, 2, 3) == (-inf, inf)
    assert _domain_square_root_of_quad(1, -2, 1) == (-inf, inf)
    assert _domain_square_root_of_quad(1, -3, 2) == ((-inf, 1), (2, inf))
    assert _domain_square_root_of_quad(-1, -2, -3) is None
    assert _domain_square_root_of_quad(-1, 2, -1) == 1
    assert _domain_square_root_of_quad(-1, 3, -2) == (1, 2)
