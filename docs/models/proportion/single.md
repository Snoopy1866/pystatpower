# 单组率置信区间

## 渐进正态法

假设有效率 $p$ 服从二项分布，则 $E(p) = p$，$Var(p) = p(1-p)/n$，渐进正态法使用以下公式计算置信区间：

$$
p \pm z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}}
$$

使用上述公式计算的置信区间上下限在某些情况下可能会超出 $[0, 1]$ 范围，因此置信区间宽度的计算需要考虑边界问题：

$$
d = \min\left\lbrace p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}}, 1\right\rbrace - \max\left\lbrace p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}}, 0\right\rbrace
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

    这种情况下置信区间宽度恒等于 1，与样本量 $n$ 无关，无实际意义。

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
    n = \frac{4 z_{1-\alpha/2}^2 p(1-p)}{d^2} \ ,\  d \lt \max\left\lbrace 2p, 2(1-p) \right\rbrace
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
\frac{4 z_{1-\alpha/2}^2 p(1-p)}{d^2}                &, d \lt \max\left\lbrace 2p, 2(1-p) \right\rbrace \\
\frac{z_{1-\alpha/2}^2 p(1-p)}{(d-p)^2}              &, 2p \le d \lt 1
\end{cases}
$$

## 渐进正态法（连续性校正）

在 [渐进正态法](#渐进正态法) 的基础上添加校正项 $\frac{1}{2n}$，置信区间计算公式如下：

$$
\left(p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n}\ , \ p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{2n}\right)
$$

使用上述公式计算的置信区间上下限在某些情况下可能会超出 $[0, 1]$ 范围，因此置信区间宽度的计算需要考虑边界问题：

$$
d = \min\left\lbrace p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{2n}, 1 \right\rbrace - \max\left\lbrace p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n}, 0 \right\rbrace
$$

从上述方程中解出样本量 $n$ 需要分类讨论：

??? note "情况 1. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{2n} \ge 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n} \gt 0$"
    
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

??? note "情况 2. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{2n} \ge 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n} \le 0$"
    
    $$
    d = 1 - 0 = 1
    $$

    这种情况下置信区间宽度恒等于 1，与样本量 $n$ 无关，无实际意义。

??? note "情况 3. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{2n} \lt 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n} \gt 0$"
    
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

??? note "情况 4. $p + z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} + \frac{1}{2n} \lt 1, p - z_{1-\alpha/2} \sqrt{\frac{p(1-p)}{n}} - \frac{1}{2n} \le 0$"

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

## Clopper-Pearson

Clopper-Pearson 法使用以下公式计算置信区间：

$$
\left(\frac{np}{np + (n - np + 1)F_{1-\alpha/2; 2(n-np+1), 2np}} \ , \ \frac{(np + 1)F_{1-\alpha/2; 2(np+1), 2(n-np)}}{(n - np) + (np + 1)F_{1-\alpha/2; 2(np+1), 2(n-np)}}\right)
$$

置信区间宽度：

$$
d = \frac{(np + 1)F_{1-\alpha/2; 2(np+1), 2(n-np)}}{(n - np) + (np + 1)F_{1-\alpha/2; 2(np+1), 2(n-np)}} - \frac{np}{np + (n - np + 1)F_{1-\alpha/2; 2(n-np+1), 2np}}
$$

上述方程的求解需要使用数值方法。

### Wilson Score