# PyStatPower

![Test](https://github.com/PyStatPower/PyStatPower/actions/workflows/test.yml/badge.svg?branch=main)
[![PyPI version](https://badge.fury.io/py/pystatpower.svg)](https://badge.fury.io/py/pystatpower)

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
