from typing import LiteralString, Protocol, TypeIs, overload

class _HasAttr[K: LiteralString, V](Protocol):
    @overload
    def __getattr__(self, name: K, /) -> V: ...
    @overload
    def __getattr__(self, name: str, /) -> object: ...

def hasattr_of_type[K: LiteralString, V](
    obj: object, /, key: K, cls: type[V]
) -> TypeIs[_HasAttr[K, V]]:
    """Check whether `obj` has an attribute `key` and that it is an instance of `cls`."""
