# 两独立样本均值差异性检验

对于双侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: \mu_1 = \mu_2 \\
H_1 &: \mu_1 \neq \mu_2
\end{align}
$$

对于左单侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: \mu_1 \geqslant \mu_2 \\
H_1 &: \mu_1 \lt \mu_2
\end{align}
$$

对于右单侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: \mu_1 \leqslant \mu_2 \\
H_1 &: \mu_1 \gt \mu_2
\end{align}
$$

两样本均值分别用 $\hat{\mu}_1$ 和 $\hat{\mu}_2$ 表示，两样本方差分别用 $s_1$ 和 $s_2$ 表示，两总体方差分别用 $\sigma_1$ 和 $\sigma_2$ 表示。

以下推导过程在边界条件 $\mu_1 = \mu_2$ 下进行。

## _z_ 检验 {#z-test}

### 假设两组方差相等 {#z-test-equal-var}

令 $\sigma$ = $\sigma_1$ = $\sigma_2$，则：

$$
\operatorname{SD}(\hat{\mu}_1 - \hat{\mu}_2) = \sigma \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}
$$

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}} \sim N\left(\frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}, 1\right)
$$

=== "双侧检验"

    $$
      \text{Power}
    = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right)
    = 1 - \Phi\left(z_{1-\alpha/2} - \frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
        + \Phi\left(z_{\alpha/2} - \frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(z' < z_{\alpha}\right)
    = \Phi\left(z_{\alpha} - \frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    = 1 - \Phi\left(z_{1-\alpha} + \frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(z' > z_{1-\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    $$

??? note "单侧检验样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    z_{1-\alpha} \pm \frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}} = z_\beta
    $$

    设 $n_1 = kn_2$，由上式可解出

    $$
    n_2 = \frac{\left(z_{1-\alpha} + z_{1-\beta}\right)^2 \sigma^2 \left(\frac{1}{k} + 1\right)}{\left(\mu_1 - \mu_2\right)^2}
    $$

    $$
    n_1 = k n_2
    $$

### 假设两组方差不等 {#z-test-unequal-var}

$$
\operatorname{SD}(\hat{\mu}_1 - \hat{\mu}_2) = \sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}
$$

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}} \sim N\left(\frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}, 1\right)
$$

=== "双侧检验"

    $$
      \text{Power}
    = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right)
    = 1 - \Phi\left(z_{1-\alpha/2} - \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}\right)
        + \Phi\left(z_{\alpha/2} - \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}\right)
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(z' < z_{\alpha}\right)
    = \Phi\left(z_{\alpha} - \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}\right)
    = 1 - \Phi\left(z_{1-\alpha} + \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(z' > z_{1-\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}\right)
    $$

??? note "单侧检验样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    z_{1-\alpha} \pm \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}} = z_\beta
    $$

    设 $n_1 = kn_2$，由上式可解出

    $$
    n_2 = \frac{\left(z_{1-\alpha} + z_{1-\beta}\right)^2 \left(\frac{\sigma_1^2}{k} + \sigma_2^2\right)}{\left(\mu_1 - \mu_2\right)^2}
    $$

    $$
    n_1 = k n_2
    $$

## _t_ 检验 {#t-test}

### 假设两组方差相等 {#t-test-equal-var}

当两组总体方差相等时，即 $\sigma_1^2 = \sigma_2^2$ 时，可计算合并方差 $s_c^2$ ：

$$
s_c^2 = \frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2}
$$

$$
\operatorname{SD}(\hat{\mu}_1 - \hat{\mu}_2) = s_c \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}
$$

在 $H_0$ 成立时，可构建 $t$ 统计量：

$$
t = \frac{\hat{\mu}_1 - \hat{\mu}_2}{s_c\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}} \sim t(n_1 + n_2 - 2)
$$

在 $H_1$ 成立时，可构建 $t'$ 统计量：

