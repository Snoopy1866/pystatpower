# PyStatPower

[![build](https://img.shields.io/github/actions/workflow/status/PyStatPower/PyStatPower/release.yml?branch=main&label=build)](https://github.com/PyStatPower/PyStatPower/actions/workflows/build.yml?query=branch:main)
[![test](https://img.shields.io/github/actions/workflow/status/PyStatPower/PyStatPower/check.yml?branch=main&label=test)](https://github.com/PyStatPower/PyStatPower/actions/workflows/check.yml?query=branch:main)
[![lint](https://img.shields.io/github/actions/workflow/status/PyStatPower/PyStatPower/black.yml?branch=main&label=lint)](https://github.com/PyStatPower/PyStatPower/actions/workflows/black.yml?query=branch:main)
[![PyPI - Version](https://img.shields.io/pypi/v/pystatpower)](https://badge.fury.io/py/pystatpower)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FPyStatPower%2FPyStatPower%2Fmain%2Fpyproject.toml)
![GitHub License](https://img.shields.io/github/license/PyStatPower/PyStatPower)
![PyPI - Status](https://img.shields.io/pypi/status/PyStatPower)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pystatpower)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/PyStatPower/PyStatPower/graph/badge.svg?token=P9UWC8Q4P6)](https://codecov.io/gh/PyStatPower/PyStatPower)

PyStatPower 是一个专注于统计领域功效分析的开源的 Python 库。

主要功能：样本量和检验效能的计算，以及给定参数下估算所需效应量大小。

[详细文档](https://pystatpower.github.io/PyStatPower-Docs)

> [!WARNING]
> 本项目处于 alpha 阶段，文档尚未完成。

## 安装

```cmd
pip install pystatpower
```

## 示例

### 计算样本量

#### 单组样本率检验

```python
from pystatpower.models import one_proportion

result = one_proportion.solve_for_sample_size(
    alpha=0.05, power=0.80, nullproportion=0.80, proportion=0.95, alternative="two_sided", test_type="exact_test"
)
print(result)
```

输出：

```python
Size(41.59499160228066)
```

#### 两独立样本率差异性检验

```python
from pystatpower.models import two_proportion

result = two_proportion.solve_for_sample_size(
    alpha=0.05,
    power=0.80,
    treatment_proportion=0.95,
    reference_proportion=0.80,
    alternative="two_sided",
    test_type="z_test_pooled",
)
print(result)
```

输出：

```python
(Size(75.11862332120842), Size(75.11862332120842))
```

### 计算检验效能

```python
from pystatpower.models.two_proportion import *

result = solve_for_power(
    alpha=0.05,
    treatment_proportion=0.95,
    reference_proportion=0.80,
    alternative="two_sided",
    test_type="z_test_pooled",
    group_allocation=GroupAllocation.ForPower(
        size_of_treatment=100,
        size_of_reference=50,
    ),
)
print(result)
```

输出：

```python
Power(0.7865318578853373)
```

## 鸣谢

- [scipy](https://github.com/scipy/scipy)
- [pingouin](https://github.com/raphaelvallat/pingouin)
