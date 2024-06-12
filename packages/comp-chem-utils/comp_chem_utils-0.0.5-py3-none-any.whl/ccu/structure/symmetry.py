"""Symmetry-related functions and classes.

This class defines the :class:`Symmetry` and :class:`SymmetryOperation` subclasses.

.. admonition:: Example

    >>> import ase
    >>> from ccu.structure.symmetry import Rotation, RotationSymmetry
    >>> rotation1 = Rotation(90, [0, 0, 1])
    >>> symmetry1 = RotationSymmetry(rotation1)
    >>> co = ase.Atoms("CO", positions=[[0, 0, 0], [1, 0, 0]])
    >>> rotated = rotation1.transform(co)
    >>> rotated.positions
    array([[0.000000e+00, 0.000000e+00, 0.000000e+00],
          [6.123234e-17, 1.000000e+00, 0.000000e+00]])
    >>> symmetry1.check_symmetry(co)
    False
    >>> h2 = ase.Atoms("HH", positions=[[0, 0, 0], [1, 0, 0]])
    >>> rotation2 = Rotation(180, [0, 0, 1])
    >>> symmetry2 = RotationSymmetry(rotation2)
    >>> symmetry2.check_symmetry(h2)
    True
"""

import abc
from collections.abc import Iterable

import ase
import numpy as np
from numpy.linalg import norm
from scipy.spatial import transform

from ccu.structure import comparator


class SymmetryOperation(abc.ABC):
    """An abstract base class for symmetry operations."""

    @abc.abstractmethod
    def transform(self, structure: ase.Atoms) -> ase.Atoms:
        "Subclasses should override this method."


class Rotation(SymmetryOperation):
    """A rotation operation.

    Attributes:
        angle: A float specifying a rotation angle in degrees.
        axis: A numpy.array representing the axis of rotation.

    """

    def __init__(self, angle: float, axis: Iterable[float]) -> None:
        """Create a rotation symmetry operation.

        Args:
            angle: The angle of rotation.
            axis: The axis of rotation.
        """
        self.angle = angle
        self.axis = np.array(axis)

    def transform(self, structure: ase.Atoms) -> ase.Atoms:
        """Rotate a structure.

        This retthe given structure by the angle and about the axis
        specified as attributes of the Rotation object.

        Args:
            structure: An :class:`.atoms.Atoms` instance representing
                structure to be rotated.

        Returns:
            A copy of the original :class:`.atoms.Atoms` instance rotated by
            :attr:`Rotation.angle` about the axis :attr:`Rotation.axis`.

        """
        new_structure = structure.copy()
        new_structure.rotate(self.angle, self.axis)
        return new_structure

    def as_matrix(self) -> np.ndarray:
        """The rotation matrix of the symmetry operation."""
        rotvec = self.angle * (self.axis / norm(self.axis))
        rotation = transform.Rotation.from_rotvec(rotvec, degrees=True)
        return rotation.as_matrix()


class Inversion(SymmetryOperation):
    """An inversion operation."""


class Symmetry(abc.ABC):
    """An abstract base class for molecule symmetries."""

    @property
    @abc.abstractmethod
    def operation(self) -> SymmetryOperation:
        "Subclasses should override this method."

    @abc.abstractmethod
    def check_symmetry(self, structure: ase.Atoms, tol: float) -> bool:
        "Subclasses should override this method."


class RotationSymmetry(Symmetry):
    """A rotational symmetry."""

    def __init__(self, operation: Rotation) -> None:
        """Create a rotation symmetry.

        Args:
            operation: A rotation operation.
        """
        self._operation = operation

    @property
    def operation(self) -> Rotation:
        """The :class:`Rotation` associated with the symmetry."""
        return self._operation

    def check_symmetry(self, structure: ase.Atoms, tol: float = 5e-2) -> bool:
        """Check if the symmetry belongs to the structure's symmetry group.

        Args:
            structure: An :class:`.atoms.Atoms` instance representing the
                structure whose symmetry is to be determined.
            tol: A float specifying the absolute tolerance for positions.
                Defaults to 5e-2.

        Returns:
            A bool indicating whether or not the given structure possesses
                the symmetry of the :class:`RotationSymmetry` object subject
                to the specified tolerance.

        """
        old_structure = structure

        # Rotate structure
        rotated_structure = self._operation.transform(structure)

        # Check for similarity wrt. tolerance
        return comparator.Comparator.check_similarity(
            old_structure, rotated_structure, tol=tol
        )
