"""CLI utilities for adsorption studies."""

import pathlib
import sys
from typing import Any

from ase import collections
from ase.build.molecule import extra
import click

from ccu.adsorption import adsorbatecomplex
from ccu.adsorption.adsorbates import ALL


@click.group(name=__package__.split(".")[-1])
def main():
    """Adsorption calculation tools."""


_all_adsorbates = list(ALL.keys()) + collections.g2.names + list(extra.keys())


def print_adsorbates(
    ctx: click.Context,  # noqa: ARG001
    value: Any,  # noqa: ARG001
    param: click.Parameter,
) -> None:
    "Print a list of all adsorbates available to ccu."
    if not param:
        return

    header = "AVAILABLE ADSORBATES"
    click.echo(header)
    source_names = ["ccu", "g2", "extra"]
    sources = [ALL, collections.g2.names, extra]
    width = len(header)

    def _print_header(text: str) -> str:
        return click.echo(text.center(width, "-"))

    for name, source in zip(source_names, sources, strict=False):
        _print_header(f" from {name} ")
        for adsorbate in source:
            click.echo(adsorbate)

    sys.exit(0)


@main.command(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.argument(
    "adsorbate",
    type=click.Choice(_all_adsorbates, case_sensitive=False),
    required=True,
    metavar="ADSORBATE",
)
@click.argument(
    "structure",
    required=True,
    type=click.Path(exists=True, path_type=pathlib.Path),
)
@click.argument(
    "destination",
    default=pathlib.Path.cwd(),
    type=click.Path(file_okay=False, path_type=pathlib.Path),
)
@click.option(
    "-s",
    "--separation",
    help=(
        "specify the minimum distance between the surface and any adsorbate "
        "atom"
    ),
    default=1.8,
    type=float,
)
@click.option(
    "-c",
    "--special-centres",
    help=("include atom-centred orientations"),
    flag_value=True,
    is_flag=True,
)
@click.option(
    "-Y",
    "--symmetric",
    help="treat the adsorbate as symmetric",
    flag_value=True,
    is_flag=True,
)
@click.option(
    "-V",
    "--vertical",
    help=("include vertical adsorption configurations"),
    flag_value=True,
    is_flag=True,
)
@click.option(
    "-l",
    "--list",
    help="list all available adsorbates",
    flag_value=True,
    is_flag=True,
    is_eager=True,
    callback=print_adsorbates,
    expose_value=False,
)
def place_adsorbate(
    adsorbate,
    structure,
    destination,
    separation,
    special_centres,
    symmetric,
    vertical,
):
    """Create adsorbate complexes for a given structure and.

    Each complex is written to a ``.traj`` file with identifying metadata
    about the adsorbate identity, orientation, site, and structure.

    ADSORBATE is the name of the adsorbate to place on the surface.

    STRUCTURE is the path to the surface on which the adsorbate will be placed.

    DESTINATION is the directory in which to write the ``.traj`` files. The
    directory is created if it does not exist. Defaults to the current
    working directory.
    """
    complexes = adsorbatecomplex.generate_complexes(
        adsorbate,
        structure,
        destination,
        separation,
        special_centres,
        symmetric,
        vertical,
    )
    print(f"{len(complexes)} complexes created.")
