"""GUI widgets for displaying free energy diagrams.

Specifically, this module provides the
:class:`~ccu.fancyplots.gui.fed.FreeEnergyDiagram` and
:class:`~ccu.fancyplots.gui.fed.TightFreeEnergyDiagram` classes.
"""

import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import TYPE_CHECKING

from matplotlib import axes
from matplotlib import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ccu.fancyplots.gui import plotting
from ccu.fancyplots.gui.tooltip import Tooltip

if TYPE_CHECKING:
    from ccu.fancyplots.gui.root import FancyPlotsGUI

logger = logging.getLogger(__name__)

_TIGHT_LAYOUT_MSG = (
    "Sometimes the y-label is cut off from the graph (does "
    "not apply to the final figure).\n"
    "Tight Layout often fixes this issue, but the coordinate "
    "system displayed above is no longer consistent.\n"
    "Previewing by holding this button will allow you to see how "
    "the labels will look like in the figure you will save,\n"
    "without having to save it."
)


class FreeEnergyDiagram(tk.Toplevel):
    """View the free energy diagram.

    Attributes:
        canvas: The :class:`.FigureCanvasTkAgg` in which the free energy
            diagram in plotted.
        coordinate_label: The :class:`.ttk.Label` used to display the mouse
            coordinates.
        cleanup_button: The :class:`.ttk.Button` used to preview the diagram
            with a tight layout.
        introduction: The :class:`.ttk.Label` used to display the cursor
            coordinate hint.
        parent: The :class:`.root.FancyPlotsGUI`.
        tooltip: The :class:`~ccu.fancyplots.gui.tooltip.Tooltip` used to
            display the tight layout hint.

    """

    def __init__(self, parent: "FancyPlotsGUI", *args, **kwargs) -> None:
        """Create a window for displaying a free energy diagram.

        Args:
            parent: The running :class:`.root.FancyPlotsGUI` instance.
            *args: Positional arguments for :class:`tkinter.Toplevel`.
            **kwargs: Keyword arguments fo :class:`tkinter.Toplevel`.
        """
        super().__init__(parent._frame, *args, **kwargs)
        self._ax1: axes.Axes | None = None
        self._ax2: axes.Axes | None = None
        self._fig: figure.Figure | None = None

        self.canvas: FigureCanvasTkAgg | None = None
        self.parent = parent

        self.resize()
        self.title("Fancy Plots - Graph")

        self.coordinate_label = ttk.Label(
            self,
            text="Cursor Coordinates: (x=0.000, y=0.000)",
        )
        self.cleanup_button = ttk.Button(
            self,
            text="Hold to Preview Graph with Tight Layout",
        )
        self.tooltip = Tooltip(
            self.cleanup_button,
            text=_TIGHT_LAYOUT_MSG,
        )
        self.introduction = ttk.Label(
            self,
            text="""Hold down CTRL to check your cursor's coordinates.""",
        )
        destroy = self.update_graph()
        self.protocol(
            "WM_DELETE_WINDOW", self.parent._quit_window("graph_window", self)
        )
        self._bind_keys()
        self._organize()

        if destroy:
            self.parent._quit_window("graph_window", self)()

    def resize(self) -> None:
        """Resize the window using the formatting parameter."""
        parameters = self.parent.sections["formatting"].formatting_parameters
        scale_window_x, scale_window_y = parameters["boxsize"]

        if scale_window_x < 2:  # noqa: PLR2004
            scale_window_x = 2

        x = int((120 * scale_window_x) + 80)
        y = int((120 * scale_window_y) + 80)
        self.geometry(f"{x}x{y}")

    def update_graph(self) -> bool:
        """Update the free energy diagram.

        Returns:
            True if the graph was successfully updated. False, otherwise.

        """
        (self._ax1, self._ax2, self._fig) = self.generate_figure()

        if self.canvas:
            self.canvas._tkcanvas.destroy()

        self.canvas = FigureCanvasTkAgg(self._fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=9, column=1, padx=30)

        return not self._ax1 and not self._ax2 and not self._fig

    def generate_figure(
        self,
    ) -> tuple[axes.Axes | None, axes.Axes | None, figure.Figure | None]:
        """Generate the free energy diagram.

        Returns:
            The output of :func:`.plotting.generate_figure` if a mechanism is
            defined. Otherwise, (None, None, None).

        """
        logger.debug("Generating figure")
        if not self.parent.cache.diagram_data["mechanism"]:
            msg = "No mechanism is defined, please define at least one."
            logger.warning(msg)
            messagebox.showerror("Error!", msg)
            ax1 = ax2 = fig = None
        else:
            ax1, ax2, fig = plotting.generate_figure(
                diagram_data=self.parent.cache.diagram_data,
                parameters=self.parent.cache.style_parameters,
                annotations=self.parent.cache.annotations,
                visual=True,
            )
        return ax1, ax2, fig

    def mouse_coordinates(self, event: tk.Event) -> None:
        """Update the mouse coordinates label.

        Args:
            event: A "<Control-Motion>" ``tk.Event``.

        """
        x, y = event.x, event.y
        param_dict = self.parent.sections["formatting"].formatting_parameters
        xfactor, yfactor = param_dict["boxsize"]

        cursor_xmin = 15 * xfactor
        cursor_xmax = 108 * xfactor
        cursor_ymin = 107 * yfactor
        cursor_ymax = 15 * yfactor

        if int(x) < cursor_xmin:
            x = cursor_xmin
        elif int(x) > cursor_xmax:
            x = cursor_xmax

        if int(y) < cursor_ymax:
            y = cursor_ymax
        elif int(y) > cursor_ymin:
            y = cursor_ymin

        if self._ax1:
            xmin, xmax = self._ax1.get_xlim()
            ymin, ymax = self._ax1.get_ylim()

        x = xmin + (x - cursor_xmin) * (xmax - xmin) / (
            cursor_xmax - cursor_xmin
        )
        y = ymin + (y - cursor_ymin) * (ymax - ymin) / (
            cursor_ymax - cursor_ymin
        )
        self.coordinate_label.destroy()
        self.coordinate_label = tk.Label(
            self, text=f"Cursor Coordinates: ({x=:.3f}, {y=:.3f})"
        )
        self.coordinate_label.grid(row=11, column=1, sticky=tk.S)

    def tight_layout_on_press(self, _: tk.Event) -> None:
        """Generate a free energy diagram with a tight layout."""
        logger.debug("Launching tight layout free energy diagram")
        windows = self.parent.windows

        if windows["tight_layout"]:
            self.parent._quit_window("tight_layout")

        windows["tight_layout"] = TightFreeEnergyDiagram(self.parent)

    def tight_layout_on_release(self, _: tk.Event) -> None:
        """Destroy the tight layout free energy diagram."""
        if to_delete := self.parent.windows["tight_layout"]:
            self.parent._quit_window("tight_layout", to_delete)()

    def _bind_keys(self) -> None:
        """Configure key bindings for the widget."""
        self.bind(
            "<Control-Motion>",
            self.mouse_coordinates,
        )
        self.cleanup_button.bind(
            "<ButtonPress-1>",
            self.tight_layout_on_press,
        )
        self.cleanup_button.bind(
            "<ButtonRelease-1>",
            self.tight_layout_on_release,
        )

    def _organize(self) -> None:
        self.introduction.grid(row=1, column=1)

        if self.canvas:
            self.canvas._tkcanvas.grid(row=2, column=1, rowspan=9)

        self.coordinate_label.grid(row=11, column=1, sticky=tk.S)
        self.cleanup_button.grid(row=12, column=1, sticky=tk.S)


