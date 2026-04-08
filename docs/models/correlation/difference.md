# 相关系数差异性检验


$$
\begin{align}
H_0 & : \rho = \rho_0 \\
H_1 & : \rho \neq \rho_0
\end{align}
$$

对样本相关系数 $\hat{\rho}$ 做 Fisher's z 转换：

$$
\hat{\zeta} = \operatorname{arctanh}\hat{\rho} = \frac{1}{2} \ln{\frac{1+\hat{\rho}}{1-\hat{\rho}}}
$$

在 $H_0$ 成立时，$\hat{\zeta}$ 近似服从正态分布：

$$
\hat{\zeta} \sim N\left(\zeta_0,\ \frac{1}{n-3}\right)
$$

其中：

$$
\zeta_0 = \frac{1}{2} \ln{\frac{1+\rho_0}{1-\rho_0}} \tag{1}
$$

那么：

$$
E(\hat{\zeta} - \zeta_0) = E(\hat{\zeta}) - \zeta_0 = \zeta_0 - \zeta_0 = 0
$$

$$
Var(\hat{\zeta} - \zeta_0) = Var(\hat{\zeta}) - 0 = \frac{1}{n-3}
$$

构建 $z$ 统计量：

$$
z = \frac{\hat{\zeta} - \zeta_0}{1/\sqrt{n-3}} = \left(\hat{\zeta} - \zeta_0\right) \sqrt{n-3} \sim N(0, 1)
$$


在 $H_1$ 成立时，$\hat{\zeta}$ 近似服从正态分布：

$$
\hat{\zeta} \sim N\left(\zeta_1,\ \frac{1}{n-3}\right)
$$

其中：

$$
\zeta_1 = \frac{1}{2} \ln{\frac{1+\rho_1}{1-\rho_1}} \tag{2}
$$

构建 $z$ 统计量：

$$
z' = \frac{\hat{\zeta} - \zeta_0}{1/\sqrt{n-3}} = \left(\hat{\zeta} - \zeta_0\right) \sqrt{n-3}
$$

根据大数定律和连续映射定理，当 $n$ 较大时，$\hat{\zeta}$ 满足：

$$
\hat{\zeta} \xrightarrow{p} \zeta_1
$$

进而有：

$$
\left(\hat{\zeta} - \zeta_0\right) \sqrt{n-3} = \left(\hat{\zeta} - \zeta_1\right) \sqrt{n-3} + \left(\zeta_1 - \zeta_0\right) \sqrt{n-3} \xrightarrow{d} N\left(\left(\zeta_1 - \zeta_0\right) \sqrt{n-3}, 1\right)
$$


计算检验效能：

$$
\begin{aligned}
P\left( \left| z' \right| > z_{1-\alpha/2} \right) \approx 1 - \Phi\left( z_{1-\alpha/2} - \left|\zeta_1 - \zeta_0\right| \sqrt{n-3} \right) = 1 - \beta
\end{aligned}
$$

根据标准正态分布分位数的定义：

$$
z_{1-\alpha/2} - \left|\zeta_1 - \zeta_0\right| \sqrt{n-3} = z_{\beta}
$$

可解出：

$$
n = \frac{\left(z_{1-\alpha/2} + z_{1-\beta}\right)^2}{\left(\zeta_1 - \zeta_0\right)^2} + 3
$$

代入 $(1)$ 和 $(2)$，得：

$$
n = \frac{4 \left(z_{1-\alpha/2} + z_{1-\beta}\right)^2}{\ln^2{\frac{\left(1+\rho_1\right) \left(1-\rho_0\right)}{\left(1-\rho_1\right) \left(1+\rho_0\right)}}} + 3
$$
