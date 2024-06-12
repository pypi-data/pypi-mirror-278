"""Validation-enabled GUI elements.

This module defines the :class:`FancyFormatFrame` class.
"""

import tkinter as tk
from tkinter import ttk
from typing import Any
from typing import Protocol
from typing import TypeVar

from ccu.fancyplots.gui.tooltip import Tooltip
from ccu.fancyplots.validation import Serializer
from ccu.fancyplots.validation import Validator
from ccu.fancyplots.validation import default_serializer
from ccu.fancyplots.validation import highlight_and_warn
from ccu.fancyplots.validation import no_validation_validator

_T = TypeVar("_T")


class UpdatableFrame(Protocol):
    """A GUI element whose children's state depend on their data."""

    def update_frames(self) -> None:
        """This function should update all children of the frame."""


class FancyFormatFrame(ttk.LabelFrame):
    """A ``ttk.LabelFrame`` for setting formatting parameters.

    Note that :class:`FancyFormatFrame` instances emit the <<Validate>> event.
    To listen for this event, handlers should be bound to the event using
    ``Misc.bind`` and ``Misc.event_add``.

    Attributes:
        entry: A :class:`ttk.Entry` in which a user specifies a formatting
            parameter.
        tooltip: A :class`.tooltip.Tooltip` displaying help text.
        validator: A :class:`.validation.Validator` used to validate and
            convert the text in ``entry``.
        serializer: A :class:`.validation.Serializer` used to convert the
            Python value to a string.

    """

    def __init__(
        self,
        parent: ttk.LabelFrame,
        *args,
        label: str = "",
        value: Any = None,
        tooltip: str = "",
        validator: Validator[_T] = no_validation_validator,
        serializer: Serializer[_T] = default_serializer,
        pad: tuple[float, float, float, float] = (5, 3, 5, 3),
        **kwargs,
    ) -> None:
        """A `ttk.LabelFrame` for setting formatting parameters.

        Args:
            parent: The containing :class:`.ttk.LabelFrame`.
            *args: Positional parameters for :class:`.ttk.LabelFrame`.
            label: The name of the formatting parameter. Defaults to "".
            value: The initial value of the formatting parameter. Defaults to
                None.
            tooltip: The tooltip message. Defaults to "".
            validator: A :class:`Validator` for validating and converting user
                input. Defaults to :func:`.validation.no_validation_validator`.
            serializer: A :class:`validation.Serializer` instance for
            converting the Python version of the value to a string.
            pad: Specify the padding `(left, top, bottom, right)` to use
                for the tooltip. Defaults to `(5, 3, 5, 3)`.
            **kwargs: Keyword arguments for :class:`.ttk.LabelFrame`.

        """
        super().__init__(parent, *args, text=label, **kwargs)
        self.parent = parent
        self._var = tk.StringVar(value="")

        self.entry = ttk.Entry(
            self,
            validate="focusout",
            validatecommand=(self.register(self.alerting_validator), "%P"),
            invalidcommand=self.register(highlight_and_warn),
            textvariable=self._var,
        )
        self.tooltip = Tooltip(self, text=tooltip)
        self.entry.grid(
            padx=(pad[0], pad[2]),
            pady=(pad[1], pad[3]),
            sticky=tk.NSEW,
        )
        self.grid()
        self.validator = validator
        self.serializer = serializer
        self.value = value

    @property
    def label_text(self) -> str:
        """The text used for the `FancyFormatFrame` label."""
        return self.cget("text")

    @property
    def python_value(self) -> _T:
        """The Python value of the text in :attr:`FancyFormatFrame.entry`.

        Raises:
            ValidationError: The current value in
            :attr:`FancyFormatFrame.entry` is invalid.

        """
        return self.validator(self._var.get(), validate_only=False)

    @property
    def value(self):
        """The text in :attr:`FancyFormatFrame.entry`."""
        return self._var.get()

    @value.setter
    def value(self, new_value: Any):
        self._var.set(self.serializer(new_value))

    def alerting_validator(self, value: str) -> bool:
        """Validate a value and generate a ``<<Validate>>`` event.

        Args:
            value: The value to validate.

        Returns:
            True if the value if valid. False, otherwise.

        Note:
            Listeners should be bound to the ``<<Validate>>`` event
            in order to respond to this behaviour.
        """
        valid = self.validator(value)
        if valid:
            self.parent.event_generate("<<Validate>>", when="tail")
        return valid
