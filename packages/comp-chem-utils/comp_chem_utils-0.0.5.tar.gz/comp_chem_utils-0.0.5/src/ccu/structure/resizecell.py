"""Cell resizing tools.

This script resizes the c vector of all the ``.traj`` files in the current
working directory to the specified positive number.
"""

import pathlib

from ase.io import read
from numpy.linalg import norm


def run(structure: pathlib.Path, length: float):
    """Resize c-vector of structure and centres atoms in cell.

    Args:
        structure: A :class:`~Path` instance leading to the structure
            whose cell is to be resized.
        length: A float specifying the new c-vector of the cell.

    """
    atoms = read(structure)
    c_vector = atoms.cell[2]
    c_scale = length / norm(c_vector)
    atoms.cell[2] = c_vector * c_scale
    atoms.center()
    atoms.write(structure)