class TightFreeEnergyDiagram(tk.Toplevel):
    """View the free energy diagram with a tight layout."""

    def __init__(self, parent: "FancyPlotsGUI", *args, **kwargs) -> None:
        """Create a window for displaying a tight layout free energy diagram.

        Args:
            parent: The running :class:`.root.FancyPlotsGUI` instance.
            *args: Positional arguments for :class:`tkinter.Toplevel`.
            **kwargs: Keyword arguments fo :class:`tkinter.Toplevel`.
        """
        super().__init__(*args, **kwargs)
        self.parent = parent
        parameters = self.parent.sections["formatting"].formatting_parameters
        scale_window_x, scale_window_y = parameters["boxsize"]
        if scale_window_x < 2:  # noqa: PLR2004
            scale_window_x = 2
        x = int((120 * scale_window_x) + 80)
        y = int((120 * scale_window_y) + 80)
        self.geometry(f"{x}x{y}")
        self.title("Fancy Plots - Preview")
        self._fig = self.parent.windows["graph_window"]._fig
        self._fig.tight_layout()
        self.canvas_tl = FigureCanvasTkAgg(self._fig, master=self)
        self.canvas_tl.draw()
        self.canvas_tl.get_tk_widget().pack(
            fill="both", side="top", expand=True
        )
        self.protocol(
            "WM_DELETE_WINDOW", self.parent._quit_window("tight_layout", self)
        )
