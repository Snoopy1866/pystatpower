# PyStatPower

[![PyPI - Version](https://img.shields.io/pypi/v/pystatpower)](https://badge.fury.io/py/pystatpower)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pystatpower)
![GitHub License](https://img.shields.io/github/license/Snoopy1866/pystatpower)
![PyPI - Status](https://img.shields.io/pypi/status/pystatpower)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pystatpower)

[![Build Status](https://img.shields.io/github/actions/workflow/status/Snoopy1866/pystatpower/release.yml?branch=main&label=build)](https://github.com/Snoopy1866/pystatpower/actions/workflows/release.yml?query=branch:main)
[![Test Status](https://img.shields.io/github/actions/workflow/status/Snoopy1866/pystatpower/check.yml?branch=main&label=test)](https://github.com/Snoopy1866/pystatpower/actions/workflows/check.yml?query=branch:main)
[![Documentation Status](https://readthedocs.org/projects/pystatpower/badge/?version=latest)](https://pystatpower.readthedocs.io/zh-cn/latest/?badge=latest)
[![codecov](https://codecov.io/gh/Snoopy1866/pystatpower/graph/badge.svg?token=P9UWC8Q4P6)](https://codecov.io/gh/Snoopy1866/pystatpower)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Snoopy1866/pystatpower/main.svg)](https://results.pre-commit.ci/latest/github/Snoopy1866/pystatpower/main)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pytest](https://img.shields.io/badge/logo-pytest-blue?logo=pytest&labelColor=5c5c5c&label=%20)](https://github.com/pytest-dev/pytest)
[![sphinx](https://img.shields.io/badge/logo-sphinx-blue?logo=sphinx&labelColor=5c5c5c&label=%20)](https://github.com/sphinx-doc/sphinx)

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
   git clone https://github.com/Snoopy1866/pystatpower.git
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
