"""GUI elements for defining free energies in a mechanism.

This module defines the :class:`EnergyWindow` class.
"""

import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import TYPE_CHECKING

from ccu.fancyplots.gui.menu import show_edit_menu

if TYPE_CHECKING:
    from ccu.fancyplots.gui.mechanism import MechanismSection

logger = logging.getLogger(__name__)


class EnergyWindow(tk.Toplevel):
    """Define free energies for mechanism paths.

    Attributes:
        dropdown: A ``tk.OptionMenu`` for selecting the pathway to configure.
        energy_definition_frame: A ``ttk.Frame`` containing ``ttk.Entry``
            and ``ttk.Label`` instances for defining free energies.
        free_energy_entries: A dictionary mapping mechanism step names to the
            :class:`.ttk.Entry` widget.
        free_energy_labels: A dictionary mapping mechanism step names to the
            labeling widget.
        free_energy_vars: A dictionary mapping mechanism step names to the
            :class:`tkinter.StringVar` instances in control of the
            :class:`.ttk.Entry` widgets which record the free energies of
            the mechanism step.
        legend_entry: The ``ttk.Entry`` for defining the legend text for the
            current pathway.
        legend_label: The ``ttk.Label`` for defining the legend text for the
            current pathway.
        parent: A :class:`MechanismSection`.
        path_var: A ``tk.StringVar`` recording the name of the pathway for
            which energies are being defined.

    """

    def __init__(self, parent: "MechanismSection", *args, **kwargs) -> None:
        """Create and launch a window for specifying free energies.

        Args:
            parent: The parent :class:`.mechanism.MechanismSection`.
            *args: Positional arguments for :class:`tkinter.Toplevel`.
            **kwargs: Keyword arguments fo :class:`tkinter.Toplevel`.
        """
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        height = 160 + (15 * (len(self.parent.mechanism) // 2))
        self.geometry(f"400x{height}")
        self.title("Fancy Plots - Energy Declaration")
        self.path_var, self.dropdown = self._make_dropdown()
        self.free_energy_entries: dict[str, ttk.Entry] = {}
        self.free_energy_labels: dict[str, ttk.Label] = {}
        self.free_energy_vars: dict[str, tk.StringVar] = {}
        self.energy_definition_frame = self._create_free_energy_widgets()
        self.legend_label, self.legend_entry, self.legend_var = (
            self._create_legend_widgets()
        )
        # HACK: solution to being unable to pass the previous value
        # The the OptionMenu callback
        # This is only ever modified in EnergyWindow.update_widgets
        self._previous_pathway = self.pathway

        self._organize()
        self.protocol(
            "WM_DELETE_WINDOW",
            self.quit_window,
        )
        self._configure_key_bindings()
        to_take_focus = next(iter(self.free_energy_entries.values()))
        to_take_focus.focus_set()

    def _make_dropdown(self) -> tuple[tk.StringVar, tk.OptionMenu]:
        """Create a dropdown menu for selecting reaction pathways.

        Returns:
            A 2-tuple (``var``, ``menu``) representing the
            :class:`tkinter.StringVar` storing the value of the
            active reation pathway and the option menu.
        """
        var = tk.StringVar(self, self.options[0])

        dropdown = tk.OptionMenu(
            self,
            var,
            *self.options,
            command=self.update_widgets,
        )
        return var, dropdown

    def _organize_free_energy_widgets(self) -> None:
        """Organize the free energy widgets into an x-by-2 grid."""
        for i, (label, entry) in enumerate(
            zip(
                self.free_energy_labels.values(),
                self.free_energy_entries.values(),
                strict=True,
            )
        ):
            j = 2 * i
            row = (j // 4) + 1
            column = j % 4
            label.grid(row=row, column=column)
            entry.grid(row=row, column=column + 1)

    def _create_free_energy_widgets(
        self,
    ) -> ttk.Frame:
        """Create widgets for specifying the free energies of each path.

        This method modifies
        :attr:`ccu.fancyplots.gui.energy.EnergyWindow.free_energy_labels` and
        :attr:`ccu.fancyplots.gui.energy.EnergyWindow.free_energy_entries` in
        place.

        Returns:
            The :class:`.ttk.Frame` in which the free energy widgets reside.

        """
        energies = self.parent.diagram_data["energy_data"][self.pathway_index]
        entry_frame = ttk.Frame(self)

        def _validate_float(name: str) -> bool:
            w = self.nametowidget(name)
            try:
                # Allow empty strings
                val = float(w.get()) if w.get() else ""
                w.configure(style="Valid.Fancy.TEntry")
                self.save_energy_data()
            except ValueError:
                val = None
            return val is not None

        def _invalid_float(name: str) -> None:
            w: ttk.Entry = self.nametowidget(name)
            w.configure(style="Invalid.Fancy.TEntry")
            msg = f"'{w.get()}' is neither a number nor an empty string."
            logger.warning(msg)
            messagebox.showwarning("Number not recognized!", message=msg)
            self.lift()
            self.after(1, lambda: self.focus_force())

        validate_command = (self.register(_validate_float), "%W")
        invalid_command = (self.register(_invalid_float), "%W")

        for i, step in enumerate(self.parent.mechanism):
            label = ttk.Label(entry_frame, text=step, width=2)
            self.free_energy_labels[step] = label
            value = "" if energies[i] is None else str(float(energies[i]))
            var = tk.StringVar(value=value)

            entry = ttk.Entry(
                entry_frame,
                width=12,
                validate="focusout",
                validatecommand=validate_command,
                invalidcommand=invalid_command,
                textvariable=var,
            )
            self.free_energy_entries[step] = entry
            self.free_energy_vars[step] = var

        self._organize_free_energy_widgets()

        return entry_frame

    def _create_legend_widgets(
        self,
    ) -> tuple[ttk.Label, ttk.Entry, tk.StringVar]:
        """Create the widgets for specifying legend labels.

        Returns:
            A 2-tuple (``label``, ``entry``) whose first and second elements
            are a :class:`.ttk.Label` and :class:`.ttk.Entry`, respectively.

        """
        legend_labels = self.parent.diagram_data["legend_labels"]
        legend_label = legend_labels[self.pathway_index]
        label = ttk.Label(self, text="Path Label \n (Legend)")
        var = tk.StringVar(value=legend_label)

        def _validate_all(name: str) -> bool:
            w = self.nametowidget(name)
            try:
                # Allow empty strings
                val = float(w.get()) if w.get() else ""
                w.configure(style="Valid.Fancy.TEntry")
                self.save_legend_data()
            except ValueError:
                val = None
            return val is not None

        command = (self.register(_validate_all), "%W")
        entry = ttk.Entry(
            self,
            width=25,
            textvariable=var,
            validate="focusout",
            validatecommand=command,
        )

        return label, entry, var

    def _organize(self) -> None:
        self.dropdown.grid(row=1, column=1, columnspan=10, sticky=tk.W)
        self.energy_definition_frame.grid(row=2, column=1, columnspan=100)
        self.legend_label.grid(row=3, column=1, sticky=tk.W)
        self.legend_entry.grid(row=3, column=2, sticky=tk.W)

    def _configure_key_bindings(self) -> None:
        """Configure key bindings for the widget."""
        self.bind_class(
            "Entry",
            "<Button-3><ButtonRelease-3>",
            show_edit_menu(self),
        )
        self.bind_class(
            "Entry",
            "<Control-q>",
            self.parent.parent._select_all,
        )

    @property
    def options(self) -> list[str]:
        """The options (pathways) for the option menu."""
        options = []

        for i in range(self.parent.path_panel.npaths):
            options.append(f"Pathway {i+1}")

        return options

    @property
    def pathway(self):
        """The pathway indicated by the dropdown selection."""
        return self.path_var.get()

    @property
    def pathway_index(self):
        """The index of pathway indicated by the dropdown."""
        return self.options.index(self.pathway)

    def save_energy_data(self, index: int | None = None) -> None:
        """Update FED data with the values from :attr:`EnergyWindow.entries`.

        Args:
            index: The index of the pathway to update with the current widget
                values. Defaults to None, in which case,
                :attr:`EnergyWindow.pathway_index` is used.
        """
        logger.debug("Saving energy data")
        index = self.pathway_index if index is None else index
        feddata = self.parent.diagram_data
        energies = feddata["energy_data"][index]

        for i, entry in enumerate(self.free_energy_entries.values()):
            try:
                energies[i] = float(entry.get())
            except ValueError:
                msg = f"No value provided for step {i}. Setting to None."
                logger.info(msg)
                energies[i] = None

    def save_legend_data(self, index: int | None = None) -> None:
        """Save the legend label for the present pathway and return True.

        Args:
            index: The index of the pathway to update with the current widget
                values. Defaults to None, in which case,
                :attr:`EnergyWindow.pathway_index` is used.
        """
        logger.debug("Saving legend data")
        index = self.pathway_index if index is None else index
        feddata = self.parent.diagram_data
        label = self.legend_entry.get() or None
        feddata["legend_labels"][index] = label
        return True

    def update_widgets(self, _) -> None:
        """Update the energy and legend ``Entry`` widgets.

        .. admonition:: Developer's Note

            **This should be the only place that**
            :attr:`EnergyWindow._previous_pathway` **is edited**. Unlike other
            Tkinter widgets whose callbacks allow for the specification of
            state-dependent variables (e.g., the name of the triggering
            widget, the value before the action, etc.), the OptionMenu
            callback is always called without arguments. This makes it
            difficult to update the parameters before changing the values
            because the value in the option menu is already changed when the
            callback is called. A workaround is to duplicate the state of the
            shown option in the :attr:`EnergyWindow._previous_pathway`
            attribute and manually manage it here.
        """
        logger.info(
            f"Updating widgets in {self.__module__}.{self.__class__.__name__}"
        )
        index = self.options.index(self._previous_pathway)
        self.save_energy_data(index)
        self.save_legend_data(index)
        self._previous_pathway = self.pathway
        energies = self.parent.diagram_data["energy_data"][self.pathway_index]

        for i, var in enumerate(self.free_energy_vars.values()):
            value = energies[i]
            var.set("" if value is None else value)

        legend_labels = self.parent.diagram_data["legend_labels"]
        label = legend_labels[self.pathway_index]
        self.legend_var.set("" if label is None else label)

    def quit_window(self) -> None:
        """Gracefully quit the window and save data."""
        self.save_energy_data()
        self.save_legend_data()
        self.parent.parent._quit_window("energy_window", self)()
