# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Power analysis for proportion models.

This package provides the following subpackages:

- single: Power analysis for a single proportion.
- independent: Power analysis for two independent proportions.
- paired: Power analysis for two paired proportions.
"""

from ..proportion import independent
from ..proportion import paired
from ..proportion import single

__all__ = [
    "single",
    "independent",
    "paired",
]
