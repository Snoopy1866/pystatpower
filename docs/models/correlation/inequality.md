# 相关系数差异性检验

对于双侧检验，统计学假设如下：

$$
\begin{align}
H_0 & : \rho_1 = \rho_0 \\
H_1 & : \rho_1 \neq \rho_0
\end{align}
$$

对于左单侧检验，统计学假设如下：

$$
\begin{align}
H_0 & : \rho_1 \geqslant \rho_0 \\
H_1 & : \rho_1 \lt \rho_0
\end{align}
$$

对于右单侧检验，统计学假设如下：

$$
\begin{align}
H_0 & : \rho_1 \leqslant \rho_0 \\
H_1 & : \rho_1 \gt \rho_0
\end{align}
$$

样本相关系数用 $\hat{\rho}_1$ 表示。

以下推导过程在边界条件 $\rho_1 = \rho_0$ 下进行。

Fisher's z 转换：

$$
\zeta = \operatorname{arctanh}\rho = \frac{1}{2} \ln{\frac{1+\rho}{1-\rho}}
$$

## 未校正偏倚 {#bias-not-adj}

在 $H_0$ 成立时，$\hat{\zeta}_1$ 近似服从正态分布：

$$
\hat{\zeta}_1 \sim N\left(\zeta_0,\ \frac{1}{n-3}\right)
$$

构建 $z$ 统计量：

$$
z = \frac{\hat{\zeta}_1 - \zeta_0}{1/\sqrt{n-3}} = \left(\hat{\zeta}_1 - \zeta_0\right) \sqrt{n-3} \sim N(0, 1)
$$


在 $H_1$ 成立时，$\hat{\zeta}$ 近似服从正态分布：

$$
\hat{\zeta}_1 \sim N\left(\zeta_1,\ \frac{1}{n-3}\right)
$$

构建 $z'$ 统计量：

$$
z' = \frac{\hat{\zeta}_1 - \zeta_0}{1/\sqrt{n-3}} = \left(\hat{\zeta}_1 - \zeta_0\right) \sqrt{n-3} \sim N\left(\left(\zeta_1 - \zeta_0\right)\sqrt{n-3}, 1\right)
$$

=== "双侧检验"

    $$
    \begin{aligned}
    \text{Power}
    = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right)
    = 1 - \Phi\left(z_{1-\alpha/2} - \left(\zeta_1 - \zeta_0\right) \sqrt{n-3}\right) + \Phi\left(z_{\alpha/2} - \left(\zeta_1 - \zeta_0\right) \sqrt{n-3}\right)
    \end{aligned}
    $$

=== "左单侧检验"

    $$
    \begin{aligned}
    \text{Power}
    = P\left(z' < z_{\alpha}\right)
    = \Phi\left(z_{\alpha} - \left(\zeta_1 - \zeta_0\right) \sqrt{n-3}\right)
    = 1 - \Phi\left(z_{1-\alpha} + \left(\zeta_1 - \zeta_0\right) \sqrt{n-3}\right)
    \end{aligned}
    $$

=== "右单侧检验"

    $$
    \begin{aligned}
    \text{Power}
    = P\left(z' > z_{1-\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \left(\zeta_1 - \zeta_0\right) \sqrt{n-3}\right)
    \end{aligned}
    $$

对于单测检验，可利用功效函数得到样本量的闭式解：

根据标准正态分布分位数的定义：

$$
z_{1-\alpha/2} \pm \left(\zeta_1 - \zeta_0\right) \sqrt{n-3} = z_{\beta}
$$

可解出：

$$
n = \frac{\left(z_{1-\alpha/2} + z_{1-\beta}\right)^2}{\left(\zeta_1 - \zeta_0\right)^2} + 3
$$

利用 Fisher's z 转换得：

$$
n = 4 \left( \frac{z_{1-\alpha/2} + z_{1-\beta}}{\ln{\frac{\left(1+\rho_1\right) \left(1-\rho_0\right)}{\left(1-\rho_1\right) \left(1+\rho_0\right)}}} \right)^2+ 3
$$

## 校正偏倚 {#bias-adj}

在 [未校正偏倚](#bias-not-adj) 的基础上添加校正项 $\frac{\rho}{2(n-1)}$。

在 $H_0$ 成立时，$\hat{\zeta}_1$ 近似服从正态分布：

$$
\hat{\zeta}_1 \sim N\left(\zeta_0 + \frac{\rho_0}{2(n-1)}, \frac{1}{n-3}\right)
$$

构建 $z$ 统计量：

$$
z = \frac{\hat{\zeta}_1 - \zeta_0 - \frac{\rho_0}{2(n-1)}}{1/\sqrt{n-3}} = \left(\hat{\zeta}_1 - \zeta_0 - \frac{\rho_0}{2(n-1)}\right) \sqrt{n-3} \sim N(0, 1)
$$

在 $H_1$ 成立时，$\hat{\zeta}_1$ 近似服从正态分布：

$$
\hat{\zeta}_1 \sim N\left(\zeta_1 + \frac{\rho_1}{2(n-1)},\ \frac{1}{n-3}\right)
$$

构建 $z'$ 统计量：

$$
z' = \frac{\hat{\zeta}_1 - \zeta_0 - \frac{\rho_0}{2(n-1)}}{1/\sqrt{n-3}}
   = \left(\hat{\zeta}_1 - \zeta_0 - \frac{\rho_0}{2(n-1)}\right) \sqrt{n-3}
   \sim N\left(\left(\zeta_1 - \zeta_0 + \frac{\rho_1 - \rho_0}{2(n-1)}\right) \sqrt{n-3}, 1\right)
$$

=== "双侧检验"

    $$
    \begin{aligned}
      \text{Power}
    & = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right) \\
    & = 1 - \Phi\left(z_{1-\alpha/2} - \left(\zeta_1 - \zeta_0 + \frac{\rho_1 - \rho_0}{2(n-1)}\right) \sqrt{n-3}\right)
          + \Phi\left(z_{\alpha/2} - \left(\zeta_1 - \zeta_0 + \frac{\rho_1 - \rho_0}{2(n-1)}\right) \sqrt{n-3}\right)
    \end{aligned}
    $$

=== "左单侧检验"

    $$
    \begin{aligned}
      \text{Power}
    & = P\left(z' < z_{\alpha}\right) \\
    & = \Phi\left(z_{\alpha} - \left(\zeta_1 - \zeta_0 + \frac{\rho_1 - \rho_0}{2(n-1)}\right) \sqrt{n-3}\right) \\
    & = 1 - \Phi\left(z_{1-\alpha} + \left(\zeta_1 - \zeta_0 + \frac{\rho_1 - \rho_0}{2(n-1)}\right) \sqrt{n-3}\right)
    \end{aligned}
    $$

=== "右单侧检验"

    $$
    \begin{aligned}
      \text{Power}
    & = P\left(z' > z_{1-\alpha}\right) \\
    & = 1 - \Phi\left(z_{1-\alpha} - \left(\zeta_1 - \zeta_0 + \frac{\rho_1 - \rho_0}{2(n-1)}\right) \sqrt{n-3}\right)
    \end{aligned}
    $$
