from __future__ import annotations
import typing as t

from cleo.commands.command import Command

from .utils import to_bool
from .utils import nonecheck
from .utils import typecheck


class TypeHintedCommand(Command):
    """
    Cleo 2.x's Command.option() and Command.argument() methods return t.Any, which isn't helpful
    for type-hinting.
    This class adds type-hinted, type-enforced wrappers for these methods.
    """

    # ========
    # String

    def _get_value_str(
        self,
        *args,
        argument: bool = True,
        optional: bool = False,
        **kwargs,
    ) -> str:
        if argument:
            value = self.argument(*args, **kwargs)
            expected = str
        else:
            optional = True
            expected = tuple([str, bool])
            value = self.option(*args, **kwargs)
        typecheck(value, expected=expected, allow_none=optional)
        return value

    def option_str(self, *args, **kwargs) -> str | bool:
        return self._get_value_str(*args, argument=False, **kwargs)

    def argument_str(self, *args, **kwargs) -> str:
        return self._get_value_str(*args, argument=True, optional=False, **kwargs)

    def argument_str_optional(self, *args, **kwargs) -> str | None:
        return self._get_value_str(*args, argument=True, optional=True, **kwargs)

    # ========
    # Bool

    def _get_value_bool(
        self,
        *args,
        argument: bool = False,
        optional: bool = False,
        **kwargs,
    ) -> bool:
        if argument:
            value_any = self.argument(*args, **kwargs)
        else:
            optional = True
            value_any = self.option(*args, **kwargs)
        nonecheck(value_any, allow_none=optional)
        value: bool = to_bool(value_any)
        typecheck(value, expected=bool, allow_none=False)
        return value

    def option_bool(self, *args, **kwargs) -> bool:
        return self._get_value_bool(argument=False, *args, **kwargs)

    def argument_bool(self, *args, **kwargs) -> bool:
        return self._get_value_bool(argument=True, optional=False, *args, **kwargs)

    def argument_bool_optional(self, *args, **kwargs) -> bool:
        return self._get_value_bool(argument=True, optional=True, *args, **kwargs)

    # ========
    # Int

    def _get_value_int(
        self,
        *args,
        argument: bool = False,
        optional: bool = False,
        allow_non_zero: bool = True,
        allow_negative: bool = True,
        **kwargs,
    ) -> int:
        if argument:
            value = self.argument(*args, **kwargs)
            expected = int
        else:
            optional = True
            expected = tuple([int, bool])
            value = self.option(*args, **kwargs)
        typecheck(value, expected=expected, allow_none=optional)

        if not allow_non_zero and value == 0:
            raise ValueError(f"Received integer value == 0 but allow_non_zero is False")
        if not allow_negative and value < 0:
            raise ValueError(f"Received integer value < 0 but allow_negative is False")

        return value

    def option_int(self, *args, **kwargs) -> int:
        return self._get_value_int(*args, argument=False, **kwargs)

    def argument_int(self, *args, **kwargs) -> int:
        return self._get_value_int(*args, argument=True, optional=False, **kwargs)

    def argument_int_optional(self, *args, **kwargs) -> int:
        return self._get_value_int(*args, argument=True, optional=True, **kwargs)

    # ========
    # Float

    def _get_value_float(
        self,
        *args,
        argument: bool = False,
        optional: bool = False,
        allow_non_zero: bool = True,
        allow_negative: bool = True,
        **kwargs,
    ) -> float:
        if argument:
            value = self.argument(*args, **kwargs)
            expected = float
        else:
            optional = True
            expected = tuple([float, bool])
            value = self.option(*args, **kwargs)
        typecheck(value, expected=expected, allow_none=optional)

        if not allow_non_zero and value == 0:
            raise ValueError(f"Received float value == 0 but allow_non_zero is False")
        if not allow_negative and value < 0:
            raise ValueError(f"Received floateger value < 0 but allow_negative is False")

        return value

    def option_float(self, *args, **kwargs) -> float:
        return self._get_value_float(*args, argument=False, **kwargs)

    def argument_float(self, *args, **kwargs) -> float:
        return self._get_value_float(*args, argument=True, optional=False, **kwargs)

    def argument_float_optional(self, *args, **kwargs) -> float:
        return self._get_value_float(*args, argument=True, optional=True, **kwargs)

    # ========
    # List

    def _get_value_list(
        self,
        *args,
        argument: bool = False,
        optional: bool = False,
        **kwargs,
    ) -> list:
        if argument:
            value = self.argument(*args, **kwargs)
            expected = list
        else:
            optional = True
            expected = tuple([list, bool])
            value = self.option(*args, **kwargs)
        typecheck(value, expected=expected, allow_none=optional)
        return value

    def option_list(self, *args, **kwargs) -> list:
        return self._get_value_list(*args, argument=False, **kwargs)

    def argument_list(self, *args, **kwargs) -> list:
        return self._get_value_list(*args, argument=True, optional=False, **kwargs)

    def argument_list_optional(self, *args, **kwargs) -> list:
        return self._get_value_list(*args, argument=True, optional=True, **kwargs)
