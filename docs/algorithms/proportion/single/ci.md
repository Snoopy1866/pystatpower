# 单样本率置信区间

样本率用 $\hat{p}$ 表示，总体率用 $p$ 表示。

## _Simple Asymptotic_ {#normal-approx}

样本率 $\hat{p}$ 在大样本时，其分布近似服从正态分布：

$$
\hat{p} \ \dot{\sim} \ N\left(p, \frac{\hat{p}(1-\hat{p})}{n}\right)
$$

使用 $z$ 分布构建置信区间：

$$
z = \frac{\hat{p} - p}{\sqrt{\hat{p}(1-\hat{p})/n}} \sim N(0, 1)
$$

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{p} - z_{1-\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}} \\
    U & = \hat{p} + z_{1-\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}
    \end{align}
    $$

    定义置信区间的宽度为 $d$，则：

    $$
    d = \min(U, 1) - \max(L, 0)
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \hat{p} - z_{1-\alpha} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}} \\
    U & = 1
    \end{align}
    $$

    定义样本率到置信限的距离为 $d$，则：

    $$
    d = \hat{p} - \max(L, 0)
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = 0 \\
    U & = \hat{p} + z_{1-\alpha} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}
    \end{align}
    $$

    定义样本率到置信限的距离为 $d$，则：

    $$
    d = \min(U, 1) - \hat{p}
    $$

## _Simple Asymptotic with Continuity Correction_ {#normal-approx-cc}

在 [渐进正态法](#normal-approx) 的基础上添加校正项 $1/2n$：

$$
z = \frac{\hat{p} - p \pm \frac{1}{2n}}{\sqrt{\hat{p}(1-\hat{p})/n}} \sim N(0, 1)
$$

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{p} - z_{1-\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}} - \frac{1}{2n} \\
    U & = \hat{p} + z_{1-\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}} + \frac{1}{2n}
    \end{align}
    $$

    定义置信区间的宽度为 $d$，则：

    $$
    d = \min(U, 1) - \max(L, 0)
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \hat{p} - z_{1-\alpha} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}} - \frac{1}{2n} \\
    U & = 1
    \end{align}
    $$

    定义样本率到置信限的距离为 $d$，则：

    $$
    d = \hat{p} - \max(L, 0)
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = 0 \\
    U & = \hat{p} + z_{1-\alpha} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}} + \frac{1}{2n}
    \end{align}
    $$

    定义样本率到置信限的距离为 $d$，则：

    $$
    d = \min(U, 1) - \hat{p}
    $$

## _Wilson Score_ {#wilson-score}

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \frac{\left(2n\hat{p} + z_{1-\alpha/2}^2\right) - z_{1-\alpha/2} \sqrt{z_{1-\alpha/2}^2 + 4n\hat{p}(1-\hat{p})}}{2\left(n + z_{1-\alpha/2}^2\right)} \\
    U & = \frac{\left(2n\hat{p} + z_{1-\alpha/2}^2\right) + z_{1-\alpha/2} \sqrt{z_{1-\alpha/2}^2 + 4n\hat{p}(1-\hat{p})}}{2\left(n + z_{1-\alpha/2}^2\right)}
    \end{align}
    $$

    定义置信区间的宽度为 $d$，则：

    $$
    d = U - L
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \frac{\left(2n\hat{p} + z_{1-\alpha}^2\right) - z_{1-\alpha} \sqrt{z_{1-\alpha}^2 + 4n\hat{p}(1-\hat{p})}}{2\left(n + z_{1-\alpha}^2\right)} \\
    U & = 1
    \end{align}
    $$

    定义样本率到置信限的距离为 $d$，则：

    $$
    d = \hat{p} - L
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = 0 \\
    U & = \frac{\left(2n\hat{p} + z_{1-\alpha}^2\right) + z_{1-\alpha} \sqrt{z_{1-\alpha}^2 + 4n\hat{p}(1-\hat{p})}}{2\left(n + z_{1-\alpha}^2\right)}
    \end{align}
    $$

    定义样本率到置信限的距离为 $d$，则：

    $$
    d = U - \hat{p}
    $$

