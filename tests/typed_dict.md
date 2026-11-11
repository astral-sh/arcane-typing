# TypedDict-related features

## `Keys` and `Values`

Use `Keys` for the union of literal keys and `Values` for the union of value types in a `TypedDict`.

```py
from typing_extensions import TypedDict

from arcane_typing import Keys, TypeOf, Values


class Movie(TypedDict, closed=True):
    title: str
    year: int


type MovieKey = TypeOf[Keys[Movie]]
type MovieValue = TypeOf[Values[Movie]]


def print_detail(movie: Movie, key: MovieKey) -> None:
    reveal_type(key)  # revealed: Literal["title", "year"]


movie: Movie = {"title": "Inception", "year": 2010}
print_detail(movie, "title")
print_detail(movie, "director")  # error: [invalid-argument-type]


def takes_value(value: MovieValue) -> None:
    reveal_type(value)  # revealed: str | int


takes_value(movie["year"])
takes_value(None)  # error: [invalid-argument-type]
```

This also works for generic `TypedDict`s:

```py
class Item[T](TypedDict, closed=True):
    name: str
    value: T


type ItemKeys = TypeOf[Keys[Item[int]]]
type ItemValues = TypeOf[Values[Item[int]]]


def _(key: ItemKeys, value: ItemValues) -> None:
    reveal_type(key)  # revealed: Literal["name", "value"]
    reveal_type(value)  # revealed: str | int
```

Empty closed `TypedDict`s correspond to an empty union, i.e. `Never`:

```py
class Empty(TypedDict, closed=True):
    pass


type EmptyKeys = TypeOf[Keys[Empty]]
type EmptyValues = TypeOf[Values[Empty]]


def _(key: EmptyKeys, value: EmptyValues) -> None:
    reveal_type(key)  # revealed: Never
    reveal_type(value)  # revealed: Never
```

An open `TypedDict` yields `object` for its values:

```py
class Open(TypedDict):
    name: str


type OpenValues = TypeOf[Values[Open]]


def _(value: OpenValues) -> None:
    reveal_type(value)  # revealed: object
```

A `TypedDict` with extra items also includes the type of those extra items in the union of its values:

```py
class Extra(TypedDict, extra_items=int):
    name: str


type ExtraValues = TypeOf[Values[Extra]]


def _(value: ExtraValues) -> None:
    reveal_type(value)  # revealed: str | int
```

Make sure the type forms can be evaluated at runtime:

```py
MovieKey.__value__
MovieValue.__value__
```
