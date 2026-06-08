# 两独立样本率差置信区间

两样本率分别用 $\hat{p}_1$ 和 $\hat{p}_2$ 表示，两组样本量分别用 $n_1$ 和 $n_2$ 表示。

## Pearson's Chi-Square {#pearson-chi-square}

=== "双侧置信区间"

    $$
    \begin{align}
    \text{L} & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} \\
    \text{U} & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}}
    \end{align}
    $$

    置信区间宽度：

    $$
    d = \operatorname{min}\left(\text{U}, 1\right) - \operatorname{max}\left(\text{L}, -1\right)
    $$

    ??? note "样本量的闭式解的分类讨论"

        设 $k = n_1 / n_2$

        ??? note "$\text{L} < -1, \text{U} \leqslant 1$"

            $$
            d = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} - (-1)
            $$

            可解出：

            $$
            \begin{align}
            n_2 & = \frac{z_{1-\alpha/2}^2 \left[\hat{p}_1(1-\hat{p}_1)/k + \hat{p}_2(1-\hat{p}_2)\right]}{\left[d-(\hat{p}_1-\hat{p}_2)-1\right]^2} \\
            n_1 & = k n_2
            \end{align}
            $$

        ??? note "$\text{L} < -1, \text{U} > 1$"

            $$
            d = 1 - (-1) = 2
            $$

            $d$ 与样本量无关，无法确定样本量。

        ??? note "$\text{L} \geqslant -1, \text{U} \leqslant 1$"

            $$
            d = 2 \cdot z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}}
            $$

            可解出：

            $$
            \begin{align}
            n_2 & = \frac{4 \cdot z_{1-\alpha/2}^2 \left[\hat{p}_1(1-\hat{p}_1)/k + \hat{p}_2(1-\hat{p}_2)\right]}{d^2} \\
            n_1 & = k n_2
            \end{align}
            $$

        ??? note "$\text{L} \geqslant -1, \text{U} > 1$"

            $$
            d = 1 - \left( \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} \right),
            $$

            可解出：

            $$
            \begin{align}
            n_2 & = \frac{z_{1-\alpha/2}^2 \left[\hat{p}_1(1-\hat{p}_1)/k + \hat{p}_2(1-\hat{p}_2)\right]}{\left[d+(\hat{p}_1-\hat{p}_2)-1\right]^2} \\
            n_1 & = k n_2
            \end{align}
            $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    \text{L} & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} \\
    \text{U} & = 1
    \end{align}
    $$

    从样本率差到置信下限的距离：

    $$
    d = (\hat{p}_1-\hat{p}_2) - \operatorname{max}\left(\text{L}, -1\right)
    $$

    ??? note "样本量的闭式解的分类讨论"

        设 $k = n_1 / n_2$

        ??? note "$\text{L} < -1$"

            $$
            d = \hat{p_1} - \hat{p}_2 - (-1)
            $$

            $d$ 与样本量无关，无法确定样本量。

        ??? note "$\text{L} \geqslant -1$"

            $$
            d = (\hat{p}_1-\hat{p}_2) - \left( \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} \right),
            $$

            可解出：

            $$
            \begin{align}
            n_2 & = \frac{z_{1-\alpha}^2 \left[\hat{p}_1(1-\hat{p}_1)/k + \hat{p}_2(1-\hat{p}_2)\right]}{d^2} \\
            n_1 & = k n_2
            \end{align}
            $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    \text{L} & = -1 \\
    \text{U} & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}}
    \end{align}
    $$

    从样本率差到置信上限的距离：

    $$
    d = \operatorname{min}\left(\text{U}, 1\right) - (\hat{p}_1-\hat{p}_2)
    $$

    ??? note "样本量的闭式解的分类讨论"

        设 $k = n_1 / n_2$

        ??? note "$\text{U} \leqslant 1$"

            $$
            d = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} - (\hat{p}_1 - \hat{p}_2)
            $$

            可解出：

            $$
            \begin{align}
            n_2 & = \frac{z_{1-\alpha}^2 \left[\hat{p}_1(1-\hat{p}_1)/k + \hat{p}_2(1-\hat{p}_2)\right]}{d^2} \\
            n_1 & = k n_2
            \end{align}
            $$

        ??? note "$\text{U} > 1$"

            $$
            d = 1 - (\hat{p}_1 - \hat{p}_2)
            $$

            $d$ 与样本量无关，无法确定样本量。


