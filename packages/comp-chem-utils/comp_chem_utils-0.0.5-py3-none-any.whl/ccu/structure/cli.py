"""This module contains the ccu.structure package CLI logic."""

import math
import pathlib

from ase.io import read
import click

from ccu.structure import resizecell
from ccu.structure.defects import permute


@click.group(name=__package__.split(".")[-1])
def main():
    """Structure manipulation tools."""


@main.command(
    "resize-cell",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.argument(
    "structure",
    required=True,
    type=click.Path(exists=True, path_type=pathlib.Path),
)
@click.argument("c-vector", default=10, type=click.FLOAT)
def resize_and_centre(structure, c_vector):
    """Resizes the c-vector and centres given structure.

    STRUCTURE is the structure to be resized and centred.

    C_VECTOR is the new magnitude of the c-vector.
    """
    resizecell.run(structure, c_vector)


@main.command(
    "permute",
    epilog="""
Examples::
    ccu structure permute -o Co 1 -o Cu 1 -s Ni.traj -d trimetallics/ 0 1 2

    ccu structure permute -o Co 1 -o Cu 1 -s NiO.traj -d trimetallics/ Ni
              """,
)
@click.option(
    "-o",
    "--occupant",
    "occupants",
    nargs=2,
    type=(str, int),
    multiple=True,
    help="a 2-tuple indicating an element with which to permute the "
    "specified sites and the number of times to include the element. This "
    "option can be specified multiple times, but note that the sum of all "
    "second elements must not exceed the number of sites specified.",
)
@click.option(
    "-s",
    "--source",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path),
    help="the structure file to permute",
)
@click.option(
    "-d",
    "--destination",
    type=click.Path(file_okay=False, path_type=pathlib.Path),
    default=pathlib.Path.cwd(),
    help="the directory in which to place the permuted structure files. "
    "Defaults to current working directory.",
)
@click.argument(
    "sites",
    nargs=-1,
)
def cli_permute(
    source: pathlib.Path,
    destination: pathlib.Path,
    sites: tuple[int],
    occupants: tuple[tuple[str, int]],
):
    """Creates permutations of a given structure.

    SITES is a list of sites to permute. Can be specified as a list of
    indices or a list of chemical symbols.
    """
    structure = read(str(source))
    converted_sites: list[int | str] = []
    for site in sites:
        try:
            converted_sites.append(int(site))
        except ValueError:
            converted_sites.append(site)

    permuted_structures = permute(
        structure=structure,
        sites=converted_sites or None,
        occupancies=occupants or None,
    )

    if not destination.exists():
        destination.mkdir(parents=True)

    def format_indices(num: int) -> list[int]:
        digits = math.ceil(math.log10(num))
        formatted_indices = []
        for i in range(num + 1):
            converted_i = str(i)
            formatted_indices.append(
                f"{'0' * (digits - len(converted_i))}{converted_i}"
            )
        return formatted_indices

    formatted_indices = format_indices(len(permuted_structures) - 1)

    for i, permuted_structure in enumerate(permuted_structures):
        formatted_index = formatted_indices[i]
        permuted_structure.write(
            destination.joinpath(
                f"{source.stem}-{formatted_index}{source.suffix}"
            )
        )
