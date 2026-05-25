# 单样本率非劣效检验

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

$\delta$ 为非劣效界值，样本比例用 $\hat{p}$ 表示。

$$
\operatorname{E}(\hat{p}) = p
$$

以下推导过程在边界条件 $p - p_0 = \delta$ 下进行。


## Z-test using S(P0) {#z-test-p0}

在 $H_0$ 成立时，使用 $p_0$ 计算样本比例 $\hat{p}$ 的方差：

$$
\operatorname{Var}(\hat{p}) = \frac{p_0(1-p_0)}{n}
$$

??? warning "注意"
    这一传统做法并未考虑 $\delta$ 对样本比例方差造成的偏移。
    
    事实上，在 $H_0$ 成立时，即 $p - p_0 = \delta$ 时，$\hat{p}$ 的方差公式如下：

    $$
    \operatorname{Var}(\hat{p}) = \frac{(p_0+\delta)\left(1-(p_0+\delta)\right)}{n}
    $$

构建 $z$ 统计量：

$$
z = \frac{\hat{p}-p_0-\delta}{\sqrt{p_0(1-p_0)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}-p_0-\delta}{\sqrt{p_0(1-p_0)/n}} \sim N\left(\frac{p-p_0-\delta}{\sqrt{p_0(1-p_0)/n}}, \frac{\sqrt{p(1-p)/n}}{\sqrt{p_0(1-p_0)/n}}\right)
$$

=== "$\delta < 0$"

    $$
    \text{Power}
    = \operatorname{Pr}(z' > z_{1-\alpha})
    = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p-p_0-\delta}{\sqrt{p_0(1-p_0)/n}}}{\frac{\sqrt{p(1-p)/n}}{\sqrt{p_0(1-p_0)/n}}}\right)
    = 1 - \Phi\left(\frac{z_{1-\alpha}\sqrt{p_0(1-p_0)} - (p-p_0-\delta)\sqrt{n}}{\sqrt{p(1-p)}}\right)
    $$

=== "$\delta > 0$"

    $$
    \text{Power}
    = \operatorname{Pr}(z' < z_{\alpha})
    = \Phi\left(\frac{z_{\alpha} - \frac{p-p_0-\delta}{\sqrt{p_0(1-p_0)/n}}}{\frac{\sqrt{p(1-p)/n}}{\sqrt{p_0(1-p_0)/n}}}\right)
    = 1 - \Phi\left(\frac{z_{1-\alpha}\sqrt{p_0(1-p_0)} + (p-p_0-\delta)\sqrt{n}}{\sqrt{p(1-p)}}\right)
    $$

根据标准正态分布分位数的定义：

$$
\frac{z_{1-\alpha}\sqrt{p_0(1-p_0)} \pm (p-p_0-\delta)\sqrt{n}}{\sqrt{p(1-p)/n}} = z_{\beta}
$$

可解出：

$$
n = \frac{\left[z_{1-\alpha}\sqrt{p_0(1-p_0)} + z_{1-\beta}\sqrt{p(1-p)}\right]^2}{\left(p-p_0-\delta\right)^2}
$$


## Z-test using S(P0) 连续性校正 {#z-test-p0-cc}

在 [Z-test using S(P0)](#z-test-p0) 的基础上加入校正项 $c$：

$$
c =
\begin{cases}
- \frac{1}{2n} & , \text{if } p \gt p_0 \\
  \frac{1}{2n} & , \text{if } p \lt p_0 \\
  0            & , \text{if } \left| p - p_0 \right| \lt \frac{1}{2n}
\end{cases}
$$

在 $H_0$ 成立时，构建 $z$ 统计量：

$$
z = \frac{\hat{p}-p_0-\delta+c}{\sqrt{p_0(1-p_0)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}-p_0-\delta+c}{\sqrt{p_0(1-p_0)/n}} \sim N\left(\frac{p-p_0-\delta+c}{\sqrt{p_0(1-p_0)/n}}, \frac{\sqrt{p(1-p)/n}}{\sqrt{p_0(1-p_0)/n}}\right)
$$

=== "$\delta < 0$"

    $$
    \text{Power}
    = \operatorname{Pr}(z' > z_{1-\alpha})
    = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p-p_0-\delta+c}{\sqrt{p_0(1-p_0)/n}}}{\frac{\sqrt{p(1-p)/n}}{\sqrt{p_0(1-p_0)/n}}}\right)
    = 1 - \Phi\left(\frac{z_{1-\alpha}\sqrt{p_0(1-p_0)} - (p-p_0-\delta+c)\sqrt{n}}{\sqrt{p(1-p)}}\right)
    $$

