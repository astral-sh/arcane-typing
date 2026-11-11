from typing import LiteralString, Protocol, Sequence, TypeGuard, TypeIs, overload

from typing_extensions import TypeForm

class _HasAttr[K: LiteralString, V](Protocol):
    @overload
    def __getattr__(self, name: K, /) -> V: ...
    @overload
    def __getattr__(self, name: str, /) -> object: ...

class _HasItem[K, V](Protocol):
    def __getitem__(self, key: K, /) -> V: ...

def has_attr_of_type[K: LiteralString, V](
    obj: object, key: K, clsinfo: TypeForm[V], /
) -> TypeIs[_HasAttr[K, V]]:
    """Check whether `obj` has an attribute `key` that matches a class or union of classes."""

@overload
def has_item_of_type[M, K: LiteralString, V](
    obj: M, key: K, clsinfo: TypeForm[V], /
) -> TypeGuard[M & _HasItem[K, V]]:
    """Check whether a mapping contains a key with a value of the given type."""

@overload
def has_item_of_type(obj: object, key: str, clsinfo: TypeForm[object], /) -> bool:
    """Check a mapping entry using a key known only at runtime."""

def is_sequence_of[T](obj: object, clsinfo: TypeForm[T], /) -> TypeIs[Sequence[T]]:
    """Check whether `obj` is a sequence whose elements match a class or union of classes."""
