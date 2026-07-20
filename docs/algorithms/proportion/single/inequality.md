# 单样本率差异性检验

样本率用 $\hat{p}$ 表示，总体率用 $p$ 表示。

对于双侧检验，统计学假设如下：

$$
\begin{align}
H_0 & : p = p_0 \\
H_1 & : p \neq p_0
\end{align}
$$

对于左单侧检验，统计学假设如下：

$$
\begin{align}
H_0 & : p \geqslant p_0 \\
H_1 & : p \lt p_0
\end{align}
$$

对于右单侧检验，统计学假设如下：

$$
\begin{align}
H_0 & : p \leqslant p_0 \\
H_1 & : p \gt p_0
\end{align}
$$

以下推导过程在边界条件 $p = p_0$ 下进行。

## _Exact Test_ {#exact-test#}

=== "双侧检验"

    在 $H_0$ 成立时，设 $X_0 \sim b(n, p_0)$，寻找满足以下条件的 $k_1$ 和 $k_2$：

    $$
    k_1 = \sup \left\{ k \;\middle|\; \sum_{i=0}^{k} P(X_0 = i) \leqslant \alpha/2 \right\}
    $$

    $$
    k_2 = \inf \left\{ k \;\middle|\; \sum_{i=k}^{n} P(X_0 = i) \leqslant \alpha/2 \right\}
    $$

    在 $H_1$ 成立时，设 $X_1 \sim b(n, p)$，检验效能为：

    $$
    \text{Power} = \sum_{i=0}^{k_1} P(X_1 = i) + \sum_{i=k_2}^{n} P(X_1 = i)
    $$

=== "左单侧检验"

    在 $H_0$ 成立时，设 $X_0 \sim b(n, p_0)$，寻找满足以下条件的 $k$：

    $$
    k = \sup \left\{ k \;\middle|\; \sum_{i=0}^{k} P(X_0 = i) \leqslant \alpha \right\}
    $$

    在 $H_1$ 成立时，设 $X_1 \sim b(n, p)$，检验效能为：

    $$
    \text{Power} = \sum_{i=0}^{k} P(X_1 = i)
    $$

=== "右单侧检验"

    在 $H_0$ 成立时，设 $X_0 \sim b(n, p_0)$，寻找满足以下条件的 $k$：

    $$
    k = \inf \left\{ k \;\middle|\; \sum_{i=k}^{n} P(X_0 = i) \leqslant \alpha \right\}
    $$

    在 $H_1$ 成立时，设 $X_1 \sim b(n, p)$，检验效能为：

    $$
    \text{Power} = \sum_{i=k}^{n} P(X_1 = i)
    $$

