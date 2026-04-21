# PyStatPower

[![PyPI - Version](https://img.shields.io/pypi/v/pystatpower)](https://badge.fury.io/py/pystatpower)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pystatpower)
![GitHub License](https://img.shields.io/github/license/Snoopy1866/pystatpower)
![PyPI - Status](https://img.shields.io/pypi/status/pystatpower)
[![PyPI Downloads](https://static.pepy.tech/badge/pystatpower)](https://pepy.tech/projects/pystatpower)

[![Build Status](https://img.shields.io/github/actions/workflow/status/Snoopy1866/pystatpower/release.yml)](https://github.com/Snoopy1866/pystatpower/actions/workflows/release.yml?query=branch:main)
[![Test Status](https://img.shields.io/github/actions/workflow/status/Snoopy1866/pystatpower/pytest.yml?branch=main&label=test)](https://github.com/Snoopy1866/pystatpower/actions/workflows/pytest.yml?query=branch:main)
[![Documentation Status](https://readthedocs.org/projects/pystatpower/badge/?version=latest)](https://pystatpower.readthedocs.io/zh-cn/latest/?badge=latest)
[![codecov](https://codecov.io/gh/Snoopy1866/pystatpower/graph/badge.svg?token=P9UWC8Q4P6)](https://codecov.io/gh/Snoopy1866/pystatpower)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Snoopy1866/pystatpower/main.svg)](https://results.pre-commit.ci/latest/github/Snoopy1866/pystatpower/main)

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pytest](https://img.shields.io/badge/logo-pytest-blue?logo=pytest&labelColor=5c5c5c&label=%20)](https://github.com/pytest-dev/pytest)

PyStatPower 是一个统计学功效分析的 Python 软件包，可用于样本量、检验效能和效应量大小的估计。

目前支持的模块如下：

- 单样本率置信区间
- 单样本率差异性检验
- 两独立样本率非劣效检验
- 相关系数检验

## 使用

```bash
pip install pystatpower
```

## 示例

```python
from pystatpower.models import proportion

size = proportion.independent.noninferiority.solve_size(
    treatment_proportion=0.95,
    reference_proportion=0.90,
    margin=-0.10,
    ratio=1,
    alpha=0.025,
    power=0.8,
)
print(size)
```

输出:

```python
(48, 48)
```

## Scipy 兼容性测试结果

|            | 🐍 3.10 | 🐍 3.11 | 🐍 3.12 | 🐍 3.13 | 🐍 3.14 |
| ---------- | ------- | ------- | ------- | ------- | ------- |
| SciPy 1.7  |         |         |         |         |         |
| SciPy 1.8  |         |         |         |         |         |
| SciPy 1.9  |         |         |         |         |         |
| SciPy 1.10 |         |         |         |         |         |
| SciPy 1.11 |         |         |         |         |         |
| SciPy 1.12 |         |         |         |         |         |
| SciPy 1.13 |         |         |         |         |         |
| SciPy 1.14 |         |         |         |         |         |
| SciPy 1.15 |         |         |         |         |         |
| SciPy 1.16 |         |         |         |         |         |
| SciPy 1.17 |         |         |         |         |         |

## 鸣谢

- [scipy](https://github.com/scipy/scipy)
- [pingouin](https://github.com/raphaelvallat/pingouin)
