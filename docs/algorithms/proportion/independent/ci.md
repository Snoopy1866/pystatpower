# 两独立样本率差置信区间

两样本率分别用 $\hat{p}_1$ 和 $\hat{p}_2$ 表示。

## _Pearson's Chi-Square_ {#pearson-chi-square}

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} \\
    U & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}}
    \end{align}
    $$

    定义置信区间的宽度为 $d$，则：

    $$
    d = \operatorname{min}\left(U, 1\right) - \operatorname{max}\left(L, -1\right)
    $$

    ??? note "样本量的闭式解的分类讨论"

        设 $k = n_1 / n_2$

        ??? note "$L < -1, U \leqslant 1$"

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

        ??? note "$L < -1, U > 1$"

            $$
            d = 1 - (-1) = 2
            $$

            $d$ 与样本量无关，无法确定样本量。

        ??? note "$L \geqslant -1, U \leqslant 1$"

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

        ??? note "$L \geqslant -1, U > 1$"

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
    L & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} \\
    U & = 1
    \end{align}
    $$

    定义样本率差到置信限的距离为 $d$，则：

    $$
    d = (\hat{p}_1-\hat{p}_2) - \operatorname{max}\left(L, -1\right)
    $$

    ??? note "样本量的闭式解的分类讨论"

        设 $k = n_1 / n_2$

        ??? note "$L < -1$"

            $$
            d = \hat{p}_1 - \hat{p}_2 - (-1)
            $$

            $d$ 与样本量无关，无法确定样本量。

        ??? note "$L \geqslant -1$"

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
    L & = -1 \\
    U & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}}
    \end{align}
    $$

    定义样本率差到置信限的距离为 $d$，则：

    $$
    d = \operatorname{min}\left(U, 1\right) - (\hat{p}_1-\hat{p}_2)
    $$

    ??? note "样本量的闭式解的分类讨论"

        设 $k = n_1 / n_2$

        ??? note "$U \leqslant 1$"

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

        ??? note "$U > 1$"

            $$
            d = 1 - (\hat{p}_1 - \hat{p}_2)
            $$

            $d$ 与样本量无关，无法确定样本量。

## _Yate's Chi-Square with Continuity Correction_ {#yate-chi-square-cc}

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} - \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right) \\
    U & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} + \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right)
    \end{align}
    $$

    定义置信区间的宽度为 $d$，则：

    $$
    d = \operatorname{min}\left(U, 1\right) - \operatorname{max}\left(L, -1\right)
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} - \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right) \\
    U & = 1
    \end{align}
    $$

    定义样本率差到置信限的距离为 $d$，则：

    $$
    d = (\hat{p}_1-\hat{p}_2) - \operatorname{max}\left(L, -1\right)
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = -1 \\
    U & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} + \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right)
    \end{align}
    $$

    定义样本率差到置信限的距离为 $d$，则：

    $$
    d = \operatorname{min}\left(U, 1\right) - (\hat{p}_1-\hat{p}_2)
    $$

## _Newcombe-Wilson_ {#newcombe-wilson}

先使用 [_Wilson Score_][wilson-score] 方法计算两组各自的 Wilson 区间，再代入 Newcombe 混合误差框架构建率差的置信区间。

设 $\hat{p}_1$ 的 Wilson 区间为 $(L_1, U_1)$，$\hat{p}_2$ 的 Wilson 区间为 $(L_2, U_2)$。

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{p}_1 - \hat{p}_2 - \sqrt{\left(\hat{p}_1 - L_1\right)^2 + \left(U_2 - \hat{p}_2\right)^2} \\
    U & = \hat{p}_1 - \hat{p}_2 + \sqrt{\left(U_1 - \hat{p}_1\right)^2 + \left(\hat{p}_2 - L_2\right)^2}
    \end{align}
    $$

    定义置信区间的宽度为 $d$，则：

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

    定义样本率差到置信限的距离为 $d$，则：

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

    定义样本率差到置信限的距离为 $d$，则：

    $$
    d = U - (\hat{p}_1-\hat{p}_2)
    $$

## _Newcombe-Wilson with Continuity Correction_ {#newcombe-wilson-cc}

