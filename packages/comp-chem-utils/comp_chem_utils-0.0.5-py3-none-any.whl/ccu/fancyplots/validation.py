"""Classes, protocols, and functions for data validation.

In particular, this module defines the :class:`Validator` and
:class:`Serializer` protocols that are used to validate user input from GUI
widgets and serialize Python values for display in GUI widgets, respectively.
Validators return a boolean indicating the validity of an input with the
option to convert the input to the desired type.

.. admonition:: Example:
    A simple validator that only accepts the number 5

    .. code-block:: python

        from ccu.fancyplots.validation import ValidationError

        def simple_validator(value: Any, validate_only: bool = True):
            valid value == 5

            if validate_only:
                return valid

            if valid:
                return 5

            raise ValidationError("The value is not 5")

        simple_validator(5)
        True

:func:`validator_from_type` creates simple wrappers
around any callable that can accept a string and return a converted value. For
simple types (e.g., str, int, float), creating a validator is as simple
as:

.. code-block:: python

    from ccu.fancyplots.validation import validator_from_type

    validator = validator_from_type(str)

For creating Validators from type hints, this module defines the convenience
function :func:`type_hint_to_validator`:

.. code-block:: python

    from ccu.fancyplots.validation import type_hint_to_validator

    validator = type_hint_to_validator(list[str] | None, "")
    validator("1")
    False
    validator("1", validate_only=False)
    ...ValidationError: Unable to validate the value
    validator("1,2,3")
    True
    validator("1,2,3", validator_only=False)
    [1, 2, 3]
    # ``ccu.fancyplots`` interprets empty GUI fields as unset, so for
    # convenience, "" is a valid None type
    validator("", validator_only=False)
    None

Note:
    Validation is only supported for primitive values,
    tuples/lists of primitive values, and unions of either two:

    .. code-block:: python

        union_type = str | None  # okay
        union_type = tuple[str]  # okay
        union_type = int  # okay
        union_type = tuple[float] | None  # okay
        union_type = list[str]  # okay
        union_type = tuple[tuple[str]]  # not okay
        union_type = tuple[int | str]  # not okay

Note:
    **The order that types are specified in the union matters.**

    Validation is tried in left-to-right order. That is, if the type hint
    is ``str | int``, then the validation first attempts to convert the value
    into a string and then into an integer. This is especially important for
    unions involving strings, since every object can be converted into a
    string.

Custom validators can be constructed using some of the other utility methods.
For example, with :func:`string_to_sequence`, one can do:

>>> from ccu.fancyplots.validation import (
...     string_to_sequence,
...     validator_from_type,
... )
>>> sequence_from_type = string_to_sequence(
...     element_type=int, sequence_type=tuple, delimiter="-"
... )
>>> tuple_validator = validator_from_type(sequence_from_type)
>>> tuple_validator("1-2-3")
True
>>> tuple_validator("This should return False")
False
>>> tuple_validator("1-2-3", validate_only=False)
(1, 2, 3)

Simple unions can be handled as well:

>>> from ccu.fancyplots.validation import (
...     string_to_union,
...     validator_from_type,
... )
>>> union_from_type = string_to_union(int | str)
>>> union_validator = validator_from_type(union_from_type)
>>> union_validator("1")
True
>>> union_validator("Okay")
True
>>> union_validator("This should return False")
False
>>> union_validator("1", validate_only=False)
1
>>> union_validator("Okay", validate_only=False)
True

This module also provides a convenience Validator and Serializer,
:func:`no_validation_validator` and :func:`default_serializer`, respectively.

The :func:`highlight_and_warn` function is a handler for when invalid text is
entered into a :class:`.ttk.Entry`.

.. seealso:: :class:`~ccu.fancyplots.gui.frames.FancyFormatFrame`
"""

from collections.abc import Callable
import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from types import UnionType
from typing import Any
from typing import Generic
from typing import Literal
from typing import Protocol
from typing import TypeVar
from typing import Union
from typing import get_args
from typing import get_origin
from typing import overload

logger = logging.getLogger(__name__)


def highlight_and_warn(event: tk.Event) -> None:
    """Highlight the entry containing invalid data and warn the user.

    Args:
        event: The triggering event.

    """
    widget: ttk.Entry = event.widget
    widget.configure(style="Invalid.Fancy.TEntry")
    msg = f"'{widget.get()}' is not a valid value"
    logger.warning(msg)
    messagebox.showwarning("Number not recognized!", message=msg)


_T = TypeVar("_T")


class Validator(Protocol, Generic[_T]):
    """Callables which can validate and convert values.

    Adherents should raise a :class:`ValidationError` if `validate_only` is
    False and `value` is invalid.
    """

    @overload
    def __call__(self, value: str, validate_only: Literal[False]) -> _T: ...
    def __call__(self, value: str, validate_only: bool = True) -> bool:
        """Validate a value.

        Args:
            value: The value to validate.
            validate_only: Whether to only check the value for validity or
                also convert the value to a valid type.
        """


class ValidationError(ValueError):
    """Invalid value."""


@overload
def no_validation_validator(
    value: _T, validate_only: Literal[False]
) -> _T: ...
def no_validation_validator(
    value: _T, validate_only: bool = True
) -> bool | _T:
    """Always validate the value.

    Args:
        value: The value to validate.
        validate_only: Whether to only check the value for validity or
            also convert the value to a valid type.

    Returns:
        _description_
    """
    return validate_only or value


