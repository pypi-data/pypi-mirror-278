"""Classes for the storage of FancyPlots relevant data.

The class :class:`ccu.fancyplots.data.FancyCache` describes how data is
imported to and exported from FancyPlots.

The class :class:`ccu.fancyplots.data.FEDData` defines how free energy
diagram is stored.

The class :class:`ccu.fancyplots.data.FormattingParameters` defines how
plot formatting parameters are stored.

The class :class:`ccu.fancyplots.data.Annotation` defines how plot
annotations are stored.

Examples:
    The internal data from FancyPlots can be accessed via the attribute
    :attr:`ccu.fancyplots.gui.root.FancyPlotsGUI.cache` and dumped into
    a human-readable form via the following idiom:

    >>> import json
    >>> from pathlib import Path
    >>> from ccu.fancyplots.data import DEFAULT_PARAMETERS
    >>> from ccu.fancyplots.data import FancyCache
    >>> data = {
    ...     "energy_data": [
    ...         [0, 0.2, 0.33, -0.5],
    ...         [0, -0.1, 0.25, 0],
    ...     "mechanism": ["*", "*CHOO", "*CO", "CO"],
    ...     "legend_labels: ["Cu(111)", "Cu-NP"],
    >>> annotations = []
    >>> formatting_parameters = DEFAULT_PARAMETERS
    >>> cache = FancyCache(
    ...     formatting_parameters,
    ...     diagram_data=data,
    ...     annotations=annotations,
    ...)
    >>> with Path("fancy.cache").open(
    ...     mode="w", encoding="utf-8"
    ... ) as file:  # doctest:+SKIP
    ...     _ = json.dump(cache, file, indent=2)

    The same file (``fancy.cache``) can be loaded into a convenient format for
    FancyPlots via the following idiom:

    >>> import json
    >>> from pathlib import Path
    >>> from ccu.fancypylots.data import FancyCache
    >>> with Path("fancy.cache").open(  # doctest:+SKIP
    ...     mode="r", encoding="utf-8"
    ... ) as file:
    ...     cache = FancyCache(**json.load(file))

"""

from dataclasses import asdict
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Annotated
from typing import NamedTuple
from typing import TypedDict

FANCY_EXTENSION = ".fancy"


class FEDData(TypedDict):
    """Energies and metadata for a free energy diagram.

    Keys:
        energy_data: A list of lists. Each list defines energies for each step
            in the mechanism.
        mechanism: The labels for each mechanism step.
        legend_labels: The legend labels for each pathway.

    Valid :class:`ccu.fancyplots.data.FEDData` instances should satisfy the following
    condition for seamless use with ``FancyPlots``:

    - The lengths of each element in
      :attr:`ccu.fancyplots.data.FEDData.energy_data` should be equal to the
      lengths of :attr:`ccu.fancyplots.data.FEDData.mechanism` and
      :attr:`ccu.fancyplots.data.FEDData.legend_labels`. This translates to
      the condition that the number of energies defined for each step should
      equal the number of steps in the mechanism.

    """

    energy_data: list[list[float | None]]
    mechanism: list[str]
    legend_labels: list[str | None]


