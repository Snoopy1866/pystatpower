## OpenPower

OpenPower 是一个用于功效分析的开源的 Python 库。

## 安装

```
pip install openpower
```

## 使用

```python
from openpower.procedures import *

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
