# PyStatPower

[![PyPI - Version](https://img.shields.io/pypi/v/pystatpower)](https://badge.fury.io/py/pystatpower)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pystatpower)
![GitHub License](https://img.shields.io/github/license/Snoopy1866/pystatpower)
![PyPI - Status](https://img.shields.io/pypi/status/pystatpower)
[![PyPI Downloads](https://static.pepy.tech/badge/pystatpower)](https://pepy.tech/projects/pystatpower)

[![Build Status](https://img.shields.io/github/actions/workflow/status/Snoopy1866/pystatpower/release.yml?branch=main&label=build)](https://github.com/Snoopy1866/pystatpower/actions/workflows/release.yml?query=branch:main)
[![Test Status](https://img.shields.io/github/actions/workflow/status/Snoopy1866/pystatpower/check.yml?branch=main&label=test)](https://github.com/Snoopy1866/pystatpower/actions/workflows/check.yml?query=branch:main)
[![Documentation Status](https://readthedocs.org/projects/pystatpower/badge/?version=latest)](https://pystatpower.readthedocs.io/zh-cn/latest/?badge=latest)
[![codecov](https://codecov.io/gh/Snoopy1866/pystatpower/graph/badge.svg?token=P9UWC8Q4P6)](https://codecov.io/gh/Snoopy1866/pystatpower)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Snoopy1866/pystatpower/main.svg)](https://results.pre-commit.ci/latest/github/Snoopy1866/pystatpower/main)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pytest](https://img.shields.io/badge/logo-pytest-blue?logo=pytest&labelColor=5c5c5c&label=%20)](https://github.com/pytest-dev/pytest)
[![sphinx](https://img.shields.io/badge/logo-sphinx-blue?logo=sphinx&labelColor=5c5c5c&label=%20)](https://github.com/sphinx-doc/sphinx)

[简体中文](README.md) | [English](README-en.md)

PyStatPower is an open-source Python library focused on power analysis in the field of statistics.

Main features: calculation of sample size and test power, and estimation of the required effect size

## Installation

```bash
pip install pystatpower
```

## Example

```python
from pystatpower.models import one_proportion

result = one_proportion.solve_for_sample_size(
    alpha=0.05, power=0.80, nullproportion=0.80, proportion=0.95, alternative="two_sided", test_type="exact_test"
)
print(result)
```

Output:

```python
Size(41.59499160228066)
```

## Build

1. Clone this repository

   ```bash
   git clone https://github.com/Snoopy1866/pystatpower.git
   ```

2. Install dependencies

   ```bash
   pip install .[docs]
   ```

3. Change to the documentation directory

   ```bash
   cd docs
   ```

4. Build the documentation

   ```bash
   make clean
   make html
   ```

You can view the generated documentation in the `docs/build/html` directory by opening `index.html` in your browser.

## Acknowledgements

- [scipy](https://github.com/scipy/scipy)
- [pingouin](https://github.com/raphaelvallat/pingouin)
