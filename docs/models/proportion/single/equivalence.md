# 单样本率等效性检验

$$
\begin{align}
H_{01} &: p - p_0 \leqslant \delta_1 \text{ 或 } H_{02}: p - p_0 \geqslant \delta_2 \\
H_1 \  &: \delta_1 < p - p_0 < \delta_2
\end{align}
$$

$\delta_1$ 和 $\delta_2$ 为等效性界值，$\delta_1 < 0$，$\delta_2 > 0$，样本比例用 $\hat{p}$ 表示。

$$
\operatorname{E}(\hat{p}) = p
$$

以下推导过程在边界条件 $p - p_0 = \delta_1$ 和 $p - p_0 = \delta_2$ 下进行。


## Z-test using S(P0) {#z-test-p0}

在 $H_{01}$ 成立时，使用 $p_0$ 计算样本比例 $\hat{p}$ 的方差：

$$
\operatorname{Var}(\hat{p}) = \frac{(p_0+\delta_1)(1-p_0-\delta_1)}{n}
$$

构建 $z_1$ 统计量：

$$
z_1 = \frac{\hat{p}-p_0-\delta_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'_1$ 统计量：

$$
z'_1 = \frac{\hat{p}-p_0-\delta_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}} \sim N\left(\frac{p-p_0-\delta_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}, \frac{\sqrt{p(1-p)/n}}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}\right)
$$

在 $H_{02}$ 成立时，使用 $p_0$ 计算样本比例 $\hat{p}$ 的方差：

$$
\operatorname{Var}(\hat{p}) = \frac{(p_0+\delta_2)(1-p_0-\delta_2)}{n}
$$

构建 $z_2$ 统计量：

$$
z_2 = \frac{\hat{p}-p_0-\delta_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'_2$ 统计量：

$$
z'_2 = \frac{\hat{p}-p_0-\delta_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}} \sim N\left(\frac{p-p_0-\delta_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}, \frac{\sqrt{p(1-p)/n}}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}\right)
$$

计算检验效能：

$$
\begin{align}
    \text{Power}
& = \operatorname{Pr}(z'_1 > z_{1-\alpha} \ \cap \ z'_2 < -z_{1-\alpha}) \\
& = \operatorname{Pr}(z'_1 > z_{1-\alpha}) + \operatorname{Pr}(z'_2 < -z_{1-\alpha}) - \operatorname{Pr}(z'_1 > z_{1-\alpha} \ \cup \ z'_2 < -z_{1-\alpha}) \\
& = \operatorname{Pr}(z'_1 > z_{1-\alpha}) + \operatorname{Pr}(z'_2 < -z_{1-\alpha}) - 1 \\
& = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p-p_0-\delta_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}}{\frac{\sqrt{p(1-p)/n}}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}}\right)
      + \Phi\left(\frac{-z_{1-\alpha} - \frac{p-p_0-\delta_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}}{\frac{\sqrt{p(1-p)/n}}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}}\right)
      - 1 \\
& = \begin{aligned}[t]
    1 & - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n} - (p-p_0-\delta_1)}{\sqrt{p(1-p)/n}}\right) + \\
    1 & - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n} + (p-p_0-\delta_2)}{\sqrt{p(1-p)/n}}\right) - 1
    \end{aligned} \\
& = \begin{aligned}[t]
    1 & - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)} - (p-p_0-\delta_1)\sqrt{n}}{\sqrt{p(1-p)}}\right) \\
      & - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)} + (p-p_0-\delta_2)\sqrt{n}}{\sqrt{p(1-p)}}\right)
    \end{aligned}
\end{align}
$$

??? note "$\operatorname{Pr}(z'_1 > z_{1-\alpha} \ \cup \ z'_2 < -z_{1-\alpha}) = 1$ 的证明"
    略。


## Z-test using S(P0) 连续性校正 {#z-test-p0-cc}

