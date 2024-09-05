from enum import Enum


class EnumMemberNotExistError(Exception):
    """异常: 枚举成员不存在

    Attributes
    ----------
        enum : Enum
            枚举类
        value : str
            枚举成员的字符串表示
        message : str
            异常信息
    """

    def __init__(self, enum: Enum, value: str) -> None:
        self.enum = enum
        self.value = value
        self.message = f"Enum {enum} does not have member {value}"
        super().__init__(self.message)

    def __repr__(self) -> str:
        return self.message

    def __str__(self) -> str:
        return self.message


class ParameterError(Exception):
    """异常: 参数错误

    Attributes
    ----------
        message : str
            异常信息
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __repr__(self) -> str:
        return self.message

    def __str__(self) -> str:
        return self.message


class ParameterTypeError(ParameterError):
    """异常: 参数类型错误

    Attributes
    ----------
        message : str
            异常信息
    """

    pass


class ParameterValueNotInDomainError(ParameterError):
    """异常: 参数值不在定义域内

    Attributes
    ----------
        message : str
            异常信息
    """

    pass


class ParameterValueEmptyError(ParameterError):
    """异常: 参数值为空

    Attributes
    ----------
        message : str
            异常信息
    """

    pass


class TargetParameterError(ParameterError):
    """异常: 目标参数错误

    Attributes
    ----------
        message : str
            异常信息
    """

    pass


class TargetParameterNotExistError(TargetParameterError):
    """异常: 目标参数不存在

    Attributes
    ----------
        message : str
            异常信息
    """

    pass


class TargetParameterNotUniqueError(TargetParameterError):
    """异常: 目标参数不唯一

    Attributes
    ----------
        message : str
            异常信息
    """

    pass


class CalculationError(Exception):
    """异常: 计算错误

    Attributes
    ----------
        message : str
            异常信息
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __repr__(self) -> str:
        return self.message

    def __str__(self) -> str:
        return self.message


class CalculationSolutionNotFoundError(CalculationError):
    """异常: 无解

    Attributes
    ----------
        message : str
            异常信息
    """

    pass