=== "$\delta > 0$"

    $$
    \text{Power}
    = \operatorname{Pr}(z' < z_{\alpha})
    = \Phi\left(\frac{z_{\alpha} - \frac{p-p_0-\delta+c}{\sqrt{p_0(1-p_0)/n}}}{\frac{\sqrt{p(1-p)/n}}{\sqrt{p_0(1-p_0)/n}}}\right)
    = 1 - \Phi\left(\frac{z_{1-\alpha}\sqrt{p_0(1-p_0)} + (p-p_0-\delta+c)\sqrt{n}}{\sqrt{p(1-p)}}\right)
    $$


## Z-test using S(Phat) {#z-test-phat}

在 $H_0$ 成立时，使用 $p$ 计算样本比例 $\hat{p}$ 的方差：

$$
\operatorname{Var}(\hat{p}) = \frac{p(1-p)}{n}
$$

构建 $z$ 统计量：

$$
z = \frac{\hat{p}-p_0-\delta}{\sqrt{p(1-p)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}-p_0-\delta}{\sqrt{p(1-p)/n}} \sim N\left(\frac{p-p_0-\delta}{\sqrt{p(1-p)/n}}, 1\right)
$$

=== "$\delta < 0$"

    $$
    \text{Power}
    = \operatorname{Pr}(z' > z_{1-\alpha})
    = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta}{\sqrt{p(1-p)/n}}\right)
    $$

=== "$\delta > 0$"

    $$
    \text{Power}
    = \operatorname{Pr}(z' < z_{\alpha})
    = \Phi\left(z_{\alpha} - \frac{p-p_0-\delta}{\sqrt{p(1-p)/n}}\right)
    = 1 - \Phi\left(z_{1-\alpha} + \frac{p-p_0-\delta}{\sqrt{p(1-p)/n}}\right)
    $$


根据标准正态分布分位数的定义：

$$
z_{1-\alpha} \pm \frac{p-p_0-\delta}{\sqrt{p(1-p)/n}} = z_{\beta}
$$

可解出：

$$
n = \frac{\left(z_{1-\alpha}+z_{1-\beta}\right)^2 p(1-p)}{\left(p-p_0-\delta\right)^2}
$$


## Z-test using S(Phat) 连续性校正 {z-test-phat-cc}

在 [Z-test using S(Phat)](#z-test-phat) 的基础上加入校正项 $c$：

$$
c =
\begin{cases}
- \frac{1}{2n} & , \text{if } \hat{p} \gt p_0 \\
  \frac{1}{2n} & , \text{if } \hat{p} \lt p_0 \\
  0            & , \text{if } \left| \hat{p} - p_0 \right| \lt \frac{1}{2n}
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

=== "$\delta < 0$"

    $$
    \text{Power}
    = \operatorname{Pr}(z' > z_{1-\alpha})
    = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta+c}{\sqrt{p(1-p)/n}}\right)
    $$

=== "$\delta > 0$"

    $$
    \text{Power}
    = \operatorname{Pr}(z' < z_{\alpha})
    = \Phi\left(z_{\alpha} - \frac{p-p_0-\delta+c}{\sqrt{p(1-p)/n}}\right)
    = 1 - \Phi\left(z_{1-\alpha} + \frac{p-p_0-\delta+c}{\sqrt{p(1-p)/n}}\right)
    $$