## Yate's Chi-Square with Continuity Correction {#yate-chi-square-cc}

=== "双侧置信区间"

    $$
    \begin{align}
    \text{L} & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} - \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right) \\
    \text{U} & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} + \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right)
    \end{align}
    $$

    置信区间宽度：

    $$
    d = \operatorname{min}\left(\text{U}, 1\right) - \operatorname{max}\left(\text{L}, -1\right)
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    \text{L} & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} - \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right) \\
    \text{U} & = 1
    \end{align}
    $$

    从样本率差到置信下限的距离：

    $$
    d = (\hat{p}_1-\hat{p}_2) - \operatorname{max}\left(\text{L}, -1\right)
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    \text{L} & = -1 \\
    \text{U} & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} + \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right)
    \end{align}
    $$

    从样本率差到置信上限的距离：

    $$
    d = \operatorname{min}\left(\text{U}, 1\right) - (\hat{p}_1-\hat{p}_2)
    $$


## Newcombe-Wilson

先使用 [Wilson Score][wilson-score] 方法计算两组各自的 Wilson 区间，再代入 Newcombe 混合误差框架构建率差的置信区间。

设 $\hat{p}_1$ 的 Wilson 区间为 $(L_1, U_1)$，$\hat{p_2}$ 的 Wilson 区间为 $(L_2, U_2)$。

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{p}_1 - \hat{p}_2 - \sqrt{\left(\hat{p}_1 - L_1\right)^2 + \left(U_2 - \hat{p}_2\right)^2} \\
    U & = \hat{p}_1 - \hat{p}_2 + \sqrt{\left(U_1 - \hat{p}_1\right)^2 + \left(\hat{p}_2 - L_2\right)^2}
    \end{align}
    $$

    置信区间宽度：

    $$
    d = U - L
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \hat{p}_1 - \hat{p}_2 - \sqrt{\left(\hat{p}_1 - L_1\right)^2 + \left(U_2 - \hat{p}_2\right)^2} \\
    U & = 1
    \end{align}
    $$

    从样本率差到置信下限的距离：

    $$
    d = (\hat{p}_1-\hat{p}_2) - L
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = -1 \\
    U & = \hat{p}_1 - \hat{p}_2 + \sqrt{\left(U_1 - \hat{p}_1\right)^2 + \left(\hat{p}_2 - L_2\right)^2}
    \end{align}
    $$

    从样本率差到置信上限的距离：

    $$
    d = U - (\hat{p}_1-\hat{p}_2)
    $$


## Newcombe-Wilson with Continuity Correction

先使用 [Wilson Score 连续性校正][wilson-score-cc] 方法计算两组各自的 Wilson 区间，再代入 Newcombe 混合误差框架构建率差的置信区间。

设 $\hat{p}_1$ 的 Wilson 区间为 $(L_1, U_1)$，$\hat{p_2}$ 的 Wilson 区间为 $(L_2, U_2)$。

!!! note "Wilson Score 连续性校正置信区间溢出问题"

    使用 Wilson Score 连续性校正方法计算单组率置信区间时，若 $L_i < 0$ 则截断为 $0$，若 $U_i > 1$ 则截断为 $1$。


=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{p}_1 - \hat{p}_2 - \sqrt{\left(\hat{p}_1 - L_1\right)^2 + \left(U_2 - \hat{p}_2\right)^2} \\
    U & = \hat{p}_1 - \hat{p}_2 + \sqrt{\left(U_1 - \hat{p}_1\right)^2 + \left(\hat{p}_2 - L_2\right)^2}
    \end{align}
    $$

    置信区间宽度：

    $$
    d = U - L
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \hat{p}_1 - \hat{p}_2 - \sqrt{\left(\hat{p}_1 - L_1\right)^2 + \left(U_2 - \hat{p}_2\right)^2} \\
    U & = 1
    \end{align}
    $$

    从样本率差到置信区间下限的距离：

    $$
    d = (\hat{p}_1-\hat{p}_2) - L
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = -1 \\
    U & = \hat{p}_1 - \hat{p}_2 + \sqrt{\left(U_1 - \hat{p}_1\right)^2 + \left(\hat{p}_2 - L_2\right)^2}
    \end{align}
    $$

    从样本率差到置信区间上限的距离：

    $$
    d = U - (\hat{p}_1-\hat{p}_2)
    $$


