"""GUI elements for viewing the matplotlib colour palette.

This module defines the :class:`PaletteWindow` class.
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from ccu.fancyplots.gui.utils import open_image

if TYPE_CHECKING:
    from ccu.fancyplots.gui.root import FancyPlotsGUI

IMAGE_FILE = "color_palette.png"


class PaletteWindow(tk.Toplevel):
    """View available matplotlib colours.

    Attributes:
        image: The A Tkinter-compatible version of the usage instructions.
        image_label: The :class:`.ttk.Label` containing the image.
        parent: The running :class:`.root.FancyPlotsGUI` instance.
        source_label: The :class:`.ttk.Label` containing the image source.

    """

    def __init__(self, parent: "FancyPlotsGUI", *args, **kwargs) -> None:
        """Create a subpanel for defining a reaction mechanism.

        Args:
            parent: The runnnig :class:`.root.FancyPlotsGUI` instance.
            *args: Positional arguments for :class:`.tk.Toplevel`.
            **kwargs: Keyword arguments for :class:`.tk.Toplevel`.
        """
        super().__init__(parent._frame, *args, **kwargs)
        self.parent = parent
        self.geometry("553x800")
        self.title("Fancy Plots - Color Palettes")
        self.image = open_image(IMAGE_FILE, 553, 771)
        self.image_label = ttk.Label(self, image=self.image)
        self.source_label = ttk.Label(
            self,
            text="Source: "
            "https://matplotlib.org/cheatsheets/_images/cheatsheets-2.png",
        )
        self.protocol(
            "WM_DELETE_WINDOW",
            self.parent._quit_window("matplotlib_palette", self),
        )
        self._organize()

    def _organize(self) -> None:
        self.image_label.grid(row=0, column=0, columnspan=3)
        self.source_label.grid(row=1, column=1)
