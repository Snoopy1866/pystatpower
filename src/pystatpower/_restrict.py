# 定义约束


class Restrict:
    @staticmethod
    def is_alpha_gt_one_half(alpha: float) -> bool:
        """检查显著性水平是否超出 0.5。

        从 Neyman–Pearson lemma 和 Statistical Decision Theory 的角度看: 一个合理的检验不应该系统性地违背数据的似然结构。

        α > 0.5 的检验意味着在大多数情况下做出错误决策，因此任何这样的检验都可以通过“翻转拒绝规则”变成一个 α < 0.5 的更优检验。

        Args:
            alpha (float): 显著性水平

        Returns:
            _bool_: 若显著性水平超出 0.5，则返回True，否则返回 False
        """
        return alpha > 0.5

    @staticmethod
    def is_power_lt_alpha(alpha: float, power: float):
        """Neyman-Pearson 引理：检验的功效不应当低于显著性水平，即 1 - β ≥ α

        Args:
            alpha (float): 显著性水平
            power (float): 检验效能

        Returns:
            _bool_: 若检验效能低于显著性水平则返回 True，否则返回 False
        """
        return power < alpha
