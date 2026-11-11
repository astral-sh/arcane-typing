from typing import Any


class _RuntimeSpecialForm:
    def __class_getitem__(cls, _argument: object, /) -> Any:
        return Any


class TypeOf(_RuntimeSpecialForm): ...


class Top(_RuntimeSpecialForm): ...


class Bottom(_RuntimeSpecialForm): ...
