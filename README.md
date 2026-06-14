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
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/37b044b24840497c9153ac4be7b841d9)](https://app.codacy.com/gh/Snoopy1866/pystatpower/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

PyStatPower 是一个统计学功效分析的 Python 软件包，可用于样本量、检验效能和效应量大小的估计。

## 📚 功能模块

| 模型分类        | 样本类型   | 置信区间 | 差异性检验 | 非劣效检验 | 优效性检验 | 等效性检验 |
| --------------- | ---------- | -------- | ---------- | ---------- | ---------- | ---------- |
| **📊 均值模型** | 单样本     | ✅       | ✅         | ✅         | ⏳ _WIP_   | ⏳ _WIP_   |
|                 | 两独立样本 | ✅       | ✅         | ✅         | ✅         | ⏳ _WIP_   |
| **🍰 比例模型** | 单样本     | ✅       | ✅         | ✅         | ✅         | ✅         |
|                 | 两独立样本 | ✅       | ✅         | ✅         | ✅         | ⏳ _WIP_   |
| **📈 相关系数** |            | ✅       | ✅         | 🚫         | 🚫         | 🚫         |

> 📌 **图例说明**：
>
> - ✅ = 已实现
> - ⏳ _WIP_ = 计划实现/开发中（欢迎提交 PR 贡献代码！ 🚀）
> - 🚫 = 理论上不适用或暂无计划

## 📦 安装

前置需求：Python 3.10+

```bash
pip install pystatpower
```

## 🔨 使用示例

### 估算样本量

- 单样本率置信区间

  ```python
  from pystatpower import proportion

  size = proportion.single.ci.solve_size(
      proportion=0.9,
      distance=0.10,
      conf_level=0.95,
      interval_type="two-sided",
  )
  print(size)

  # output: 158
  ```

- 单样本率差异性检验（单组目标值法）

  ```python
  from pystatpower import proportion

  size = proportion.single.inequality.solve_size(
      null_proportion=0.80,
      proportion=0.95,
      alternative="one-sided",
      alpha=0.025,
      power=0.8,
  )
  print(size)

  # output: 42
  ```

- 两独立样本率非劣效检验

  ```python
  from pystatpower import proportion

  size = proportion.independent.noninferiority.solve_size(
      treatment_proportion=0.95,
      reference_proportion=0.90,
      margin=-0.10,
      ratio=1,
      alpha=0.025,
      power=0.8,
  )
  print(size)

  # output: (48, 48)
  ```

- 两独立样本均值优效性检验

  ```python
  from pystatpower import mean

  size = mean.independent.superiority.solve_size(
      diff=0.5,
      margin=0.1,
      treatment_std=1.2,
      reference_std=1.2,
      ratio=2,
      alpha=0.025,
      power=0.8,
  )
  print(size)

  # output: (214, 107)
  ```

### 计算检验效能

```python
from pystatpower import proportion

power = proportion.independent.noninferiority.solve_power(
    treatment_proportion=0.95,
    reference_proportion=0.90,
    margin=-0.10,
    treatment_size=48,
    reference_size=48,
    alpha=0.025,
)
print(power)

# output: 0.800282915718918
```

### 反推效应量

```python
from pystatpower import proportion

treatment_proportion = proportion.independent.noninferiority.solve_treatment_proportion(
    reference_proportion=0.90,
    margin=-0.10,
    treatment_size=48,
    reference_size=48,
    alpha=0.025,
    power=0.8,
)
print(treatment_proportion)

# output: 0.9499637015276098
```

## 🧪 兼容性测试结果

[![Test Status](https://img.shields.io/github/actions/workflow/status/Snoopy1866/pystatpower/pytest_full.yml?branch=main&label=test)](https://github.com/Snoopy1866/pystatpower/actions/workflows/pytest_full.yml?query=branch:main)

|            | 🐍 3.10 | 🐍 3.11 | 🐍 3.12 | 🐍 3.13 | 🐍 3.14 |
| ---------- | ------- | ------- | ------- | ------- | ------- |
| SciPy 1.7  | ✅      | -       | -       | -       | -       |
| SciPy 1.8  | ✅      | -       | -       | -       | -       |
| SciPy 1.9  | ✅      | -       | -       | -       | -       |
| SciPy 1.10 | ✅      | ✅      | -       | -       | -       |
| SciPy 1.11 | ✅      | ✅      | ✅      | -       | -       |
| SciPy 1.12 | ✅      | ✅      | ✅      | -       | -       |
| SciPy 1.13 | ✅      | ✅      | ✅      | -       | -       |
| SciPy 1.14 | ✅      | ✅      | ✅      | -       | -       |
| SciPy 1.15 | ✅      | ✅      | ✅      | ✅      | -       |
| SciPy 1.16 | -       | ✅      | ✅      | ✅      | ✅      |
| SciPy 1.17 | -       | ✅      | ✅      | ✅      | ✅      |

注： `-` 表示该 Python 版本下不存在对应的 SciPy 发行版。

## 🔮 鸣谢

- [scipy](https://github.com/scipy/scipy)
- [pingouin](https://github.com/raphaelvallat/pingouin)
