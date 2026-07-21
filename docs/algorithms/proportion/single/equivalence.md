# 单样本率等效性检验

样本率用 $\hat{p}$ 表示，总体率用 $p$ 表示，下等效界值用 $\delta_1$ 表示，上等效界值用 $\delta_2$ 表示，$\delta_1 < 0$，$\delta_2 > 0$。

$$
\begin{align}
H_{01} &: p - p_0 \leqslant \delta_1 \;\text{或}\; H_{02}: p - p_0 \geqslant \delta_2 \\
H_1 \  &: \delta_1 < p - p_0 < \delta_2
\end{align}
$$

以下推导过程在边界条件 $p - p_0 = \delta_1$ 和 $p - p_0 = \delta_2$ 下进行。

## _Z-Test Using S(P0)_ {#z-test-p0}

在 $H_{01}$ 成立时，可构建 $z_1$ 统计量：

$$
z_1 = \frac{\hat{p}-p_0-\delta_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}} \sim N(0, 1)
$$

在 $H_{02}$ 成立时，可构建 $z_2$ 统计量：

$$
z_2 = \frac{\hat{p}-p_0-\delta_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'_1$ 和 $z'_2$ 统计量：

$$
z'_1 = \frac{\hat{p}-p_0-\delta_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}} \sim N\left(\frac{p-p_0-\delta_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}, \frac{p(1-p)}{(p_0+\delta_1)(1-p_0-\delta_1)}\right)
$$

$$
z'_2 = \frac{\hat{p}-p_0-\delta_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}} \sim N\left(\frac{p-p_0-\delta_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}, \frac{p(1-p)}{(p_0+\delta_2)(1-p_0-\delta_2)}\right)
$$

计算检验效能：

$$
\begin{align}
    \text{Power}
& = P(z'_1 > z_{1-\alpha} \ \cap \ z'_2 < z_{\alpha}) \\
& = P(z'_1 > z_{1-\alpha}) + P(z'_2 < z_{\alpha}) - P(z'_1 > z_{1-\alpha} \ \cup \ z'_2 < z_{\alpha}) \\
& \approx P(z'_1 > z_{1-\alpha}) + P(z'_2 < z_{\alpha}) - 1 \\
& = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p-p_0-\delta_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}}{\sqrt{\frac{p(1-p)}{(p_0+\delta_1)(1-p_0-\delta_1)}}}\right)
      + \Phi\left(\frac{z_{\alpha} - \frac{p-p_0-\delta_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}}{\sqrt{\frac{p(1-p)}{(p_0+\delta_2)(1-p_0-\delta_2)}}}\right) - 1 \\
& = \begin{aligned}[t]
    & - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n} - (p-p_0-\delta_1)}{\sqrt{p(1-p)/n}}\right) \\
    & + \Phi\left(\frac{z_{\alpha}\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n} - (p-p_0-\delta_2)}{\sqrt{p(1-p)/n}}\right)
    \end{aligned}
\end{align}
$$

## _Z-Test Using S(P0) with Continuity Correction_ {#z-test-p0-cc}

在 [_Z-Test Using S(P0)_](#z-test-p0) 的基础上加入校正项 $c_1$ 和 $c_2$：

$$
c_1 =
\begin{cases}
- \frac{1}{2n} & , \text{if } p \gt p_0 + \delta_1 \\
  \frac{1}{2n} & , \text{if } p \lt p_0 + \delta_1 \\
  0            & , \text{if } \left| p - p_0 - \delta_1 \right| \lt \frac{1}{2n}
\end{cases}
$$

$$
c_2 =
\begin{cases}
- \frac{1}{2n} & , \text{if } p \gt p_0 + \delta_2 \\
  \frac{1}{2n} & , \text{if } p \lt p_0 + \delta_2 \\
  0            & , \text{if } \left| p - p_0 - \delta_2 \right| \lt \frac{1}{2n}
\end{cases}
$$

在 $H_{01}$ 成立时，可构建 $z_1$ 统计量：

$$
z_1 = \frac{\hat{p}-p_0-\delta_1+c_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}} \sim N(0, 1)
$$

在 $H_{02}$ 成立时，可构建 $z_2$ 统计量：

$$
z_2 = \frac{\hat{p}-p_0-\delta_2+c_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'_1$ 和 $z'_2$ 统计量：

$$
z'_1 = \frac{\hat{p}-p_0-\delta_1+c_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}} \sim N\left(\frac{p-p_0-\delta_1+c_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}, \frac{p(1-p)}{(p_0+\delta_1)(1-p_0-\delta_1)}\right)
$$

$$
z'_2 = \frac{\hat{p}-p_0-\delta_2+c_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}} \sim N\left(\frac{p-p_0-\delta_2+c_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}, \frac{p(1-p)}{(p_0+\delta_2)(1-p_0-\delta_2)}\right)
$$

计算检验效能：

$$
\begin{align}
    \text{Power}
& = P(z'_1 > z_{1-\alpha} \ \cap \ z'_2 < z_{\alpha}) \\
& = P(z'_1 > z_{1-\alpha}) + P(z'_2 < z_{\alpha}) - P(z'_1 > z_{1-\alpha} \ \cup \ z'_2 < z_{\alpha}) \\
& \approx P(z'_1 > z_{1-\alpha}) + P(z'_2 < z_{\alpha}) - 1 \\
& = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p-p_0-\delta_1+c_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}}{\sqrt{\frac{p(1-p)}{(p_0+\delta_1)(1-p_0-\delta_1)}}}\right)
      + \Phi\left(\frac{z_{\alpha} - \frac{p-p_0-\delta_2+c_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}}{\sqrt{\frac{p(1-p)}{(p_0+\delta_2)(1-p_0-\delta_2)}}}\right) - 1 \\
