# Core functionality and types

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

## `NonEmptyString`

`NonEmptyString` is an alias for `str` that excludes the empty string literal.

```py
from arcane_typing import NonEmptyString


def greet(name: NonEmptyString) -> str:
    return f"Hello, {name}!"


greet("Ada")
greet("")  # error: [invalid-argument-type]


def _(name: str) -> str:
    if name:
        return greet(name)
    return "Hello!"
```

## `NonStringSequence`

A `NonStringSequence` accepts sequences of strings and excludes bare strings.

```py
from typing import TYPE_CHECKING, Sequence

from arcane_typing import NonStringSequence


def join_words(words: NonStringSequence) -> str:
    return ", ".join(words)


assert join_words(["hello", "world"]) == "hello, world"
assert join_words(("hello", "world")) == "hello, world"


def _(words: Sequence[str]):
    if not isinstance(words, str):
        return join_words(words)


if TYPE_CHECKING:
    join_words("hello")  # error: [invalid-argument-type]
    join_words([42])  # error: [invalid-argument-type]
```

## `try_import_module`

This function can be used to attempt an optional import of a module and safely handle the case where the module is not available.
It is supposed to be used like this:

```py
from arcane_typing import try_import_module

if tomllib := try_import_module("tomllib"):
    reveal_type(tomllib)  # revealed: <module 'tomllib'>
    # revealed: def loads(s: str, /, *, parse_float: (str, /) -> Any = ...) -> dict[str, Any]
    reveal_type(tomllib.loads)
    assert tomllib.loads("answer = 42") == {"answer": 42}
else:
    print("Warning: tomllib not available")
```

Ideally, this code should be type-checked in an environment where the module is available (we use `tomllib` for demonstration purposes
here. It is always available in the test environment). The code should still type-check correctly
even if the module is not available. To demonstrate this, here is the same code snippet with a non-existent module:

```py
from arcane_typing import try_import_module

if othertoml := try_import_module("othertoml"):
    reveal_type(othertoml)  # revealed: ModuleType & ~AlwaysFalsy
    reveal_type(othertoml.loads)  # revealed: Any
    othertoml.loads("answer = 42") == {"answer": 42}
else:
    print("Warning: othertoml module not available")
```


The following section tests the actual runtime behavior:

```py
tomllib = try_import_module("tomllib")
assert tomllib is not None
assert hasattr(tomllib, "loads")

nonexistent = try_import_module("nonexistent")
assert nonexistent is None
```

## `static_assert`

`static_assert` can be used to enforce conditions at type-check time. At runtime, this is a normal assertion.

```py
from arcane_typing import static_assert

static_assert(1 + 1 == 2)

try:
    static_assert(1 + 1 == 3, "A message")  # error: [static-assert-error]
except AssertionError as exc:
    assert str(exc) == "A message"
else:
    raise AssertionError("static_assert did not raise")
```
