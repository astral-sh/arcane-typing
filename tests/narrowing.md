# Type-narrowing helpers

## `has_attr_of_type`

This function can be used to check whether an object has an attribute with a specific type, allowing type narrowing based on the attribute's presence and type:

```py
from arcane_typing import has_attr_of_type


class Record:
    ordinary_attr: int


def check(record: Record) -> None:
    if has_attr_of_type(record, "dynamic_attr", str):
        reveal_type(record.ordinary_attr)  # revealed: int
        reveal_type(record.dynamic_attr)  # revealed: str


def check_union(record: Record) -> None:
    if has_attr_of_type(record, "dynamic_attr", int | str):
        reveal_type(record.dynamic_attr)  # revealed: int | str


def check_two(record: Record) -> None:
    if has_attr_of_type(record, "name", str) and has_attr_of_type(record, "count", int):
        reveal_type(record.name)  # revealed: str
        reveal_type(record.count)  # revealed: int
```

Check the runtime functionality:

```py
from types import SimpleNamespace

assert has_attr_of_type(SimpleNamespace(value="hello"), "value", str)
assert not has_attr_of_type(SimpleNamespace(value=42), "value", str)
assert not has_attr_of_type(SimpleNamespace(), "value", str)

assert has_attr_of_type(SimpleNamespace(value="hello"), "value", int | str)
assert has_attr_of_type(SimpleNamespace(value=1), "value", int | str)
assert not has_attr_of_type(SimpleNamespace(value=None), "value", int | str)
```

## `has_item_of_type`

Check whether a mapping contains a key with a value of a given type.

```py
from typing import Mapping

from arcane_typing import has_item_of_type


def check(payload: Mapping[str, object]) -> None:
    if has_item_of_type(payload, "name", str):
        reveal_type(payload["name"])  # revealed: str
        reveal_type(payload["count"])  # revealed: object


def check_union(payload: Mapping[str, object]) -> None:
    if has_item_of_type(payload, "name", str | int):
        reveal_type(payload["name"])  # revealed: str | int


def check_object(payload: object) -> None:
    if has_item_of_type(payload, "name", str):
        reveal_type(payload["name"])  # revealed: str
        payload["count"]  # error: [invalid-argument-type]


def check_two(payload: object) -> None:
    if has_item_of_type(payload, "name", str) and has_item_of_type(
        payload, "count", int
    ):
        reveal_type(payload["name"])  # revealed: str
        reveal_type(payload["count"])  # revealed: int
```

Check the runtime functionality.

```py
payload = {"name": "Ada", "count": 1}
assert has_item_of_type(payload, "name", str)
assert not has_item_of_type(payload, "missing", str)
assert not has_item_of_type(payload, "count", str)
assert has_item_of_type(payload, "count", str | int)
assert not has_item_of_type(payload, "count", str | bytes)
assert not has_item_of_type(None, "name", str)
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
