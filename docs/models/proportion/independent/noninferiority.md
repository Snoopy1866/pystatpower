# 两独立样本率非劣效检验

## Z-Test Pooled {#z-test-pooled}

统计学假设：

$$
\begin{align}
H_0 &: p_1 - p_2 \le \delta \\
H_1 &: p_1 - p_2 \gt \delta
\end{align}
$$

其中，$\delta$ 为非劣效界值。

$H_0$ 成立时，考虑边界条件 $p_1 - p_2 = \delta$，假设两样本率分别用 $\hat{p}_1$ 和 $\hat{p}_2$ 表示:

$$
E(\hat{p}_1 - \hat{p}_2) = p_1 - p_2 = \delta
$$

$$
Var(\hat{p}_1 - \hat{p}_2)  = \frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}
$$

假设 $\bar{p}$ 表示合并总体率，则：

$$
\bar{p} = \frac{n_1 p_1 + n_2 p_2}{n_1 + n_2}
$$

Pooled 方法假设两样本的方差可以用 $\bar{p}$ 来表示：

$$
Var(\hat{p}_1 - \hat{p}_2) = \frac{\bar{p}(1-\bar{p})}{n_1} + \frac{\bar{p}(1-\bar{p})}{n_2} = \bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)
$$

!!! warning "注意"
    这种做法实际上是站不住脚的，因为在 $H_0$ 的边界条件下，两组总体率不相等，强行合并两组率是不合适的，实际应用中应该使用 [Unpooled 方法](#z-test-unpooled)。


构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 - \delta}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \sim N(0,1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 - \delta}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}
$$

根据中心极限定理，当 $n_1$ 和 $n_2$ 较大时，满足：

$$
\frac{(\hat{p}_1 - \hat{p}_2) - (p_1 - p_2)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

进而有：

$$
\begin{align}
z' & = \frac{(\hat{p}_1 - \hat{p}_2) - (p_1 - p_2) + (p_1 - p_2 - \delta)}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \\
   & = \frac{(\hat{p}_1 - \hat{p}_2) - (p_1 - p_2) + (p_1 - p_2 - \delta)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \cdot \frac{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \\
   & = \frac{(\hat{p}_1 - \hat{p}_2) - (p_1 - p_2)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \cdot \frac{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} + \frac{p_1 - p_2 - \delta}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \\
   & \xrightarrow{d} N\left(\frac{p_1 - p_2 - \delta}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}, \frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}\right)
\end{align}
$$

计算检验效能：

$$
\begin{align}
P\left(\left|z'\right| > z_{1-\alpha}\right) & = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{\left|p_1 - p_2 - \delta\right|}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}{\sqrt{\frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}\right) \\
                                             & = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left|p_1-p_2-\delta\right|}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right) \\
                                             & = 1 - \beta
\end{align}
$$

根据标准正态分布分位数的定义：

$$
\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left|p_1-p_2-\delta\right|}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} = z_\beta
$$

设 $n_1 = kn_2$，由上式可解出：

$$
n_2 = \frac{\left(z_{1-\alpha} \sqrt{\left(\frac{kp_1+p_2}{k+1}\right) \left(1-\frac{kp_1+p_2}{k+1}\right) \left(\frac{1}{k}+1\right)} + z_{1-\beta} \sqrt{\frac{1}{k}p_1(1-p_1) + p_2(1-p_2)}\right)^2}{(p_1-p_2-\delta)^2}
$$

$$
n_1 = k n_2
$$

## Z-Test Pooled Continuity Correction {#z-test-pooled-cc}

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 - \delta - \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \sim N(0,1)
$$

## Z-Test Unpooled {#z-test-unpooled}