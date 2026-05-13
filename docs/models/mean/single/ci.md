# 单样本均值置信区间

## 正态分布 {#z-dist}

当总体方差 $\sigma^2$ 已知时，可使用正态分布构建置信区间。

$$
Z = \frac{\bar{X} - \mu}{\sigma/\sqrt{n}} \sim N(0, 1)
$$

=== "双侧置信区间"

    $$
    \text{Confidence Interval} = \left(\bar{X}-\frac{z_{1-\alpha/2}\sigma}{\sqrt{n}}, \ \bar{X}+\frac{z_{1-\alpha/2}\sigma}{\sqrt{n}}\right)
    $$

    设均值到置信限的距离为 $d$，则：

    $$
    d = \frac{z_{1-\alpha/2}\sigma}{\sqrt{n}}
    $$

    === "解出 $n$"

        $$
        n = \frac{z_{1-\alpha/2}^2\sigma^2}{d^2}
        $$

    === "解出 $\sigma$"

        $$
        \sigma = \frac{d\sqrt{n}}{z_{1-\alpha/2}}
        $$

=== "左侧置信区间"

    $$
    \text{Confidence Interval} = \left(-\infty, \ \bar{X}+\frac{z_{1-\alpha}\sigma}{\sqrt{n}}\right)
    $$

    设均值到置信限的距离为 $d$，则：

    $$
    d = \frac{z_{1-\alpha}\sigma}{\sqrt{n}}
    $$

    === "解出 $n$"

        $$
        n = \frac{z_{1-\alpha}^2\sigma^2}{d^2}
        $$

    === "解出 $\sigma$"

        $$
        \sigma = \frac{d\sqrt{n}}{z_{1-\alpha}}
        $$

=== "右侧置信区间"

    $$
    \text{Confidence Interval} = \left(\bar{X}-\frac{z_{1-\alpha}\sigma}{\sqrt{n}}, \ +\infty\right)
    $$

    设均值到置信限的距离为 $d$，则：

    $$
    d = \frac{z_{1-\alpha}\sigma}{\sqrt{n}}
    $$

    === "解出 $n$"

        $$
        n = \frac{z_{1-\alpha}^2\sigma^2}{d^2}
        $$

    === "解出 $\sigma$"

        $$
        \sigma = \frac{d\sqrt{n}}{z_{1-\alpha}}
        $$

!!! note ""
    若已知标准差 $\sigma = 1$ 时，均值到置信限的距离为 $d$，则当均值到置信限的距离为 $d'$ 时，标准差 $\sigma' = d'/d$，
    利用此关系可以简化 [`solve_std`][pystatpower.models.mean.single.ci.solve_std] 函数的实现，而不必使用 `brentq` 进行反解。

## *t* 分布 {#t-dist}

当总体方差 $\sigma^2$ 未知时，可使用 $t$ 分布构建置信区间。

$$
T = \frac{\bar{X} - \mu}{S/\sqrt{n}} \sim t(n - 1)
$$

=== "双侧置信区间"

    $$
    \text{Confidence Interval} = \left(\bar{X}-\frac{t_{1-\alpha/2,\ n-1}S}{\sqrt{n}}, \ \bar{X}+\frac{t_{1-\alpha/2,\ n-1}S}{\sqrt{n}}\right)
    $$

    设均值到置信限的距离为 $d$，则：

    $$
    d = \frac{t_{1-\alpha/2, \ n-1}S}{\sqrt{n}}
    $$

    === "解出 $S$"

        $$
        S = \frac{d\sqrt{n}}{t_{1-\alpha/2, \ n-1}}
        $$

=== "左侧置信区间"

    $$
    \text{Confidence Interval} = \left(-\infty, \ \bar{X}+\frac{t_{1-\alpha,\ n-1}S}{\sqrt{n}}\right)
    $$

    设均值到置信限的距离为 $d$，则：

    $$
    d = \frac{t_{1-\alpha, \ n-1}S}{\sqrt{n}}
    $$

    === "解出 $S$"

        $$
        S = \frac{d\sqrt{n}}{t_{1-\alpha, \ n-1}}
        $$

=== "右侧置信区间"

    $$
    \text{Confidence Interval} = \left(\bar{X}-\frac{t_{1-\alpha,\ n-1}S}{\sqrt{n}}, \ +\infty\right)
    $$

    设均值到置信限的距离为 $d$，则：

    $$
    d = \frac{t_{1-\alpha, \ n-1}S}{\sqrt{n}}
    $$

    === "解出 $S$"

        $$
        S = \frac{d\sqrt{n}}{t_{1-\alpha, \ n-1}}
        $$

!!! note ""
    若已知标准差 $S = 1$ 时，均值到置信限的距离为 $d$，则当均值到置信限的距离为 $d'$ 时，标准差 $S' = d'/d$，
    利用此关系可以简化 [`solve_std`][pystatpower.models.mean.single.ci.solve_std] 函数的实现，而不必使用 `brentq` 进行反解。
