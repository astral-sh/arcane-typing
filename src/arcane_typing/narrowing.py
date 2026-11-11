def hasattr_of_type(obj: object, /, key: str, cls: type[object]) -> bool:
    try:
        value = getattr(obj, key)
    except AttributeError:
        return False

    return isinstance(value, cls)
