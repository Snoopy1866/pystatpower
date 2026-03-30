# 单组率置信区间

## 渐进正态法 {#normal-approx}

假设有效率 $p$ 服从二项分布，则 $E(p) = p$，$Var(p) = p(1-p)/n$，渐进正态法使用以下公式计算置信区间：2

$$
L = p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} \ , \ U = p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}}
$$

使用上述公式计算的置信区间上下限在某些情况下可能会超出 $[0, 1]$ 范围，因此置信区间宽度的计算需要考虑边界问题：

$$
d = \min\left\lbrace U, 1\right\rbrace - \max\left\lbrace L, 0\right\rbrace
$$

从上述方程中解出样本量 $n$ 需要分类讨论：

??? note "情况 1. $U \ge 1, L \gt 0$"

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

??? note "情况 2. $U \ge 1, L \le 0$"

    $$
    d = 1 - 0 = 1
    $$

    这种情况下置信区间宽度恒等于 1，与样本量 $n$ 无关，无实际意义。

??? note "情况 3. $U \lt 1, L \gt 0$"

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
    n = \frac{4 z_{1-\alpha/2}^2 p(1-p)}{d^2} \ ,\  d \lt \max\left\lbrace 2p, 2(1-p) \right\rbrace
    $$

??? note "情况 4. $U \lt 1, L \le 0$"

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
\frac{4 z_{1-\alpha/2}^2 p(1-p)}{d^2}                &, d \lt \max\left\lbrace 2p, 2(1-p) \right\rbrace \\
\frac{z_{1-\alpha/2}^2 p(1-p)}{(d-p)^2}              &, 2p \le d \lt 1
\end{cases}
$$

## 渐进正态法（连续性校正） {#normal-approx-cc}

在 [渐进正态法](#normal-approx) 的基础上添加校正项 $\frac{1}{2n}$，置信区间计算公式如下：

$$
L = p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n}\ , \ U = p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{2n}
$$

使用上述公式计算的置信区间上下限在某些情况下可能会超出 $[0, 1]$ 范围，因此置信区间宽度的计算需要考虑边界问题：

$$
d = \min\left\lbrace U, 1 \right\rbrace - \max\left\lbrace L, 0 \right\rbrace
$$

从上述方程中解出样本量 $n$ 需要分类讨论：

??? note "情况 1. $U \ge 1, L \gt 0$"

    $$
    d = 1 - \left(p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n}\right) \Rightarrow \frac{1}{2n} + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - (p + d - 1) = 0
    $$

    令 $x = \frac{1}{\sqrt{n}}$，$A = z_{1 - \alpha/2}\sqrt{p(1-p)}$，则：

    $$
    \frac{1}{2}x^2 + Ax - (p + d - 1) = 0
    $$

    解上述一元二次方程，取正根：

    $$
    x = -A + \sqrt{A^2 + 2(p + d - 1)}
    $$

    代入 $x = \frac{1}{\sqrt{n}}$，得：

    $$
    n = \frac{1}{x^2} = \frac{1}{\left(-A + \sqrt{A^2 + 2(p + d - 1)}\right)^2}
    $$

    将上式代入条件，且根据 $\frac{1}{2}x^2 + Ax = p + d - 1$：

    $$
    p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{2n} \ge 1 \Rightarrow p + Ax + \frac{1}{2}x^2 \ge 1 \Rightarrow d \ge 2(1-p)
    $$

    $$
    p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n} \gt 0 \Rightarrow p - Ax - \frac{1}{2}x^2 \gt 0 \Rightarrow d \lt 1
    $$

    因此，

    $$
    n = \frac{1}{\left(-A + \sqrt{A^2 + 2(p + d - 1)}\right)^2} \ , \ 2(1-p) \le d \lt 1
    $$

??? note "情况 2. $U \ge 1, L \le 0$"

    $$
    d = 1 - 0 = 1
    $$

    这种情况下置信区间宽度恒等于 1，与样本量 $n$ 无关，无实际意义。

