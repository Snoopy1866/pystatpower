# 单组率置信区间

## 渐进正态法

假设有效率 $p$ 服从二项分布，则 $E(p) = p$，$Var(p) = p(1-p)/n$，渐进正态法使用以下公式计算置信区间：

$$
p \pm z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}}
$$

使用上述公式计算的置信区间上下限在某些情况下可能会超出 $[0, 1]$ 范围，因此置信区间宽度的计算需要考虑边界问题：

$$
d = \min\left(p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}}, 1\right) - \max\left(p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}}, 0\right)
$$

从上述方程中解出样本量 $n$ 需要分类讨论：

??? note "情况 1. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \ge 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \gt 0$"
    $$
    d = 1 - \left(p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}}\right) \Rightarrow n = \frac{z_{1-\alpha/2}^2 p(1-p)}{\left(d+p-1\right)^2}
    $$

    将上式代入条件：

    $$
    p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \ge 1 \Rightarrow d \ge 2(1-p)
    $$

    $$
    p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \gt 0 \Rightarrow d \lt 1
    $$

    因此，

    $$
    n = \frac{z_{1-\alpha/2}^2 p(1-p)}{\left(d+p-1\right)^2} \ ,\  2(1-p) \le d \lt 1
    $$

??? note "情况 2. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \ge 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \le 0$"
    $$
    d = 1 - 0 = 1
    $$

    这种情况下置信区间宽度恒等于 1，无法求解样本量 $n$.

??? note "情况 3. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \lt 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \gt 0$"
    $$
    d = \left(p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}}\right) - \left(p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}}\right) \Rightarrow n = \frac{4 z_{1-\alpha/2}^2 p(1-p)}{d^2}
    $$

    将上式代入条件：

    $$
    p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \lt 1 \Rightarrow d \lt 2(1-p)
    $$

    $$
    p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \gt 0 \Rightarrow d \lt 2p
    $$

    因此，

    $$
    n = \frac{4 z_{1-\alpha/2}^2 p(1-p)}{d^2} \ ,\  d \lt \max\{2p, 2(1-p)\}
    $$

??? note "情况 4. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \lt 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \le 0$"
    $$
    d = \left(p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}}\right) - 0 \Rightarrow n = \frac{z_{1-\alpha/2}^2 p(1-p)}{(d-p)^2}\ 且 \ d \gt p
    $$

    将上式代入条件：

    $$
    p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \lt 1 \Rightarrow d \lt 1
    $$

    $$
    p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \le 0 \Rightarrow d \ge 2p
    $$

    因此，

    $$
    n = \frac{z_{1-\alpha/2}^2 p(1-p)}{(d-p)^2} \ ,\  2p \le d \lt 1
    $$

综上，

$$
n =
\begin{cases}
\frac{z_{1-\alpha/2}^2 p(1-p)}{\left(d+p-1\right)^2} &, 2(1-p) \le d \lt 1 \\
\frac{4 z_{1-\alpha/2}^2 p(1-p)}{d^2}                &, d \lt \max\{2p, 2(1-p)\} \\
\frac{z_{1-\alpha/2}^2 p(1-p)}{(d-p)^2}              &, 2p \le d \lt 1
\end{cases}
$$