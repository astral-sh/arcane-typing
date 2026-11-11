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
```

Check the runtime result for matching, mismatched, and missing attributes.

```py
from types import SimpleNamespace

assert hasattr_of_type(SimpleNamespace(value="hello"), "value", str)
assert not hasattr_of_type(SimpleNamespace(value=42), "value", str)
assert not hasattr_of_type(SimpleNamespace(), "value", str)
```
