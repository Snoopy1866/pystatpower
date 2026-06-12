# 两独立样本率非劣效检验

对于高优指标（$\delta < 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p_1 - p_2 \le \delta \\
H_1 &: p_1 - p_2 \gt \delta
\end{align}
$$

对于低优指标（$\delta > 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p_1 - p_2 \ge \delta \\
H_1 &: p_1 - p_2 \lt \delta
\end{align}
$$

$\delta$ 为非劣效界值，两样本率分别用 $\hat{p}_1$ 和 $\hat{p}_2$ 表示。

$$
E(\hat{p}_1 - \hat{p}_2) = p_1 - p_2, \ \ Var(\hat{p}_1 - \hat{p}_2)  = \frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}
$$

以下推导过程在边界条件 $p_1 - p_2 = \delta$ 下进行。

## Z-Test Pooled {#z-test-pooled}

假设 $\bar{p}$ 表示合并总体率，则：

$$
\bar{p} = \frac{n_1 \hat{p}_1 + n_2 \hat{p}_2}{n_1 + n_2}
$$

在 $H_0$ 成立时：

两样本的方差可以用 $\bar{p}$ 来表示：

$$
Var(\hat{p}_1 - \hat{p}_2) = \frac{\bar{p}(1-\bar{p})}{n_1} + \frac{\bar{p}(1-\bar{p})}{n_2} = \bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)
$$

