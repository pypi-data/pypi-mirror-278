"""GUI elements for viewing the FancyPlots walkthrough.

This module defines the :class:`InstricutionsWindow` class.
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from ccu.fancyplots.gui.utils import open_image

if TYPE_CHECKING:
    from ccu.fancyplots.gui.root import FancyPlotsGUI

TUTORIAL_FILE = "fancy_plots_tutorial.png"


class InstructionsWindow(tk.Toplevel):
    """View the instructions of how to use FancyPlots.

    Attributes:
        parent: The running :class:`.root.FancyPlotsGUI` instance.
        image: The A Tkinter-compatible version of the usage instructions.
        image_label: The :class:`.ttk.Label` containing the image.

    """

    def __init__(self, parent: "FancyPlotsGUI", *args, **kwargs) -> None:
        """Create a windown for viewing the instructions.

        Args:
            parent: The running :class:`root.FancyPlotsGUI` instance.
            *args: Positional arguments for :class:`.tkinter.Toplevel`.
            **kwargs: Keyword arguments for :class:`.tkinter.Toplevel`.
        """
        super().__init__(parent._frame, *args, **kwargs)
        self.parent = parent
        self.geometry("1400x788")
        self.title("Fancy Plots - Instructions")
        self.image = open_image(TUTORIAL_FILE, 1400, 788)
        self.image_label = ttk.Label(self, image=self.image)
        self.protocol(
            "WM_DELETE_WINDOW",
            self.parent._quit_window("instructions_window", self),
        )
        self.image_label.grid(row=0, column=0, columnspan=3)
        self.lift()
