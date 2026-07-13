# 两独立样本率优效性检验

两样本率分别用 $\hat{p}_1$ 和 $\hat{p}_2$ 表示，优效界值用 $\delta$ 表示。

对于高优指标（$\delta > 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p_1 - p_2 \leqslant \delta \\
H_1 &: p_1 - p_2 \gt \delta
\end{align}
$$

对于低优指标（$\delta < 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p_1 - p_2 \geqslant \delta \\
H_1 &: p_1 - p_2 \lt \delta
\end{align}
$$

以下推导过程在边界条件 $p_1 - p_2 = \delta$ 下进行。

--8<-- "docs/algorithms/proportion/independent/noninferiority.md:algorithm"

!!! quote "参考文献"

    1. Chow S C, Shao J, Wang H, et al. Sample size calculations in clinical research[M]. chapman and hall/CRC, 2017.
