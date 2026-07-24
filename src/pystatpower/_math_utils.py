# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""A module containing mathematical tool functions."""

from math import inf
from math import sqrt
from typing import TypeAlias

Domain: TypeAlias = tuple[float, float]


def _domain_square_root_of_quad(a: float, b: float, c: float, /) -> Domain | tuple[Domain, Domain] | float | None:
    r"""Solve the domain of the function f(x) = \sqrt{ax^2+bx+c} (a ≠ 0)."""
    delta = b**2 - 4 * a * c
    if a > 0:
        if delta <= 0:
            return -inf, inf
        else:
            x1 = (-b - sqrt(delta)) / (2 * a)
            x2 = (-b + sqrt(delta)) / (2 * a)
            return ((-inf, x1), (x2, inf))
    else:  # a < 0
        if delta < 0:
            return None
        elif delta == 0:
            return -b / (2 * a)
        else:
            x1 = (-b - sqrt(delta)) / (2 * a)
            x2 = (-b + sqrt(delta)) / (2 * a)
            return x2, x1
