"""Utilities for determining a molecule's orientation axes.

.. admonition:: Example

    The function :func:`get_axes` returns all three orientation axes for a
    given molecule.

    >>> import ase
    >>> from ccu.structure.axisfinder import get_axes
    >>> coh = ase.Atoms("COH", positions=[[0, 0, 0], [-2, 0, 0], [-1, 0.5, 0]])
    >>> get_axes(coh)
    (array([1., 0., 0.]), array([0., 1., 0.]), array([0., 0., 1.]))

.. admonition:: Example

    The function :func:`find_farthest_atoms` returns the two atoms within a
    molecule whose separation is the greatest. For example,

    >>> import ase
    >>> from ccu.structure.axisfinder import find_farthest_atoms
    >>> coh = ase.Atoms("COH", positions=[[0, 0, 0], [-2, 0, 0], [-1, 0.5, 0]])
    >>> find_farthest_atoms(coh)
    (Atom('C', [0.0, 0.0, 0.0], index=0), Atom('O', [-2.0, 0.0, 0.0], index=1))

.. admonition:: Example

    The function :func:`find_primary_axis` returns the primary orientation axis
    for a given molecule. For example,

    >>> import ase
    >>> from ccu.structure.axisfinder import find_primary_axis
    >>> coh = ase.Atoms("COH", positions=[[0, 0, 0], [-2, 0, 0], [-1, 0.5, 0]])
    >>> find_primary_axis(coh)
    array([1., 0., 0.])

.. admonition:: Example

    The function :func:`find_secondary_axis` returns the primary orientation
    axis for a given molecule. For example,

    >>> import ase
    >>> from ccu.structure.axisfinder import find_secondary_axis
    >>> coh = ase.Atoms("COH", positions=[[0, 0, 0], [-2, 0, 0], [-1, 0.5, 0]])
    >>> find_secondary_axis(coh)
    array([0., 1., 0.])

.. admonition:: Example

    The function :func:`find_tertiary_axis` returns the primary orientation
    axis for a given molecule. For example,

    >>> import ase
    >>> from ccu.structure.axisfinder import find_tertiary_axis
    >>> coh = ase.Atoms("COH", positions=[[0, 0, 0], [-2, 0, 0], [-1, 0.5, 0]])
    >>> find_tertiary_axis(coh)
    array([0., 0., 1.])
"""

from itertools import product

import ase
import numpy as np
from numpy import cross
from numpy import dot
from numpy.linalg import norm


def get_axes(molecule: ase.Atoms) -> tuple[np.array]:
    """Determine a molecule's three orientation axes.

    The primary axis is defined as the vector between the two most distant
    atoms. The secondary axis is defined as the orthogonal component (to the
    primary axis) of the vector from the primary axis to the atom farthest
    from the line between the two most distant atoms. The tertiary axis is the
    cross product of the primary and secondary axes. The axes so defined are
    orthogonal. Note that if the molecule is unimolecular, all three vectors
    will be the zero vector, and that if the molecule is linear only the
    primary axis will be nonzero.

    Args:
        molecule: An ase.Atoms instance whose axes are to be determined.

    Returns:
        A tuple containing unit vectors reprsenting the three orientation
        axes. The first, second, and third entries are the primary, secondary,
        and tertiary axes, respectively. For nonlinear molecules, the axes
        form an orthonormal set.

    """
    primary_axis = find_primary_axis(molecule)
    secondary_axis = find_secondary_axis(molecule)
    tertiary_axis = cross(primary_axis, secondary_axis)
    return primary_axis, secondary_axis, tertiary_axis


