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


两样本均值分别用 $\hat{\mu}_1$ 和 $\hat{\mu}_2$ 表示，两样本方差分别用 $S_1$ 和 $S_2$ 表示。

$$
E(\hat{\mu}_1 - \hat{\mu}_2) = \mu_1 - \mu_2, \ \ Var(\hat{\mu}_1 - \hat{\mu}_2) = \frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}
$$

以下推导过程在边界条件 $\mu_1 = \mu_2$ 下进行。

## Z 检验 {#z-test}

大样本时，可使用 $Z$ 检验进行推导。

### 方差相等 {#z-test-equal-variance}

在 $H_0$ 成立时，可构建 $Z$ 统计量：

$$
Z = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $Z'$ 统计量：

$$
Z' = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}} \sim N\left(\frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}, 1\right)
$$

=== "双侧检验"

    $$
    \text{Power}
    = P\left(Z' > z_{1-\alpha}\right) + P\left(Z' < z_{\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
        + \Phi\left(z_{\alpha} - \frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    $$

=== "$左单侧检验$"

    $$
    \text{Power}
    = P\left(Z' < z_{\alpha}\right)
    = \Phi\left(z_{\alpha} - \frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    = 1 - \Phi\left(z_{1-\alpha} + \frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    $$

=== "$右单侧检验$"

    $$
    \text{Power}
    = P\left(Z' > z_{1-\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{\mu_1 - \mu_2}{\sigma\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    $$

对于单侧检验，可利用功效函数得到样本量的闭式解：

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


### 方差不相等 {#z-test-unequal-variance}


在 $H_0$ 成立时，可构建 $Z$ 统计量：

$$
Z = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $Z'$ 统计量：

$$
Z' = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}} \sim N\left(\frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}, 1\right)
$$

=== "$双侧检验$"

    $$
    \text{Power}
    = P\left(Z' > z_{1-\alpha}\right) + P\left(Z' < z_{\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}\right)
        + \Phi\left(z_{\alpha} - \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}\right)
    $$

=== "$左单侧检验$"

    $$
    \text{Power}
    = P\left(Z' < z_{\alpha}\right)
    = \Phi\left(z_{\alpha} - \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}\right)
    = 1 - \Phi\left(z_{1-\alpha} + \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}\right)
    $$

=== "$右单侧检验$"

    $$
    \text{Power}
    = P\left(Z' > z_{1-\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{\mu_1 - \mu_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}\right)
    $$

对于单侧检验，可利用功效函数得到样本量的闭式解：

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

## t 检验 {#t-test}

小样本时，可使用 $t$ 检验进行推导。

### 方差相等 {#t-test-equal-variance}

当两总体方差相等时，即 $\sigma_1^2 = \sigma_2^2$ 时，可将样本方差合并，计算合并方差 $S_c^2$：

$$
S_c^2 = \frac{(n_1 - 1)S_1^2 + (n_2 - 1)S_2^2}{n_1 + n_2 - 2}
$$

在 $H_0$ 成立时，可构建 $T$ 统计量：

$$
T = \frac{\hat{\mu}_1 - \hat{\mu}_2}{S_c\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}} \sim t(n_1 + n_2 - 2)
$$

在 $H_1$ 成立时，可构建 $T'$ 统计量：

$$
T' = \frac{\hat{\mu}_1 - \hat{\mu}_2}{S_c\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}
   \sim t\left(n_1 + n_2 - 2, \frac{\mu_1 - \mu_2}{S_c\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
$$

令 $F(x;v,\lambda)$ 为自由度为 $v$、非中心参数为 $\lambda$ 的非中心 $t$ 分布的累积分布函数。

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(T' > t_{1-\alpha}\right) + P\left(T' < t_{\alpha}\right) \\
    & = 1 - F\left(t_{1-\alpha, n_1 + n_2 - 2}; n_1 + n_2 - 2, \frac{\mu_1 - \mu_2}{S_c\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
          + F\left(t_{\alpha, n_1 + n_2 - 2}; n_1 + n_2 - 2, \frac{\mu_1 - \mu_2}{S_c\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(T' < t_{\alpha}\right)
    = F\left(t_{\alpha, n_1 + n_2 - 2}; n_1 + n_2 - 2, \frac{\mu_1 - \mu_2}{S_c\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(T' > t_{1-\alpha}\right)
    = 1 - F\left(t_{1-\alpha, n_1 + n_2 - 2}; n_1 + n_2 - 2, \frac{\mu_1 - \mu_2}{S_c\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}\right)
    $$

### 方差不相等 {#t-test-unequal-variance}

当两总体方差不相等时，即 $\sigma_1^2 \ne \sigma_2^2$ 时，可使用以下近似 $t$ 检验进行推导。

#### Satterthwaite 近似 t 检验 {#t-test-unequal-variance-satterthwaite}

在 $H_0$ 成立时，可构建 $T$ 统计量：

$$
T = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}} \sim t(v')
$$

其中：

$$
v' = \frac{\left(\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}\right)^2}{\frac{S_1^4}{n_1^2(n_1 - 1)} + \frac{S_2^4}{n_2^2(n_2 - 1)}}
$$

在 $H_1$ 成立时，可构建 $T'$ 统计量：

$$
T' = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}
   \sim t\left(v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}\right)
$$

令 $F(x;v,\lambda)$ 为自由度为 $v$、非中心参数为 $\lambda$ 的非中心 $t$ 分布的累积分布函数。

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(T' > t_{1-\alpha}\right) + P\left(T' < t_{\alpha}\right) \\
    & = 1 - F\left(t_{1-\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}\right)
          + F\left(t_{\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(T' < t_{\alpha}\right)
    = F\left(t_{\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(T' > t_{1-\alpha}\right)
    = 1 - F\left(t_{1-\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}\right)
    $$

#### Welch 近似 t 检验 {#t-test-unequal-variance-welch}

在 $H_0$ 成立时，可构建 $T$ 统计量：

$$
T = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}} \sim t(v')
$$

其中：

$$
v' = \frac{\left(\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}\right)^2}{\frac{S_1^4}{n_1^2(n_1 + 1)} + \frac{S_2^4}{n_2^2(n_2 + 1)}} - 2
$$

在 $H_1$ 成立时，可构建 $T'$ 统计量：

$$
T' = \frac{\hat{\mu}_1 - \hat{\mu}_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}
   \sim t\left(v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}\right)
$$

令 $F(x;v,\lambda)$ 为自由度为 $v$、非中心参数为 $\lambda$ 的非中心 $t$ 分布的累积分布函数。

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(T' > t_{1-\alpha}\right) + P\left(T' < t_{\alpha}\right) \\
    & = 1 - F\left(t_{1-\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}\right)
          + F\left(t_{\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(T' < t_{\alpha}\right)
    = F\left(t_{\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(T' > t_{1-\alpha}\right)
    = 1 - F\left(t_{1-\alpha, v'}; v', \frac{\mu_1 - \mu_2}{\sqrt{\frac{S_1^2}{n_1} + \frac{S_2^2}{n_2}}}\right)
    $$
