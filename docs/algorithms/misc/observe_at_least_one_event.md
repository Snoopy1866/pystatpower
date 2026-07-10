# 至少观察到一例事件的检出能力

事件发生率用 $p$ 表示。

## 二项分布 {#bin}

设随机变量 $X$ 服从二项分布：

$$
P(X = k) = \mathrm{C}_n^k p^k (1-p)^{n-k}
$$

至少观察到一例事件的概率：

$$
P(X \geqslant 1) = 1 - P(X = 0) = 1 - (1-p)^n
$$

## 泊松分布 {#poisson}

设随机变量 $X$ 服从泊松分布：

$$
P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}
$$

其中，$\lambda = np$。

至少观察到一例事件的概率：

$$
P(X \geqslant 1) = 1 - P(X = 0) = 1 - e^{-\lambda} = 1 - e^{-np}
$$
