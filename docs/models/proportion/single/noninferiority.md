# 单样本率非劣效检验

对于高优指标（$\delta < 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p - p_0 \leqslant \delta \\
H_1 &: p - p_0 \gt \delta
\end{align}
$$

对于低优指标（$\delta > 0$），统计学假设如下：

$$
\begin{align}
H_0 &: p - p_0 \geqslant \delta \\
H_1 &: p - p_0 \lt \delta
\end{align}
$$

$\delta$ 为非劣效界值，样本比例用 $\hat{p}$ 表示。

$$
\operatorname{E}(\hat{p}) = p
$$

以下推导过程在边界条件 $p - p_0 = \delta$ 下进行。


## Z-test using S(P0) {#z-test-p0}

在 $H_0$ 成立时，使用 $p_0$ 计算样本比例 $\hat{p}$ 的方差：

$$
\operatorname{Var}(\hat{p}) = \frac{p_0(1-p_0)}{n}
$$

??? warning "注意"
    这一传统做法并未考虑 $\delta$ 对样本比例方差造成的偏移。
    
    事实上，在 $H_0$ 成立时，即 $p - p_0 = \delta$ 时，$\hat{p}$ 的方差公式如下：

    $$
    \operatorname{Var}(\hat{p}) = \frac{(p_0+\delta)\left(1-(p_0+\delta)\right)}{n}
    $$

构建 $z$ 统计量：

$$
z = \frac{\hat{p} - p_0}{\sqrt{p_0(1-p_0)/n}} \sim N(0, 1)
$$

在 $H_1$ 成立时，构建 $z'$ 统计量：

$$
z' = \frac{\hat{p} - p_0}{\sqrt{p_0(1-p_0)/n}} \sim N()
$$

根据中心极限定理，当 $n$ 较大时，样本比例 $\hat{p}$ 满足：

$$
\sqrt{n}(\hat{p} - p_1) \xrightarrow{d} N(0, p_1(1-p_1))
$$

即 $\sqrt{n}\left(\hat{p} - p_1\right)$ 依分布收敛到均值为 $0$，方差为 $p_1(1-p_1)$ 的正态分布，进而有：

$$
z' = \frac{\sqrt{n}(\hat{p} - p_0)}{\sqrt{p_0(1-p_0)}} = \frac{\sqrt{n}(\hat{p} - p_1) + \sqrt{n}(p_1 - p_0)}{\sqrt{p_0(1-p_0)}} \xrightarrow{d} N\left( \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_0(1-p_0)}}, \frac{p_1(1-p_1)}{p_0(1-p_0)} \right)
$$

根据检验类型分类讨论：

