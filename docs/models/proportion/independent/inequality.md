# 两独立样本率差异性检验

对于双侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: p_1 - p_2 = 0 \\
H_1 &: p_1 - p_2 \neq 0
\end{align}
$$

对于左单侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: p_1 - p_2 \geqslant 0 \\
H_1 &: p_1 - p_2 \lt 0
\end{align}
$$

对于右单侧检验，统计学假设如下：

$$
\begin{align}
H_0 &: p_1 - p_2 \leqslant 0 \\
H_1 &: p_1 - p_2 \gt 0
\end{align}
$$

两样本率分别用 $\hat{p}_1$ 和 $\hat{p}_2$ 表示。

$$
E(\hat{p}_1 - \hat{p}_2) = p_1 - p_2, \ \ Var(\hat{p}_1 - \hat{p}_2)  = \frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}
$$

以下推导过程在边界条件 $p_1 = p_2$ 下进行。

## Z-Test Pooled {#z-test-pooled}

假设 $\bar{p}$ 表示总体合并率，则：

$$
\bar{p} = \frac{n_1 p_1 + n_2 p_2}{n_1 + n_2}
$$

在 $H_0$ 成立时，$p_1 = p_2 = \bar{p}$，两样本率差的方差可以用 $\bar{p}$ 来表示：

$$
Var(\hat{p}_1 - \hat{p}_2) = \frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2} = \frac{\bar{p}(1-\bar{p})}{n_1} + \frac{\bar{p}(1-\bar{p})}{n_2} = \bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)
$$

构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \sim N(0,1)
$$

在 $H_1$ 成立时，两样本率差的方差如下：

$$
Var(\hat{p}_1 - \hat{p}_2) = \frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}
$$


构建 $z'$ 统计量：

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
        \text{Power}
    & = P\left(z' < z_{\alpha}\right)  \\
    & = \Phi\left(\frac{z_{\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left(p_1-p_2\right)}
                       {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
            \right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} + \left(p_1-p_2\right)}
                           {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                \right)
    \end{align}
    $$

=== "右单侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(z' > z_{1-\alpha}\right)  \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left(p_1-p_2\right)}
                           {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                \right)
    \end{align}
    $$

对于**单侧检验**，可利用功效函数得到样本量的闭式解：

根据标准正态分布分位数的定义：

$$
\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} \pm (p_1-p_2)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} = z_\beta
$$

设 $n_1 = kn_2$，由上式可解出：

$$
n_2 = \frac{\left(z_{1-\alpha} \sqrt{\left(\frac{kp_1+p_2}{k+1}\right) \left(1-\frac{kp_1+p_2}{k+1}\right) \left(\frac{1}{k}+1\right)}
                + z_{1-\beta} \sqrt{\frac{1}{k}p_1(1-p_1) + p_2(1-p_2)}\right)^2}{(p_1-p_2)^2}
$$

$$
n_1 = k n_2
$$

## Z-Test Pooled 连续性校正 {#z-test-pooled-cc}

在 [Z-Test Pooled](#z-test-pooled) 的基础上，添加校正项 $c$，其中：

$$
c =
\begin{cases}
  \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right), & \text{if 左侧检验} \\
- \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right), & \text{if 右侧检验}
\end{cases}
$$

在 $H_0$ 成立时，构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 + c}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \sim N(0,1)
$$

在 $H_1$ 成立时，构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 + c}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}
   \sim N\left(\frac{p_1-p_2+c}{\sqrt{\bar{p}(1-\bar{p}\left(\frac{1}{n_1} + \frac{1}{n_2}\right))}},
               \frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}
         \right)
$$

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right)  \\
    & = \begin{aligned}[t]
        1 & - \Phi\left(\frac{z_{1-\alpha/2} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left(p_1-p_2-\frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)\right)}
                             {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                  \right) \\
          & + \Phi\left(\frac{z_{\alpha/2} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left(p_1-p_2+\frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)\right)}
                             {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                  \right)
        \end{aligned} \\
    & = \begin{aligned}[t]
        1 & - \Phi\left(\frac{z_{1-\alpha/2} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2)+\frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}
                             {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                  \right) \\
          & + \Phi\left(\frac{z_{\alpha/2} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2)-\frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}
                             {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                  \right)
        \end{aligned}
    \end{align}
    $$

=== "左单侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(z' < z_{\alpha}\right)  \\
    & = \Phi\left(\frac{z_{\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left(p_1-p_2+\frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)\right)}
                       {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
            \right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} + (p_1-p_2)+\frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}
                           {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                \right)
    \end{align}
    $$

=== "右单侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(z' > z_{1-\alpha}\right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left(p_1-p_2-\frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)\right)}
                           {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                \right) \\
    & = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2)+\frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}
                           {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                \right)
    \end{align}
    $$

## Z-Test Unpooled {#z-test-unpooled}

在 $H_0$ 成立时，构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

在 $H_1$ 成立时，构建 $z'$ 统计量：

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
    = 1 - \Phi\left(z_{1-\alpha} + \frac{p_1 - p_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(z' > z_{1-\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{p_1 - p_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    $$

对于**单侧检验**，可利用功效函数得到样本量的闭式解：

根据标准正态分布分位数的定义：

$$
z_{1-\alpha} \pm \frac{p_1 - p_2}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} = z_\beta
$$

设 $n_1 = kn_2$，由上式可解出：

$$
n_2 = \frac{\left(z_{1-\alpha} + z_{1-\beta}\right)^2 \left[ \frac{1}{k}p_1(1-p_1) + p_2(1-p_2) \right]}{(p_1-p_2)^2}
$$

$$
n_1 = k n_2
$$

## Z-Test Unpooled 连续性校正 {#z-test-unpooled-cc}

在 [Z-Test Unpooled](#z-test-unpooled) 的基础上，添加校正项 $c$，其中：

$$
c =
\begin{cases}
  \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right), & \text{if 左侧检验} \\
- \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right), & \text{if 右侧检验}
\end{cases}
$$

在 $H_0$ 成立时，构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 + c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

在 $H_1$ 成立时，构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 + c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N\left(\frac{p_1 - p_2 + c}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}, \ 1\right)
$$

=== "双侧检验"

    $$
    \begin{align}
        \text{Power}
    & = P\left(z' > z_{1-\alpha/2}\right) + P\left(z' < z_{\alpha/2}\right) \\
    & = 1 - \Phi\left(z_{1-\alpha/2} - \frac{p_1 - p_2 - \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
          + \Phi\left(z_{\alpha/2} - \frac{p_1 - p_2 + \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    \end{align}
    $$

=== "左单侧检验"

    $$
      \text{Power}
    = P\left(z' < z_{\alpha}\right)
    = \Phi\left(z_{\alpha} - \frac{p_1 - p_2 + \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    = 1 - \Phi\left(z_{1-\alpha} + \frac{p_1 - p_2 + \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    $$

=== "右单侧检验"

    $$
      \text{Power}
    = P\left(z' > z_{1-\alpha}\right)
    = 1 - \Phi\left(z_{1-\alpha} - \frac{p_1 - p_2 - \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}\right)
    $$
