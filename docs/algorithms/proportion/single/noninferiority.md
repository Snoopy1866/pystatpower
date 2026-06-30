# 单样本率非劣效检验

样本率用 $\hat{p}$ 表示，总体率用 $p$ 表示，非劣界值用 $\delta$ 表示。

对于高优指标（$\delta < 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p - p_0 \leqslant \delta \\
H_1 &: p - p_0 \gt \delta
\end{align}
$$

对于低优指标（$\delta > 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p - p_0 \geqslant \delta \\
H_1 &: p - p_0 \lt \delta
\end{align}
$$

以下推导过程在边界条件 $p - p_0 = \delta$ 下进行。

## _z-test using s(p0)_ {#z-test-p0}

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}-p_0-\delta}{\sqrt{(p_0+\delta)(1-p_0-\delta)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}-p_0-\delta}{\sqrt{(p_0+\delta)(1-p_0-\delta)/n}} \sim N\left(\frac{p-p_0-\delta}{\sqrt{(p_0+\delta)(1-p_0-\delta)/n}}, \frac{p(1-p)}{(p_0+\delta)(1-p_0-\delta)}\right)
$$

=== "高优指标"

    $$
    \begin{align}
        \text{Power}
    & = \operatorname{Pr}(z' > z_{1-\alpha}) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p-p_0-\delta}{\sqrt{(p_0+\delta)(1-p_0-\delta)/n}}}{\frac{\sqrt{p(1-p)}}{\sqrt{(p_0+\delta)(1-p_0-\delta)}}}\right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta)(1-p_0-\delta)} - (p-p_0-\delta)\sqrt{n}}{\sqrt{p(1-p)}}\right)
    \end{align}
    $$

=== "低优指标"

    $$
    \begin{align}
        \text{Power}
    & = \operatorname{Pr}(z' < z_{\alpha}) \\
    & = \Phi\left(\frac{z_{\alpha} - \frac{p-p_0-\delta}{\sqrt{(p_0+\delta)(1-p_0-\delta)/n}}}{\frac{\sqrt{p(1-p)}}{\sqrt{(p_0+\delta)(1-p_0-\delta)}}}\right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta)(1-p_0-\delta)} + (p-p_0-\delta)\sqrt{n}}{\sqrt{p(1-p)}}\right)
    \end{align}
    $$

??? note "样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    \frac{z_{1-\alpha}\sqrt{(p_0+\delta)(1-p_0-\delta)} \pm (p-p_0-\delta)\sqrt{n}}{\sqrt{p(1-p)}} = z_{\beta}
    $$

    可解出：

    $$
    n = \frac{\left[z_{1-\alpha}\sqrt{(p_0+\delta)(1-p_0-\delta)} + z_{1-\beta}\sqrt{p(1-p)}\right]^2}{\left(p-p_0-\delta\right)^2}
    $$

## _z-test using s(p0) with continuity correction_ {#z-test-p0-cc}

在 [_z-test using s(p0)_](#z-test-p0) 的基础上加入校正项 $c$：

$$
c =
\begin{cases}
- \frac{1}{2n} & , \text{if } p \gt p_0 + \delta \\
  \frac{1}{2n} & , \text{if } p \lt p_0 + \delta \\
  0            & , \text{if } \left| p - p_0 - \delta \right| \leqslant \frac{1}{2n}
\end{cases}
$$

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}-p_0-\delta+c}{\sqrt{(p_0+\delta)(1-p_0-\delta)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}-p_0-\delta+c}{\sqrt{(p_0+\delta)(1-p_0-\delta)/n}} \sim N\left(\frac{p-p_0-\delta+c}{\sqrt{(p_0+\delta)(1-p_0-\delta)/n}}, \frac{p(1-p)}{(p_0+\delta)(1-p_0-\delta)}\right)
$$

=== "高优指标"

    $$
    \begin{align}
        \text{Power}
    & = \operatorname{Pr}(z' > z_{1-\alpha}) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p-p_0-\delta+c}{\sqrt{(p_0+\delta)(1-p_0-\delta)/n}}}{\frac{\sqrt{p(1-p)}}{\sqrt{(p_0+\delta)(1-p_0-\delta)}}}\right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta)(1-p_0-\delta)} - (p-p_0-\delta+c)\sqrt{n}}{\sqrt{p(1-p)}}\right)
    \end{align}
    $$

=== "低优指标"

    $$
    \begin{align}
        \text{Power}
    & = \operatorname{Pr}(z' < z_{\alpha}) \\
    & = \Phi\left(\frac{z_{\alpha} - \frac{p-p_0-\delta+c}{\sqrt{(p_0+\delta)(1-p_0-\delta)/n}}}{\frac{\sqrt{p(1-p)}}{\sqrt{(p_0+\delta)(1-p_0-\delta)}}}\right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta)(1-p_0-\delta)} + (p-p_0-\delta+c)\sqrt{n}}{\sqrt{p(1-p)}}\right)
    \end{align}
    $$

## _z-test using s(phat)_ {#z-test-phat}

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}-p_0-\delta}{\sqrt{p(1-p)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}-p_0-\delta}{\sqrt{p(1-p)/n}} \sim N\left(\frac{p-p_0-\delta}{\sqrt{p(1-p)/n}}, 1\right)
$$

=== "高优指标"

    $$
    \text{Power} = \operatorname{Pr}(z' > z_{1-\alpha}) = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta}{\sqrt{p(1-p)/n}}\right)
    $$

=== "低优指标"

    $$
    \text{Power} = \operatorname{Pr}(z' < z_{\alpha}) = \Phi\left(z_{\alpha} - \frac{p-p_0-\delta}{\sqrt{p(1-p)/n}}\right) = 1 - \Phi\left(z_{1-\alpha} + \frac{p-p_0-\delta}{\sqrt{p(1-p)/n}}\right)
    $$

??? note "样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    z_{1-\alpha} \pm \frac{p-p_0-\delta}{\sqrt{p(1-p)/n}} = z_{\beta}
    $$

    可解出：

    $$
    n = \frac{\left(z_{1-\alpha}+z_{1-\beta}\right)^2 p(1-p)}{\left(p-p_0-\delta\right)^2}
    $$

## _z-test using s(phat) with continuity correction_ {#z-test-phat-cc}

在 [_z-test using s(phat)_](#z-test-phat) 的基础上加入校正项 $c$：

$$
c =
\begin{cases}
- \frac{1}{2n} & , \text{if } p \gt p_0 + \delta \\
  \frac{1}{2n} & , \text{if } p \lt p_0 + \delta \\
  0            & , \text{if } \left| p - p_0 - \delta \right| \leqslant \frac{1}{2n}
\end{cases}
$$

在 $H_0$ 成立时，构建 $z$ 统计量：

$$
z = \frac{\hat{p}-p_0-\delta+c}{\sqrt{p(1-p)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}-p_0-\delta+c}{\sqrt{p(1-p)/n}} \sim N\left(\frac{p-p_0-\delta+c}{\sqrt{p(1-p)/n}}, 1\right)
$$

=== "高优指标"

    $$
    \text{Power} = \operatorname{Pr}(z' > z_{1-\alpha}) = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta+c}{\sqrt{p(1-p)/n}}\right)
    $$

=== "低优指标"

    $$
    \text{Power} = \operatorname{Pr}(z' < z_{\alpha}) = \Phi\left(z_{\alpha} - \frac{p-p_0-\delta+c}{\sqrt{p(1-p)/n}}\right) = 1 - \Phi\left(z_{1-\alpha} + \frac{p-p_0-\delta+c}{\sqrt{p(1-p)/n}}\right)
    $$
