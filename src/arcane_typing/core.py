from importlib import import_module
from types import ModuleType
from typing import Any, Callable, LiteralString, Sequence


class _RuntimeSpecialForm:
    def __class_getitem__(cls, _argument: object, /) -> Any:
        return Any


class Intersection(_RuntimeSpecialForm): ...


class Not(_RuntimeSpecialForm): ...


class TypeOf(_RuntimeSpecialForm): ...


class Top(_RuntimeSpecialForm): ...


class Bottom(_RuntimeSpecialForm): ...


type FunctionLikeCallable[**P, R] = Callable[P, R]

type NonEmptyString = str
type NonStringSequence = Sequence[str]


def try_import_module(name: str, /) -> ModuleType | None:
    try:
        return import_module(name)
    except ImportError:
        return None


def static_assert(condition: object, msg: LiteralString | None = None) -> None:
    assert condition, msg
