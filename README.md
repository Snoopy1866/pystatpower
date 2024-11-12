# PyStatPower

[![PyPI - Version](https://img.shields.io/pypi/v/pystatpower)](https://badge.fury.io/py/pystatpower)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FPyStatPower%2FPyStatPower%2Fmain%2Fpyproject.toml)
![GitHub License](https://img.shields.io/github/license/PyStatPower/PyStatPower)
![PyPI - Status](https://img.shields.io/pypi/status/PyStatPower)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pystatpower)

[![Build Status](https://img.shields.io/github/actions/workflow/status/PyStatPower/PyStatPower/release.yml?branch=main&label=build)](https://github.com/PyStatPower/PyStatPower/actions/workflows/release.yml?query=branch:main)
[![Documentation Status](https://readthedocs.org/projects/pystatpower/badge/?version=latest)](https://pystatpower.readthedocs.io/zh-cn/latest/?badge=latest)
[![Test Status](https://img.shields.io/github/actions/workflow/status/PyStatPower/PyStatPower/check.yml?branch=main&label=test)](https://github.com/PyStatPower/PyStatPower/actions/workflows/check.yml?query=branch:main)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/gh/PyStatPower/PyStatPower/graph/badge.svg?token=P9UWC8Q4P6)](https://codecov.io/gh/PyStatPower/PyStatPower)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/PyStatPower/PyStatPower/main.svg)](https://results.pre-commit.ci/latest/github/PyStatPower/PyStatPower/main)

[简体中文](README.md) | [English](README-en.md)

PyStatPower 是一个专注于统计领域功效分析的开源的 Python 库。

主要功能：样本量和检验效能的计算，以及给定参数下估算所需效应量大小。

## 安装

```bash
pip install pystatpower
```

## 示例

```python
from pystatpower.models import one_proportion

result = one_proportion.solve_for_sample_size(
    alpha=0.05, power=0.80, nullproportion=0.80, proportion=0.95, alternative="two_sided", test_type="exact_test"
)
print(result)
```

输出:

```python
Size(41.59499160228066)
```

## 构建

1. 克隆本仓库

   ```bash
   git clone https://github.com/PyStatPower/PyStatPower.git
   ```

2. 安装依赖

   ```bash
   pip install .[docs]
   ```

3. 安装 pre-commit

   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

4. 切换到文档目录

   ```bash
   cd docs
   ```

5. 构建文档

   ```bash
   make clean
   make html
   ```

你可以在 `docs/build/html` 目录下看到生成的文档，双击 `index.html` 即可在浏览器中查看。

## 鸣谢

- [scipy](https://github.com/scipy/scipy)
- [pingouin](https://github.com/raphaelvallat/pingouin)
