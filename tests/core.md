# Core typing helpers

## `Intersection` and `Not`

Intersection and negation types can be spelled using `&` and `~` respectively, or by using the `Intersection` and `Not` type forms:

```py
from typing import TYPE_CHECKING, Sequence

from arcane_typing import Intersection, Not

class A: ...
class B: ...

def takes_intersection(obj: Intersection[A, B]) -> None:
    reveal_type(obj)  # revealed: A & B

class Both(A, B): ...

takes_intersection(Both())

takes_intersection(A())  # error: [invalid-argument-type]
takes_intersection(B())  # error: [invalid-argument-type]

def takes_negation(obj: Not[None]) -> None:
    reveal_type(obj)  # revealed: ~None

takes_negation(1)

takes_negation(None)  # error: [invalid-argument-type]
```

Make sure the annotation can be evaluated at runtime.

```py
from typing import get_type_hints

get_type_hints(takes_intersection)
get_type_hints(takes_negation)
```

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

## `FunctionLikeCallable`

This type describes Python functions with a specified call signature and exposes function attributes.

```py
from typing import TYPE_CHECKING

from arcane_typing import FunctionLikeCallable


def takes_function_like_callable(f: FunctionLikeCallable[[int, str], bytes]) -> None:
    reveal_type(f.__name__)  # revealed: str
    reveal_type(f.__qualname__)  # revealed: str
    reveal_type(f.__code__)  # revealed: CodeType
    reveal_type(f(1, "a"))  # revealed: bytes

    if TYPE_CHECKING:
        f("wrong", "a")  # error: [invalid-argument-type]
        f(1)  # error: [missing-argument]


def f(x: int, y: str) -> bytes:
    return b""


takes_function_like_callable(f)


def wrong(x: str, y: str) -> bytes:
    return b""


if TYPE_CHECKING:
    takes_function_like_callable(wrong)  # error: [invalid-argument-type]
```

Make sure the annotation can be evaluated at runtime.

```py
from typing import get_type_hints

get_type_hints(takes_function_like_callable)
```
