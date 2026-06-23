# 单样本均值差异性检验

对于双侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: \mu = \mu_0 \\
H_1 &: \mu \neq \mu_0
\end{align}
$$

对于左单侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: \mu \geqslant \mu_0 \\
H_1 &: \mu \lt \mu_0
\end{align}
$$

对于右单侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: \mu \leqslant \mu_0 \\
H_1 &: \mu \gt \mu_0
\end{align}
$$

样本均值用 $\hat{\mu}$ 表示，样本方差用 $s$ 表示，总体方差用 $\sigma$ 表示。

以下推导过程在边界条件 $\mu = \mu_0$ 下进行。

## _z_ 检验 {#z-test}

当总体方差 $\sigma^2$ 已知时，可使用 $z$ 检验进行推导。

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{\mu} - \mu_0}{\sigma/\sqrt{n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{\mu} - \mu_0}{\sigma/\sqrt{n}} \sim N\left(\frac{\mu - \mu_0}{\sigma/\sqrt{n}}, 1\right)
$$

=== "双侧检验"

    $$
      \text{Power}
    = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right)
    = 1 - \Phi\left(z_{1-\alpha/2} - \frac{\mu - \mu_0}{\sigma/\sqrt{n}}\right) + \Phi\left(z_{\alpha/2} - \frac{\mu - \mu_0}{\sigma/\sqrt{n}}\right)
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(z' < z_{\alpha}\right)
    = \Phi\left(z_{\alpha} - \frac{\mu - \mu_0}{\sigma/\sqrt{n}}\right)
    = 1 - \Phi\left(z_{1-\alpha} + \frac{\mu - \mu_0}{\sigma/\sqrt{n}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(z' > z_{1-\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{\mu - \mu_0}{\sigma/\sqrt{n}}\right)
    $$

??? note "单侧检验样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    z_{1-\alpha} \pm \frac{\mu - \mu_0}{\sigma/\sqrt{n}} = z_\beta
    $$

    由上式可解出

    $$
    n = \frac{\left(z_{1-\alpha} + z_{1-\beta}\right)^2 \sigma^2}{\left(\mu - \mu_0\right)^2}
    $$

## _t_ 检验 {#t-test}

当总体方差 $\sigma^2$ 未知时，可使用 $t$ 检验进行推导。

在 $H_0$ 成立时，可构建 $t$ 统计量：

$$
t = \frac{\hat{\mu} - \mu_0}{s/\sqrt{n}} \sim t(n - 1)
$$

在 $H_1$ 成立时，可构建 $t'$ 统计量：

$$
t' = \frac{\hat{\mu} - \mu_0}{s/\sqrt{n}} \sim t\left(n - 1, \frac{\mu - \mu_0}{\sigma/\sqrt{n}}\right)
$$

令 $T(x;v,\lambda)$ 为自由度为 $v$，非中心参数为 $\lambda$ 的非中心 $t$ 分布的累积分布函数。

=== "双侧检验"

    $$
        \text{Power}
    = P\left(t' > t_{1-\alpha/2}\right) + P\left(t' < t_{\alpha/2}\right)
    = 1 - T\left(t_{1-\alpha/2, n - 1}; n - 1, \frac{\mu - \mu_0}{\sigma/\sqrt{n}}\right)
          + T\left(t_{\alpha/2, n - 1}; n - 1, \frac{\mu - \mu_0}{\sigma/\sqrt{n}}\right)
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(t' < t_{\alpha}\right)
    = T\left(t_{\alpha, n - 1}; n - 1, \frac{\mu - \mu_0}{\sigma/\sqrt{n}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(t' > t_{1-\alpha}\right)
    = 1 - T\left(t_{1-\alpha, n - 1}; n - 1, \frac{\mu - \mu_0}{\sigma/\sqrt{n}}\right)
    $$
