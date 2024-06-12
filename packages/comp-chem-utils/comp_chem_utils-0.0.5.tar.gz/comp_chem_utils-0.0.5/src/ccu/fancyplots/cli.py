"""Command-line interface for FancyPlots."""

from pathlib import Path
import tkinter as tk

import click

from ccu.fancyplots.gui.root import FancyPlotsGUI


@click.command(
    name=__package__.split(".")[-1],
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option(
    "--cache",
    "cache_file",
    type=click.Path(path_type=Path),
    help="Load fancyplots with a cached session.",
    metavar="CACHE_FILE",
)
@click.option(
    "--data",
    "data_file",
    type=click.Path(path_type=Path),
    help="Initialize fancyplots with free energy diagram data.",
    metavar="DATA_FILE",
)
@click.option(
    "--style",
    "style_file",
    type=click.Path(path_type=Path),
    help="Specify a style file.",
    metavar="STYLE_FILE",
)
def main(cache_file: Path, data_file: Path, style_file: Path) -> None:  # noqa: ARG001
    """Launch the FancyPlots GUI."""
    root = tk.Tk()
    app = FancyPlotsGUI(cache_file=cache_file, master=root)
    app.master.mainloop()
