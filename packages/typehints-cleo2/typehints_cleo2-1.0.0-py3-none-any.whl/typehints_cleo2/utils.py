from __future__ import annotations
import typing as t


def to_bool(val: None | bool | int | float | str) -> bool:
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        if val == 0:
            return False
        return True
    if isinstance(val, float):
        if val == 0.0:
            return False
        return True
    if isinstance(val, str):
        val = val.strip().lower()
        if val == "" or val in ["false", "no", "n", "0"]:
            return False
        if val in ["true", "yes", "y", "1"]:
            return True

    raise ValueError(f"Unable to coerce value to boolean: {val}")


def nonecheck(value: t.Any, allow_none: bool = False) -> bool:
    if value is not None:
        return False
    if allow_none:
        return True
    raise TypeError("Received NoneType value but allow_none is False")


def typecheck(
    value: t.Any, expected: t.Type | tuple[t.Type, ...], allow_none: bool = False
) -> bool:

    none_check_passed = nonecheck(value, allow_none=allow_none)

    if none_check_passed or isinstance(value, expected):
        return True

    expected_type_str = expected.__name__ if not isinstance(expected, tuple) else str(expected)
    raise TypeError(
        f"Received value with wrong type: Expected Type: '{expected_type_str}' - "
        f"Actual Type: '{type(value).__name__}' - Value: '{value}'"
    )
