## Theory

### 大数定律

当样本量 $n \Rightarrow \infty$ 时，样本比例 $\hat{p}$ 依概率收敛于总体比例 $p$，即

$$
\hat{p} \xrightarrow{P} p
$$

### 连续映射定理

若 $g$ 是连续函数，且 $X_n \xrightarrow{P} X$，则 $g(X_n) \xrightarrow{P} g(X)$

### 正态分布的性质

1. 若 $X \sim N(\mu, \sigma^2)$，则 $P(X \le x) = \Phi(\frac{x-\mu}{\sigma})$
2. 若 $X \sim N(\mu, \sigma^2)$，则 $P(X \ge x) = 1 - \Phi(\frac{x-\mu}{\sigma})$
3. $\Phi(x) = 1 - \Phi(-x)$