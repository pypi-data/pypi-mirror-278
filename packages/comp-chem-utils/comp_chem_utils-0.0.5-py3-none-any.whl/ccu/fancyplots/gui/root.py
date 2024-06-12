"""The main logic for the FancyPlots root window.

The :class:`FancyPlotsGUI` class encompasses the main application logic for a
FancyPlots application.

In addition to the main application class, :class:`FancyPlotsGUI`,
this module also defines the following :class:`TypedDict` subclasses:

* :class:`Windows`: A mapping whose values are the top-level subwindows of
  a FancyPlots GUI application.

* :class:`Sections`: A mapping whose values are subframes of the FancyPlots
  root window.

Example:
    Launch the FancyPlots GUI

    .. code-block:: python

        import tkinter as tk
        from ccu.fancyplots.gui.root import FancyPlotsGUI

        root = tk.Tk()
        app = FancyPlotsGUI(master=root)
        app.master.mainloop()

"""

from collections.abc import Callable
import json
import logging
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from typing import TypedDict

from ccu.fancyplots.data import DEFAULT_PARAMETERS
from ccu.fancyplots.data import FANCY_EXTENSION
from ccu.fancyplots.data import FancyCache
from ccu.fancyplots.data import FEDData
from ccu.fancyplots.gui.annotation import AnnotationSection
from ccu.fancyplots.gui.energy import EnergyWindow
from ccu.fancyplots.gui.fed import FreeEnergyDiagram
from ccu.fancyplots.gui.fed import TightFreeEnergyDiagram
from ccu.fancyplots.gui.footer import FooterSection
from ccu.fancyplots.gui.formatting import FormattingSection
from ccu.fancyplots.gui.instructions import InstructionsWindow
from ccu.fancyplots.gui.mechanism import MechanismSection
from ccu.fancyplots.gui.menu import show_edit_menu
from ccu.fancyplots.gui.palette import PaletteWindow
from ccu.fancyplots.styles import initialize_styles

logger = logging.getLogger(__name__)

_DEFAULT_ROOT_SIZE = "1200x700"


class Windows(TypedDict):
    """The top-level windows of a FancyPlots GUI.

    Keys:
        energy_window: The :class:`tkinter.Toplevel` instance for defining
            Gibbs free energies.
        graph_window: The :class:`tkinter.Toplevel` instance for viewing
            the free energy diagram.
        tight_layout: The :class:`tkinter.Toplevel` instance for viewing
            the free energy diagram in a tight layout.
        instructions_window: The :class:`tkinter.Toplevel` instance for viewing
            the instructions for using FancyPlots.
        matplotlib_palette: The :class:`tkinter.Toplevel` instance for viewing
            the instructions for viewing the :mod:`matplotlib` colour
            palette.

    Example:
        >>> import tkinter as tk
        >>> from ccu.fancyplots.gui.root import FancyPlotsGUI
        >>> root = tk.Tk()
        >>> app = FancyPlotsGUI(master=root)
        >>> app.master.mainloop()
        >>> app.windows[...]

    """

    energy_window: EnergyWindow | None
    graph_window: FreeEnergyDiagram | None
    tight_layout: TightFreeEnergyDiagram | None
    instructions_window: InstructionsWindow | None
    matplotlib_palette: PaletteWindow | None


class Sections(TypedDict):
    """The subframes of a FancyPlotsGUI app.

    Keys:
        formatting: The subsection for defining plot formatting parameters.
        mechanism: The subsection for defining reaction free energies and
            legend labels.
        footer: The subsection for miscelleneous support (e.g., instructions,
            graph viewing/saving.)
        annotation: The subsection for defining graph annotations.

    Example:
        >>> import tkinter as tk
        >>> from ccu.fancyplots.gui.root import FancyPlotsGUI
        >>> root = tk.Tk()
        >>> app = FancyPlotsGUI(master=root)
        >>> app.master.mainloop()
        >>> app.sections[...]
    """

    formatting: FormattingSection
    mechanism: MechanismSection
    footer: FooterSection
    annotation: AnnotationSection


