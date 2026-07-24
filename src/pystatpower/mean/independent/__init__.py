# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Power analysis for two independent means.

This package provides the following modules:

- ci: Confidence intervals for two independent means.
- inequality: Inequality tests for two independent means.
- noninferiority: Non-inferiority tests for two independent means.
- superiority: Superiority tests for two independent means.
"""

from ...mean.independent import ci
from ...mean.independent import inequality
from ...mean.independent import noninferiority
from ...mean.independent import superiority

__all__ = [
    "ci",
    "inequality",
    "noninferiority",
    "superiority",
]
