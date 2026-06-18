# 两独立样本均值优效性检验

对于高优指标（$\delta \geqslant 0$），统计学假设如下：

$$
\begin{align}
H_0 &: \mu_1 - \mu_2 \leqslant \delta \\
H_1 &: \mu_1 - \mu_2 \gt \delta
\end{align}
$$

对于低优指标（$\delta \leqslant 0$），统计学假设如下：

$$
\begin{align}
H_0 &: \mu_1 - \mu_2 \geqslant \delta \\
H_1 &: \mu_1 - \mu_2 \lt \delta
\end{align}
$$

$\delta$ 为优效界值，两样本均值分别用 $\hat{\mu}_1$ 和 $\hat{\mu}_2$ 表示，两样本方差分别用 $s_1$ 和 $s_2$ 表示，两总体方差分别用 $\sigma_1$ 和 $\sigma_2$ 表示。

以下推导过程在边界条件 $\mu_1 - \mu_2 = \delta$ 下进行。

--8<-- "docs/algorithms/mean/independent/noninferiority.md:algorithm"