在 [Z-test using S(P0)](#z-test-p0) 的基础上加入校正项 $c_1$ 和 $c_2$：

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

在 $H_{01}$ 成立时，构建 $z_1$ 统计量：

$$
z_1 = \frac{\hat{p}-p_0-\delta_1+c_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'_1$ 统计量：

$$
z'_1 = \frac{\hat{p}-p_0-\delta_1+c_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}} \sim N\left(\frac{p-p_0-\delta_1+c_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}, \frac{\sqrt{p(1-p)/n}}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}\right)
$$

在 $H_{02}$ 成立时，构建 $z_2$ 统计量：

$$
z_2 = \frac{\hat{p}-p_0-\delta_2+c_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'_2$ 统计量：

$$
z'_2 = \frac{\hat{p}-p_0-\delta_2+c_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}} \sim N\left(\frac{p-p_0-\delta_2+c_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}, \frac{\sqrt{p(1-p)/n}}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}\right)
$$

计算检验效能：

$$
\begin{align}
    \text{Power}
& = \operatorname{Pr}(z'_1 > z_{1-\alpha} \ \cap \ z'_2 < -z_{1-\alpha}) \\
& = \operatorname{Pr}(z'_1 > z_{1-\alpha}) + \operatorname{Pr}(z'_2 < -z_{1-\alpha}) - \operatorname{Pr}(z'_1 > z_{1-\alpha} \ \cup \ z'_2 < -z_{1-\alpha}) \\
& = \operatorname{Pr}(z'_1 > z_{1-\alpha}) + \operatorname{Pr}(z'_2 < -z_{1-\alpha}) - 1 \\
& = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p-p_0-\delta_1+c_1}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}}{\frac{\sqrt{p(1-p)/n}}{\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n}}}\right)
      + \Phi\left(\frac{-z_{1-\alpha} - \frac{p-p_0-\delta_2+c_2}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}}{\frac{\sqrt{p(1-p)/n}}{\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n}}}\right)
      - 1 \\
& = \begin{aligned}[t]
    1 & - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)/n} - (p-p_0-\delta_1+c_1)}{\sqrt{p(1-p)/n}}\right) + \\
    1 & - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)/n} + (p-p_0-\delta_2+c_2)}{\sqrt{p(1-p)/n}}\right) - 1
    \end{aligned} \\
& = \begin{aligned}[t]
    1 & - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta_1)(1-p_0-\delta_1)} - (p-p_0-\delta_1+c_1)\sqrt{n}}{\sqrt{p(1-p)}}\right) \\
      & - \Phi\left(\frac{z_{1-\alpha}\sqrt{(p_0+\delta_2)(1-p_0-\delta_2)} + (p-p_0-\delta_2+c_2)\sqrt{n}}{\sqrt{p(1-p)}}\right)
    \end{aligned}
\end{align}
$$


## Z-test using S(Phat) {#z-test-phat}


在 $H_{01}$ 成立时，使用 $p$ 计算样本比例 $\hat{p}$ 的方差：

$$
\operatorname{Var}(\hat{p}) = \frac{p(1-p)}{n}
$$

构建 $z_1$ 统计量：

$$
z_1 = \frac{\hat{p}-p_0-\delta_1}{\sqrt{p(1-p)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'_1$ 统计量：

$$
z'_1 = \frac{\hat{p}-p_0-\delta_1}{\sqrt{p(1-p)/n}} \sim N\left(\frac{p-p_0-\delta_1}{\sqrt{p(1-p)/n}}, 1\right)
$$

在 $H_{01}$ 成立时，使用 $p$ 计算样本比例 $\hat{p}$ 的方差：

$$
\operatorname{Var}(\hat{p}) = \frac{p(1-p)}{n}
$$

构建 $z_2$ 统计量：

$$
z_2 = \frac{\hat{p}-p_0-\delta_2}{\sqrt{p(1-p)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'_2$ 统计量：

$$
z'_2 = \frac{\hat{p}-p_0-\delta_2}{\sqrt{p(1-p)/n}} \sim N\left(\frac{p-p_0-\delta_2}{\sqrt{p(1-p)/n}}, 1\right)
$$

计算检验效能：

$$
\begin{align}
    \text{Power}
& = \operatorname{Pr}(z'_1 > z_{1-\alpha} \ \cap \ z'_2 < -z_{1-\alpha}) \\
& = \operatorname{Pr}(z'_1 > z_{1-\alpha}) + \operatorname{Pr}(z'_2 < -z_{1-\alpha}) - \operatorname{Pr}(z'_1 > z_{1-\alpha} \ \cup \ z'_2 < -z_{1-\alpha}) \\
& = \operatorname{Pr}(z'_1 > z_{1-\alpha}) + \operatorname{Pr}(z'_2 < -z_{1-\alpha}) - 1 \\
& = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta_1}{\sqrt{p(1-p)/n}}\right)
      + \Phi\left(-z_{1-\alpha} - \frac{p-p_0-\delta_2}{\sqrt{p(1-p)/n}}\right)
      - 1 \\
& = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta_1}{\sqrt{p(1-p)/n}}\right) +
    1 - \Phi\left(z_{1-\alpha} + \frac{p-p_0-\delta_2}{\sqrt{p(1-p)/n}}\right) - 1 \\
