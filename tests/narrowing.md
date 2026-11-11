# Narrowing helpers

## `hasattr_of_type`

This function can be used to check whether an object has an attribute with a specific type, allowing type narrowing based on the attribute's presence and type:

```py
from arcane_typing import hasattr_of_type


class Record:
    ordinary_attr: int


def check(record: Record) -> None:
    if hasattr_of_type(record, "dynamic_attr", str):
        reveal_type(record.ordinary_attr)  # revealed: int
        reveal_type(record.dynamic_attr)  # revealed: str


def check_union(record: Record) -> None:
    if hasattr_of_type(record, "dynamic_attr", int | str):
        reveal_type(record.dynamic_attr)  # revealed: int | str
```

Check the runtime functionality:

```py
from types import SimpleNamespace

assert hasattr_of_type(SimpleNamespace(value="hello"), "value", str)
assert not hasattr_of_type(SimpleNamespace(value=42), "value", str)
assert not hasattr_of_type(SimpleNamespace(), "value", str)

assert hasattr_of_type(SimpleNamespace(value="hello"), "value", int | str)
assert hasattr_of_type(SimpleNamespace(value=1), "value", int | str)
assert not hasattr_of_type(SimpleNamespace(value=None), "value", int | str)
```

## `is_sequence_of`

This function can be used to check whether an object is a sequence whose elements match a specific type, allowing type narrowing based on the sequence's element types:

```py
from typing import Sequence

from arcane_typing import is_sequence_of


def narrow_from_object(xs: object) -> None:
    if is_sequence_of(xs, int):
        reveal_type(xs)  # revealed: Sequence[int]
    if is_sequence_of(xs, int | str):
        reveal_type(xs)  # revealed: Sequence[int | str]


def narrow_from_sequence(xs: Sequence[object]) -> None:
    if is_sequence_of(xs, int):
        reveal_type(xs)  # revealed: Sequence[int]


def narrow_from_tuple(xs: tuple[object, ...]) -> None:
    if is_sequence_of(xs, int):
        reveal_type(xs)  # revealed: tuple[int, ...]


def negative_case(xs: Sequence[object] | None):
    if is_sequence_of(xs, int):
        reveal_type(xs)  # revealed: Sequence[int]
    else:
        # Sequence is still present because it could be a sequence of something else
        reveal_type(xs)  # revealed: (Sequence[object] & ~Sequence[int]) | None
```

Check the runtime functionality:

```py
assert is_sequence_of((1, 2), int)
assert not is_sequence_of((1, "two"), int)
assert is_sequence_of((1, "two"), int | str)
assert not is_sequence_of((1, None), int | str)
assert not is_sequence_of({1, 2}, int)
```
