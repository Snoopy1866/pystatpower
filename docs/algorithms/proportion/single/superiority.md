# 单样本率优效性检验

样本率用 $\hat{p}$ 表示，总体率用 $p$ 表示，优效界值用 $\delta$ 表示。

对于高优指标（$\delta > 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p - p_0 \leqslant \delta \\
H_1 &: p - p_0 \gt \delta
\end{align}
$$

对于低优指标（$\delta < 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p - p_0 \geqslant \delta \\
H_1 &: p - p_0 \lt \delta
\end{align}
$$

以下推导过程在边界条件 $p - p_0 = \delta$ 下进行。

--8<-- "docs/algorithms/proportion/single/noninferiority.md:algorithm"
