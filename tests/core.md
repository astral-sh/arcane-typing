# Core typing helpers

## `TypeOf`

`TypeOf[expr]` can be used to obtain ty's inferred type for an expression in a type annotation or type alias:

```py
import collections

from arcane_typing import TypeOf


def takes_module(x: TypeOf[collections]):
    reveal_type(x)  # revealed: <module 'collections'>


type Three = TypeOf[1 + 2]


def _(three: Three):
    reveal_type(three)  # revealed: Literal[3]
```

Make sure the annotation can be evaluated at runtime.

```py
from typing import get_type_hints

get_type_hints(takes_module)
```

## `Top` and `Bottom`

```py
from typing import Any, Sequence

from arcane_typing import Bottom, Top


def takes_materializations(
    sequence_top: Top[Sequence[Any]],
    sequence_bottom: Bottom[Sequence[Any]],
    list_top: Top[list[Any]],
    list_bottom: Bottom[list[Any]],
) -> None:
    reveal_type(sequence_top)  # revealed: Sequence[object]
    reveal_type(sequence_bottom)  # revealed: Sequence[Never]
    reveal_type(list_top)  # revealed: Top[list[Any]]
    reveal_type(list_bottom)  # revealed: Bottom[list[Any]]
```

Make sure the annotations can be evaluated at runtime.

```py
from typing import get_type_hints

get_type_hints(takes_materializations)
```
