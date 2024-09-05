## PyStatPower

PyStatPower 是一个专注于功效分析的开源的 Python 库。

## 安装

```
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
