# 单样本均值优效性检验

对于高优指标 ($\delta > 0$)，统计学假设如下：

$$
\begin{align}
H_0 &: \mu - \mu_0 \leqslant \delta \\
H_1 &: \mu - \mu_0 \gt \delta
\end{align}
$$

对于低优指标 ($\delta < 0$)，统计学假设如下：

$$
\begin{align}
H_0 &: \mu - \mu_0 \geqslant \delta \\
H_1 &: \mu - \mu_0 \lt \delta
\end{align}
$$

样本均值用 $\hat{\mu}$ 表示，样本标准差用 $s$ 表示，总体标准差用 $\sigma$ 表示，以下推导过程在边界条件 $\mu - \mu_0 = \delta$ 下进行。

在 $H_0$ 成立时，可构建 $t$ 统计量：

$$
t = \frac{\hat{\mu} - \mu_0 - \delta}{s/\sqrt{n}} \sim t(n-1)
$$

在 $H_1$ 成立时，可构建 $t'$ 统计量：

$$
t' = \frac{\hat{\mu} - \mu_0 - \delta}{s/\sqrt{n}} \sim t\left(n-1, \frac{\mu-\mu_0-\delta}{\sigma/\sqrt{n}}\right)
$$

用 $T(x;v,\lambda)$ 表示自由度为 $v$，非中心参数为 $\lambda$ 的非中心 $t$ 分布的累积分布函数。

=== "高优指标"

    $$
    \text{Power}
    = P\left(t' > t_{1-\alpha, n-1}\right)
    = 1 - T\left(t_{1-\alpha, n-1}; n-1, \frac{\mu-\mu_0-\delta}{\sigma/\sqrt{n}}\right)
    $$

=== "低优指标"

    $$
    \text{Power}
    = P\left(t' < t_{\alpha, n-1}\right)
    = T\left(t_{\alpha, n-1}; n-1, \frac{\mu-\mu_0-\delta}{\sigma/\sqrt{n}}\right)
    $$
