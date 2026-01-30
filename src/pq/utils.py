"""Shared utility functions."""

from typing import Any


def truncate_value(value: Any, max_length: int = 100) -> Any:
    """Truncate string representation of a value.

    Args:
        value: Value to truncate
        max_length: Maximum length of representation

    Returns:
        Truncated value or original if not a string
    """
    if isinstance(value, str):
        if len(value) > max_length:
            return value[: max_length - 3] + "..."
        return value
    elif isinstance(value, (dict, list, tuple)):
        str_repr = str(value)
        if len(str_repr) > max_length:
            return str_repr[: max_length - 3] + "..."
        return value
    return value


def get_type_name(value: Any) -> str:
    """Get human-readable type name.

    Args:
        value: Value to get type name for

    Returns:
        Type name string
    """
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "str"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "dict"
    elif isinstance(value, tuple):
        return "tuple"
    elif isinstance(value, set):
        return "set"
    else:
        return type(value).__name__
