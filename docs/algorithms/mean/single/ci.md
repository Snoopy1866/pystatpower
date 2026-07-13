# 单样本均值置信区间

样本均值用 $\hat{\mu}$ 表示，总体均值用 $\mu$ 表示，样本方差用 $s^2$ 表示，总体方差用 $\sigma^2$ 表示。

## _z_ 分布 {#z-dist}

当总体方差 $\sigma^2$ 已知时，可使用 _z_ 分布构建置信区间。

$$
z = \frac{\hat{\mu} - \mu}{\sigma/\sqrt{n}} \sim N(0, 1)
$$

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{\mu} - z_{1-\alpha/2} \frac{\sigma}{\sqrt{n}} \\
    U & = \hat{\mu} + z_{1-\alpha/2} \frac{\sigma}{\sqrt{n}}
    \end{align}
    $$

    定义均值到置信限的距离为 $d$，则：

    $$
    d = z_{1-\alpha/2} \frac{\sigma}{\sqrt{n}}
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \hat{\mu} - z_{1-\alpha} \frac{\sigma}{\sqrt{n}} \\
    U & = +\infty
    \end{align}
    $$

    定义均值到置信限的距离为 $d$，则：

    $$
    d = z_{1-\alpha} \frac{\sigma}{\sqrt{n}}
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = -\infty \\
    U & = \hat{\mu} + z_{1-\alpha} \frac{\sigma}{\sqrt{n}}
    \end{align}
    $$

    定义均值到置信限的距离为 $d$，则：

    $$
    d = z_{1-\alpha} \frac{\sigma}{\sqrt{n}}
    $$

## _t_ 分布 {#t-dist}

当总体方差 $\sigma^2$ 未知时，可使用 $t$ 分布构建置信区间。

$$
t = \frac{\hat{\mu} - \mu}{s/\sqrt{n}} \sim t(n - 1)
$$

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{\mu} - t_{1-\alpha/2,\ n-1} \frac{s}{\sqrt{n}} \\
    U & = \hat{\mu} + t_{1-\alpha/2,\ n-1} \frac{s}{\sqrt{n}}
    \end{align}
    $$

    定义均值到置信限的距离为 $d$，则：

    $$
    d = t_{1-\alpha/2,\ n-1} \frac{s}{\sqrt{n}}
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \hat{\mu} - t_{1-\alpha,\ n-1} \frac{s}{\sqrt{n}} \\
    U & = +\infty
    \end{align}
    $$

    定义均值到置信限的距离为 $d$，则：

    $$
    d = t_{1-\alpha,\ n-1} \frac{s}{\sqrt{n}}
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = -\infty \\
    U & = \hat{\mu} + t_{1-\alpha,\ n-1} \frac{s}{\sqrt{n}}
    \end{align}
    $$

    定义均值到置信限的距离为 $d$，则：

    $$
    d = t_{1-\alpha,\ n-1} \frac{s}{\sqrt{n}}
    $$

??? tip "给定参数求解对应标准差的技巧"

    以上述 *t* 分布双侧置信区间为例，需求解给定参数 $n$ 和 $d$ 下对应的标准差$s$。

    标准差为 $s$ 时，样本均值到置信限的距离为 $d$：

    $$
    d = t_{1-\alpha/2,\ n-1} \frac{s}{\sqrt{n}}
    $$

    标准差为 $s'$ 时，样本均值到置信限的距离为 $d'$：

    $$
    d' = t_{1-\alpha/2,\ n-1} \frac{s'}{\sqrt{n}}
    $$


    则有：

    $$
    \frac{d}{d'} = \frac{s}{s'} \Rightarrow s = s' \cdot \frac{d}{d'}
    $$

    当 $s' = 1$ 时：

    $$
    s = \frac{d}{d'}
    $$

    因此，可以先求解标准差 $s' = 1$ 时的 $d'$，再代入上述公式，即可得到标准差 $s$。

!!! quote "参考文献"

    1. JH Z. Zar JH. Dichotomous variables[J]. Biostatistical Analysis 5th ed. Upper Saddle River, NJ: Prentice-Hall, 2010: 557-558.