??? note "情况 3. $U \lt 1, L \gt 0$"

    $$
    d = \left(p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{2n}\right) - \left(p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n}\right)
    $$

    化简:

    $$
    d = 2z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{n}
    $$

    令 $x = \frac{1}{\sqrt{n}}$，$A = z_{1 - \alpha/2}\sqrt{p(1-p)}$，则：

    $$
    x^2 + 2Ax - d = 0
    $$

    解上述一元二次方程，取正根：

    $$
    x = -A + \sqrt{A^2 + d}
    $$

    代入 $x = \frac{1}{\sqrt{n}}$，得：

    $$
    n = \frac{1}{x^2} = \frac{1}{\left(-A + \sqrt{A^2 + d}\right)^2}
    $$

    将上式代入条件，且根据 $x^2 + 2Ax = d$：

    $$
    p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{2n} \lt 1 \Rightarrow p + Ax + \frac{1}{2}x^2 \lt 1 \Rightarrow d \lt 2(1-p)
    $$

    $$
    p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n} \gt 0 \Rightarrow p - Ax - \frac{1}{2}x^2 \gt 0 \Rightarrow d \lt 2p
    $$

    因此，

    $$
    n = \frac{1}{\left(-A + \sqrt{A^2 + d}\right)^2} \ , \ d \lt \min\left\lbrace 2p, 2(1-p) \right\rbrace
    $$

??? note "情况 4. $U \lt 1, L \le 0$"

    $$
    d = \left(p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n}\right) - 0
    $$

    令 $x = \frac{1}{\sqrt{n}}$，$A = z_{1 - \alpha/2}\sqrt{p(1-p)}$，则：

    $$
    \frac{1}{2}x^2 + Ax + p - d = 0
    $$

    解上述一元二次方程，取正根：

    $$
    x = -A + \sqrt{A^2 - 2(p - d)}
    $$

    代入 $x = \frac{1}{\sqrt{n}}$，得：

    $$
    n = \frac{1}{x^2} = \frac{1}{\left(-A + \sqrt{A^2 - 2(p - d)}\right)^2}
    $$

    将上式代入条件，且根据 $\frac{1}{2}x^2 + Ax = d - p$：

    $$
    p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{2n} \lt 1 \Rightarrow p + Ax + \frac{1}{2}x^2 \lt 1 \Rightarrow d \lt 1
    $$

    $$
    p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n} \le 0 \Rightarrow p - Ax - \frac{1}{2}x^2 \le 0 \Rightarrow d \ge 2p
    $$

    因此，

    $$
    n = \frac{1}{\left(-A + \sqrt{A^2 - 2(p - d)}\right)^2} \ , \ 2p \le d \lt 1
    $$

综上，

$$
n =
\begin{cases}
\frac{1}{\left(-A + \sqrt{A^2 + 2(p + d - 1)}\right)^2} &, 2(1-p) \le d \lt 1 \\
\frac{1}{\left(-A + \sqrt{A^2 + d}\right)^2}            &, d \lt \min\left\lbrace 2p, 2(1-p) \right\rbrace \\
\frac{1}{\left(-A + \sqrt{A^2 - 2(p - d)}\right)^2}     &, 2p \le d \lt 1
\end{cases}
$$

其中，$A = z_{1 - \alpha/2}\sqrt{p(1-p)}$ 。

## Clopper-Pearson {#clpooer-pearson}

Clopper-Pearson 法使用以下公式计算置信区间：

$$
L = \frac{np}{np + (n - np + 1)F_{1-\alpha/2; 2(n-np+1), 2np}}
$$

$$
U = \frac{(np + 1)F_{1-\alpha/2; 2(np+1), 2(n-np)}}{(n - np) + (np + 1)F_{1-\alpha/2; 2(np+1), 2(n-np)}}
$$

置信区间宽度：

$$
d = U - L
$$

