# PyStatPower

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/PyStatPower/PyStatPower/check.yml?branch=main)](https://github.com/PyStatPower/PyStatPower/actions/workflows/check.yml?query=branch:main)
[![PyPI - Version](https://img.shields.io/pypi/v/pystatpower)](https://badge.fury.io/py/pystatpower)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FPyStatPower%2FPyStatPower%2Fmain%2Fpyproject.toml)
![GitHub License](https://img.shields.io/github/license/PyStatPower/PyStatPower)
![PyPI - Status](https://img.shields.io/pypi/status/PyStatPower)
![PyPI - Downloads](https://img.shields.io/pypi/dw/pystatpower)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/PyStatPower/PyStatPower/graph/badge.svg?token=P9UWC8Q4P6)](https://codecov.io/gh/PyStatPower/PyStatPower)

PyStatPower 是一个专注于统计领域功效分析的开源的 Python 库。

主要功能：样本量和检验效能的计算，以及给定参数下估算所需效应量大小。

[详细文档](https://pystatpower.github.io/PyStatPower-Docs)

## 安装

```cmd
pip install pystatpower
```

## 使用

```python
from pystatpower.procedures import ospp

result = ospp.solve(n=None, alpha=0.05, power=0.80, nullproportion=0.80, proportion=0.95)
print(result)
```

输出：

```python
41.594991602280594
```

## 鸣谢

- [scipy](https://github.com/scipy/scipy)
- [pingouin](https://github.com/raphaelvallat/pingouin)
