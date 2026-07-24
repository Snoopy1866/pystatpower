# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Power analysis for a single mean.

This package provides the following modules:

- ci: Confidence intervals for a single mean.
- inequality: Inequality tests for a single mean.
- noninferiority: Non-inferiority tests for a single mean.
- superiority: Superiority tests for a single mean.
- equivalence: Equivalence tests for a single mean.
"""

from ...mean.single import ci
from ...mean.single import inequality
from ...mean.single import noninferiority
from ...mean.single import superiority

__all__ = [
    "ci",
    "inequality",
    "noninferiority",
    "superiority",
]
