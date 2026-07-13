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

!!! quote "参考文献"

    1. 郑青山,孙瑞元,陈志扬.新药临床试验最低例数规定的安全性评价[J].中国临床药理学与治疗学,2003,(3)354-355.
    2. 翟静波,郑文科,王辉,等.真实世界研究样本量估计的统计学考虑[J].世界中医药,2019,14(12)3123-3126.
    3. 施文,王永铭,程能能,等.非甾体抗炎药不良反应队列研究的样本量估计[J].中国临床药理学杂志,2002,(6)445-447.DOI:10.13699/j.cnki.1001-6821.2002.06.012.
    4. Hanley J A, Lippman-Hand A. If nothing goes wrong, is everything all right?: interpreting zero numerators[J]. Jama, 1983, 249(13): 1743-1745.
    5. Eypasch E, Lefering R, Kum C K, et al. Probability of adverse events that have not yet occurred: a statistical reminder[J]. Bmj, 1995, 311(7005): 619-620.
