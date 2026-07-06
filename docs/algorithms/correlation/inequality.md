# 相关系数差异性检验

样本相关系数用 $\hat{r}$ 表示，总体相关系数用 $r$ 表示。

对于双侧检验，统计学假设如下：

$$
\begin{align}
H_0 & : r = r_0 \\
H_1 & : r \neq r_0
\end{align}
$$

对于左单侧检验，统计学假设如下：

$$
\begin{align}
H_0 & : r \geqslant r_0 \\
H_1 & : r \lt r_0
\end{align}
$$

对于右单侧检验，统计学假设如下：

$$
\begin{align}
H_0 & : r \leqslant r_0 \\
H_1 & : r \gt r_0
\end{align}
$$

以下推导过程在边界条件 $r = r_0$ 下进行。

定义 _Fisher's z_ 转换：

$$
z_r = \operatorname{arctanh}r = \frac{1}{2} \ln{\frac{1+r}{1-r}}
$$

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{z_{\hat{r}} - z_{r_0}}{1/\sqrt{n-3}} = (z_{\hat{r}} - z_{r_0}) \sqrt{n-3} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{z_{\hat{r}} - z_{r_0}}{1/\sqrt{n-3}} = (z_{\hat{r}} - z_{r_0}) \sqrt{n-3} \sim N\left((z_r - z_{r_0})\sqrt{n-3}, 1\right)
$$

=== "双侧检验"

    $$
    \begin{align}
    \text{Power} & = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right) \\
                 & = 1 - \Phi\left(z_{1-\alpha/2} - (z_r - z_{r_0}) \sqrt{n-3}\right) + \Phi\left(z_{\alpha/2} - (z_r - z_{r_0}) \sqrt{n-3}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
    \begin{align}
    \text{Power} = P\left(z' < z_{\alpha}\right)
                 = \Phi\left(z_{\alpha} - (z_r - z_{r_0}) \sqrt{n-3}\right)
    \end{align}
    $$

=== "右单侧检验"

    $$
    \begin{align}
    \text{Power} = P\left(z' > z_{1-\alpha}\right)
                 = 1 - \Phi\left(z_{1-\alpha} - (z_r - z_{r_0}) \sqrt{n-3}\right)
    \end{align}
    $$

??? note "单侧检验样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    z_{1-\alpha} \pm (z_r - z_{r_0}) \sqrt{n-3} = z_{\beta}
    $$

    可解出：

    $$
    n = \frac{\left(z_{1-\alpha} + z_{1-\beta}\right)^2}{(z_r - z_{r_0})^2} + 3
    $$

    利用 _Fisher's z_ 转换得：

    $$
    n = 4 \cdot \frac{\left(z_{1-\alpha} + z_{1-\beta}\right)^2}
                     {\ln^2\frac{(1+r)(1-r_0)}{(1-r)(1+r_0)}}
          + 3
    $$