& = 1 - \Phi\left(z_{1-\alpha} - \frac{(p-p_0-\delta_1)\sqrt{n}}{\sqrt{p(1-p)}}\right) - \Phi\left(z_{1-\alpha} + \frac{(p-p_0-\delta_2)\sqrt{n}}{\sqrt{p(1-p)}}\right)
\end{align}
$$


## Z-test using S(Phat) 连续性校正 {#z-test-phat-cc}

在 [Z-test using S(Phat)](#z-test-phat) 的基础上加入校正项 $c$：

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

在 $H_{01}$ 成立时，构建 $z_1$ 统计量：

$$
z_1 = \frac{\hat{p}-p_0-\delta_1+c_1}{\sqrt{p(1-p)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'_1$ 统计量：

$$
z'_1 = \frac{\hat{p}-p_0-\delta_1+c_1}{\sqrt{p(1-p)/n}} \sim N\left(\frac{p-p_0-\delta_1+c_1}{\sqrt{p(1-p)/n}}, 1\right)
$$

在 $H_{01}$ 成立时，构建 $z_2$ 统计量：

$$
z_2 = \frac{\hat{p}-p_0-\delta_2+c_2}{\sqrt{p(1-p)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'_2$ 统计量：

$$
z'_2 = \frac{\hat{p}-p_0-\delta_2+c_2}{\sqrt{p(1-p)/n}} \sim N\left(\frac{p-p_0-\delta_2+c_2}{\sqrt{p(1-p)/n}}, 1\right)
$$

计算检验效能：

$$
\begin{align}
    \text{Power}
& = \operatorname{Pr}(z'_1 > z_{1-\alpha} \ \cap \ z'_2 < -z_{1-\alpha}) \\
& = \operatorname{Pr}(z'_1 > z_{1-\alpha}) + \operatorname{Pr}(z'_2 < -z_{1-\alpha}) - \operatorname{Pr}(z'_1 > z_{1-\alpha} \ \cup \ z'_2 < -z_{1-\alpha}) \\
& = \operatorname{Pr}(z'_1 > z_{1-\alpha}) + \operatorname{Pr}(z'_2 < -z_{1-\alpha}) - 1 \\
& = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta_1+c_1}{\sqrt{p(1-p)/n}}\right)
      + \Phi\left(-z_{1-\alpha} - \frac{p-p_0-\delta_2+c_2}{\sqrt{p(1-p)/n}}\right)
      - 1 \\
& = 1 - \Phi\left(z_{1-\alpha} - \frac{p-p_0-\delta_1+c_1}{\sqrt{p(1-p)/n}}\right) +
    1 - \Phi\left(z_{1-\alpha} + \frac{p-p_0-\delta_2+c_2}{\sqrt{p(1-p)/n}}\right) - 1 \\
& = 1 - \Phi\left(z_{1-\alpha} - \frac{(p-p_0-\delta_1+c_1)\sqrt{n}}{\sqrt{p(1-p)}}\right) - \Phi\left(z_{1-\alpha} + \frac{(p-p_0-\delta_2+c_2)\sqrt{n}}{\sqrt{p(1-p)}}\right)
\end{align}
$$
