from typing import Iterable, LiteralString, Mapping

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