## Farrington and Manning's Score

基于得分检验，构建 FMD 统计量：

$$
z_{FMD} = \frac{\hat{p}_1 - \hat{p}_2 - \delta_0}{\sqrt{\frac{\tilde{p}_1(1-\tilde{p}_1)}{n_1} + \frac{\tilde{p}_2(1-\tilde{p}_2)}{n_2}}} \sim N(0, 1)
$$

通过反转该检验得到 $\delta_0$ 的范围，即为 $\hat{p}_1 - \hat{p}_2$ 的置信区间。

其中：

<!-- $$
\begin{align}
\tilde{p}_1 & = \tilde{p}_2 + \delta_0 \\
\tilde{p}_2 & = 2B\cos(A) - \frac{L_2}{3L_3} \\
A           & = \frac{1}{3} \left[\pi + \cos^{-1}\left(\frac{C}{B^3}\right)\right] \\
B           & = \operatorname{sign}(C) \sqrt{\frac{L_2^2}{9L_3^2} - \frac{L_1}{3L_3}} \\
C           & = \frac{L_2^3}{27L_3^3} - \frac{L_1L_2}{6L_3^2} + \frac{L_0}{2L_3} \\
L_0         & = n_2\hat{p}_2 \delta_0\left(1-\delta_0\right) \\
L_1         & = \left[n_2\delta_0 - (n_1 + n_2) - 2 n_2\hat{p}_2\right] \delta_0 + n_1\hat{p}_1 + n_2\hat{p}_2 \\
L_2         & = \left(n_1 + 2n_2\right)\delta_0 - (n_1 + n_2) - \left(n_1\hat{p}_1 + n_2\hat{p}_2\right) \\
L_3         & = n_1 + n_2 \\
m_1         & = x_{11} + x_{21} \\
x_{11}      & = n_1\hat{p}_1 \\
x_{21}      & = n_2\hat{p}_2
\end{align}
$$ -->

$$
\begin{align}
& \tilde{p}_1  = \tilde{p}_2 + \delta_0 \\
& \tilde{p}_2  = 2B\cos(A) - \frac{L_2}{3L_3} \\
& A            = \frac{1}{3} \left[\pi + \arccos\left(\frac{C}{B^3}\right)\right] \\
& B            = \operatorname{sign}(C) \sqrt{\frac{L_2^2}{9L_3^2} - \frac{L_1}{3L_3}} \\
& C            = \frac{L_2^3}{27L_3^3} - \frac{L_1L_2}{6L_3^2} + \frac{L_0}{2L_3} \\
& L_0          = x_{21} \delta_0(1-\delta_0) \\
& L_1          = \left[n_2\delta_0 - N - 2 x_{21}\right] \delta_0 + m_1 \\
& L_2          = \left(N + n_2\right)\delta_0 - N - m_1 \\
& L_3          = N \\
& m_1          = x_{11} + x_{21} \\
& N            = n_1 + n_2 \\
& x_{11}       = n_1\hat{p}_1 \\
& x_{21}       = n_2\hat{p}_2
\end{align}
$$


=== "双侧置信区间"

    $$
    \begin{align}
    z_{FMD}(L) & = z_{1 - \alpha/2} \\
    z_{FMD}(U) & = z_{\alpha/2}
    \end{align}
    $$

    置信区间宽度：

    $$
    d = U - L
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    z_{FMD}(L) & = z_{1 - \alpha} \\
    U          & = 1
    \end{align}
    $$

    从样本率差到置信下限的距离：

    $$
    d = (\hat{p}_1-\hat{p}_2) - L
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L          & = -1 \\
    z_{FMD}(U) & = z_{\alpha}
    \end{align}
    $$

    从样本率差到置信上限的距离：

    $$
    d = U - (\hat{p}_1-\hat{p}_2)
    $$
