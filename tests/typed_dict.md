# TypedDict features

## `Keys`

`Keys` can be used to build a union of literals representing the keys of a `TypedDict`:

```py
from typing_extensions import TypedDict

from arcane_typing import Keys, TypeOf


class Movie(TypedDict, closed=True):
    title: str
    year: int


type MovieKey = TypeOf[Keys[Movie]]


def print_detail(movie: Movie, key: MovieKey) -> None:
    reveal_type(key)  # revealed: Literal["title", "year"]


movie: Movie = {"title": "Inception", "year": 2010}
print_detail(movie, "title")
print_detail(movie, "director")  # error: [invalid-argument-type]
```

This also works for generic `TypedDict`s:

```py
class Item[T](TypedDict, closed=True):
    name: str
    value: T


type ItemKeys = TypeOf[Keys[Item[int]]]


def _(key: ItemKeys) -> None:
    reveal_type(key)  # revealed: Literal["name", "value"]
```

And empty `TypedDict`s result in a `Never` type for their keys:

```py
class Empty(TypedDict, closed=True):
    pass


type EmptyKeys = TypeOf[Keys[Empty]]


def _(key: EmptyKeys) -> None:
    reveal_type(key)  # revealed: Never
```