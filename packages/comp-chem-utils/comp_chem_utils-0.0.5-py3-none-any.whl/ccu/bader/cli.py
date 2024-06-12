"""CLI commands for Bader charge analysis."""

from collections.abc import Iterable
import logging

import ase
import ase.io
import click

from ccu.bader import analysis

logger = logging.getLogger(__package__.split(".")[0])


@click.group(name=__package__.split(".")[-1])
def main():
    """Bader charge analysis tools."""


def _get_tag_indices(atoms: ase.Atoms) -> dict[int, list[int]]:
    """Group indices by tag on an ase.Atoms object.

    Args:
        atoms: An :class:`ase.atoms.Atoms` object.

    Returns:
        A dictionary mapping tag numbers to the indices of atoms with that tag
        number.

    """
    indices: dict[int, list[int]] = {}

    for i, atom in enumerate(atoms):
        if atom.tag in indices:
            indices[atom.tag].append(i)
        else:
            indices[atom.tag] = [i]

    return indices


@main.command(
    "sum",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option(
    "--atoms",
    help="A file from which an ase.Atoms object can be read via "
    "ase.io.read. This option is required if --smart-mode is used.",
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "--smart-mode",
    required=False,
    is_flag=True,
    default=False,
    help="This is a special mode that will print out cumulative Bader "
    "charges for each tag group in the format ``<<TAG>>: <<BADER_CHARGE>>`` "
    "where ``<<TAG>>`` is an integer used to tag atoms in an "
    ":class:`~.atoms.Atoms` object and ``<<BADER_CHARGE>>`` is the sum of the "
    "Bader charge of all atoms with that tag. To use this option, you must "
    "specify a file from which an Atoms object can be read via ase.io.read "
    "via the :option:`--atoms` option. Note that if both "
    ":option:`--smart-mode` and ``INDICES`` are specified, this option is "
    "ignored.",
)
@click.option(
    "--sort-file",
    help="Specify a file in the format of ``ase-sort.dat`` used to translate "
    "indices in the Bader charge analysis file to the indices in the "
    "corresponding :class:`ase.atoms.Atoms` object.",
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "--bader-file",
    default="CHARGE_ANALYSIS.txt",
    help="Specify a path to the ``CHARGE_ANALYSIS.txt`` file produced by "
    "``bader_analysis.py``",
    show_default=True,
)
@click.argument(
    "indices",
    nargs=-1,
    type=int,
)
def sum_bader(
    atoms: str | None,
    smart_mode: bool,
    sort_file: str,
    bader_file: str,
    indices: Iterable[int],
) -> None:
    """Sum the bader charges atoms specified by indices.

    INDICES is a list of integers indicating the indices for which to sum
    Bader charges. Unless the ``--sort-file`` option is used, these
    indices are interpreted as the indices within the
    CHARGE_ANALYSIS.txt file. Note that if specified along with
    ``--smart-mode``, ``--smart-mode`` is ignored.
    """
    if smart_mode and atoms is None:
        msg = "You must specify a value to --atoms if --smart-mode is used"
        raise ValueError(msg)

    if not indices and not smart_mode:
        msg = "Either --smart-mode or INDICES must be specified"
        raise ValueError(msg)
    elif indices and smart_mode:
        logger.info(
            "Both INDICES and --smart-mode specified. Ignoring --smart-mode."
        )
    elif smart_mode:
        logger.debug("Smart mode activated")
        tag_to_indices = _get_tag_indices(atoms=ase.io.read(atoms))

        for tag, indices in tag_to_indices.items():
            bader_charge = analysis.moiety_sum(
                sort_file=sort_file,
                bader_file=bader_file,
                indices=indices,
            )
            print(f"{tag}: {bader_charge}")

    else:
        bader_charge = analysis.moiety_sum(
            sort_file=sort_file,
            bader_file=bader_file,
            indices=indices,
        )
        print(f"{indices!r}: {bader_charge}")
