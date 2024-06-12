"""This module defines the Fingerprint class."""

from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import MutableMapping
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    import ase


class Fingerprint(MutableMapping):
    """A set of displacement vectors relative to a particular atom.

    The displacement vectors for atoms of a given chemical symbol can be
    accessed through the ``MutableMapping`` interface. For example::

        structure = ase.Atoms("CO", positions=[[0, 0, 0], [1, 0, 0]])
        fp = Fingerprint(structure, 0, [0, 1])
        fp["C"]

    Attributes:
        structure: The ase.Atoms instance to which the :class:`Fingerprint`
            instance is related.
        reference: An int indicating the index of the reference
            atom used to construct the :class:`Fingerprint` instance.
        indices: A tuple indicating the indices of the atoms within the
            structure used to construct the :class:`Fingerprint` instance.

    """

    def __init__(
        self,
        structure: ase.Atoms,
        reference: int,
        indices: Iterable[int] | None = None,
    ) -> None:
        """Generate a fingerprint from a structure.

        Args:
            structure: The structure for which the ``Fingerprint`` will be
                generated.
            reference: The index of the reference atom within ``structure`` to
                ``Fingerprint``.
            indices: The indices of the atoms corresponding to the points for
                which the displacements will be calculated to generate the
                fingerprint. Defaults to None.
        """
        if indices is None:
            indices = range(len(structure))

        histogram = {}
        for atom in structure[indices]:
            displacement = atom.position - structure[reference].position
            if atom.symbol not in histogram:
                histogram[atom.symbol] = np.array([displacement])
            else:
                histogram[atom.symbol] = np.vstack(
                    [histogram[atom.symbol], displacement]
                )

        self._histogram: dict[str, np.ndarray] = histogram
        self.structure = structure
        self.reference = reference
        self.indices = tuple(indices)

    def __getitem__(self, __k: str) -> np.ndarray:
        """Get displacements to atoms with symbol __k.

        Args:
            __k: A chemical symbol.
        """
        return self._histogram[__k]

    def __setitem__(self, __k: int, __v: np.ndarray) -> None:
        """Set displacements` to atoms with symbol __k.

        Args:
            __k: A chemical symbol.
            __v: A 2D array of atomic displacements.
        """
        self._histogram[__k] = __v

    def __delitem__(self, __k) -> None:
        """Delete displacements to atoms with symbol __k.

        Args:
            __k: A chemical symbol.
        """
        del self._histogram[__k]

    def __iter__(self) -> Iterator[str]:
        """An iterator of chemical symbols."""
        return iter(self._histogram)

    def __len__(self) -> int:
        """The number of chemical symbols in the ``Fingerprint``."""
        return len(self._histogram)

    @classmethod
    def from_structure(cls, structure: ase.Atoms) -> list[Fingerprint]:
        """Creates a list of Fingerprint objects from an ase.Atoms object.

        Args:
            structure: An ase.Atoms instance representing the structure from
                which to create the list of ``Fingerprints``.

        Returns:
            A list of the ``Fingerprints`` for each atom.

        """
        fingerprints = []

        for i, _ in enumerate(structure):
            fingerprints.append(cls(structure, i))

        return fingerprints
