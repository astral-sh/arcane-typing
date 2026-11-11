# `arcane-typing`

This package provides experimental and advanced typing patterns for Python projects that use [ty](https://docs.astral.sh/ty/).

## Features

### Core utilities

- `TypeOf[expr]` can be used to obtain ty's inferred type for an expression in a type annotation or type alias.
- `Top[T]` can be used to refer to the top-materialization of `T`.
- `Bottom[T]` can be used to refer to the bottom-materialization of `T`.

### TypedDict

- `TypeOf[Keys[T]]` gives a union of string literals for the keys that can appear in a `TypedDict` `T`.

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