def validator_from_type(from_type: Callable[[str], _T]) -> Validator[_T]:
    """Create a :class:`Validator` from a type (or factory function).

    Args:
        from_type: A function that can accept a string as input and return
            an object of the desired type.

    Returns:
        A :class:`Validator` for objects of the type produced by `from_type`.

    """

    @overload
    def _validator(value: str, validate_only: bool = False) -> _T: ...
    def _validator(value: str, validate_only: bool = True) -> bool:
        valid_value = False
        try:
            value = from_type(value)
            valid_value = True
        except (TypeError, ValueError) as err:
            msg = "Unable to validate the value"
            raise ValidationError(msg) from err
        finally:
            if validate_only:
                # Silence error if only validating
                return valid_value  # noqa: B012

        return value

    return _validator


Primitive = TypeVar("Primitive", Any, str, int, float, bool, None)


def string_to_primitive(
    type_hint: type[Primitive],
) -> Callable[[str], Primitive]:
    """Return a function that parses a string into a Python primitive.

    Note that the empty string is parsed as None.

    Args:
        type_hint: One of ``str``, ``int``, ``float``, ``bool``, or ``None``.

    Returns:
        A :class:`Validator` capable of validating Python primitives from
        strings.

    """
    if type_hint is Any:
        return lambda x: no_validation_validator(x, False)

    if type_hint in (str, int, float, bool):
        return lambda x: type_hint(x)

    def _none_from_type(value: str) -> None:
        if value == "":
            return None
        msg = f"Unable to validate {value!r} as None"
        raise ValueError(msg)

    return _none_from_type


def string_to_sequence(
    element_type: Validator[_T],
    sequence_type: type[list] | type[tuple],
    delimiter: str = ",",
) -> Callable[[str], tuple[_T, ...]]:
    """Return a function that parses a string into a sequence.

    Args:
        element_type: The type into which elements of the sequence should be cast.
        sequence_type: The type of sequence to be constructed. Must be either
            ``list`` or ``tuple``.
        delimiter: A character used to split the string into a sequence.

    Returns:
        A function that can be supplied to :func:`validator_from_type` to
        produce a :class:`Validator`.

    """

    def _func(value: str) -> sequence_type[_T]:
        return sequence_type(
            element_type(x, validate_only=False)
            for x in value.split(delimiter)
        )

    return _func


def string_to_union(
    validators: list[Validator[_T]],
) -> Callable[[str], _T]:
    """Return a function that tries to validate/convert a string into a union.

    Args:
        validators: A :class:`ccu.fancyplots.validation.Validator` instances
            corresponding to the union.

    Returns:
        A Callable that can be used to convert a str into a member type
        of the union.
    """

    def _func(value: str) -> _T:
        for validator in validators:
            try:
                return validator(value, validate_only=False)
            except (ValueError, TypeError):
                logger.info(
                    f"Unable to validate value {value!r} with {validator!r}"
                )
        msg = f"Unable to validate value {value!r}"
        raise ValidationError(msg)

    return _func


def type_hint_to_validator(type_hint: type[_T], label: str) -> Validator[_T]:
    """Return a :class:`Validator` from a type hint.

    Args:
        type_hint: A bare (no annotations) type hint such as ``str``, ``int``,
            ``None``, ``tuple[int]``, ``int | None``.
        label: The name of the parameter to which the type hint belongs.

    Returns:
        A :class:`Validator` capable of validating a value against the
        type hint provided.

    Examples:
        >>> from ccu.fancyplots.validation import type_hint_to_validator
        >>> validator = type_hint_to_validator(int | str, "")
        >>> validator("1")
        True
        >>> validator("Okay")
        True
        >>> validator("This should return False")
        True
        >>> validator("1", validate_only=False)
        1
        >>> validator("Okay", validate_only=False)
        "Okay"

    """
    origin = get_origin(type_hint)

    if origin is None:
        # primitive type: int, str, float, bool
        from_type: Validator[type_hint] = string_to_primitive(type_hint)
    elif origin is Union or origin is UnionType:
        hints = get_args(type_hint)
        validators = []
        for hint in hints:
            validator = type_hint_to_validator(hint, "")
            validators.append(validator)

        from_type = string_to_union(validators)
    elif issubclass(origin, list | tuple):
        arg_type = get_args(type_hint)[0]
        element_type = type_hint_to_validator(arg_type, "")
        from_type = string_to_sequence(element_type, origin)
    else:
        msg = "Unsupported annotation type {0} for parameter {1}"
        raise NotImplementedError(msg.format(origin, label))

    return validator_from_type(from_type)


class Serializer(Protocol, Generic[_T]):
    """Serialize a value."""

    def __call__(self, value: _T) -> str:
        """Serialize a value.

        Args:
            value: The value to serialize.

        Returns:
            A string representation of the value.
        """


def default_serializer(value: _T, *, delimiter: str = ",") -> str:
    """Serialize values as strings.

    Args:
        value: The value to be serialized.
        delimiter: A character to be used to delimit list values.

    Returns:
        A string representation of ``value``.

    """
    if isinstance(value, list | tuple):
        return delimiter.join(str(x) for x in value)

    if value is None:
        return ""

    return str(value)
