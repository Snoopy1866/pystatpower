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

    由上式可解出：

    $$
    n = \frac{z_{1-\alpha/2}^2\sigma^2}{d^2}
    $$

=== "左侧置信区间"

    $$
    \text{Confidence Interval} = \left(-\infty, \ \bar{X}+\frac{z_{1-\alpha}\sigma}{\sqrt{n}}\right)
    $$

    设均值到置信限的距离为 $d$，则：

    $$
    d = \frac{z_{1-\alpha}\sigma}{\sqrt{n}}
    $$

    由上式可解出：

    $$
    n = \frac{z_{1-\alpha}^2\sigma^2}{d^2}
    $$

=== "右侧置信区间"

    $$
    \text{Confidence Interval} = \left(\bar{X}-\frac{z_{1-\alpha}\sigma}{\sqrt{n}}, \ +\infty\right)
    $$

    设均值到置信限的距离为 $d$，则：

    $$
    d = \frac{z_{1-\alpha}\sigma}{\sqrt{n}}
    $$

    由上式可解出：

    $$
    n = \frac{z_{1-\alpha}^2\sigma^2}{d^2}
    $$

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

    由上式可解出：

    $$
    n = \frac{t_{1-\alpha/2, \ n-1}^2S^2}{d^2}
    $$

=== "左侧置信区间"

    $$
    \text{Confidence Interval} = \left(-\infty, \ \bar{X}+\frac{t_{1-\alpha/2,\ n-1}S}{\sqrt{n}}\right)
    $$

    设均值到置信限的距离为 $d$，则：

    $$
    d = \frac{t_{1-\alpha, \ n-1}S}{\sqrt{n}}
    $$

    由上式可解出：

    $$
    n = \frac{t_{1-\alpha, \ n-1}^2S^2}{d^2}
    $$

=== "右侧置信区间"

    $$
    \text{Confidence Interval} = \left(\bar{X}-\frac{t_{1-\alpha/2,\ n-1}S}{\sqrt{n}}, \ +\infty\right)
    $$

    设均值到置信限的距离为 $d$，则：

    $$
    d = \frac{t_{1-\alpha, \ n-1}S}{\sqrt{n}}
    $$

    由上式可解出：

    $$
    n = \frac{t_{1-\alpha, \ n-1}^2S^2}{d^2}
    $$
