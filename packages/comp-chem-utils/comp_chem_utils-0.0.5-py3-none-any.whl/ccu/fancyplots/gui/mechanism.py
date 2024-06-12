"""GUI elements for defining reaction mechanisms.

Specifically, this module defines the :class:`StepPanel`, :class:`PathPanel`,
and :class:`MechanismSection` classes.
"""

import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import TYPE_CHECKING
from typing import Literal

from ccu.fancyplots.data import FEDData
from ccu.fancyplots.gui.energy import EnergyWindow
from ccu.fancyplots.gui.frames import UpdatableFrame

if TYPE_CHECKING:
    from ccu.fancyplots.gui.root import FancyPlotsGUI

logger = logging.getLogger(__name__)


class StepPanel(ttk.LabelFrame):
    """Define the name and number of mechanism steps.

    Note that step names are stripped of all surrounding whitespace.

    Attributes:
        entry: The :class:`ttk.Entry` used to define mechanism steps.
        parent: The parent
            :class:`ccu.fancyplots.gui.mechanism.MechanismSection`.
        var: The :class:`tk.StringVar` for the :class:`ttk.Entry`.

    """

    def __init__(self, parent: "MechanismSection", *args, **kwargs) -> None:
        """Create a subpanel for defining the mechanism steps.

        Args:
            parent: The containing :class:`.mechanism.MechanismSection`.
            *args: Positional arguments for :class:`.ttk.LabelFrame`.
            **kwargs: Keyword arguments for :class:`.ttk.LabelFrame`.
        """
        text = "Mechanism Steps:"
        super().__init__(parent, *args, text=text, **kwargs)
        self.var = tk.StringVar(self)
        self.parent = parent
        cmd = self.register(self.update_data)
        self.entry = ttk.Entry(
            self,
            width=30,
            justify=tk.CENTER,
            textvariable=self.var,
            validate="focusout",
            validatecommand=cmd,
        )
        self.entry.grid(row=1, column=1)

    @property
    def mechanism(self) -> list[str]:
        """The names used to define mechanism steps."""
        return [x.strip() for x in self.entry.get().split(",") if x.strip()]

    @mechanism.setter
    def mechanism(self, new_value: list[str]) -> None:
        self.var.set(",".join(x.strip() for x in new_value))

    def update_data(self) -> Literal[True]:
        """Update the mechanism data.

        Returns True so as to ensure that tkinter accepts the new input.

        Note:
            No validation is performed on the mechanism steps.
        """
        return self.parent.update_data()


class PathPanel(ttk.LabelFrame):
    """Define the number of pathways.

    Attributes:
        parent: The parent
            :class:`ccu.fancyplots.gui.mechanism.MechanismSection`.
        spinbox: The :class:`tk.Spinbox` used to define the number of
            pathways.
        var: The :class:`tkinter.IntVar` for the :class:`tk.Spinbox`.

    """

    def __init__(self, parent: "MechanismSection", *args, **kwargs) -> None:
        """Create a subpanel for defining the number of mechanism pathways.

        Args:
            parent: The containing :class:`.mechanism.MechanismSection`.
            *args: Positional arguments for :class:`.ttk.LabelFrame`.
            **kwargs: Keyword arguments for :class:`.ttk.LabelFrame`.
        """
        text = "Number of Paths:"
        super().__init__(parent, *args, text=text, **kwargs)
        self.parent = parent
        self.var = tk.IntVar(self, 1)
        cmd = self.register(self.update_data)
        self.spinbox = tk.Spinbox(
            self,
            from_=1,
            to=30,
            textvariable=self.var,
            width=3,
            command=cmd,
            state="readonly",
        )
        self.spinbox.pack(side="top", fill="both")

    @property
    def npaths(self) -> int:
        """The number of pathways."""
        return self.var.get()

    @npaths.setter
    def npaths(self, new_value: int) -> None:
        self.var.set(new_value)

    def update_data(self) -> None:
        """Update the mechanism data.

        Returns True so as to ensure that tkinter accepts the new input.

        Note:
            No validation is performed on the mechanism steps.
        """
        _ = self.parent.update_data()