def find_farthest_atoms(
    molecule: ase.Atoms, tol: float = 1e-5
) -> tuple[ase.Atoms]:
    """Find the two atoms in the molecule separated by the greatest distance.

    In molecules for which there are several pairs of atoms with equidistant
    separations, this function will return the pair of atoms with lowest
    indices whose separation is within a given tolerance of the largest
    atomic separation in the molecule. Each pair is sorted according to the
    index of the lowest index atom and then the index of the second atom. For
    example,

    *   If atoms 0 and 1 have the same separation as atoms 2 and 3, atoms
        0 and 1 will be returned since 0 < 2.
    *   If atoms 0 and 1 have the same separation as atoms 0 and 3, atoms
        0 and 1 will be returned since 1 < 3.
    *   If atoms 1 and 2 have the same separation as atoms 0 and 4, atoms
        0 and 4 will be returned since 0 < 1.
    *   If atoms 1 and 2 have the same separation as atoms 0 and 2, atoms
        0 and 2 will be returned since 0 < 1.

    Args:
        molecule: The molecule for whom the two farthest atoms are to be
            determined.
        tol: A float indicating the resolution (in Angstroms) between atomic
            distances.

    Returns:
        A tuple containing the two atoms in the molecule separated by the
        greatest distance. The atoms are ordered by lowest index within the
        structure.

    """
    max_distance = 0
    for atom1, atom2 in product(molecule, repeat=2):
        distance = norm(atom1.position - atom2.position)
        if distance - max_distance > tol or max_distance == 0:
            max_distance = distance
            if atom1.index < atom2.index:
                farthest_atoms = atom1, atom2
            else:
                farthest_atoms = atom2, atom1

    return farthest_atoms


def find_primary_axis(molecule: ase.Atoms) -> np.array:
    """Determine the primary orientation axis of a molecule.

    The primary axis is defined as the unit vector which is parallel to the
    direction vector between the two most distant atoms in the molecule and
    points from the higher index atom to the lower index atom.

    Args:
        molecule: An :class:`.atoms.Atoms` instance representing the molecule
            for whom the primary axis is to be determined.

    Returns:
        A :class:`numpy.array` representing a unit vector in the direction of
        the primary orientation axis. Note that for zero-dimensional molecules,
        this function will return the zero vector.

    """
    farthest_atoms = find_farthest_atoms(molecule)
    primary_axis = farthest_atoms[0].position - farthest_atoms[1].position
    if norm(primary_axis) > 0:
        return primary_axis / norm(primary_axis)

    return primary_axis


def find_secondary_axis(
    molecule: ase.Atoms, min_distance: float = 0.1
) -> np.array:
    """Determine the secondary orientation axis of a molecule.

    Let :math:`L` be the line between the two farthest atoms in the molecule,
    let :math:`v` be the vector which defines the primary axis, and let
    :math:`P` be the position of the atom farthest from :math:`L`. Further,
    let :math:`w` be the vector from :math:`L` to :math:`P`, and
    let :math:`z` be the component of :math:`w` which is orthogonal to
    :math:`v`. The secondary axis is defined as the unit vector in the
    direction of :math:`z`.

    Args:
        molecule: An :class:`.atoms.Atoms` instance representing the molecule
            for whom the secondary axis is to be determined.
        min_distance: A float specifying the minimum distance from the primary
            axis (in Angstroms) to be considered for defining the secondary
            axis. Defaults to 0.1.

    Returns:
        A :class:`numpy.array` representing a unit vector in the direction of
        the secondary orientation axis. Note that for zero- and one-dimensional
        molecules, this function will return the zero vector.

    """
    farthest_atom1, _ = find_farthest_atoms(molecule)
    primary_axis = find_primary_axis(molecule)
    max_distance = min_distance
    secondary_axis = np.array([0.0, 0.0, 0.0])
    for atom in molecule:
        distance_vector = atom.position - farthest_atom1.position
        perpendicular_vector = (
            distance_vector - dot(distance_vector, primary_axis) * primary_axis
        )
        distance_from_primary_axis = norm(perpendicular_vector)
        if distance_from_primary_axis > max_distance:
            secondary_axis = perpendicular_vector / distance_from_primary_axis

    return secondary_axis


def find_tertiary_axis(molecule: ase.Atoms) -> np.array:
    """Determine the tertiary orientation axis of a molecule.

    The tertiary orientation axis is simply the cross product of the primary
    and secondary orientation axes. See :func:`find_primary_axis` and
    :func:`find_secondary_axis` for information on how these axes are defined.

    Args:
        molecule: An :class:`.atoms.Atoms` instance representing the molecule
            for whom the tertiary axis is to be determined.

    Returns:
        A :class:`numpy.array` representing a unit vector in the direction of
        the tertiary orientation axis. Note that if the molecule is zero- or
        one-dimensional, this function will return the zero vector.

    """
    primary_axis = find_primary_axis(molecule)
    secondary_axis = find_secondary_axis(molecule)
    return cross(primary_axis, secondary_axis)
