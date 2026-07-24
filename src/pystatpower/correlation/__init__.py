# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Power analysis for correlation coefficient.

This package provides the following modules:

- ci: Confidence intervals for correlation coefficient.
- inequality: Inequality tests for correlation coefficient.
"""

from ..correlation import ci
from ..correlation import inequality

__all__ = [
    "ci",
    "inequality",
]
