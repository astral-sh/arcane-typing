from types import UnionType
from typing import Sequence, get_args


def has_attr_of_type(obj: object, key: str, clsinfo: object, /) -> bool:
    try:
        value = getattr(obj, key)
    except AttributeError:
        return False

    return isinstance(value, _validate_clsinfo(clsinfo))


def is_sequence_of(obj: object, clsinfo: object, /) -> bool:
    clsinfo = _validate_clsinfo(clsinfo)
    return isinstance(obj, Sequence) and all(isinstance(item, clsinfo) for item in obj)


def _validate_clsinfo(clsinfo: object) -> type | UnionType:
    if not isinstance(clsinfo, (type, UnionType)) or (
        isinstance(clsinfo, UnionType)
        and any(not isinstance(member, type) for member in get_args(clsinfo))
    ):
        raise TypeError("Expected a class or a union of classes")

    return clsinfo
