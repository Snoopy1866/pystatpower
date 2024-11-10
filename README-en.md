# PyStatPower

[![PyPI - Version](https://img.shields.io/pypi/v/pystatpower)](https://badge.fury.io/py/pystatpower)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FPyStatPower%2FPyStatPower%2Fmain%2Fpyproject.toml)
![GitHub License](https://img.shields.io/github/license/PyStatPower/PyStatPower)
![PyPI - Status](https://img.shields.io/pypi/status/PyStatPower)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pystatpower)

[![Build Status](https://img.shields.io/github/actions/workflow/status/PyStatPower/PyStatPower/release.yml?branch=main&label=build)](https://github.com/PyStatPower/PyStatPower/actions/workflows/release.yml?query=branch:main)
[![Documentation Status](https://readthedocs.org/projects/pystatpower/badge/?version=latest)](https://pystatpower.readthedocs.io/zh-cn/latest/?badge=latest)
[![Test Status](https://img.shields.io/github/actions/workflow/status/PyStatPower/PyStatPower/check.yml?branch=main&label=test)](https://github.com/PyStatPower/PyStatPower/actions/workflows/check.yml?query=branch:main)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/PyStatPower/PyStatPower/graph/badge.svg?token=P9UWC8Q4P6)](https://codecov.io/gh/PyStatPower/PyStatPower)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/PyStatPower/PyStatPower/main.svg)](https://results.pre-commit.ci/latest/github/PyStatPower/PyStatPower/main)

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
   git clone https://github.com/PyStatPower/PyStatPower.git
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
