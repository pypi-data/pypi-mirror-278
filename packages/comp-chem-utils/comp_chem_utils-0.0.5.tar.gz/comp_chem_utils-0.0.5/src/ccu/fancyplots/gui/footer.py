"""Miscellaneous GUI elements for FancyPlots.

This module defines the :class:`FooterSection` class which contains various
:class:`.ttk.Button` instances for saving and displaying the graph, resetting
parameters, and showing documentation.

"""

from contextlib import suppress
import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import TYPE_CHECKING

from ccu.fancyplots.gui import plotting
from ccu.fancyplots.gui.fed import FreeEnergyDiagram
from ccu.fancyplots.gui.frames import UpdatableFrame
from ccu.fancyplots.gui.instructions import InstructionsWindow
from ccu.fancyplots.gui.palette import PaletteWindow

if TYPE_CHECKING:
    from ccu.fancyplots.gui.root import FancyPlotsGUI

logger = logging.getLogger(__name__)


class FooterSection(ttk.Frame, UpdatableFrame):
    """A collection of utility buttons for settings, instructions, and graphs.

    Attributes:
        parent: A :class:`FancyPlotsGUI`.
        reset_button: A ``ttk.Button`` for resetting formatting parameters.
        show_button: A ``ttk.Button`` for showing the free energy diagram.
        save_button: A ``ttk.Button`` for saveing the free energy diagram.
        palette_button: A ``ttk.Button`` for showing the matplotlib palette.
        instructions_button: A ``ttk.Button`` for showing the instructions of
            how to use FancyPlots.

    """

    def __init__(
        self,
        parent: "FancyPlotsGUI",
        *args,
        **kwargs,
    ) -> None:
        """Create a section with miscellaneous GUI elements.

        Args:
            parent: The running :class:`.root.FancyPlotsGUI` instance.
            *args: Positional arguments for :class:`tkinter.Toplevel`.
            **kwargs: Keyword arguments fo :class:`tkinter.Toplevel`.
        """
        super().__init__(parent._frame, *args, **kwargs)
        self.parent = parent
        self.reset_button = ttk.Button(
            self,
            text="Reset Formatting Settings",
            command=self.reset_defaults,
        )
        self.show_button = ttk.Button(
            self,
            text="Show Graph",
            command=self.show_graph,
        )
        self.save_button = ttk.Button(
            self,
            text="Save Graph",
            command=self.save_figure,
        )
        self.palette_button = ttk.Button(
            self,
            text="Color Palettes",
            command=self.show_palette,
        )
        self.instructions_button = ttk.Button(
            self,
            text="Instructions",
            command=self.show_instructions,
        )
        self._organize()

    def _organize(self) -> None:
        self.reset_button.grid(row=1, column=1)
        self.show_button.grid(row=1, column=2, sticky=tk.W)
        self.save_button.grid(row=1, column=3, sticky=tk.W)
        self.palette_button.grid(row=1, column=4, sticky=tk.W)
        self.instructions_button.grid(row=1, column=5, sticky=tk.W)

    def reset_defaults(self) -> None:
        """Reset the formatting parameters to their default values."""
        logger.debug("Resetting formatting parameters to default")
        if self.parent.sections and self.parent.sections["formatting"]:
            self.parent.sections["formatting"].reset_defaults()
            logger.info("Succesfully reset defaults")
        else:
            logger.info("Unable to reset defaults")

    def show_graph(self) -> None:
        """Show the free energy diagram."""
        windows = self.parent.windows
        if windows["graph_window"]:
            self.parent._quit_window("graph_window", windows["graph_window"])()

        logger.debug("Showing free energy diagram")
        window = FreeEnergyDiagram(self.parent)
        with suppress(tk.TclError):
            _ = window.winfo_viewable()
            windows["graph_window"] = window

    def save_figure(self) -> None:
        """Save the free energy diagram."""
        logger.debug("Saving figure")
        _ = plotting.generate_figure(
            diagram_data=self.parent.cache.diagram_data,
            parameters=self.parent.cache.style_parameters,
            annotations=self.parent.cache.annotations,
            visual=False,
        )
        msg = "Succesfully saved figure"
        logger.info(msg)
        messagebox.showinfo(message=msg)

    def show_palette(self) -> None:
        """Show the matplotlib colour palette."""
        logger.debug("Launching the colour palette window")
        windows = self.parent.windows
        if windows["matplotlib_palette"]:
            self.parent._quit_window(windows, "matplotlib_palette")()

        logger.debug("Showing colour palette")
        window = PaletteWindow(self.parent)
        with suppress(tk.TclError):
            _ = window.winfo_viewable()
            windows["matplotlib_palette"] = window

    def show_instructions(self) -> None:
        """Show the FancyPlots walkthrough."""
        logger.debug("Launching the instructions window")
        windows = self.parent.windows
        if windows["instructions_window"]:
            self.parent._quit_window("instructions_window", self)()

        logger.debug("Showing instructions")
        window = InstructionsWindow(self.parent)
        with suppress(tk.TclError):
            _ = window.winfo_viewable()
            windows["instructions_window"] = window

    def update_frames(self) -> None:
        """Empty function."""
        logger.debug(
            "Updating frames in %s.%s", __package__, __class__.__name__
        )
