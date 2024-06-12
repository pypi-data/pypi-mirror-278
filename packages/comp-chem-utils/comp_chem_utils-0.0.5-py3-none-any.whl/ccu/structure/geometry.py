"""Geometry-related functions for atomic structures."""

from itertools import product
import math

import ase
from numpy.linalg import norm


def calculate_separation(
    structure1: ase.Atoms, structure2: ase.Atoms
) -> float:
    """Calculates the separation between two Atoms instances.

    The distance is defined as the smallest distance between an atom in one
    structure and an atom in the second structure.

    Args:
        structure1: An :class:`.atoms.Atoms` instance.
        structure2: An :class:`.atoms.Atoms` instance.

    Returns:
        A float representing the separation between the two structures.

    """
    minimum_separation = math.inf
    structures = product(structure1.positions, structure2.positions)
    for position1, position2 in structures:
        separation = norm(position1 - position2)
        if separation < minimum_separation:
            minimum_separation = separation

    return minimum_separation
