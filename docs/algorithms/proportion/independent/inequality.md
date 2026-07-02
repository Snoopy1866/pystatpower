# 两独立样本率差异性检验

两样本率分别用 $\hat{p}_1$ 和 $\hat{p}_2$ 表示。

对于双侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: p_1 = p_2 \\
H_1 &: p_1 \neq p_2
\end{align}
$$

对于左单侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: p_1 \geqslant p_2 \\
H_1 &: p_1 \lt p_2
\end{align}
$$

对于右单侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: p_1 \leqslant p_2\\
H_1 &: p_1 \gt p_2
\end{align}
$$

以下推导过程在边界条件 $p_1 = p_2$ 下进行。

## _Z-Test Pooled_ {#z-test-pooled}

假设 $\bar{p}$ 表示总体合并率：

$$
\bar{p} = \frac{n_1 p_1 + n_2 p_2}{n_1 + n_2}
$$

在 $H_0$ 成立时，$p_1 = p_2 = \bar{p}$，两样本率差的方差可以用 $\bar{p}$ 来表示：

$$
\operatorname{Var}(\hat{p}_1 - \hat{p}_2) = \frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2} = \bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)
$$

可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \sim N(0,1)
$$

在 $H_1$ 成立时，两样本率差的方差如下：

$$
\operatorname{Var}(\hat{p}_1 - \hat{p}_2) = \frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}
$$

可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}
   \sim N\left(\frac{p_1-p_2}{\sqrt{\bar{p}(1-\bar{p}\left(\frac{1}{n_1} + \frac{1}{n_2}\right))}},
               \frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}
         \right)
$$

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right)  \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha/2} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left(p_1-p_2\right)}
                           {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                \right)
          + \Phi\left(\frac{z_{\alpha/2} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left(p_1-p_2\right)}
                           {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                \right)
    \end{align}
    $$

=== "左单侧检验"

    $$
    \begin{align}
    \text{Power} = P\left(z' < z_{\alpha}\right)
                 = \Phi\left(\frac{z_{\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left(p_1-p_2\right)}
                                  {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                       \right)
    \end{align}
    $$

=== "右单侧检验"

    $$
    \begin{align}
    \text{Power} = P\left(z' > z_{1-\alpha}\right)
                 = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left(p_1-p_2\right)}
                                      {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                           \right)
    \end{align}
    $$

??? note "单侧检验样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    \frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} \pm (p_1-p_2)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} = z_\beta
    $$

    设 $n_1 = kn_2$，由上式可解出：

    $$
    n_2 = \frac{\left(z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p})(1/k+1)} + z_{1-\beta} \sqrt{p_1(1-p_1)/k + p_2(1-p_2)}\right)^2}{(p_1-p_2)^2}
    $$

    $$
    n_1 = k n_2
    $$

## _Z-Test Pooled with Continuity Correction_ {#z-test-pooled-cc}

在 [_Z-Test Pooled_](#z-test-pooled) 的基础上，添加校正项 $c$：

$$
c =
\begin{cases}
- \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right) & , \text{if } \hat{p}_1 - \hat{p}_2 > 0 \\
  \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right) & , \text{if } \hat{p}_1 - \hat{p}_2 < 0 \\
  0 & , \text{if } |\hat{p}_1 - \hat{p}_2| \leqslant \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)
\end{cases}
$$

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 + c}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \sim N(0,1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 + c}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}
   \sim N\left(\frac{p_1-p_2+c}{\sqrt{\bar{p}(1-\bar{p}\left(\frac{1}{n_1} + \frac{1}{n_2}\right))}},
               \frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}
         \right)
$$

=== "双侧检验"

    $$
    \begin{align}
    \text{Power} & = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right) \\
                 & = \begin{aligned}[t]
                     1 & - \Phi\left(\frac{z_{1-\alpha/2} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2+c)}
                                          {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                               \right) \\
                       & + \Phi\left(\frac{z_{\alpha/2} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2+c)}
                                          {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                               \right)
                     \end{aligned}
    \end{align}
    $$

=== "左单侧检验"

    $$
    \begin{align}
    \text{Power} = P\left(z' < z_{\alpha}\right)
                 = \Phi\left(\frac{z_{\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2+c)}
                                  {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                       \right)
    \end{align}
    $$

=== "右单侧检验"

    $$
    \begin{align}
    \text{Power} = P\left(z' > z_{1-\alpha}\right)
                 = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2+c)}
                                      {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                           \right)
    \end{align}
    $$

## _Z-Test Unpooled_ {#z-test-unpooled}

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N\left(\frac{p_1 - p_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}, \ 1\right)
$$

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right) \\
    & = 1 - \Phi\left(z_{1-\alpha/2} - \frac{p_1 - p_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
          + \Phi\left(z_{\alpha/2} - \frac{p_1 - p_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(z' < z_{\alpha}\right)
    = \Phi\left(z_{\alpha} - \frac{p_1 - p_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(z' > z_{1-\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{p_1 - p_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    $$

??? note "单侧检验样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    z_{1-\alpha} \pm \frac{p_1 - p_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} = z_\beta
    $$

    设 $n_1 = kn_2$，由上式可解出：

    $$
    n_2 = \frac{\left(z_{1-\alpha} + z_{1-\beta}\right)^2 \left[ p_1(1-p_1)/k + p_2(1-p_2) \right]}{(p_1-p_2)^2}
    $$

    $$
    n_1 = k n_2
    $$

## _Z-Test Unpooled with Continuity Correction_ {#z-test-unpooled-cc}

在 [_Z-Test Unpooled_](#z-test-unpooled) 的基础上，添加校正项 $c$，其中：

$$
c =
\begin{cases}
- \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right) & , \text{if } \hat{p}_1 - \hat{p}_2 > 0 \\
  \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right) & , \text{if } \hat{p}_1 - \hat{p}_2 < 0 \\
  0 & , \text{if } |\hat{p}_1 - \hat{p}_2| \leqslant \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)
\end{cases}
$$

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 + c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 + c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N\left(\frac{p_1 - p_2 + c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}, \ 1\right)
$$

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right) \\
    & = 1 - \Phi\left(z_{1-\alpha/2} - \frac{p_1-p_2+c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
          + \Phi\left(z_{\alpha/2} - \frac{p_1-p_2+c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(z' < z_{\alpha}\right)
    = \Phi\left(z_{\alpha} - \frac{p_1-p_2+c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(z' > z_{1-\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{p_1-p_2+c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    $$
