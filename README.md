# `arcane-typing`

[![PyPI](https://img.shields.io/pypi/v/arcane-typing.svg)](https://pypi.org/project/arcane-typing/)

This package provides advanced typing patterns for Python projects that use [ty](https://docs.astral.sh/ty/).

> [!NOTE]
> This project is highly experimental and currently makes no promises regarding backward compatibility.

## Usage

Add [`arcane-typing`](https://pypi.org/project/arcane-typing/) as a dependency to your project:

```sh
uv add arcane-typing
```

Use one of its typing features in your code, for example:

```py
from arcane_typing import hasattr_of_type

def get_name(obj: object) -> str:
    if hasattr_of_type(obj, "name", str):
        return obj.name.upper()
    else:
        return "<unknown>"
```

Use [ty](https://docs.astral.sh/ty/) to type-check your code:

```sh
uv add --dev ty  # If you are not already using it

uv run ty check
```

## Features

### Core utilities

[Tests](https://github.com/astral-sh/arcane-typing/blob/main/tests/core.md)

- `TypeOf[expr]` can be used to obtain ty's inferred type for an expression in a type annotation or type alias.
- `Top[T]` can be used to refer to the [top-materialization](https://docs.astral.sh/ty/features/type-system/#top-and-bottom-materializations) of `T`.
- `Bottom[T]` can be used to refer to the [bottom-materialization](https://docs.astral.sh/ty/features/type-system/#top-and-bottom-materializations) of `T`.
- `FunctionLikeCallable[P, R]` works just like `Callable[P, R]` but also allows attributes like `__name__`, `__qualname__`, or `__code__` to be accessed.

### TypedDict features

[Tests](https://github.com/astral-sh/arcane-typing/blob/main/tests/typed_dict.md)

- `TypeOf[Keys[T]]` gives a union of string literals for the keys that can appear in a `TypedDict` `T`.

### Type Narrowing

[Tests](https://github.com/astral-sh/arcane-typing/blob/main/tests/narrowing.md)

- `hasattr_of_type(obj, "name", T)` narrows `obj.name` to type `T` if the attribute exists and if
  it is an instance of `T` (which can be a class or a union of classes)
- `is_sequence_of(obj, T)` checks that `obj` is a sequence and that every element is an instance of `T` (which can be a class or a union of classes). It narrows `obj` to `Sequence[T]` on success.

## Development

Use [uv](https://docs.astral.sh/uv/) to run the following development tasks:

```sh
# Linting and formatting
uv run ruff check
uv run ruff format --check

# Type checking
TY_UV=scripts uv run ty check

# Markdown tests
uv run mdtest.py
```
