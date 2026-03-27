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

1. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \ge 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \gt 0$
2. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \ge 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \le 0$
3. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \lt 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \gt 0$
4. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \lt 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \lt 0$