class MechanismSection(ttk.LabelFrame, UpdatableFrame):
    """GUI element for specifying mechanism free energies.

    Attributes:
        parent: The running :class:`.root.FancyPlotsGUI` instance.
        step_panel: A :class:`ttk.LabelFrame` for defining the names of
            mechanism steps.
        path_panel: A :class:`ttk.LabelFrame` for defining the number of
            pathways.
        gibbs_button: A :class:`ttk.Button` for launching the :class:`EnergyWindow`.
        reorder_button: A :class:`ttk.Button` for launching the
            :class:`ReorderWindow`.

    """

    def __init__(self, parent: "FancyPlotsGUI", *args, **kwargs) -> None:
        """Create a subpanel for defining a reaction mechanism.

        Args:
            parent: The containing :class:`.mechanism.MechanismSection`.
            *args: Positional arguments for :class:`.ttk.LabelFrame`.
            **kwargs: Keyword arguments for :class:`.ttk.LabelFrame`.
        """
        super().__init__(
            parent._frame, *args, text="Mechanism Design", **kwargs
        )
        self.parent = parent
        self.step_panel = StepPanel(self)
        self.path_panel = PathPanel(self)
        self.gibbs_button = ttk.Button(
            self,
            text="Define Gibbs Free Energies",
            command=self.launch_energy_window,
        )

        self._organize()

        self.diagram_data = FEDData(
            pathways=[], step_names=[], legend_entries=[]
        )

    def launch_energy_window(self) -> None:
        """Launch a window for defining mechanism free energies."""
        logger.debug("Launching energy window")
        energy_window = self.parent.windows["energy_window"]
        if energy_window:
            self.parent.windows["energy_window"] = energy_window.destroy()

        if not self.mechanism:
            messagebox.showerror(
                "Divisions not found!",
                "Please define the mechanism's divisions under 'Mechanism Steps'.",
            )
        elif not self.npaths:
            messagebox.showerror(
                "The number of pathways is zero!",
                "Please define the mechanism's divisions in 'Full Mechanism "
                "Divisions' entry box.",
            )
        else:
            self.parent.windows["energy_window"] = EnergyWindow(self)

    @property
    def npaths(self) -> int:
        """The number of pathways."""
        return self.path_panel.npaths

    @npaths.setter
    def npaths(self, new_value: int) -> None:
        self.path_panel.npaths = new_value

    @property
    def mechanism(self) -> list[str]:
        """The names used to define mechanism steps."""
        return self.step_panel.mechanism

    @mechanism.setter
    def mechanism(self, new_value: int) -> None:
        self.step_panel.mechanism = new_value

    def update_data(self) -> Literal[True]:
        """Update the free energy diagram (meta)data.

        Note that this method returns True in order for validation via tkinter
        to permit the value within :attr:`.StepPanel.entry` to change.
        """
        logger.debug("Saving mechanism data")
        new_pathways = []
        new_legend_labels = []
        nsteps = len(self.mechanism)

        # Update mechanism
        self.diagram_data["mechanism"] = self.mechanism

        # Update free energy data and legend entries
        for i in range(self.npaths):
            if i < len(self.diagram_data["energy_data"]):
                existing_data = self.diagram_data["energy_data"][i]
                new_data = []
                for j in range(nsteps):
                    if j < len(existing_data):
                        new_data.append(existing_data[j])
                    else:
                        new_data.append(None)

                new_pathways.append(new_data)
            else:
                new_pathways.append([None] * nsteps)

            if i < len(self.diagram_data["legend_labels"]):
                new_legend_labels.append(self.diagram_data["legend_labels"][i])
            else:
                new_legend_labels.append(None)

        self.diagram_data["energy_data"] = new_pathways
        self.diagram_data["legend_labels"] = new_legend_labels

        return True

    def update_frames(self) -> None:
        """Update the path and step panels."""
        logger.debug(
            "Updating frames in %s.%s", __package__, __class__.__name__
        )
        mechanism = ",".join(step for step in self.diagram_data["mechanism"])
        self.step_panel.var.set(mechanism)
        self.path_panel.var.set(len(self.diagram_data["energy_data"]))

    def _organize(self) -> None:
        """Update the values in the step and path panels."""
        self.step_panel.grid(row=1, column=1, columnspan=3, padx=5)
        self.path_panel.grid(row=1, column=4, padx=5)
        self.gibbs_button.grid(
            row=1, column=5, columnspan=2, padx=10, sticky=tk.NSEW
        )
