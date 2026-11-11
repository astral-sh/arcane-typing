from typing import LiteralString, Protocol, Sequence, TypeIs, overload

from typing_extensions import TypeForm

class _HasAttr[K: LiteralString, V](Protocol):
    @overload
    def __getattr__(self, name: K, /) -> V: ...
    @overload
    def __getattr__(self, name: str, /) -> object: ...

def has_attr_of_type[K: LiteralString, V](
    obj: object, key: K, clsinfo: TypeForm[V], /
) -> TypeIs[_HasAttr[K, V]]:
    """Check whether `obj` has an attribute `key` that matches a class or union of classes."""

def is_sequence_of[T](obj: object, clsinfo: TypeForm[T], /) -> TypeIs[Sequence[T]]:
    """Check whether `obj` is a sequence whose elements match a class or union of classes."""