上述方程的求解需要使用数值方法。

## Wilson Score {#wilson-score}

Wilson Score 法使用以下公式计算置信区间：

$$
L = \frac{\left(2np + z_{1-\alpha/2}^2\right) - z_{1-\alpha/2} \sqrt{z_{1-\alpha/2}^2 + 4np(1-p)}}{2\left(n + z_{1-\alpha}^2\right)}
$$

$$
U = \frac{\left(2np + z_{1-\alpha/2}^2\right) + z_{1-\alpha/2} \sqrt{z_{1-\alpha/2}^2 + 4np(1-p)}}{2\left(n + z_{1-\alpha}^2\right)}
$$

置信区间宽度：

$$
d = U - L = \frac{z_{1-\alpha/2} \sqrt{z_{1-\alpha/2}^2 + 4np(1-p)}}{n + z_{1-\alpha}^2}
$$

整理可得：

$$
\begin{align}
            & \left(n + z_{1-\alpha/2}^2\right)^2 d^2 = z_{1-\alpha/2}^2 \left(z_{1-\alpha/2}^2 + 4np(1-p)\right) \\
\Rightarrow & \left(n^2 + 2z_{1-\alpha/2}^2 n + z_{1-\alpha/2}^4\right) d^2 = z_{1-\alpha/2}^4 + 4p(1-p)z_{1-\alpha/2}^2 n \\
\Rightarrow & d^2 n^2 + 2z_{1-\alpha/2}^2 \left(d^2 - 2p(1-p)\right) n + z_{1-\alpha/2}^4 (d^2 - 1) = 0
\end{align}
$$

设 $A = d^2$，$B = 2z_{1-\alpha/2}^2 \left(d^2 - 2p(1-p)\right)$，$C = z_{1-\alpha/2}^4 (d^2 - 1)$，则：

$$
n = \frac{-B \pm \sqrt{B^2 - 4AC}}{2A}
$$

此处应选取较大的那个根：

$$
n = \frac{-B + \sqrt{B^2 - 4AC}}{2A}
$$

??? note "判别式 $B^2 - 4AC \ge 0$ 的证明"
    $$
    \begin{align}
    B^2 - 4AC = & 4 z_{1-\alpha/2}^4 \left(d^2 - 2p(1-p)\right)^2 - 4 d^2 z_{1-\alpha/2}^4 (d^2 - 1) \\
              = & 4 z_{1-\alpha/2}^4 \left(d^4 - 4p(1-p)d^2 + 4p^2(1-p)^2 - d^4 + d^2\right) \\
              = & 4 z_{1-\alpha/2}^4 \left(d^2(1-4p(1-p)) + 4p^2(1-p)^2\right) \\
              = & 4 z_{1-\alpha/2}^4 \left(d^2 (1-2p)^2 + 4p^2(1-p)^2\right)
    \end{align}
    $$

    由于 $d^2 (1-2p)^2 \ge 0$，$4p^2(1-p)^2 \ge 0$ 恒成立，因此判别式 $B^2 - 4AC \ge 0$ 恒成立。

## Wilson Score 连续性校正 {#wilson-score-cc}

Wilson Score 连续性校正的置信区间公式如下：

$$
L = \frac{\left(2np + z_{1-\alpha/2}^2 - 1\right) - z_{1-\alpha/2} \sqrt{z_{1-\alpha/2}^2 - \frac{1}{n} + 4np(1-p) + 4p - 2}}{2\left(n + z_{1-\alpha}^2\right)}
$$

$$
U = \frac{\left(2np + z_{1-\alpha/2}^2 + 1\right) + z_{1-\alpha/2} \sqrt{z_{1-\alpha/2}^2 - \frac{1}{n} + 4np(1-p) - 4p + 2}}{2\left(n + z_{1-\alpha}^2\right)}
$$

置信区间宽度：

$$
d = U - L
$$

上述方程的求解需要使用数值方法。
