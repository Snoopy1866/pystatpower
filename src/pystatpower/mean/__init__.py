# Copyright (C) 2024-present The Package Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Power analysis for mean models.

This package provides the following subpackages:

- single: Power analysis for a single mean.
- independent: Power analysis for two independent mean.
"""

from ..mean import independent
from ..mean import single

__all__ = [
    "single",
    "independent",
]
