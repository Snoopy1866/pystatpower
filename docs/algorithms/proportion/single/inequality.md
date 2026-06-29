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

## _z-test using s(p0)_ {#z-test-p0}

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
    \text{Power} = P\left(z' > z_{1-\alpha/2} \right) + P\left(z' < z_{\alpha/2} \right)
                 = 1 - \Phi\left(\frac{z_{1-\alpha/2} - \frac{p-p_0}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right)
                     + \Phi\left(\frac{z_{\alpha/2} - \frac{p-p_0}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right)
    $$

=== "左单侧检验"

    $$
    \text{Power} = P\left(z' < z_{\alpha} \right)
                 = \Phi\left(\frac{z_{\alpha} - \frac{p-p_0}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right)
    $$

=== "右单侧检验"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha} \right)
                 = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p-p_0}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right)
    $$

??? note "单侧检验样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    \frac{z_{1-\alpha} \pm \frac{p-p_0}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}} = \frac{z_{1-\alpha} \sqrt{p_0(1-p_0)} \pm \sqrt{n}(p_1-p_0)}{\sqrt{p(1-p)}} = z_{\beta}
    $$

    可解出：

    $$
    n = \frac{\left(z_{1-\alpha}\sqrt{p_0(1-p_0)} + z_{1-\beta}\sqrt{p(1-p)}\right)^2}{\left(p-p_0\right)^2}
    $$

## _z-test using s(p0) with continuity correction_ {#z-test-p0-cc}

在 [_z-test using s(p0)_](#z-test-p0) 的基础上加入校正项 $c$：

$$
c =
\begin{cases}
- \frac{1}{2n} & , \text{if } \hat{p} \gt p_0 \\
  \frac{1}{2n} & , \text{if } \hat{p} \lt p_0 \\
  0            & , \text{if } \left| \hat{p} - p_0 \right| \leqslant \frac{1}{2n}
\end{cases}
$$

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}-p_0+c}{\sqrt{p_0(1-p_0)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}-p_0+c}{\sqrt{p_0(1-p_0)/n}} \sim N\left(\frac{p-p_0+c}{\sqrt{p_0(1-p_0)/n}}, \frac{p(1-p)}{p_0(1-p_0)}\right)
$$

=== "双侧检验"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha/2} \right) + P\left(z' < z_{\alpha/2} \right)
                 = 1 - \Phi\left(\frac{z_{1-\alpha/2} - \frac{p-p_0+c}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right)
                     + \Phi\left(\frac{z_{\alpha/2} - \frac{p-p_0+c}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right)
    $$

=== "左单侧检验"

    $$
    \text{Power} = P\left(z' < z_{\alpha} \right)
                 = \Phi\left(\frac{z_{\alpha} - \frac{p-p_0+c}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right)
    $$

=== "右单侧检验"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha} \right)
                 = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p-p_0+c}{\sqrt{p_0(1-p_0)/n}}}{\sqrt{\frac{p(1-p)}{p_0(1-p_0)}}}\right)
    $$

## _z-test using s(phat)_ {#z-test-phat}

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

## _z-test using s(phat) with continuity correction_ {#z-test-phat-cc}

在 [_z-test using s(phat)_](#z-test-phat) 的基础上加入校正项 $c$：

$$
c =
\begin{cases}
- \frac{1}{2n} & , \text{if } \hat{p} \gt p_0 \\
  \frac{1}{2n} & , \text{if } \hat{p} \lt p_0 \\
  0            & , \text{if } \left| \hat{p} - p_0 \right| \le \frac{1}{2n}
\end{cases}
$$

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}-p_0+c}{\sqrt{\hat{p}(1-\hat{p})/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}-p_0+c}{\sqrt{\hat{p}(1-\hat{p})/n}} \sim N\left(\frac{p-p_0+c}{\sqrt{p(1-p)/n}}, 1\right)
$$

=== "双侧检验"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha/2} \right) + P\left(z' < z_{\alpha/2} \right)
                 = 1 - \Phi\left(z_{1-\alpha/2} - \frac{p-p_0+c}{\sqrt{p(1-p)/n}}\right)
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
                 = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0+c}{\sqrt{p(1-p)/n}}\right)
    $$