# TODO: add missing parameters:
#   xlim, ylim
class FormattingParameters(TypedDict):
    """The formatting parameters to use to plot free energy diagrams.

    Keys:
    """

    boxsize: Annotated[
        tuple[float, float],
        "Defines the width:height ratio of the graph by specifying "
        "'width,height' in inches.",
    ]
    font: Annotated[
        str,
        "Specify a font family. Any system font can be specified. See "
        "the documentation for matplotlib.text.Text.set_fontfamily for "
        "details.",
    ]
    fontsize: Annotated[
        float,
        "Size of the font for x-axis, y-axis and paths' labels. Title"
        "will have a value of the fontize+1 and additional text fontsize-2.",
    ]
    markeredgewidth: Annotated[float, "The marker edge width"]
    markersize: Annotated[int, "The marker size"]
    linewidth: Annotated[
        float,
        "Width of the paths' lines, graph's margins are affected as well.",
    ]
    xlim: Annotated[
        None | tuple[float, float],
        "Defines a non-default x-range by specifying *xmin*,*xmax*.",
    ]
    ylim: Annotated[
        None | tuple[float, float],
        "Defines a non-default y-range by specifying 'ymin,ymax'.",
    ]
    xscale: Annotated[
        str,
        "Defines the scale to use for the x-axis. One of 'linear', 'log', "
        "'symlog', 'asinh', 'logit', 'function', 'functionlog'.",
    ]
    yscale: Annotated[
        str,
        "Defines the scale to use for the y-axis. One of 'linear', 'log', "
        "'symlog', 'asinh', 'logit', 'function', 'functionlog'.",
    ]
    tick_loc: Annotated[
        str,
        "Defines the tick's location - inside or outside of the "
        "graph's margin. Supports 'in' and 'out' keywords.",
    ]
    tick_dec: Annotated[
        float,
        "Defines the tick's decimal numbers. If '2' is stated, ticks "
        "will show e.g. 1.00, 2.00,...",
    ]
    tick_min: Annotated[
        float,
        "Defines how many minor ticks between the major ones are " "desired.",
    ]
    tick_double: Annotated[
        bool, "If True, ticks will be shown on the right-hand side as well."
    ]
    legend_loc: Annotated[
        str,
        "Location of the legends. Accepted keywords: best, upper "
        "right, upper left, lower right, lower left, upper center, lower "
        "center, center left, center right, center.",
    ]
    xlabel: Annotated[
        str,
        "Defines a label for the x-axis. If no label is desired, "
        "leave this space in blank.",
    ]
    ylabel: Annotated[
        str,
        "Defines a label for the y-axis. If no label is desired, "
        "leave this space in blank.",
    ]
    colors: Annotated[
        tuple[str, ...],
        "Color palettes are shown if 'Color Palettes' button is " "clicked.",
    ]

    title: Annotated[
        str,
        "States the title of the graph, leave this space in black if "
        "no title is desired.",
    ]
    visual: Annotated[
        bool,
        "Visual is enabled by default and cannot be changed. This "
        "keyword is recognized by fancy plots to enable GUI.",
    ]
    savename: Annotated[
        str,
        "Saves the figure with its corresponding extension (png,jpg,"
        "pdf,svg,...).",
    ]
    dpi: Annotated[
        int,
        "Dots per inch defines the resolution of the figure. This "
        "number will do nothing for pdf, svg and eps formats since these are "
        "vector images.",
    ]


DEFAULT_PARAMETERS = FormattingParameters(
    boxsize=(6, 4.5),
    font="Sans Serif",
    fontsize=14,
    markeredgewidth=0.3,
    markersize=7,
    linewidth=2.25,
    xlim=None,
    ylim=None,
    xscale="linear",
    yscale="linear",
    tick_loc="out",
    tick_dec=2,
    tick_min=1,
    tick_double=False,
    legend_loc="best",
    xlabel="Reaction Coordinate",
    ylabel=r"$\Delta$G / eV",
    colors=("black", "blue", "red", "lime", "fuchsia"),
    savename="fed.svg",
    dpi=1200,
    title="",
)


class Annotation(NamedTuple):
    """A free energy diagram annotation.

    Attributes:
        color: The color to use for the annotation.
        fontsize: The fontsize to use for the annotation.
        text: The annotation text.
        x: The x-coordinate of the annotation.
        y: The y-coordinate of the annotation.

    """

    color: str = "k"
    fontsize: float = DEFAULT_PARAMETERS["fontsize"] * 0.8
    text: str = ""
    x: float = 0.0
    y: float = 0.0


@dataclass
class FancyCache:
    """The data model for caching/loading data into FancyPlots.

    Attributes:
        style_parameters: The formatting parameters to use to plot the
            free energy diagram.
        diagram_data: The energy data and metadata for plotting the free
            energy diagram.
        annotations: The annotations associated with the free energy diagram.

    """

    style_parameters: FormattingParameters
    diagram_data: FEDData
    annotations: list[Annotation]

    def save(self, savename: str | Path = f"cache.{FANCY_EXTENSION}") -> None:
        """Save the FancyCache.

        Args:
            savename: The filename in which to save the cache. Defaults to
            f"cache.{FANCY_EXTENSION}".
        """
        with Path(savename).open(mode="w", encoding="utf-8") as file:
            json.dump(asdict(self), file, indent=2)