$$
t' = \frac{\hat{\mu}_1 - \hat{\mu}_2}{s_c\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}
     \sim t\left(n_1 + n_2 - 2, \frac{\mu_1 - \mu_2}{\sigma \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
$$

令 $T(x;v,\lambda)$ 为自由度为 $v$，非中心参数为 $\lambda$ 的非中心 $t$ 分布的累积分布函数。

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(t' > t_{1-\alpha/2}\right) + P\left(t' < t_{\alpha/2}\right) \\
    & = 1 - T\left(t_{1-\alpha/2, n_1 + n_2 - 2}; n_1 + n_2 - 2, \frac{\mu_1 - \mu_2}{\sigma \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
          + T\left(t_{\alpha/2, n_1 + n_2 - 2}; n_1 + n_2 - 2, \frac{\mu_1 - \mu_2}{\sigma \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(t' < t_{\alpha}\right)
    = T\left(t_{\alpha, n_1 + n_2 - 2}; n_1 + n_2 - 2, \frac{\mu_1 - \mu_2}{\sigma \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(t' > t_{1-\alpha}\right)
    = 1 - T\left(t_{1-\alpha, n_1 + n_2 - 2}; n_1 + n_2 - 2, \frac{\mu_1 - \mu_2}{\sigma \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    $$

### 假设两组方差不等 {#t-test-unequal-var}

$$
\operatorname{SD}(\hat{\mu}_1 - \hat{\mu}_2) = \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}
$$

当两总体方差不相等时，即 $\sigma_1^2 \ne \sigma_2^2$ 时，可使用以下近似 $t$ 检验进行推导。

#### _Welch_ 近似 _t_ 检验 {#t-test-unequal-var-welch}

在 $H_0$ 成立时，可构建 $t$ 统计量：

$$
t = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}} \sim t(v')
$$

其中：

$$
v' = \frac{\left(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}\right)^2}{\frac{s_1^4}{n_1^2(n_1 + 1)} + \frac{s_2^4}{n_2^2(n_2 + 1)}} - 2
$$

在 $H_1$ 成立时，可构建 $t'$ 统计量：

$$
t' = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}
     \sim t\left(v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}\right)
$$

令 $T(x;v,\lambda)$ 为自由度为 $v$，非中心参数为 $\lambda$ 的非中心 $t$ 分布的累积分布函数。

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(t' > t_{1-\alpha/2}\right) + P\left(t' < t_{\alpha/2}\right) \\
    & = 1 - T\left(t_{1-\alpha/2, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}\right)
          + T\left(t_{\alpha/2, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(t' < t_{\alpha}\right)
    = T\left(t_{\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(t' > t_{1-\alpha}\right)
    = 1 - T\left(t_{1-\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}\right)
    $$

#### _Satterthwaite_ 近似 _t_ 检验 {#t-test-unequal-var-satterthwaite}

在 $H_0$ 成立时，可构建 $t$ 统计量：

$$
t = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}} \sim t(v')
$$

其中：

$$
v' = \frac{\left(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}\right)^2}{\frac{s_1^4}{n_1^2(n_1 - 1)} + \frac{s_2^4}{n_2^2(n_2 - 1)}}
$$

在 $H_1$ 成立时，可构建 $t'$ 统计量：

$$
t' = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}
     \sim t\left(v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}\right)
$$

令 $T(x;v,\lambda)$ 为自由度为 $v$，非中心参数为 $\lambda$ 的非中心 $t$ 分布的累积分布函数。

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(t' > t_{1-\alpha/2}\right) + P\left(t' < t_{\alpha/2}\right) \\
    & = 1 - T\left(t_{1-\alpha/2, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}\right)
          + T\left(t_{\alpha/2, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(t' < t_{\alpha}\right)
    = T\left(t_{\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(t' > t_{1-\alpha}\right)
    = 1 - T\left(t_{1-\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}\right)
    $$

!!! quote "参考文献"

    1. JH Z. Zar JH. Dichotomous variables[J]. Biostatistical Analysis 5th ed. Upper Saddle River, NJ: Prentice-Hall, 2010: 557-558.
    2. Chow S C, Shao J, Wang H, et al. Sample size calculations in clinical research[M]. chapman and hall/CRC, 2017.
