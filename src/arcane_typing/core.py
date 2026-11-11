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


def static_assert(condition: object, msg: LiteralString | None = None) -> None:
    assert condition, msg


type NonEmptyString = str
type NonStringSequence = Sequence[str]
