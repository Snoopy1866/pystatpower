from enum import Enum
from typing import TypeVar

from pystatpower.exception import EnumMemberNotExistError


T = TypeVar("T", bound=Enum)


def get_enum_by_name(enum_class: T, name: str) -> T:
    """根据枚举成员名的字符串表示获取枚举成员。

    Parameters
    ----------
    enum_class : Type[T]
        枚举类
    name : str
        枚举名称的字符串表示

    Returns
    -------
    T
        枚举成员
    """

    if name is None or isinstance(name, enum_class):
        return name
    else:
        try:
            return enum_class[name.upper()]
        except KeyError:
            raise EnumMemberNotExistError(enum_class, name)