class FancyPlotsGUI:
    """A Fancy Plots GUI application.

    Attributes:
        master: The application root window - the topmost :class:`tkinter.Tk`
            instance.
        windows: A dictionary containing the child windows
            (:class`tkinter.TopLevel`) of the GUI.
        sections: A :class:`Sections` instance.

    Note:
        :class:`FancyPlotsGUI` is **not** a window and, as such, one cannot
        use it directly to manipulate properties of the GUI. For that, use
        :attr:`FancyPlots.master`.

    """

    def __init__(
        self,
        cache_file: str | Path | None = None,
        master=tk.Tk,
    ) -> None:
        """Launch the main GUI for FancyPlots.

        Args:
            cache_file: A string or :class:`Path` pointing to a cache file.
                Defaults to None. If provided, it is used to pre-populate the
                formatting parameters, mechanism info, and annotations.
                Otherwise, a fresh FancyPlots application is launched.
            master: The top level :class:`tkinter.Tk` instance.
        """
        cache_file = None if cache_file is None else Path(cache_file)
        self._initial_dir = cache_file.parent if cache_file else Path.cwd()
        self.master = master
        self.master.geometry(_DEFAULT_ROOT_SIZE)
        self.master.title("Fancy Plots GUI")
        self.windows = self._initialize_windows()
        self._configure_windows()
        self._frame = ttk.Frame(self.master)
        self.sections = self._create_sections()
        self.cache = self._load_cache(cache_file)

        self._organize()

    def _initialize_windows(self) -> Windows:
        return Windows(
            energy_window=None,
            graph_window=None,
            reorder=None,
            tight_layout=None,
            instructions_window=None,
            matplotlib_palette=None,
        )

    def _select_all(self, event: tk.Event) -> None:
        self.master.after(50, event.widget.select_range(0, "end"))

    def _quit_window(
        self, key: str, window: tk.Toplevel
    ) -> Callable[[], None]:
        def _func() -> None:
            if key not in self.windows:
                msg = f"Key {key} not in windows"
                raise ValueError(msg)

            self.windows[key] = None
            logger.info("Quitting window '%s'", key)
            window.destroy()

        return _func

    def _quit_all(self) -> None:
        save_cache = None
        save_cache = messagebox.askyesnocancel(
            "Quit", "Do you want to save all settings to a file?"
        )
        if save_cache is not None:
            if save_cache:
                self.save_cache()

            self.master.destroy()

    def _configure_windows(self) -> None:
        """Define subwindows and key bindings for GUI.

        Args:
            windows: A dictionary mapping names to `tkinter.Toplevel`
                instances and containing the root window.

        """
        self.master.bind_class(
            "Entry",
            "<Button-3><ButtonRelease-3>",
            show_edit_menu(self),
        )
        self.master.bind_class(
            "Entry",
            "<Control-q>",
            self._select_all,
        )
        self.master.protocol("WM_DELETE_WINDOW", self._quit_all)
        initialize_styles()

    def _create_sections(self) -> Sections:
        formatting = FormattingSection(self)
        mechanism = MechanismSection(self)
        annotation = AnnotationSection(self)
        footer = FooterSection(self)

        return Sections(
            formatting=formatting,
            mechanism=mechanism,
            annotation=annotation,
            footer=footer,
        )

    def _load_cache(self, cache_file: Path) -> FancyCache:
        if cache_file:
            logger.debug("Loading cache file from %s", cache_file)
            with cache_file.open(mode="r", encoding="utf-8") as file:
                cache = FancyCache(**json.load(file))
        else:
            logger.debug(
                "No cache file provided. Initializing cache from scratch"
            )
            parameters = DEFAULT_PARAMETERS
            data = FEDData(energy_data=[], mechanism=[], legend_labels=[])
            annotations = []
            cache = FancyCache(
                style_parameters=parameters,
                diagram_data=data,
                annotations=annotations,
            )

        return cache

    def _organize(self) -> None:
        self.sections["formatting"].pack(
            side="top", fill="none", anchor=tk.N, pady=10
        )
        self.sections["mechanism"].pack(
            side="top", fill="none", anchor=tk.N, pady=10
        )
        self.sections["annotation"].pack(
            side="top", fill="none", anchor=tk.N, pady=10
        )
        self.sections["footer"].pack(
            side="top", fill="none", anchor=tk.N, pady=10
        )
        self._frame.pack(side="top", fill="both", expand=True)

    def _update_graph(self, _: tk.Event) -> None:
        """Update the free energy graph."""
        logger.debug("Updating graph")
        if self.windows["graph_window"]:
            _ = self.windows["graph_window"].update_graph()
            logger.info("Successfully updated graph")
        else:
            logger.info("No graph to update")

    @property
    def cache(self) -> FancyCache:
        """Retrieve an updated account of FancyPlots' data."""
        style_parameters = self.sections["formatting"].formatting_parameters
        data = self.sections["mechanism"].diagram_data
        annotations = self.sections["annotation"].annotations
        cache = FancyCache(
            style_parameters=style_parameters,
            diagram_data=data,
            annotations=annotations,
        )
        return cache

    @cache.setter
    def cache(self, new_data: FancyCache) -> None:
        """Specify data to use for FancyPlots and update all GUI elements.

        Args:
            new_data: A :class:`FancyCache` containing the new data.
        """
        self.sections[
            "formatting"
        ].formatting_parameters = new_data.style_parameters
        self.sections["mechanism"].diagram_data = new_data.diagram_data
        self.sections["annotation"].annotations = new_data.annotations

        for section in self.sections.values():
            section.update_frames()

    def save_cache(self) -> None:
        """Save the FancyPlots cache."""
        savename = asksaveasfilename(
            defaultextension=FANCY_EXTENSION,
            filetypes=[
                ("FancyPlots cache files", f"*.{FANCY_EXTENSION}"),
                ("All files", "*"),
            ],
            initialdir=self._initial_dir,
        )
        if savename:
            logger.debug("Saving FancyPlots data to cache file: %s", savename)
            self.cache.save(savename)
