# `arcane-typing`

This package provides advanced typing patterns for Python projects that use [ty](https://docs.astral.sh/ty/).

> [!WARNING]
> This project is highly experimental and currently makes no promises regarding backward compatibility.

## Features

### Core utilities

- `TypeOf[expr]` can be used to obtain ty's inferred type for an expression in a type annotation or type alias.
- `Top[T]` can be used to refer to the top-materialization of `T`.
- `Bottom[T]` can be used to refer to the bottom-materialization of `T`.

### TypedDict features

- `TypeOf[Keys[T]]` gives a union of string literals for the keys that can appear in a `TypedDict` `T`.

### Type Narrowing

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
