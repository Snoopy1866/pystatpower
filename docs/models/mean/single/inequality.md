# 单样本均值差异性检验

对于双侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: \mu_1 = \mu_0 \\
H_1 &: \mu_1 \neq \mu_0
\end{align}
$$

对于左单侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: \mu_1 \geqslant \mu_0 \\
H_1 &: \mu_1 \lt \mu_0
\end{align}
$$

对于右单侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: \mu_1 \leqslant \mu_0 \\
H_1 &: \mu_1 \gt \mu_0
\end{align}
$$

样本均值用 $\hat{\mu}_1$ 表示，样本方差用 $S$ 表示。

以下推导过程在边界条件 $\mu_1 = \mu_0$ 下进行。

## Z 检验 {#z-test}

当总体方差 $\sigma^2$ 已知时，可使用 $Z$ 检验进行推导。

在 $H_0$ 成立时，可构建 $Z$ 统计量：

$$
Z = \frac{\hat{\mu}_1 - \mu_0}{\sigma/\sqrt{n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $Z'$ 统计量：

$$
Z' = \frac{\hat{\mu}_1 - \mu_0}{\sigma/\sqrt{n}} \sim N\left(\frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}}, 1\right)
$$

=== "双侧检验"

    $$
    \text{Power}
    = P\left(Z' > z_{1-\alpha}\right) + P\left(Z' < z_{\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}}\right)
        + \Phi\left(z_{\alpha} - \frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}}\right)
    $$

=== "$左单侧检验$"

    $$
    \text{Power}
    = P\left(Z' < z_{\alpha}\right)
    = \Phi\left(z_{\alpha} - \frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}}\right)
    = 1 - \Phi\left(z_{1-\alpha} + \frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}}\right)
    $$

=== "$右单侧检验$"

    $$
    \text{Power}
    = P\left(Z' > z_{1-\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}}\right)
    $$

对于单侧检验，可利用功效函数得到样本量的闭式解：

根据标准正态分布分位数的定义：

$$
z_{1-\alpha} \pm \frac{\mu_1 - \mu_0}{\sigma/\sqrt{n}} = z_\beta
$$

由上式可解出

$$
n = \frac{\left(z_{1-\alpha} + z_{1-\beta}\right)^2 \sigma^2}{\left(\mu_1 - \mu_0\right)^2}
$$

## t 检验 {#t-test}

当总体方差 $\sigma^2$ 未知时，可使用 $t$ 检验进行推导。

在 $H_0$ 成立时，可构建 $T$ 统计量：

$$
T = \frac{\hat{\mu}_1 - \mu_0}{S/\sqrt{n}} \sim t(n - 1)
$$

在 $H_1$ 成立时，可构建 $T'$ 统计量：

$$
T' = \frac{\hat{\mu}_1 - \mu_0}{S/\sqrt{n}} \sim t\left(n - 1, \frac{\mu_1 - \mu_0}{S/\sqrt{n}}\right)
$$

令 $F(x;v,\lambda)$ 为自由度为 $v$、非中心参数为 $\lambda$ 的非中心 $t$ 分布的累积分布函数。

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(T' > t_{1-\alpha}\right) + P\left(T' < t_{\alpha}\right) \\
    & = 1 - F\left(t_{1-\alpha, n - 1}; n - 1, \frac{\mu_1 - \mu_0}{S/\sqrt{n}}\right)
          + F\left(t_{\alpha, n - 1}; n - 1, \frac{\mu_1 - \mu_0}{S/\sqrt{n}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(T' < t_{\alpha}\right)
    = F\left(t_{\alpha, n - 1}; n - 1, \frac{\mu_1 - \mu_0}{S/\sqrt{n}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(T' > t_{1-\alpha}\right)
    = 1 - F\left(t_{1-\alpha, n - 1}; n - 1, \frac{\mu_1 - \mu_0}{S/\sqrt{n}}\right)
    $$
