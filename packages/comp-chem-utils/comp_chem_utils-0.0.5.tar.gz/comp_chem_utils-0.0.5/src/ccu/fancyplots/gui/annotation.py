"""GUI elements for defining free energy diagram annotations.

This module defines the :class:`AnnotationSection` class.
"""

import logging
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from ccu.fancyplots.data import Annotation
from ccu.fancyplots.gui.frames import FancyFormatFrame
from ccu.fancyplots.gui.frames import UpdatableFrame
from ccu.fancyplots.validation import validator_from_type

if TYPE_CHECKING:
    from ccu.fancyplots.gui.root import FancyPlotsGUI

logger = logging.getLogger(__name__)


class AnnotationSection(ttk.LabelFrame, UpdatableFrame):
    """GUI component for adding annotations to the free energy diagram.

    Attributes:
        annotations: A list of :class:`.data.Annotations`

    """

    def __init__(self, parent: "FancyPlotsGUI", *args, **kwargs) -> None:
        """Create section for adding annotations to the free energy diagram."""
        super().__init__(
            parent._frame, *args, text="Add Annotations", **kwargs
        )
        self.parent = parent
        int_validator = validator_from_type(int)
        str_validator = validator_from_type(str)
        self._text_frame = FancyFormatFrame(
            self, label="Additional Text:", validator=str_validator
        )
        self._x_frame = FancyFormatFrame(
            self, label="X Coordinate:", validator=int_validator
        )
        self._y_frame = FancyFormatFrame(
            self, label="Y Coordinate:", validator=int_validator
        )
        self._color_frame = FancyFormatFrame(
            self, label="Color:", validator=str_validator
        )
        self._font_frame = FancyFormatFrame(
            self, label="Fontsize:", validator=int_validator
        )
        self._index_frame, self._annotation_var = self._create_spinbox_frame()
        self._save_button = self.create_save_button()
        self.annotations: list[Annotation] = []
        self._organize()

    def update_annotation(self) -> None:
        """Update the displayed annotation data."""
        index = self._annotation_var.get()

        if len(self.annotations) < index:
            self.annotations.append(
                Annotation(text="", x="", y="", color="", fontsize="")
            )

        self._text_frame.value = self.annotations[index].text
        self._x_frame.value = self.annotations[index].x
        self._y_frame.value = self.annotations[index].y
        self._color_frame.value = self.annotations[index].color
        self._font_frame.value = self.annotations[index].fontsize

    def _create_spinbox_frame(self) -> tuple[ttk.LabelFrame, tk.IntVar]:
        frame = ttk.LabelFrame(self)
        var = tk.IntVar(self, 1)
        _ = ttk.Spinbox(
            frame,
            from_=1,
            to=100,
            state="readonly",
            textvariable=var,
            width=3,
            command=self.update_annotation,
        ).pack(expand=True, fill="both", side="left")
        return frame, var

    def update_frames(self) -> None:
        """Update the values in the subframes with the annotation."""
        logger.debug(
            "Updating frames in %s.%s", __package__, __class__.__name__
        )
        if not self.annotations:
            return

        self._text_frame.value = self.annotations[0].text
        self._x_frame.value = self.annotations[0].x
        self._y_frame.value = self.annotations[0].y
        self._color_frame.value = self.annotations[0].color
        self._font_frame.value = self.annotations[0].fontsize

    def save_annotation(self) -> None:
        """Save the created annotation data."""
        index = self._annotation_var.get()
        self.annotations[index].text = self._text_frame.value
        self.annotations[index].x = self._x_frame.value
        self.annotations[index].y = self._y_frame.value
        self.annotations[index].color = self._color_frame.value
        self.annotations[index].fontsize = self._font_frame.value

    def create_save_button(self) -> ttk.Button:
        """Create a save button."""
        return ttk.Button(
            self,
            text="Save Text",
            command=self.save_annotation,
        )

    def _organize(self) -> None:
        """Organize widgets into 1x7 grid."""
        self._text_frame.grid(row=1, column=1)
        self._x_frame.grid(row=1, column=2)
        self._y_frame.grid(row=1, column=3)
        self._color_frame.grid(row=1, column=4)
        self._font_frame.grid(row=1, column=5)
        self._index_frame.grid(row=1, column=6)
        self._save_button.grid(row=1, column=7, sticky=tk.NSEW)
