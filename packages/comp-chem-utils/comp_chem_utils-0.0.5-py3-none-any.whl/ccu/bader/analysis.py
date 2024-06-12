"""Utilities for analyzing Bader charge data."""

from collections.abc import Iterable
import logging
import pathlib

logger = logging.getLogger(__name__)


def _convert_to_poscar_indices(
    indices: Iterable[int], sort_file: str | pathlib.Path
) -> list[int]:
    """Convert ASE indices to VASP indices.

    This method requires the presence of an ``ase-sort.dat``-type file.

    Args:
        indices: The indices to convert.
        sort_file: A :class:`Path` representing the sort file.

    Returns:
        The original indices converted into VASP indices.

    Note:
        Given an :class:`.atoms.Atoms` object with ASE indices and a ``POSCAR``
        or ``CONTCAR`` file. This method enables conversion between the indices
        of the :class:`.atoms.Atoms` object and the resulting structure in the
        VASP file.
    """
    logger.debug(
        f"Converting ASE indices {indices!r} to VASP indices using "
        f"{sort_file}"
    )
    with pathlib.Path(sort_file).open(mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    conversion_table = [int(line.split()[-1]) for line in lines]

    new_indices = [conversion_table[i] for i in indices]

    logger.debug(
        f"Successfully converted ASE indices: {indices!r} -> {new_indices!r}"
    )
    return new_indices


def moiety_sum(
    indices: Iterable[int],
    sort_file: str | None = None,
    bader_file: str = "CHARGE_ANALYSIS.txt",
) -> int:
    """Calculate the cumulative Bader charge within a moiety.

    Args:
        indices: An iterable of integers, each representing an index of an
            atom within the moiety.
        sort_file: A string pointing to a file in the same format as
            ase-sort.dat to be used to map indices. If not provided, indices
            will be interpreted without conversion. Defaults to None.
        bader_file: A string representing the path to the charge analysis
            file. Defaults to "CHARGE_ANALYSIS.txt".

    Returns:
        The cumulative Bader charge of the moiety.

    """
    if sort_file:
        indices = _convert_to_poscar_indices(
            indices=indices, sort_file=sort_file
        )

    with pathlib.Path(bader_file).open(mode="r", encoding="utf-8") as file:
        lines = file.readlines()[1:]  # skip the header line

    bader_charges = [float(line.split()[-1]) for line in lines]

    return sum(bader_charges[i] for i in indices)
