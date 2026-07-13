# 相关系数置信区间

假设总体相关系数用 $r$ 表示，经 Fisher's z 转换后用 $z_r$ 表示：

$$
z_r = \operatorname{arctanh}r = \frac{1}{2} \ln{\frac{1+r}{1-r}}
$$

则样本相关系数 $\hat{r}$ 经 Fisher's z 转换后，近似服从正态分布：

$$
z_\hat{r} \sim N\left(z_r, \frac{1}{n-3}\right)
$$

通过计算 $z_\hat{r}$ 的置信区间，并利用以下公式将置信限反转，可得到样本相关系数 $\hat{r}$ 的置信区间：

$$
r = \operatorname{tanh}r = \frac{e^{2 z_r} - 1}{e^{2 z_r} + 1}
$$

以下仅给出 $z_{\hat{r}}$ 的置信限。

## 未校正偏倚 {#bias-not-adj}

=== "双侧置信区间"

    $$
    \begin{align}
    L & = z_{\hat{r}} - z_{1-\alpha/2} \sqrt{\frac{1}{n-3}} \\
    U & = z_{\hat{r}} + z_{1-\alpha/2} \sqrt{\frac{1}{n-3}}
    \end{align}
    $$

    置信区间宽度：

    $$
    d = \operatorname{tanh}U - \operatorname{tanh}L
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = z_{\hat{r}} - z_{1-\alpha} \sqrt{\frac{1}{n-3}} \\
    U & = 1
    \end{align}
    $$

    从相关系数到置信下限的距离：

    $$
    d = r - \operatorname{tanh}L
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = -1 \\
    U & = z_{\hat{r}} + z_{1-\alpha} \sqrt{\frac{1}{n-3}}
    \end{align}
    $$

    从相关系数到置信上限的距离：

    $$
    d = \operatorname{tanh}U - r
    $$

## 校正偏倚 {#bias-adj}

在 [未校正偏倚][bias-not-adj] 的基础上加入校正项 $\frac{r}{2(n-1)}$，即：

$$
z_\hat{r} + \frac{\hat{r}}{2(n-1)} \sim N\left(z_r, \frac{1}{n-3}\right)
$$

=== "双侧置信区间"

    $$
    \begin{align}
    L & = z_{\hat{r}} - \frac{\hat{r}}{2(n-1)} - z_{1-\alpha/2} \sqrt{\frac{1}{n-3}} \\
    U & = z_{\hat{r}} - \frac{\hat{r}}{2(n-1)} + z_{1-\alpha/2} \sqrt{\frac{1}{n-3}}
    \end{align}
    $$

    置信区间宽度：

    $$
    d = \operatorname{tanh}U - \operatorname{tanh}L
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = z_{\hat{r}} - \frac{\hat{r}}{2(n-1)} - z_{1-\alpha} \sqrt{\frac{1}{n-3}} \\
    U & = 1
    \end{align}
    $$

    从相关系数到置信下限的距离：

    $$
    d = r - \operatorname{tanh}L
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = -1 \\
    U & = z_{\hat{r}} - \frac{\hat{r}}{2(n-1)} + z_{1-\alpha} \sqrt{\frac{1}{n-3}}
    \end{align}
    $$

    从相关系数到置信上限的距离：

    $$
    d = \operatorname{tanh}U - r
    $$

!!! quote "参考文献"

    1. JH Z. Zar JH. Dichotomous variables[J]. Biostatistical Analysis 5th ed. Upper Saddle River, NJ: Prentice-Hall, 2010: 557-558.
