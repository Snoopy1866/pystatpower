from enum import Enum, EnumMeta, unique


class Option(EnumMeta):
    """自定义功效分析选项的枚举元类，用于支持大小写不敏感的枚举值访问。"""

    def __getitem__(self, name):
        if isinstance(name, str):
            return super().__getitem__(name.upper())
        else:
            return super().__getitem__(name)


@unique
class Alternative(Enum, metaclass=Option):
    """备择假设类型

    Attributes
    ----------
        TWO_SIDED : (int)
            双侧检验
        ONE_SIDED : (int)
            单侧检验
    """

    TWO_SIDED = 1
    ONE_SIDED = 2


@unique
class SearchDirection(Enum, metaclass=Option):
    """搜索方向

    Attributes
    ----------
        LESS : (int)
            向下搜索
        GREATER : (int)
            向上搜索
    """

    LESS = 1
    GREATER = 2