## _Wilson Score with Continuity Corrrection_ {#wilson-score-cc}

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \frac{\left(2n\hat{p} + z_{1-\alpha/2}^2 - 1\right) - z_{1-\alpha/2} \sqrt{z_{1-\alpha/2}^2 - \frac{1}{n} + 4n\hat{p}(1-\hat{p}) + 4\hat{p} - 2}}{2\left(n + z_{1-\alpha/2}^2\right)} \\
    U & = \frac{\left(2n\hat{p} + z_{1-\alpha/2}^2 + 1\right) + z_{1-\alpha/2} \sqrt{z_{1-\alpha/2}^2 - \frac{1}{n} + 4n\hat{p}(1-\hat{p}) - 4\hat{p} + 2}}{2\left(n + z_{1-\alpha/2}^2\right)}
    \end{align}
    $$

    定义置信区间的宽度为 $d$，则：

    $$
    d = U - L
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \frac{\left(2n\hat{p} + z_{1-\alpha}^2 - 1\right) - z_{1-\alpha} \sqrt{z_{1-\alpha}^2 - \frac{1}{n} + 4n\hat{p}(1-\hat{p}) + 4\hat{p} - 2}}{2\left(n + z_{1-\alpha}^2\right)} \\
    U & = 1
    \end{align}
    $$

    定义样本率到置信限的距离为 $d$，则：

    $$
    d = \hat{p} - L
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = 0 \\
    U & = \frac{\left(2n\hat{p} + z_{1-\alpha}^2 + 1\right) + z_{1-\alpha} \sqrt{z_{1-\alpha}^2 - \frac{1}{n} + 4n\hat{p}(1-\hat{p}) - 4\hat{p} + 2}}{2\left(n + z_{1-\alpha}^2\right)}
    \end{align}
    $$

    定义样本率到置信限的距离为 $d$，则：

    $$
    d = U - \hat{p}
    $$

??? note "Wilson Score 连续性校正置信区间宽度随样本量 $n$ 的变化"

    以 $p = 0.9$ 为例，绘制双侧 95% 置信区间宽度随样本量 $n$ 变化的图像如下：
    ![Wilson Score 连续性校正置信区间宽度图像](./figure-wilson-score-cc-ci.png)

    如果将 $n$ 视为连续型变量，则随着 $n$ 的增大，置信区间宽度先增大后减小，这可能会给数值求解带来一些麻烦。

    若设定置信区间宽度为 $0.8$，则理论上存在两个数值解，实际应取较大的解作为样本量估算结果。

    [brentq][scipy.optimize.brentq] 要求求根区间左右两端点处的函数值异号，此时可先用 [minimize_scalar][scipy.optimize.minimize_scalar] 求出区间内的极大值，将极大值点作为求根区间下限，再应用 [brentq][scipy.optimize.brentq] 进行数值求解。

## _Clopper-Pearson_ {#clpooer-pearson}

设 $F_{x;v_1,v_2}$ 表示自由度为 $v_1$ 和 $v_2$ 的 $F$ 分布的 $x$ 分位数。

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \left[ 1 + \frac{n - n\hat{p} + 1}{n\hat{p} F_{\alpha/2;\ 2n\hat{p},\ 2(n - n\hat{p} + 1)}} \right]^{-1} \\
    U & = \left[ 1 + \frac{n - n\hat{p}}{(n\hat{p} + 1) F_{1-\alpha/2;\ 2(n\hat{p} + 1), \ 2(n - n\hat{p})}} \right]^{-1}
    \end{align}
    $$

    定义置信区间的宽度为 $d$，则：

    $$
    d = U - L
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \left[ 1 + \frac{n - n\hat{p} + 1}{n\hat{p} F_{\alpha;\ 2n\hat{p},\ 2(n - n\hat{p} + 1)}} \right]^{-1} \\
    U & = 1
    \end{align}
    $$

    定义样本率到置信限的距离为 $d$，则：

    $$
    d = \hat{p} - L
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = 0 \\
    U & = \left[ 1 + \frac{n - n\hat{p}}{(n\hat{p} + 1) F_{1-\alpha;\ 2(n\hat{p} + 1), \ 2(n - n\hat{p})}} \right]^{-1}
    \end{align}
    $$

    定义样本率到置信限的距离为 $d$，则：

    $$
    d = U - \hat{p}
    $$