!!! warning "注意"
    这种做法实际上是站不住脚的，因为在 $H_0$ 的边界条件下，两组总体率不相等，并不是来自同一个总体，强行合并两组率是不合适的，实际应用中建议使用 [Unpooled 方法](#z-test-unpooled)。


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
z' & = \frac{\left(\hat{p}_1 - \hat{p}_2\right) - \left(p_1 - p_2\right) + \left(p_1 - p_2 - \delta\right)}
            {\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \\
   & = \frac{\left(\hat{p}_1 - \hat{p}_2\right) - \left(p_1 - p_2\right) + \left(p_1 - p_2 - \delta\right)}
            {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
       \cdot
       \frac{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
            {\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \\
   & = \frac{\left(\hat{p}_1 - \hat{p}_2\right) - \left(p_1 - p_2\right)}
            {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
       \cdot
       \frac{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
            {\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}
       +
       \frac{p_1 - p_2 - \delta}
            {\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \\
   & \xrightarrow{d}
       N\left(\frac{p_1 - p_2 - \delta}
                   {\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}, \
              \frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}
                   {\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}
        \right)
\end{align}
$$

=== "$\delta < 0$"

    $$
    \begin{align}
     Power & = P\left(z' > z_{1-\alpha}\right) \\
           & = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p_1 - p_2 - \delta}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                                  {\sqrt{\frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                       \right) \\
           & = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left(p_1-p_2-\delta\right)}
                                  {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                       \right) \\
           & = 1 - \beta
     \end{align}
    $$

=== "$\delta > 0$"

    $$
    \begin{align}
     Power & = P\left(z' < -z_{1-\alpha}\right) \\
           & = \Phi\left(\frac{-z_{1-\alpha} - \frac{p_1 - p_2 - \delta}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                              {\sqrt{\frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                   \right) \\
           & = 1 - \Phi\left(\frac{z_{1-\alpha} + \frac{p_1 - p_2 - \delta}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                                  {\sqrt{\frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                       \right) \\
           & = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} + \left(p_1-p_2-\delta\right)}
                                  {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                       \right) \\
           & = 1 - \beta
     \end{align}
    $$

在 $H_1$ 成立时：

若 $\delta < 0$，则 $p_1 - p_2 - \delta > 0$；

若 $\delta > 0$，则 $p_1 - p_2 - \delta < 0$。

$$
Power = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left|p_1-p_2-\delta\right|}
                           {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                \right)
$$

??? note "样本量公式推导"
    根据标准正态分布分位数的定义：

    $$
    \frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left|p_1-p_2-\delta\right|}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} = z_\beta
    $$

    设 $n_1 = kn_2$，由上式可解出

    $$
    n_2 = \frac{\left(z_{1-\alpha} \sqrt{\left(\frac{kp_1+p_2}{k+1}\right) \left(1-\frac{kp_1+p_2}{k+1}\right) \left(\frac{1}{k}+1\right)} + z_{1-\beta} \sqrt{\frac{1}{k}p_1(1-p_1) + p_2(1-p_2)}\right)^2}{(p_1-p_2-\delta)^2}
    $$

    $$
    n_1 = k n_2
    $$

## Z-Test Pooled 连续性校正 {#z-test-pooled-cc}

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 - \delta + c}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \sim N(0,1)
$$

其中：

$$
c =
\begin{cases}
- \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right), & \delta < 0 \\
\frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right),   & \delta > 0
\end{cases}
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 - \delta + c}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}
$$

根据中心极限定理，当 $n_1$ 和 $n_2$ 较大时，满足：

$$
\frac{(\hat{p}_1 - \hat{p}_2) - (p_1 - p_2)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

进而有：

$$
\begin{align}
z' & = \frac{\left(\hat{p}_1 - \hat{p}_2\right) - \left(p_1 - p_2\right) + \left(p_1 - p_2 - \delta + c\right)}
            {\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \\
   & = \frac{\left(\hat{p}_1 - \hat{p}_2\right) - \left(p_1 - p_2\right) + \left(p_1 - p_2 - \delta + c\right)}
            {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
       \cdot
       \frac{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
            {\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \\
   & = \frac{\left(\hat{p}_1 - \hat{p}_2\right) - \left(p_1 - p_2\right)}
            {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
       \cdot
       \frac{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
            {\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}
       +
       \frac{p_1 - p_2 - \delta + c}
            {\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}} \\
   & \xrightarrow{d}
       N\left(\frac{p_1 - p_2 - \delta + c}
                   {\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}, \
              \frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}
                   {\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}
        \right)
\end{align}
$$

=== "$\delta < 0$"

    $$
    \begin{align}
     Power & = P\left(z' > z_{1-\alpha}\right) \\
           & = 1 - \Phi\left(\frac{z_{1-\alpha} - \frac{p_1 - p_2 - \delta - \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                                  {\sqrt{\frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                       \right) \\
           & = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - (p_1-p_2-\delta) + \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}
                                  {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                       \right) \\
           & = 1 - \beta
     \end{align}
    $$

=== "$\delta > 0$"

    $$
    \begin{align}
     Power & = P\left(z' < -z_{1-\alpha}\right) \\
           & = \Phi\left(\frac{-z_{1-\alpha} - \frac{p_1 - p_2 - \delta + \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                              {\sqrt{\frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                   \right) \\
           & = 1 - \Phi\left(\frac{z_{1-\alpha} + \frac{p_1 - p_2 - \delta + \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}{\sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                                  {\sqrt{\frac{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}}
                       \right) \\
           & = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} + (p_1-p_2-\delta) + \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}
                                  {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                       \right) \\
           & = 1 - \beta
     \end{align}
    $$

在 $H_1$ 成立时：

若 $\delta < 0$，则 $p_1 - p_2 - \delta > 0$；

若 $\delta > 0$，则 $p_1 - p_2 - \delta < 0$。

$$
Power = 1 - \Phi\left(\frac{z_{1-\alpha} \sqrt{\bar{p}(1-\bar{p}) \left(\frac{1}{n_1} + \frac{1}{n_2}\right)} - \left|p_1-p_2-\delta\right| + \frac{1}{2}\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}
                           {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
                \right)
$$

## Z-Test Unpooled {#z-test-unpooled}

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 - \delta}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 - \delta}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
$$

根据中心极限定理，当 $n_1$ 和 $n_2$ 较大时，满足：

$$
\frac{(\hat{p}_1 - \hat{p}_2) - (p_1 - p_2)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

进而有：

$$
\begin{align}
z' & = \frac{\left(\hat{p}_1 - \hat{p}_2\right) - \left(p_1 - p_2\right) + \left(p_1 - p_2 - \delta\right)}
            {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \\
   & = \frac{\left(\hat{p}_1 - \hat{p}_2\right) - \left(p_1 - p_2\right)}
            {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
       +
       \frac{\left(p_1 - p_2 - \delta\right)}
            {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \\
   & \xrightarrow{d}
       N\left(\frac{p_1 - p_2 - \delta}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}, \ 1\right)
\end{align}
$$

=== "$\delta < 0$"

    $$
    Power = P\left(z' > z_{1-\alpha}\right)
          = 1 - \Phi\left(z_{1-\alpha} - \frac{p_1-p_2-\delta}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
          = 1 - \beta
    $$

=== "$\delta > 0$"

    $$
    Power = P\left(z' < -z_{1-\alpha}\right)
          = \Phi\left(-z_{1-\alpha} - \frac{p_1-p_2-\delta}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
          = 1 - \Phi\left(z_{1-\alpha} + \frac{p_1-p_2-\delta}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
          = 1 - \beta
    $$

在 $H_1$ 成立时：

若 $\delta < 0$，则 $p_1 - p_2 - \delta > 0$；

若 $\delta > 0$，则 $p_1 - p_2 - \delta < 0$。

$$
Power = 1 - \Phi\left(z_{1-\alpha} - \frac{\left|p_1-p_2-\delta\right|}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
$$

??? note "样本量公式推导"

    根据标准正态分布分位数的定义：

    $$
    z_{1-\alpha} - \frac{\left|p_1 - p_2 - \delta\right|}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} = z_\beta
    $$

    设 $n_1 = kn_2$，由上式可解出：

    $$
    n_2 = \frac{\left(z_{1-\alpha} + z_{1-\beta}\right)^2 \left[ \frac{1}{k}p_1(1-p_1) + p_2(1-p_2) \right]}{(p_1-p_2-\delta)^2}
    $$

    $$
    n_1 = k n_2
    $$

## Z-Test Unpooled 连续性校正 {#z-test-unpooled-cc}

在 $H_0$ 成立时，可构建 $z$ 统计量：

$$
z = \frac{\hat{p}_1 - \hat{p}_2 - \delta + c}
         {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

其中：

$$
c =
\begin{cases}
- \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right), & \delta < 0 \\
\frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right),   & \delta > 0
\end{cases}
$$

在 $H_1$ 成立时，可构建 $z'$ 统计量：

$$
z' = \frac{\hat{p}_1 - \hat{p}_2 - \delta + c}
          {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
$$

根据中心极限定理，当 $n_1$ 和 $n_2$ 较大时，满足：

$$
\frac{(\hat{p}_1 - \hat{p}_2) - (p_1 - p_2)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \sim N(0,1)
$$

进而有：

$$
\begin{align}
z' & = \frac{\left(\hat{p}_1 - \hat{p}_2\right) - \left(p_1 - p_2\right) + \left(p_1 - p_2 - \delta + c\right)}
            {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \\
   & = \frac{\left(\hat{p}_1 - \hat{p}_2\right) - \left(p_1 - p_2\right)}
            {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}
       +
       \frac{\left(p_1 - p_2 - \delta + c\right)}
            {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \\
   & \xrightarrow{d}
       N\left(\frac{p_1 - p_2 - \delta + c}
                   {\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}}, \ 1
        \right)
\end{align}
$$


=== "$\delta < 0$"

    $$
    Power = P\left(z' > z_{1-\alpha}\right)
          = 1 - \Phi\left(z_{1-\alpha} - \frac{p_1-p_2-\delta - \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
          = 1 - \beta
    $$

=== "$\delta > 0$"

    $$
    Power = P\left(z' < -z_{1-\alpha}\right)
          = \Phi\left(-z_{1-\alpha} - \frac{p_1-p_2-\delta + \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
          = 1 - \Phi\left(z_{1-\alpha} + \frac{p_1-p_2-\delta + \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
          = 1 - \beta
    $$

在 $H_1$ 成立时：

若 $\delta < 0$，则 $p_1 - p_2 - \delta > 0$；

若 $\delta > 0$，则 $p_1 - p_2 - \delta < 0$。

$$
Power = 1 - \Phi\left(z_{1-\alpha} - \frac{\left|p_1-p_2-\delta\right| - \frac{1}{2}\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}{\sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}} \right)
$$
