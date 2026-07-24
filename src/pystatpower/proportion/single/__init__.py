# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Power analysis for a single proportion.

This package provides the following modules:

- ci: Confidence intervals for a single proportion.
- inequality: Inequality tests for a single proportion.
- noninferiority: Non-inferiority tests for a single proportion.
- superiority: Superiority tests for a single proportion.
- equivalence: Equivalence tests for a single proportion.
"""

from . import ci
from . import equivalence
from . import inequality
from . import noninferiority
from . import superiority

__all__ = [
    "ci",
    "inequality",
    "noninferiority",
    "superiority",
    "equivalence",
]