& = \begin{aligned}[t]
    & - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n} - (p-p_0-\delta_1+c_1)}{\sqrt{p(1-p)/n}}\right) \\
    & + \Phi\left(\frac{z_{\alpha}\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n} - (p-p_0-\delta_2+c_2)}{\sqrt{p(1-p)/n}}\right)
    \end{aligned}
\end{align}
$$

## _Z-Test Using S(Phat)_ {#z-test-phat}

在 $H_{01}$ 成立时，可构建 $z_1$ 统计量：

$$
z_1 = \frac{\hat{p}-p_0-\delta_1}{\sqrt{p(1-p)/n}} \sim N(0, 1)
$$

在 $H_{02}$ 成立时，可构建 $z_2$ 统计量：

$$
z_2 = \frac{\hat{p}-p_0-\delta_2}{\sqrt{p(1-p)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'_1$ 和 $z'_2$ 统计量：

$$
z'_1 = \frac{\hat{p}-p_0-\delta_1}{\sqrt{p(1-p)/n}} \sim N\left(\frac{p-p_0-\delta_1}{\sqrt{p(1-p)/n}}, 1\right)
$$

$$
z'_2 = \frac{\hat{p}-p_0-\delta_2}{\sqrt{p(1-p)/n}} \sim N\left(\frac{p-p_0-\delta_2}{\sqrt{p(1-p)/n}}, 1\right)
$$

计算检验效能：

$$
\begin{align}
    \text{Power}
& = P(z'_1 > z_{1-\alpha} \ \cap \ z'_2 < z_{\alpha}) \\
& = P(z'_1 > z_{1-\alpha}) + P(z'_2 < z_{\alpha}) - P(z'_1 > z_{1-\alpha} \ \cup \ z'_2 < z_{\alpha}) \\
& \approx P(z'_1 > z_{1-\alpha}) + P(z'_2 < z_{\alpha}) - 1 \\
& = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta_1}{\sqrt{p(1-p)/n}}\right)
      + \Phi\left(z_{\alpha} - \frac{p-p_0-\delta_2}{\sqrt{p(1-p)/n}}\right) - 1 \\
& = - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta_1}{\sqrt{p(1-p)/n}}\right) + \Phi\left(z_{\alpha} - \frac{p-p_0-\delta_2}{\sqrt{p(1-p)/n}}\right)
\end{align}
$$

## _Z-Test Using S(Phat) with Continuity Correction_ {#z-test-phat-cc}

在 [_Z-Test Using S(Phat)_](#z-test-phat) 的基础上加入校正项 $c$：

$$
c_1 =
\begin{cases}
- \frac{1}{2n} & , \text{if } p \gt p_0 + \delta_1 \\
  \frac{1}{2n} & , \text{if } p \lt p_0 + \delta_1 \\
  0            & , \text{if } \left| p - p_0 - \delta_1 \right| \lt \frac{1}{2n}
\end{cases}
$$

$$
c_2 =
\begin{cases}
- \frac{1}{2n} & , \text{if } p \gt p_0 + \delta_2 \\
  \frac{1}{2n} & , \text{if } p \lt p_0 + \delta_2 \\
  0            & , \text{if } \left| p - p_0 - \delta_2 \right| \lt \frac{1}{2n}
\end{cases}
$$

在 $H_{01}$ 成立时，可构建 $z_1$ 统计量：

$$
z_1 = \frac{\hat{p}-p_0-\delta_1+c_1}{\sqrt{p(1-p)/n}} \sim N(0, 1)
$$

在 $H_{02}$ 成立时，可构建 $z_2$ 统计量：

$$
z_2 = \frac{\hat{p}-p_0-\delta_2+c_2}{\sqrt{p(1-p)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，可构建 $z'_1$ 和 $z'_2$ 统计量：

$$
z'_1 = \frac{\hat{p}-p_0-\delta_1+c_1}{\sqrt{p(1-p)/n}} \sim N\left(\frac{p-p_0-\delta_1+c_1}{\sqrt{p(1-p)/n}}, 1\right)
$$

$$
z'_2 = \frac{\hat{p}-p_0-\delta_2+c_2}{\sqrt{p(1-p)/n}} \sim N\left(\frac{p-p_0-\delta_2+c_2}{\sqrt{p(1-p)/n}}, 1\right)
$$

计算检验效能：

$$
\begin{align}
    \text{Power}
& = P(z'_1 > z_{1-\alpha} \ \cap \ z'_2 < z_{\alpha}) \\
& = P(z'_1 > z_{1-\alpha}) + P(z'_2 < z_{\alpha}) - P(z'_1 > z_{1-\alpha} \ \cup \ z'_2 < z_{\alpha}) \\
& \approx P(z'_1 > z_{1-\alpha}) + P(z'_2 < z_{\alpha}) - 1 \\
& = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta_1+c_1}{\sqrt{p(1-p)/n}}\right)
      + \Phi\left(z_{\alpha} - \frac{p-p_0-\delta_2+c_2}{\sqrt{p(1-p)/n}}\right) - 1 \\
& = - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta_1+c_1}{\sqrt{p(1-p)/n}}\right) + \Phi\left(z_{\alpha} - \frac{p-p_0-\delta_2+c_2}{\sqrt{p(1-p)/n}}\right)
\end{align}
$$

!!! quote "参考文献"

    1. Chow S C, Shao J, Wang H, et al. Sample size calculations in clinical research[M]. chapman and hall/CRC, 2017.