## _Z-Test Using S(P0)_ {#z-test-p0}

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}-p_0}{\sqrt{p_0(1-p_0)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}-p_0}{\sqrt{p_0(1-p_0)/n}} \sim N\left(\frac{p-p_0}{\sqrt{p_0(1-p_0)/n}}, \frac{p(1-p)}{p_0(1-p_0)}\right)
$$

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(z' > z_{1-\alpha/2} \right) + P\left(z' < z_{\alpha/2} \right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha/2} - \frac{p-p_0}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right)
          + \Phi\left(\frac{z_{\alpha/2} - \frac{p-p_0}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha/2}\sqrt{p_0(1-p_0)/n} - (p-p_0)}{\sqrt{p(1-p)/n}}\right)
          + \Phi\left(\frac{z_{\alpha/2}\sqrt{p_0(1-p_0)/n} - (p-p_0)}{\sqrt{p(1-p)/n}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
    \text{Power} = P\left(z' < z_{\alpha} \right)
                 = \Phi\left(\frac{z_{\alpha}\sqrt{p_0(1-p_0)/n} - (p-p_0)}{\sqrt{p(1-p)/n}}\right)
    $$

=== "右单侧检验"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha} \right)
                 = 1 - \Phi\left(\frac{z_{1-\alpha}\sqrt{p_0(1-p_0)/n} - (p-p_0)}{\sqrt{p(1-p)/n}}\right)
    $$

??? note "单侧检验样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    \frac{z_{1-\alpha} \sqrt{p_0(1-p_0)/n} \pm (p-p_0)}{\sqrt{p(1-p)/n}} = z_{\beta}
    $$

    可解出：

    $$
    n = \frac{\left(z_{1-\alpha}\sqrt{p_0(1-p_0)} + z_{1-\beta}\sqrt{p(1-p)}\right)^2}{\left(p-p_0\right)^2}
    $$

## _Z-Test Using S(P0) with Continuity Correction_ {#z-test-p0-cc}

在 [_Z-Test Using S(P0)_](#z-test-p0) 的基础上加入校正项 $c$：

定义：

$$
c =
\begin{cases}
\frac{1}{2n} & , \text{if } \left| \hat{p} - p_0 \right| \gt \frac{1}{2n} \\
0            & , \text{otherwise}
\end{cases}
$$

校正项的符号由检验方向决定，左侧检验时，校正项为 $+c$，右侧检验时，校正项为 $-c$。

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p} - p_0 \pm c}{\sqrt{p_0(1-p_0)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p} - p_0 \pm c}{\sqrt{p_0(1-p_0)/n}} \sim N\left(\frac{p - p_0 \pm c}{\sqrt{p_0(1-p_0)/n}}, \frac{p(1-p)}{p_0(1-p_0)}\right)
$$

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(z' > z_{1-\alpha/2} \right) + P\left(z' < z_{\alpha/2} \right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha/2} - \frac{p-p_0-c}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right)
          + \Phi\left(\frac{z_{\alpha/2} - \frac{p-p_0+c}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha/2}\sqrt{p_0(1-p_0)/n} - (p-p_0-c)}{\sqrt{p(1-p)/n}}\right)
          + \Phi\left(\frac{z_{\alpha/2}\sqrt{p_0(1-p_0)/n} - (p-p_0+c)}{\sqrt{p(1-p)/n}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
    \text{Power} = P\left(z' < z_{\alpha} \right)
                 = \Phi\left(\frac{z_{\alpha}\sqrt{p_0(1-p_0)/n} - (p-p_0+c)}{\sqrt{p(1-p)/n}}\right)
    $$

=== "右单侧检验"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha} \right)
                 = 1 - \Phi\left(\frac{z_{1-\alpha}\sqrt{p_0(1-p_0)/n} - (p-p_0-c)}{\sqrt{p(1-p)/n}}\right)
    $$

## _Z-Test Using S(Phat)_ {#z-test-phat}

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}-p_0}{\sqrt{\hat{p}(1-\hat{p})/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量:

$$
z' = \frac{\hat{p}-p_0}{\sqrt{\hat{p}(1-\hat{p})/n}} \sim N\left(\frac{p-p_0}{\sqrt{p(1-p)/n}}, 1\right)
$$

=== "双侧检验"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha/2} \right) + P\left(z' < z_{\alpha/2} \right)
                 = 1 - \Phi\left(z_{1-\alpha/2} - \frac{p-p_0}{\sqrt{p(1-p)/n}}\right)
                     + \Phi\left(z_{\alpha/2} - \frac{p-p_0}{\sqrt{p(1-p)/n}}\right)
    $$

=== "左单侧检验"

    $$
    \text{Power} = P\left(z' < z_{\alpha} \right)
                 = \Phi\left(z_{\alpha} - \frac{p-p_0}{\sqrt{p(1-p)/n}}\right)
    $$

=== "右单侧检验"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha} \right)
                 = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0}{\sqrt{p(1-p)/n}}\right)
    $$

??? note "单侧检验样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    z_{1-\alpha} \pm \frac{p-p_0}{\sqrt{p(1-p)/n}} = z_{\beta}
    $$

    可解出：

    $$
    n = \frac{\left(z_{1-\alpha}+z_{1-\beta}\right)^2 p(1-p)}{\left(p-p_0\right)^2}
    $$

## _Z-Test Using S(Phat) with Continuity Correction_ {#z-test-phat-cc}

在 [_Z-Test Using S(Phat)_](#z-test-phat) 的基础上加入校正项 $c$：

定义：

$$
c =
\begin{cases}
\frac{1}{2n} & , \text{if } \left| \hat{p} - p_0 \right| \gt \frac{1}{2n} \\
0            & , \text{otherwise}
\end{cases}
$$

校正项的符号由检验方向决定，左侧检验时，校正项为 $+c$，右侧检验时，校正项为 $-c$。

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p} - p_0 \pm c}{\sqrt{\hat{p}(1-\hat{p})/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p} - p_0 \pm c}{\sqrt{\hat{p}(1-\hat{p})/n}} \sim N\left(\frac{p - p_0 \pm c}{\sqrt{p(1-p)/n}}, 1\right)
$$

=== "双侧检验"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha/2} \right) + P\left(z' < z_{\alpha/2} \right)
                 = 1 - \Phi\left(z_{1-\alpha/2} - \frac{p-p_0-c}{\sqrt{p(1-p)/n}}\right)
                     + \Phi\left(z_{\alpha/2} - \frac{p-p_0+c}{\sqrt{p(1-p)/n}}\right)
    $$

=== "左单侧检验"

    $$
    \text{Power} = P\left(z' < z_{\alpha} \right)
                 = \Phi\left(z_{\alpha} - \frac{p-p_0+c}{\sqrt{p(1-p)/n}}\right)
    $$

=== "右单侧检验"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha} \right)
                 = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0-c}{\sqrt{p(1-p)/n}}\right)
    $$

!!! quote "参考文献"

    1. JH Z. Zar JH. Dichotomous variables[J]. Biostatistical Analysis 5th ed. Upper Saddle River, NJ: Prentice-Hall, 2010: 557-558.
    2. Chow S C, Shao J, Wang H, et al. Sample size calculations in clinical research[M]. chapman and hall/CRC, 2017.
    3. Ryan, Thomas. (2013). Sample Size Determination and Power. Sample Size Determination and Power. 10.1002/9781118439241.