先使用 [_Wilson Score With Continuity Correction_][wilson-score-cc] 方法计算两组各自的 Wilson 区间，再代入 Newcombe 混合误差框架构建率差的置信区间。

设 $\hat{p}_1$ 的 Wilson 区间为 $(L_1, U_1)$，$\hat{p}_2$ 的 Wilson 区间为 $(L_2, U_2)$，若 $L_i < 0$ 则截断为 $0$，若 $U_i > 1$ 则截断为 $1$。

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{p}_1 - \hat{p}_2 - \sqrt{\left(\hat{p}_1 - L_1\right)^2 + \left(U_2 - \hat{p}_2\right)^2} \\
    U & = \hat{p}_1 - \hat{p}_2 + \sqrt{\left(U_1 - \hat{p}_1\right)^2 + \left(\hat{p}_2 - L_2\right)^2}
    \end{align}
    $$

    定义置信区间的宽度为 $d$，则：

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

    定义样本率差到置信限的距离为 $d$，则：

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

    定义样本率差到置信限的距离为 $d$，则：

    $$
    d = U - (\hat{p}_1-\hat{p}_2)
    $$

## _Farrington and Manning's Score_ {#farrington-manning}

基于得分检验，构建 FMD 统计量：

$$
z_{FMD} = \frac{\hat{p}_1 - \hat{p}_2 - \delta_0}{\sqrt{\frac{\tilde{p}_1(1-\tilde{p}_1)}{n_1} + \frac{\tilde{p}_2(1-\tilde{p}_2)}{n_2}}} \sim N(0, 1)
$$

其中：

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

将 $z_{FMD}$ 视为关于 $\delta_0$ 的函数：

$$
f(\delta_0) = z_{FMD}(\delta_0)
$$

$\hat{p}_1 - \hat{p}_2$ 的置信区间端点可通过解方程得到。

=== "双侧置信区间"

    $$
    \begin{align}
    f(L) & = z_{1 - \alpha/2} \\
    f(U) & = z_{\alpha/2}
    \end{align}
    $$

    定义置信区间的宽度为 $d$，则：

    $$
    d = U - L
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    f(L) & = z_{1 - \alpha} \\
    U    & = 1
    \end{align}
    $$

    定义样本率差到置信限的距离为 $d$，则：

    $$
    d = (\hat{p}_1-\hat{p}_2) - L
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L    & = -1 \\
    f(U) & = z_{\alpha}
    \end{align}
    $$

    定义样本率差到置信限的距离为 $d$，则：

    $$
    d = U - (\hat{p}_1-\hat{p}_2)
    $$

## _Miettinen and Nurminen's Score_ {#miettinen-nurminen}

在 [_Farrington and Maning's Score_][farrington-manning] 的基础上增加校正因子 $N/(N-1)$，降低方差估计的偏倚。

基于得分检验，构建 MND 统计量：

$$
z_{MND} = \frac{\hat{p}_1 - \hat{p}_2 - \delta_0}{\sqrt{\left(\frac{\tilde{p}_1(1-\tilde{p}_1)}{n_1} + \frac{\tilde{p}_2(1-\tilde{p}_2)}{n_2}\right)\left(\frac{N}{N-1}\right)}} \sim N(0, 1)
$$

其中：

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

将 $z_{MND}$ 视为关于 $\delta_0$ 的函数：

$$
f(\delta_0) = z_{MND}(\delta_0)
$$

$\hat{p}_1 - \hat{p}_2$ 的置信区间端点可通过解方程得到。

=== "双侧置信区间"

    $$
    \begin{align}
    f(L) & = z_{1 - \alpha/2} \\
    f(U) & = z_{\alpha/2}
    \end{align}
    $$

    定义置信区间的宽度为 $d$，则：

    $$
    d = U - L
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    f(L) & = z_{1 - \alpha} \\
    U    & = 1
    \end{align}
    $$

    定义样本率差到置信限的距离为 $d$，则：

    $$
    d = (\hat{p}_1-\hat{p}_2) - L
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L    & = -1 \\
    f(U) & = z_{\alpha}
    \end{align}
    $$

    定义样本率差到置信限的距离为 $d$，则：

    $$
    d = U - (\hat{p}_1-\hat{p}_2)
    $$
