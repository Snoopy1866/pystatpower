# 快速开始

## 安装

使用 PyStatPower 前，需要先安装 [Python 解释器](https://www.python.org/downloads/)，支持 3.10 及以上版本。

使用以下命令安装 pystatpower：

```bash
pip install pystatpower
```

安装完成后，运行以下命令检查是否正确安装：

```bash
python -m pystatpower
```

你应当看到类似如下的版本号信息：

```bash
pystatpower version 0.0.2
```

## 示例

pystatpower 提供了一些模块用于对不同假设检验场景下的分析，下面是一些具体的代码示例：

### 单样本率差异性检验

#### 估算样本量

```python
from pystatpower.models import one_proportion

result = one_proportion.solve_for_sample_size(
    alpha=0.05,
    power=0.80,
    nullproportion=0.80,
    proportion=0.95,
    alternative="two_sided",
    test_type="exact_test"
)
print(result)
```

输出:

```python
42.0
```

### 两独立样本率差异性检验

#### 估算样本量

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

输出:

```python
(76.0, 76.0)
```

#### 计算检验效能

```python
from pystatpower.models.two_proportion import solve_for_power, GroupAllocation

result = solve_for_power(
    alpha=0.05,
    treatment_proportion=0.95,
    reference_proportion=0.80,
    alternative="two_sided",
    test_type="z_test_pooled",
    group_allocation=GroupAllocation(
        size_of_treatment=100,
        size_of_reference=50,
    ),
)
print(result)
```

输出:

```python
0.7865318578853373
```
