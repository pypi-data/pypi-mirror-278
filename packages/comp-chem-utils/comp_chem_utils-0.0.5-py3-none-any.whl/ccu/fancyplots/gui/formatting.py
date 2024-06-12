"""GUI elements for defining plot formatting parameters.

This module defines the :class:`FormattingSection` class.
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from typing import get_args
from typing import get_type_hints

from ccu.fancyplots.data import DEFAULT_PARAMETERS
from ccu.fancyplots.data import FormattingParameters
from ccu.fancyplots.gui.frames import FancyFormatFrame
from ccu.fancyplots.gui.frames import UpdatableFrame
from ccu.fancyplots.validation import type_hint_to_validator

if TYPE_CHECKING:
    from ccu.fancyplots.gui.root import FancyPlotsGUI


class FormattingSection(ttk.LabelFrame, UpdatableFrame):
    """A :class:`ttk.LabelFrame` containing all formatting parameters.

    Note that instances of this class are listeners for the custom
    <Validate> event emitted by :class:`.frames.FancyFormatFrame`
    instances.

    Attributes:
        parent: The :class:`.root.FancyPlotsGUI`.
        formatting_parameters: A :class:`.data.FormattingParameters` instance
            mapping the names of formatting parameters to their values.
            Defaults to a copy of :attr:`data.DEFAULT_PARAMETERS`.
        frames: A list of :class:`FancyFormatFrame` instances in which the
            formatting parameters are set.

    """

    def __init__(
        self,
        parent: "FancyPlotsGUI",
        *args,
        parameters: FormattingParameters | None = None,
        **kwargs,
    ) -> None:
        """Create a section for specifying plot formatting parameters.

        Args:
            parent: The running :class:`.root.FancyPlotsGUI` instance.
            *args: Positional arguments for :class:`tkinter.Toplevel`.
            parameters: A :class:`.formatting.FormattingParameters`
                dictionary mapping parameter names to their values. Defauls
                to :data:`.DEFAULT_PARAMETERS`.
            **kwargs: Keyword arguments fo :class:`tkinter.Toplevel`.
        """
        super().__init__(
            parent._frame, *args, text="Plot Formatting", **kwargs
        )
        self.parent = parent
        if parameters is None:
            self.formatting_parameters = DEFAULT_PARAMETERS.copy()
        else:
            self.formatting_parameters = parameters

        self.frames = self.initialize_frames()
        self._organize()
        self.bind("<Return>", self.parent._update_graph)
        self.bind("<<Validate>>", self.update_parameters)

    def reset_defaults(self) -> None:
        """Reset the parameter values to their defaults."""
        for frame in self.frames:
            frame.value = DEFAULT_PARAMETERS[frame.label_text]

    def initialize_frames(self) -> list[FancyFormatFrame]:
        """Create ``ttk.LabelFrame`` widgets for setting formatting parameters.

        Returns:
            A list of :class:`FancyFormatFrame` widgets used to set formatting
            parameters.

        Raises:
            NotImplementedError: Unsupported annotation type for formatting
            parameter. Only annotated type hints are supported.

        """
        frames = []
        type_hints = get_type_hints(FormattingParameters, include_extras=True)

        for label, value in self.formatting_parameters.items():
            annotated_type_hint = type_hints[label]
            type_hint, *tooltips = get_args(annotated_type_hint)
            tooltip = " ".join(t for t in tooltips if isinstance(t, str))
            validator = type_hint_to_validator(type_hint, label)

            frame = FancyFormatFrame(
                parent=self,
                label=label,
                value=value,
                tooltip=tooltip,
                validator=validator,
            )
            self.event_add("<<Validate>>", "None")
            self.bind("<<Validate>>", self.update_parameters)

            frames.append(frame)

        return frames

    def _organize(self) -> None:
        cols = 3
        for i, frame in enumerate(self.frames):
            col = i % cols
            row = i // cols
            frame.grid(column=col, row=row, sticky=tk.E + tk.W)

    def update_frames(self) -> None:
        """Update the values in the frame with the formatting parameters."""
        for frame in self.frames:
            param = frame.label_text
            value = self.formatting_parameters[param]
            frame.value = value

    def update_parameters(self, _: tk.Event) -> None:
        """Update :attr:`FormattingSection.formatting_parameters`."""
        for frame in self.frames:
            self.formatting_parameters[frame.label_text] = frame.python_value
