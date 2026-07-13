# 单样本均值优效性检验

样本均值用 $\hat{\mu}$ 表示，样本标准差用 $s$ 表示，总体标准差用 $\sigma$ 表示。

对于高优指标 ($\delta > 0$)，统计学假设如下：

$$
\begin{align}
H_0 &: \mu - \mu_0 \leqslant \delta \\
H_1 &: \mu - \mu_0 \gt \delta
\end{align}
$$

对于低优指标 ($\delta < 0$)，统计学假设如下：

$$
\begin{align}
H_0 &: \mu - \mu_0 \geqslant \delta \\
H_1 &: \mu - \mu_0 \lt \delta
\end{align}
$$

以下推导过程在边界条件 $\mu - \mu_0 = \delta$ 下进行。

--8<-- "docs/algorithms/mean/single/noninferiority.md:algorithm"

!!! quote "参考文献"

    1. Chow S C, Shao J, Wang H, et al. Sample size calculations in clinical research[M]. chapman and hall/CRC, 2017.
