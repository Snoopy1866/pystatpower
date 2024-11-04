# pystatpower.option

```{eval-rst}
.. autoclass:: pystatpower.option.Option
```

```{eval-rst}
.. autoclass:: pystatpower.option.Alternative
```

::::{note}

大多数假设检验都有单侧检验和双侧检验两种版本，选择单侧检验还是双侧检验将会直接影响试验假设。

以单样本率检验为例：

- 选择单侧检验：
  :::{math}
  H_0: p_1 = p_0

  H_1: p_1 \gt p_0
  :::

  或

  :::{math}
  H_0: p_1 = p_0

  H_1: p_1 \lt p_0
  :::

- 选择双侧检验：
  :::{math}
  H_0: p_1 = p_0

  H_1: p_1 \ne p_0
  :::
  ::::

```{eval-rst}
.. autoclass:: pystatpower.option.SearchDirection
```

:::{important}

{class}`SearchDirection <pystatpower.option.SearchDirection>` 仅在部分求解情况下可用，例如：单样本率差异性检验下，反推效应量。
:::
