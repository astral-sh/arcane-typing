from typing import Iterable, LiteralString, Mapping, Protocol, ValuesView

from typing_extensions import TypeForm

class Keys:
    """`TypeOf[Keys[T]]` is a union of string literals representing the keys of the TypedDict `T`.

    Example:
        class Movie(TypedDict, closed=True):
            title: str
            year: int

        type MovieKey = TypeOf[Keys[Movie]]  # Literal["title", "year"]
    """

    def __class_getitem__[K: LiteralString](
        cls, schema: TypeForm[Mapping[str, object] & Iterable[K]], /
    ) -> K: ...

class _HasValues[V](Protocol):
    def values(self) -> ValuesView[V]: ...

class Values:
    """`TypeOf[Values[T]]` is the union of value types that can appear in the TypedDict `T`.

    A closed TypedDict with `str` and `int` fields yields `str | int`. A TypedDict
    with typed extra items includes their type. An open TypedDict yields `object`.
    """

    def __class_getitem__[V](
        cls, schema: TypeForm[Mapping[str, object] & _HasValues[V]], /
    ) -> V: ...
