# 两独立样本率差置信区间

两样本率分别用 $\hat{p}_1$ 和 $\hat{p}_2$ 表示，两组样本量分别用 $n_1$ 和 $n_2$ 表示。

## Pearson's Chi-Square {#pearson-chi-square}

=== "双侧置信区间"
    
    $$
    \begin{align}
    \text{L} & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} \\
    \text{U} & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}}
    \end{align}
    $$

    置信区间宽度：

    $$
    d = \operatorname{min}\left(\text{U}, 1\right) - \operatorname{max}\left(\text{L}, -1\right)
    $$

    ??? note "样本量的闭式解的分类讨论"
        
        设 $k = n_1 / n_2$

        ??? note "$\text{L} < -1, \text{U} \leqslant 1$"

            $$
            d = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} - (-1)
            $$

            可解出：

            $$
            \begin{align}
            n_2 & = \frac{z_{1-\alpha/2}^2 \left[\hat{p}_1(1-\hat{p}_1)/k + \hat{p}_2(1-\hat{p}_2)\right]}{\left[d-(\hat{p}_1-\hat{p}_2)-1\right]^2} \\
            n_1 & = k n_2
            \end{align}
            $$

        ??? note "$\text{L} < -1, \text{U} > 1$"

            $$
            d = 1 - (-1) = 2
            $$

            置信区间宽度恒等于 2，无法求解样本量。

        ??? note "$\text{L} \geqslant -1, \text{U} \leqslant 1$"

            $$
            d = 2 \cdot z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}}
            $$

            可解出：

            $$
            \begin{align}
            n_2 & = \frac{4 \cdot z_{1-\alpha/2}^2 \left[\hat{p}_1(1-\hat{p}_1)/k + \hat{p}_2(1-\hat{p}_2)\right]}{d^2} \\
            n_1 & = k n_2
            \end{align}
            $$

        ??? note "$\text{L} \geqslant -1, \text{U} > 1$"

            $$
            d = 1 - \left( \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} \right),
            $$

            可解出：

            $$
            \begin{align}
            n_2 & = \frac{z_{1-\alpha/2}^2 \left[\hat{p}_1(1-\hat{p}_1)/k + \hat{p}_2(1-\hat{p}_2)\right]}{\left[d+(\hat{p}_1-\hat{p}_2)-1\right]^2} \\
            n_1 & = k n_2
            \end{align}
            $$

=== "左侧置信区间"

    $$
    \begin{align}
    \text{L} & = -1 \\
    \text{U} & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}}
    \end{align}
    $$

    从样本率差到置信上限的距离：

    $$
    d = \operatorname{min}\left(\text{U}, 1\right) - (\hat{p}_1-\hat{p}_2)
    $$

    ??? note "样本量的闭式解的分类讨论"
        
        设 $k = n_1 / n_2$

        ??? note "$\text{U} \leqslant 1$"

            $$
            d = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} - (\hat{p}_1 - \hat{p}_2)
            $$

            可解出：

            $$
            \begin{align}
            n_2 & = \frac{z_{1-\alpha}^2 \left[\hat{p}_1(1-\hat{p}_1)/k + \hat{p}_2(1-\hat{p}_2)\right]}{d^2} \\
            n_1 & = k n_2
            \end{align}
            $$

        ??? note "$\text{U} > 1$"

            $$
            d = 1 - (-1) = 2
            $$

            置信区间宽度恒等于 2，无法求解样本量。

=== "右侧置信区间"

    $$
    \begin{align}
    \text{L} & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} \\
    \text{U} & = 1
    \end{align}
    $$

    从样本率差到置信下限的距离：

    $$
    d = (\hat{p}_1-\hat{p}_2) - \operatorname{max}\left(\text{L}, -1\right)
    $$

    ??? note "样本量的闭式解的分类讨论"

        设 $k = n_1 / n_2$

        ??? note "$\text{L} < -1$"

            $$
            d = 1 - (-1) = 2
            $$

            置信区间宽度恒等于 2，无法求解样本量。

        ??? note "$\text{L} \geqslant -1$"

            $$
            d = (\hat{p}_1-\hat{p}_2) - \left( \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} \right),
            $$

            可解出：

            $$
            \begin{align}
            n_2 & = \frac{z_{1-\alpha}^2 \left[\hat{p}_1(1-\hat{p}_1)/k + \hat{p}_2(1-\hat{p}_2)\right]}{d^2} \\
            n_1 & = k n_2
            \end{align}
            $$


## Yate's Chi-Square with Continuity Correction {#yate-chi-square-cc}

=== "双侧置信区间"

    $$
    \begin{align}
    \text{L} & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} - \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right) \\
    \text{U} & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} + \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right)
    \end{align}
    $$

    置信区间宽度：

    $$
    d = \operatorname{min}\left(\text{U}, 1\right) - \operatorname{max}\left(\text{L}, -1\right)
    $$

=== "左侧置信区间"

    $$
    \begin{align}
    \text{L} & = -1 \\
    \text{U} & = \hat{p}_1 - \hat{p}_2 + z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} + \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right)
    \end{align}
    $$

    从样本率差到置信上限的距离：

    $$
    d = \operatorname{min}\left(\text{U}, 1\right) - (\hat{p}_1-\hat{p}_2)
    $$

=== "右侧置信区间"

    $$
    \begin{align}
    \text{L} & = \hat{p}_1 - \hat{p}_2 - z_{1 - \alpha} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}} - \frac{1}{2} \left(\frac{1}{n_1} + \frac{1}{n_2}\right) \\
    \text{U} & = 1
    \end{align}
    $$

    从样本率差到置信下限的距离：

    $$
    d = (\hat{p}_1-\hat{p}_2) - \operatorname{max}\left(\text{L}, -1\right)
    $$
