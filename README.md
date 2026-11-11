# arcane-typing

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
from arcane_typing import has_attr_of_type

def get_name(obj: object) -> str:
    if has_attr_of_type(obj, "name", str):
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

### Core functionality and types

- [`Intersection[A, B]`](https://github.com/astral-sh/arcane-typing/blob/main/tests/core.md#intersection-and-not) is an [intersection type](https://docs.astral.sh/ty/features/type-system/#intersection-types) that represents values that are both of type `A` and type `B`.
- [`Not[T]`](https://github.com/astral-sh/arcane-typing/blob/main/tests/core.md#intersection-and-not) describes values that are [not of type `T`](https://docs.astral.sh/ty/features/type-system/#intersection-types).
- [`TypeOf[expr]`](https://github.com/astral-sh/arcane-typing/blob/main/tests/core.md#typeof) can be used to obtain ty's inferred type for an expression in a type annotation or type alias.
- [`Top[T]`](https://github.com/astral-sh/arcane-typing/blob/main/tests/core.md#top-and-bottom) can be used to refer to the [top-materialization](https://docs.astral.sh/ty/features/type-system/#top-and-bottom-materializations) of `T`.
- [`Bottom[T]`](https://github.com/astral-sh/arcane-typing/blob/main/tests/core.md#top-and-bottom) can be used to refer to the [bottom-materialization](https://docs.astral.sh/ty/features/type-system/#top-and-bottom-materializations) of `T`.
- [`FunctionLikeCallable[P, R]`](https://github.com/astral-sh/arcane-typing/blob/main/tests/core.md#functionlikecallable) works just like `Callable[P, R]` but also allows attributes like `__name__`, `__qualname__`, or `__code__` to be accessed.
- [`NonEmptyString`](https://github.com/astral-sh/arcane-typing/blob/main/tests/core.md#nonemptystring) excludes the empty string literal from `str`.
- [`NonStringSequence`](https://github.com/astral-sh/arcane-typing/blob/main/tests/core.md#nonstringsequence) excludes bare `str` from `Sequence[str]`.
- [`try_import_module(name)`](https://github.com/astral-sh/arcane-typing/blob/main/tests/core.md#try_import_module) returns the specific module type for a resolvable name, or `None` if it is not available.
- [`static_assert(condition[, msg])`](https://github.com/astral-sh/arcane-typing/blob/main/tests/core.md#static_assert) enforces a condition at type-check time.

### TypedDict-related features

- [`TypeOf[Keys[T]]`](https://github.com/astral-sh/arcane-typing/blob/main/tests/typed_dict.md#keys-and-values) gives a union of string literals for the keys that can appear in a `TypedDict` `T`.
- [`TypeOf[Values[T]]`](https://github.com/astral-sh/arcane-typing/blob/main/tests/typed_dict.md#keys-and-values) gives the union of value types that can appear in a `TypedDict` `T`.

### Type-narrowing helpers

- [`has_attr_of_type(obj, "name", T)`](https://github.com/astral-sh/arcane-typing/blob/main/tests/narrowing.md#has_attr_of_type) narrows `obj.name` to type `T` if the attribute exists and if
  it is an instance of `T` (which can be a class or a union of classes)
- [`has_item_of_type(obj, "key", T)`](https://github.com/astral-sh/arcane-typing/blob/main/tests/narrowing.md#has_item_of_type) narrows `obj["key"]` to `T` if the mapping contains the key and its value is an instance of `T`.
- [`is_sequence_of(obj, T)`](https://github.com/astral-sh/arcane-typing/blob/main/tests/narrowing.md#is_sequence_of) checks that `obj` is a sequence and that every element is an instance of `T` (which can be a class or a union of classes). It narrows `obj` to `Sequence[T]` on success.

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