!!! note "单侧检验，$p_1 > p_0$"

    $$
    \begin{align}
        P\left(z' > z_{1-\alpha} \right)
    & = 1 - \Phi\left( \frac{z_{1-\alpha} - \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_0(1-p_0)}}}{\sqrt{\frac{p_1(1-p_1)}{p_0(1-p_0)}}} \right) \\
    & = 1 - \Phi\left( \frac{z_{1-\alpha} \sqrt{p_0(1-p_0)} - \sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right) \\
    & = 1 - \beta
    \end{align}
    $$

!!! note "单侧检验，$p_1 < p_0$"

    $$
    \begin{align}
        P\left(z' < -z_{1-\alpha} \right)
    & = \Phi\left( \frac{-z_{1-\alpha} - \frac{\sqrt{n} (p_1-p_0)}{\sqrt{p_0(1-p_0)}}}{\sqrt{\frac{p_1(1-p_1)}{p_0(1-p_0)}}} \right) \\
    & = 1 - \Phi\left( \frac{z_{1-\alpha} \sqrt{p_0(1-p_0)} + \sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right) \\
    & = 1 - \beta
    \end{align}
    $$

!!! note "双侧检验，$p_1 \neq p_0$"

    $$
    \begin{align}
        P\left( \left| z' \right| > z_{1-\alpha/2} \right)
    & = P\left(z' > z_{1-\alpha/2} \right) + P\left(z' < -z_{1-\alpha/2} \right) \\
    & = 1 - \Phi\left( \frac{z_{1-\alpha/2} - \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_0(1-p_0)}}}{\sqrt{\frac{p_1(1-p_1)}{p_0(1-p_0)}}} \right)
          + \Phi\left( \frac{-z_{1-\alpha/2} - \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_0(1-p_0)}}}{\sqrt{\frac{p_1(1-p_1)}{p_0(1-p_0)}}} \right) \\
    & = 1 - \Phi\left( \frac{z_{1-\alpha/2} \sqrt{p_0(1-p_0)} - \sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right) +
        1 - \Phi\left( \frac{z_{1-\alpha/2} \sqrt{p_0(1-p_0)} + \sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right) \\
    & = 2 - \left[
                  \Phi\left( \frac{z_{1-\alpha/2} \sqrt{p_0(1-p_0)} - \sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right) +
                  \Phi\left( \frac{z_{1-\alpha/2} \sqrt{p_0(1-p_0)} + \sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right)
            \right] \\
    & = 1 - \beta
    \end{align}
    $$

!!! example "以单侧检验为例，推导样本量计算公式"

    根据标准正态分布分位数的定义：

    $$
    \frac{z_{1-\alpha} \sqrt{p_0(1-p_0)} - \sqrt{n}|p_1-p_0|}{\sqrt{p_1(1-p_1)}} = z_{\beta}
    $$

    可解出：

    $$
    n = \frac{\left( z_{1-\alpha} \sqrt{p_0(1-p_0)} + z_{1-\beta} \sqrt{p_1(1-p_1)} \right)^2}{\left( p_1 - p_0 \right)^2}
    $$


## Z-test using S(P0) 连续性校正 {#z-test-p0-cc}

在 [Z-test using S(P0)](#z-test-p0) 的基础上加入校正项 $c$：

$$
z = \frac{\hat{p} - p_0 + c}{\sqrt{p_0(1-p_0)/n}} \sim N(0, 1)
$$

其中：

$$
c =
\begin{cases}
- \frac{1}{2n} & , \text{if } \hat{p} \gt p_0 \\
  \frac{1}{2n} & , \text{if } \hat{p} \lt p_0 \\
  0            & , \text{if } \left| \hat{p} - p_0 \right| \le \frac{1}{2n}
\end{cases}
$$

在 $H_1$ 成立时，可构建统计量：

$$
z' = \frac{\hat{p} - p_0 + c}{\sqrt{p_0(1-p_0)/n}} = \frac{\sqrt{n}(\hat{p} - p_0 + c)}{\sqrt{p_0(1-p_0)}}
$$

根据中心极限定理，当 $n$ 较大时，样本比例 $\hat{p}$ 满足：

$$
\sqrt{n}(\hat{p} - p_1) \xrightarrow{d} N(0, p_1(1-p_1))
$$

即 $\sqrt{n}\left(\hat{p} - p_1\right)$ 依分布收敛到均值为 $0$，方差为 $p_1(1-p_1)$ 的正态分布，进而有：

$$
z' =  \frac{\sqrt{n}(\hat{p} - p_1) + \sqrt{n}(p_1 - p_0 + c)}{\sqrt{p_0(1-p_0)}} \xrightarrow{d} N\left( \frac{\sqrt{n}(p_1-p_0+c)}{\sqrt{p_0(1-p_0)}}, \frac{p_1(1-p_1)}{p_0(1-p_0)} \right)
$$

根据检验类型分类讨论：

!!! note "单侧检验，$p_1 > p_0$"

    $$
    \begin{align}
        P\left(z' > z_{1-\alpha} \right)
    & = 1 - \Phi\left( \frac{z_{1-\alpha} - \frac{\sqrt{n} \left(p_1-p_0-\frac{1}{2n} \right)}{\sqrt{p_0(1-p_0)}}}{\sqrt{\frac{p_1(1-p_1)}{p_0(1-p_0)}}} \right) \\
    & = 1 - \Phi\left( \frac{z_{1-\alpha} \sqrt{p_0(1-p_0)} - \sqrt{n} \left(p_1-p_0-\frac{1}{2n} \right)}{\sqrt{p_1(1-p_1)}} \right) \\
    & = 1 - \beta
    \end{align}
    $$

!!! note "单侧检验，$p_1 < p_0$"

    $$
    \begin{align}
        P\left(z' < -z_{1-\alpha} \right)
    & = \Phi\left( \frac{-z_{1-\alpha} - \frac{\sqrt{n} \left(p_1-p_0+\frac{1}{2n} \right)}{\sqrt{p_0(1-p_0)}}}{\sqrt{\frac{p_1(1-p_1)}{p_0(1-p_0)}}} \right) \\
    & = 1 - \Phi\left( \frac{z_{1-\alpha} + \frac{\sqrt{n} \left(p_1-p_0+\frac{1}{2n} \right)}{\sqrt{p_0(1-p_0)}}}{\sqrt{\frac{p_1(1-p_1)}{p_0(1-p_0)}}} \right) \\
    & = 1 - \Phi\left( \frac{z_{1-\alpha} \sqrt{p_0(1-p_0)} + \sqrt{n} \left(p_1-p_0+\frac{1}{2n} \right)}{\sqrt{p_1(1-p_1)}} \right) \\
    & = 1 - \beta
    \end{align}
    $$

!!! note "双侧检验，$p_1 \neq p_0$"

    $$
    \begin{align}
        P\left( \left| z' \right| > z_{1-\alpha/2} \right)
    & = P\left(z' > z_{1-\alpha/2} \right) + P\left(z' < -z_{1-\alpha/2} \right) \\
    & = 1 - \Phi\left( \frac{z_{1-\alpha/2} - \frac{\sqrt{n} \left(p_1-p_0-\frac{1}{2n} \right)}{\sqrt{p_0(1-p_0)}}}{\sqrt{\frac{p_1(1-p_1)}{p_0(1-p_0)}}} \right)
          + \Phi\left( \frac{-z_{1-\alpha/2} - \frac{\sqrt{n} \left(p_1-p_0+\frac{1}{2n} \right)}{\sqrt{p_0(1-p_0)}}}{\sqrt{\frac{p_1(1-p_1)}{p_0(1-p_0)}}} \right) \\
    & = 1 - \Phi\left( \frac{z_{1-\alpha/2} \sqrt{p_0(1-p_0)} - \sqrt{n} \left(p_1-p_0-\frac{1}{2n} \right)}{\sqrt{p_1(1-p_1)}} \right) +
        1 - \Phi\left( \frac{z_{1-\alpha/2} \sqrt{p_0(1-p_0)} + \sqrt{n} \left(p_1-p_0+\frac{1}{2n} \right)}{\sqrt{p_1(1-p_1)}} \right) \\
    & = 2 - \left[
                  \Phi\left( \frac{z_{1-\alpha/2} \sqrt{p_0(1-p_0)} - \sqrt{n} \left(p_1-p_0-\frac{1}{2n} \right)}{\sqrt{p_1(1-p_1)}} \right) +
                  \Phi\left( \frac{z_{1-\alpha/2} \sqrt{p_0(1-p_0)} + \sqrt{n} \left(p_1-p_0+\frac{1}{2n} \right)}{\sqrt{p_1(1-p_1)}} \right)
            \right] \\
    & = 1 - \beta
    \end{align}
    $$

??? example "以单侧检验为例，推导样本量计算公式"

    根据标准正态分布分位数的定义：

    $$
    \frac{z_{1-\alpha} \sqrt{p_0(1-p_0)} - \sqrt{n} \left( \left| p_1-p_0 \right| - \frac{1}{2n} \right)}{\sqrt{p_1(1-p_1)}} = z_{\beta} \Rightarrow z_{1-\alpha} \sqrt{p_0(1-p_0)} + z_{1-\beta} \sqrt{p_1(1-p_1)} = \sqrt{n} \left(| p_1 - p_0| - \frac{1}{2n}\right)
    $$

    令 $A = z_{1-\alpha} \sqrt{p_0(1-p_0)} + z_{1-\beta} \sqrt{p_1(1-p_1)}$，$\delta = | p_1 - p_0|$，则：

    $$
    A = \sqrt{n} \left(\delta - \frac{1}{2n}\right) \Rightarrow A\sqrt{n} = \delta  n - \frac{1}{2} \Rightarrow \delta n - A\sqrt{n} - \frac{1}{2} = 0
    $$

    令 $x = \sqrt{n}$，则：

    $$
    \delta x^2 - Ax - \frac{1}{2} = 0 \Rightarrow x = \frac{A \pm \sqrt{A^2 + 2\delta}}{2\delta}
    $$

    由于 $A \gt 0$，$\delta \gt 0$，故取正根：

    $$
    x = \frac{A + \sqrt{A^2 + 2\delta}}{2\delta}
    $$

    $$
    n = x^2 = \left( \frac{A + \sqrt{A^2 + 2\delta}}{2\delta} \right)^2 \tag{2.1}
    $$

    引入未经校正的样本量 $n'$：

    $$
    n' = \frac{A^2}{\delta^2}
    $$

    即 $A = \delta\sqrt{n'}$，代入式 $(2.1)$：

    $$
    \begin{align}
    n & = \left( \frac{\delta\sqrt{n'} + \sqrt{\delta^2 n' + 2\delta}}{2\delta} \right)^2 \\
    & = \frac{\delta^2 \left(\sqrt{n'} + \sqrt{n' + \frac{2}{\delta}}\right)^2}{4\delta^2} \\
    & = \frac{n'}{4} \left( 1 + \sqrt{1 + \frac{2}{\delta n'}}\right)^2
    \end{align}
    $$

    故：

    $$
    n = \frac{n'}{4} \left( 1 + \sqrt{1 + \frac{2}{|p_1 - p_0| n'}}\right)^2
    $$


## Z-test using S(Phat) {#z-test-phat}


$$
\begin{align}
H_0 & : p = p_0 \\
H_1 & : p \neq p_0
\end{align}
$$

在 $H_0$ 成立时：

$$
E(\hat{p} - p_0) = E(\hat{p}) - p_0 = p_0 - p_0 = 0
$$

$$
Var(\hat{p} - p_0) = Var(\hat{p}) = \frac{\hat{p}(1-\hat{p})}{n}
$$

构建 $z$ 统计量：

$$
z = \frac{\hat{p} - p_0}{\sqrt{\hat{p}(1-\hat{p})/n}} \sim N(0, 1)
$$

拒绝 $H_0$ 的条件：

$$
z > z_{1-\alpha/2}
$$

在 $H_1$ 成立时，可构建统计量:

$$
z' = \frac{\hat{p} - p_0}{\sqrt{\hat{p}\left(1 - \hat{p}\right) / n}} = \frac{\sqrt{n}\left(\hat{p} - p_0\right)}{\sqrt{\hat{p}\left(1 - \hat{p}\right)}}
$$

根据中心极限定理，当 $n$ 较大时，样本比例 $\hat{p}$ 满足：

$$
\sqrt{n}\left(\hat{p} - p_1\right) \xrightarrow{d} N\left(0, p_1(1-p_1)\right)
$$

即 $\sqrt{n}\left(\hat{p} - p_1\right)$ 依分布收敛到均值为 $0$，方差为 $p_1(1-p_1)$ 的正态分布，进而有：

$$
\sqrt{n}\left(\hat{p} - p_0\right) = \sqrt{n}\left(\hat{p} - p_1\right) + \sqrt{n}\left(p_1 - p_0\right) \xrightarrow{d} N\left(\sqrt{n}(p_1-p_0), p_1(1-p_1)\right)\tag{3.1}
$$

根据大数定律和连续映射定理：

$$
\sqrt{\hat{p}\left(1 - \hat{p}\right)} \xrightarrow{p} \sqrt{p_1\left(1-p_1\right)} \tag{3.2}
$$

由 $(3.1), (3.2)$，基于 Slutsky 定理：

$$
z' \xrightarrow{d} N\left(\frac{\sqrt{n}(p_1 - p_0)}{\sqrt{p_1(1-p_1)}}, 1\right)
$$

根据检验类型分类讨论：

!!! note "单侧检验，$p_1 > p_0$"

    $$
    P\left(z' > z_{1-\alpha} \right) = 1 - \Phi\left( z_{1-\alpha} - \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right) = 1 - \beta
    $$

!!! note "单侧检验，$p_1 < p_0$"

    $$
      P\left(z' < -z_{1-\alpha} \right)
    = \Phi\left( -z_{1-\alpha} - \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right)
    = 1 - \Phi\left( z_{1-\alpha} + \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right)
    = 1 - \beta
    $$

!!! note "双侧检验，$p_1 \neq p_0$"

    $$
    \begin{align}
        P\left( \left| z' \right| > z_{1-\alpha/2} \right)
    & = P\left(z' > z_{1-\alpha/2} \right) + P\left(z' < -z_{1-\alpha/2} \right) \\
    & = 1 - \Phi\left( z_{1-\alpha/2} - \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right)
          + \Phi\left( -z_{1-\alpha/2} - \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right) \\
    & = 1 - \Phi\left( z_{1-\alpha/2} - \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right) +
        1 - \Phi\left( z_{1-\alpha/2} + \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right) \\
    & = 2 - \left[
                  \Phi\left( z_{1-\alpha/2} - \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right) +
                  \Phi\left( z_{1-\alpha/2} + \frac{\sqrt{n}(p_1-p_0)}{\sqrt{p_1(1-p_1)}} \right)
            \right] \\
    & = 1 - \beta
    \end{align}
    $$

!!! example "以单侧检验为例，推导样本量计算公式"

    根据标准正态分布分位数的定义：

    $$
    z_{1-\alpha/2} - \frac{\sqrt{n} \left| p_1 - p_0 \right|}{\sqrt{p_1(1-p_1)}} = z_{\beta}
    $$

    可解出：

    $$
    n = \frac{\left( z_{1-\alpha/2} + z_{1-\beta} \right)^2 p_1(1-p_1)}{\left(p_1-p_0\right)^2}
    $$


## Z-test using S(Phat) 连续性校正 {z-test-phat-cc}

在 [Z-test using S(Phat)](#z-test-phat) 的基础上加入校正项 $c$：


$$
z = \frac{\hat{p} - p_0 + c}{\sqrt{\hat{p}(1-\hat{p})/n}} \sim N(0, 1)
$$

其中：

$$
c =
\begin{cases}
- \frac{1}{2n} & , \text{if } \hat{p} \gt p_0 \\
  \frac{1}{2n} & , \text{if } \hat{p} \lt p_0 \\
  0            & , \text{if } \left| \hat{p} - p_0 \right| \le \frac{1}{2n}
\end{cases}
$$

在 $H_1$ 成立时，可构建统计量：

$$
z' = \frac{\hat{p} - p_0 + c}{\sqrt{\hat{p}(1-\hat{p})/n}} = \frac{\sqrt{n}(\hat{p} - p_0 + c)}{\sqrt{\hat{p}(1-\hat{p})}}
$$

根据中心极限定理，当 $n$ 较大时，样本比例 $\hat{p}$ 满足：

$$
\sqrt{n}(\hat{p} - p_1) \xrightarrow{d} N(0, p_1(1-p_1))
$$

即 $\sqrt{n}\left(\hat{p} - p_1\right)$ 依分布收敛到均值为 $0$，方差为 $p_1(1-p_1)$ 的正态分布，进而有：

$$
\sqrt{n}\left(\hat{p} - p_0 + c\right) = \sqrt{n}\left(\hat{p} - p_1\right) + \sqrt{n}\left(p_1 - p_0 + c\right) \xrightarrow{d} N\left(\sqrt{n}(p_1 - p_0 + c), p_1(1-p_1)\right) \tag{4.1}
$$

根据大数定律和连续映射定理：

$$
\sqrt{\hat{p}\left(1 - \hat{p}\right)} \xrightarrow{p} \sqrt{p_1\left(1-p_1\right)} \tag{4.2}
$$

由 $(4.1), (4.2)$，基于 Slutsky 定理：

$$
z' \xrightarrow{d} N\left(\frac{\sqrt{n}(p_1 - p_0 + c)}{\sqrt{p_1(1-p_1)}}, 1\right)
$$


根据检验类型分类讨论：

!!! note "单侧检验，$p_1 > p_0$"

    $$
    P\left(z' > z_{1-\alpha} \right) = 1 - \Phi\left( z_{1-\alpha} - \frac{\sqrt{n}(p_1-p_0-\frac{1}{2n})}{\sqrt{p_1(1-p_1)}} \right) = 1 - \beta
    $$

!!! note "单侧检验，$p_1 < p_0$"

    $$
      P\left(z' < -z_{1-\alpha} \right)
    = \Phi\left( -z_{1-\alpha} - \frac{\sqrt{n}(p_1-p_0+\frac{1}{2n})}{\sqrt{p_1(1-p_1)}} \right)
    = 1 - \Phi\left( z_{1-\alpha} + \frac{\sqrt{n}(p_1-p_0+\frac{1}{2n})}{\sqrt{p_1(1-p_1)}} \right)
    = 1 - \beta
    $$

!!! note "双侧检验，$p_1 \neq p_0$"

    $$
    \begin{align}
        P\left( \left| z' \right| > z_{1-\alpha/2} \right)
    & = P\left(z' > z_{1-\alpha/2} \right) + P\left(z' < -z_{1-\alpha/2} \right) \\
    & = 1 - \Phi\left( z_{1-\alpha/2} - \frac{\sqrt{n}(p_1-p_0-\frac{1}{2n})}{\sqrt{p_1(1-p_1)}} \right)
          + \Phi\left( -z_{1-\alpha/2} - \frac{\sqrt{n}(p_1-p_0+\frac{1}{2n})}{\sqrt{p_1(1-p_1)}} \right) \\
    & = 1 - \Phi\left( z_{1-\alpha/2} - \frac{\sqrt{n}(p_1-p_0-\frac{1}{2n})}{\sqrt{p_1(1-p_1)}} \right) +
        1 - \Phi\left( z_{1-\alpha/2} + \frac{\sqrt{n}(p_1-p_0+\frac{1}{2n})}{\sqrt{p_1(1-p_1)}} \right) \\
    & = 2 - \left[
                  \Phi\left( z_{1-\alpha/2} - \frac{\sqrt{n}(p_1-p_0-\frac{1}{2n})}{\sqrt{p_1(1-p_1)}} \right) +
                  \Phi\left( z_{1-\alpha/2} + \frac{\sqrt{n}(p_1-p_0+\frac{1}{2n})}{\sqrt{p_1(1-p_1)}} \right)
            \right] \\
    & = 1 - \beta
    \end{align}
    $$

??? example "以单侧检验为例，推导样本量计算公式"

    根据标准正态分布分位数的定义：

    $$
    z_{1-\alpha} - \frac{\sqrt{n} \left( |p_1-p_0|-\frac{1}{2n} \right)}{\sqrt{p_1(1-p_1)}} = z_{\beta} \Rightarrow  \left(z_{1-\alpha} + z_{1-\beta}\right) \sqrt{p_1(1-p_1)} = \sqrt{n} \left(| p_1 - p_0| - \frac{1}{2n}\right)
    $$

    令 $A = \left(z_{1-\alpha} + z_{1-\beta}\right) \sqrt{p_1(1-p_1)}$，$\delta = | p_1 - p_0|$，则：

    $$
    A = \sqrt{n} \left(\delta - \frac{1}{2n}\right) \Rightarrow A\sqrt{n} = \delta  n - \frac{1}{2} \Rightarrow \delta n - A\sqrt{n} - \frac{1}{2} = 0
    $$

    令 $x = \sqrt{n}$，则：

    $$
    \delta x^2 - Ax - \frac{1}{2} = 0 \Rightarrow x = \frac{A \pm \sqrt{A^2 + 2\delta}}{2\delta}
    $$

    由于 $A \gt 0$，$\delta \gt 0$，故取正根：

    $$
    x = \frac{A + \sqrt{A^2 + 2\delta}}{2\delta}
    $$

    $$
    n = x^2 = \left( \frac{A + \sqrt{A^2 + 2\delta}}{2\delta} \right)^2 \tag{2.1}
    $$

    引入未经校正的样本量 $n'$：

    $$
    n' = \frac{A^2}{\delta^2}
    $$

    即 $A = \delta\sqrt{n'}$，代入式 $(2.1)$：

    $$
    \begin{align}
    n & = \left( \frac{\delta\sqrt{n'} + \sqrt{\delta^2 n' + 2\delta}}{2\delta} \right)^2 \\
    & = \frac{\delta^2 \left(\sqrt{n'} + \sqrt{n' + \frac{2}{\delta}}\right)^2}{4\delta^2} \\
    & = \frac{n'}{4} \left( 1 + \sqrt{1 + \frac{2}{\delta n'}}\right)^2
    \end{align}
    $$

    故：

    $$
    n = \frac{n'}{4} \left( 1 + \sqrt{1 + \frac{2}{|p_1 - p_0| n'}}\right)^2
    $$
