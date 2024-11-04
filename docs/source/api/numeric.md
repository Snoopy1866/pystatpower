# pystatpower.numeric

```{eval-rst}
.. autodata:: pystatpower.numeric.MIN_FLOAT
.. autodata:: pystatpower.numeric.MAX_FLOAT
```

:::{note}
PyStatPower 通过 `MIN_FLOAT` 和 `MAX_FLOAT` 限定数值计算的范围，这一范围相比 Python 默认的浮点数范围要小很多。

在计算机进行迭代计算时，小于 `MIN_FLOAT` 的差异会被忽略，这有助于减少数值计算的迭代次数。
此外，在实际应用中，超出 `MAX_FLOAT` 数值可能被认为是不切实际的。

例如：在计算样本量的时候，若计算结果超出 {attr}`Size.domain <pystatpower.numeric.Size.domain>` 规定的数值上限，
则认为在当前设定的参数下，满足要求的样本量是不合理的。
:::

```{eval-rst}
.. autoclass:: pystatpower.numeric.Interval
```

```{eval-rst}
.. autoclass:: pystatpower.numeric.PowerAnalysisFloat
```

```{eval-rst}
.. autoclass:: pystatpower.numeric.Alpha
.. autoclass:: pystatpower.numeric.Power
.. autoclass:: pystatpower.numeric.Mean
.. autoclass:: pystatpower.numeric.STD
.. autoclass:: pystatpower.numeric.Proportion
.. autoclass:: pystatpower.numeric.Percent
.. autoclass:: pystatpower.numeric.Ratio
.. autoclass:: pystatpower.numeric.Size
.. autoclass:: pystatpower.numeric.DropOutRate
.. autoclass:: pystatpower.numeric.DropOutSize
```
