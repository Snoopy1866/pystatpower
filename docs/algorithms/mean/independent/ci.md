# 两独立样本均值差置信区间

两组样本均值分别用 $\hat{\mu}_1$ 和 $\hat{\mu}_2$ 表示，两组样本标准差分别用 $s_1$ 和 $s_2$ 表示，两组样本量分别用 $n_1$ 和 $n_2$ 表示。

## 假设两组方差相等 {#equal_var}

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{\mu}_1 - \hat{\mu}_2 - t_{1-\alpha/2, n_1+n_2-2} \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2} \left(\frac{1}{n_1}+\frac{1}{n_2}\right)} \\
    U & = \hat{\mu}_1 - \hat{\mu}_2 + t_{1-\alpha/2, n_1+n_2-2} \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2} \left(\frac{1}{n_1}+\frac{1}{n_2}\right)}
    \end{align}
    $$

    定义均值差到置信限的距离为 $d$，则：

    $$
    d = t_{1-\alpha/2, n_1+n_2-2} \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2} \left(\frac{1}{n_1}+\frac{1}{n_2}\right)}
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \hat{\mu}_1 - \hat{\mu}_2 - t_{1-\alpha, n_1+n_2-2} \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2} \left(\frac{1}{n_1}+\frac{1}{n_2}\right)} \\
    U & = + \infty
    \end{align}
    $$

    定义均值差到置信限的距离为 $d$，则：

    $$
    d = t_{1-\alpha, n_1+n_2-2} \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2} \left(\frac{1}{n_1}+\frac{1}{n_2}\right)}
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = - \infty \\
    U & = \hat{\mu}_1 - \hat{\mu}_2 + t_{1-\alpha, n_1+n_2-2} \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2} \left(\frac{1}{n_1}+\frac{1}{n_2}\right)}
    \end{align}
    $$

    定义均值差到置信限的距离为 $d$，则：

    $$
    d = t_{1-\alpha, n_1+n_2-2} \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2} \left(\frac{1}{n_1}+\frac{1}{n_2}\right)}
    $$

## 假设两组方差不等 {#unequal_var}

两组方差不等时，不能使用一般的 $t$ 检验构建置信区间，应当使用近似 $t$ 检验，如 _Welch-Satterthwaite_ $t$ 检验。

_Welch-Satterthwaite_ $t$ 检验对自由度进行了校正：

$$
v = \frac{\left(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}\right)^2}{\frac{s_1^4}{n_1^2(n_1-1)} + \frac{s_2^4}{n_2^2(n_2-1)}}
$$

=== "双侧置信区间"

    $$
    \begin{align}
    L & = \hat{\mu}_1 - \hat{\mu}_2 - t_{1-\alpha/2, v} \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}} \\
    U & = \hat{\mu}_1 - \hat{\mu}_2 + t_{1-\alpha/2, v} \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}
    \end{align}
    $$

    定义均值差到置信限的距离为 $d$，则：

    $$
    d = t_{1-\alpha/2, v} \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}
    $$

=== "单侧置信下限区间"

    $$
    \begin{align}
    L & = \hat{\mu}_1 - \hat{\mu}_2 - t_{1-\alpha, v} \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}} \\
    U & = + \infty
    \end{align}
    $$

    定义均值差到置信限的距离为 $d$，则：

    $$
    d = t_{1-\alpha, v} \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}
    $$

=== "单侧置信上限区间"

    $$
    \begin{align}
    L & = - \infty \\
    U & = \hat{\mu}_1 - \hat{\mu}_2 + t_{1-\alpha, v} \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}
    \end{align}
    $$

    定义均值差到置信限的距离为 $d$，则：

    $$
    d = t_{1-\alpha, v} \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}
    $$

!!! quote "参考文献"

    1. JH Z. Zar JH. Dichotomous variables[J]. Biostatistical Analysis 5th ed. Upper Saddle River, NJ: Prentice-Hall, 2010: 557-558.
