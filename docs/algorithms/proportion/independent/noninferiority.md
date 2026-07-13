# 两独立样本率非劣效检验

两样本率分别用 $\hat{p}_1$ 和 $\hat{p}_2$ 表示，非劣界值用 $\delta$ 表示。

对于高优指标（$\delta < 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p_1 - p_2 \leqslant \delta \\
H_1 &: p_1 - p_2 \gt \delta
\end{align}
$$

对于低优指标（$\delta > 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p_1 - p_2 \geqslant \delta \\
H_1 &: p_1 - p_2 \lt \delta
\end{align}
$$

以下推导过程在边界条件 $p_1 - p_2 = \delta$ 下进行。

--8<-- [start:algorithm]

## _Z-Test Pooled_ {#z-test-pooled}

假设 $\bar{p}$ 表示合并总体率，则：

$$
\bar{p} = \frac{n_1 \hat{p}_1 + n_2 \hat{p}_2}{n_1 + n_2}
$$

在 $H_0$ 成立时，两样本的方差可以用 $\bar{p}$ 来表示：

$$
\operatorname{Var}(\hat{p}_1 - \hat{p}_2) = \frac{\bar{p}(1-\bar{p})}{n_1} + \frac{\bar{p}(1-\bar{p})}{n_2} = \bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)
$$

!!! warning

    事实上，$H_0$ 成立时，其边界条件 $p_1 = p_2 + \delta$，两组总体率不相等，强行将两组率进行合并是不合适的，实际应用中建议使用 [_Z-test Unpooled_](#z-test-unpooled)。

可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 - \delta}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \sim N(0,1)
$$

在 $H_1$ 成立时，两样本率差的方差如下：

$$
\operatorname{Var}(\hat{p}_1 - \hat{p}_2) = \frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}
$$

可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 - \delta}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}
   \sim N\left(\frac{p_1 - p_2 - \delta}
                    {\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}, \
               \frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}
                    {\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}
         \right)
$$

=== "高优指标"

    $$
    \begin{align}
    \text{Power} & = P\left(z' > z_{1-\alpha}\right) \\
                 & = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p_1 - p_2 - \delta}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                                        {\sqrt{\frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                             \right) \\
                 & = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2-\delta)}
                                        {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                             \right) \\
     \end{align}
    $$

=== "低优指标"

    $$
    \begin{align}
    \text{Power} & = P\left(z' < z_{\alpha}\right) \\
                 & = \Phi\left(\frac{z_{\alpha} - \frac{p_1 - p_2 - \delta}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                                    {\sqrt{\frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                         \right) \\
                 & = \Phi\left(\frac{z_{\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2-\delta)}
                                    {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                         \right)
     \end{align}
    $$

??? note "样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    \frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} \pm (p_1-p_2-\delta)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} = z_\beta
    $$

    设 $n_1 = kn_2$，由上式可解出

    $$
    n_2 = \frac{\left(z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p})(1/k+1)} + z_{1-\beta} \sqrt{p_1(1-p_1)/k + p_2(1-p_2)}\right)^2}{(p_1-p_2-\delta)^2}
    $$

    $$
    n_1 = k n_2
    $$

## _Z-Test Pooled with Continuity Correction_ {#z-test-pooled-cc}

在 [_Z-Test Pooled_](#z-test-pooled) 的基础上，添加校正项。

定义：

$$
c = \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)
$$

校正项的符号由检验方向决定，左侧检验时，校正项为 $+c$，右侧检验时，校正项为 $-c$。

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 - \delta \pm c}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \sim N(0,1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 - \delta \pm c}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}
   \sim N\left(\frac{p_1 - p_2 - \delta \pm c}{\sqrt{\bar{p}(1-\bar{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}},
               \frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}
         \right)
$$

=== "高优指标"

    $$
    \begin{align}
    \text{Power} = P\left(z' > z_{1-\alpha}\right)
                 = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2-\delta-c)}
                                      {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                           \right)
    \end{align}
    $$

=== "低优指标"

    $$
    \begin{align}
    \text{Power} = P\left(z' < z_{\alpha}\right)
                 = \Phi\left(\frac{z_{\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2-\delta+c)}
                                  {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                       \right)
    \end{align}
    $$

## _Z-Test Unpooled_ {#z-test-unpooled}

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 - \delta}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 - \delta}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N\left(\frac{p_1 - p_2 - \delta}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}, \ 1\right)
$$

=== "高优指标"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha}\right)
                 = 1 - \Phi\left(z_{1-\alpha} - \frac{p_1-p_2-\delta}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
    $$

=== "低优指标"

    $$
    \text{Power} = P\left(z' < z_{\alpha}\right)
                 = \Phi\left(z_{\alpha} - \frac{p_1-p_2-\delta}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
    $$

??? note "样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    z_{1-\alpha} \pm \frac{(p_1 - p_2 - \delta)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} = z_\beta
    $$

    设 $n_1 = kn_2$，由上式可解出：

    $$
    n_2 = \frac{\left(z_{1-\alpha} + z_{1-\beta}\right)^2 \left[ p_1(1-p_1)/k + p_2(1-p_2) \right]}{(p_1-p_2-\delta)^2}
    $$

    $$
    n_1 = k n_2
    $$

## _Z-Test Unpooled with Continuity Correction_ {#z-test-unpooled-cc}

在 [_Z-Test Unpooled_](#z-test-unpooled) 的基础上，添加校正项。

定义：

$$
c = \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)
$$

校正项的符号由检验方向决定，左侧检验时，校正项为 $+c$，右侧检验时，校正项为 $-c$。

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 - \delta \pm c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 - \delta \pm c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N\left(\frac{p_1 - p_2 - \delta + c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}, \ 1\right)
$$

=== "高优指标"

    $$
    \text{Power} = P\left(z' > z_{1-\alpha}\right)
                 = 1 - \Phi\left(z_{1-\alpha} - \frac{p_1-p_2-\delta-c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
    $$

=== "低优指标"

    $$
    \text{Power} = P\left(z' < z_{\alpha}\right)
                 = \Phi\left(z_{\alpha} - \frac{p_1-p_2-\delta+c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
    $$

--8<-- [end:algorithm]

!!! quote "参考文献"

    1. Chow S C, Shao J, Wang H, et al. Sample size calculations in clinical research[M]. chapman and hall/CRC, 2017.
