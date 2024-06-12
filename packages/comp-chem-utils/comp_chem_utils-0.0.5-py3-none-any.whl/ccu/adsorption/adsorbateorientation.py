"""Classes for orienting adsorbates on adsorption sites."""

from collections.abc import Iterable
from collections.abc import Sequence

import ase
import numpy as np
from numpy import cross
from numpy.linalg import norm
from scipy.spatial import transform

from ccu.adsorption import sitefinder
from ccu.structure import axisfinder
from ccu.structure import symmetry


class AdsorbateOrientation:
    """An orientation of an adsorbate.

    An AdsorbateOrientation object contains the information required to
    unambiguously orient an adsorbate in space.

    Attributes:
        description: A string describing the adsorbate orientation.
        vectors: A tuple of numpy.array instances which are the vectors along
            which an adsorbate will be oriented. The sequence should contain
            two linearly independent unit vectors. The first vector is the
            primary orientation axis. The secondary vector is secondary
            orientation axis.

    """

    def __init__(
        self, description: str, orientation_vectors: Sequence[np.array]
    ) -> None:
        """Create an adsorbate orientation.

        Args:
            description: A description of the orientation.
            orientation_vectors: Two linearly independent vectors with which
                to orient the adsorbate.

        """
        self.description = description
        self.vectors = orientation_vectors


class AdsorbateOrientationFactory:
    """An AdsorbateOrientation factory.

    An AdsorbateOrientationFactory creates a collection of
    AdsorbateOrientation objects for a given AdsorptionSite subject to
    symmetry and orientation specifications.

    Attributes:
        site: A sitefinder.AdsorptionSite instance indicating site for which
            the orientations are to be created.
        adsorbate: An ase.Atoms instance representing the adsorbate which will
            assume the orientations.
        force_symmetry: A boolean indicating whether or not to force the
            adsorbate to be treated as symmetric.
        vertical: A boolean indicating whether or not vertical orientations
            will be created.

    """

    def __init__(
        self,
        site: sitefinder.AdsorptionSite,
        adsorbate: ase.Atoms,
        force_symmetry: bool = False,
        vertical: bool = False,
    ) -> None:
        """Create a factory.

        Args:
            site: The site on which the adsorbate will reside.
            adsorbate: The adsorbate to orient.
            force_symmetry: Whether or not to treat the adsorbate as
                symmetric. Defaults to False.
            vertical: Whether or not to generate vertical orientations.
                Defaults to False.

        """
        self.site = site
        self.adsorbate = adsorbate
        self.force_symmetry = force_symmetry
        self.vertical = vertical

    def create_orientations(self) -> list[AdsorbateOrientation]:
        """Creates a list of AdsorbateOrientation objects.

        Returns:
            A list of AdsorbateOrientation objects.

        """
        orientations = []
        # Single orientation for zero dimensional adsorbate
        if norm(axisfinder.find_primary_axis(self.adsorbate)) == 0:
            vectors = (self.site.alignments[0].vector, self.site.surface_norm)
            orientation = AdsorbateOrientation("", vectors)
            return [orientation]

        for alignment in self.site.alignments:
            orientation = AdsorbateOrientation(
                f"{alignment.description} 1",
                [alignment.vector, self.site.surface_norm],
            )

            if self.force_symmetry:
                orientations.append(orientation)
            else:
                orientations.extend(
                    self._create_asymmetric_orientations(
                        alignment, orientation
                    )
                )

        if self.vertical:
            orientations.extend(self._create_vertical_orientations())

        return orientations

    def _create_asymmetric_orientations(
        self,
        alignment: sitefinder.SiteAlignment,
        orientation: AdsorbateOrientation,
    ) -> list[AdsorbateOrientation]:
        """Create a list of asymmetric orientations.

        Args:
            alignment: A sitefinder.SiteAlignment instance representing the
                alignment for the adsorption site.
            orientation: An AdsorbateOrientation instance representing the
                adsorbate orientation to be combined with the newly created
                orientations.

        Returns:
            The list of AdsorbateOrientation instances representing adsorption
            sites.

        """
        primary_axis = axisfinder.find_primary_axis(self.adsorbate)

        orientations = [orientation]

        for i in range(1, 4):
            rotation_ = symmetry.Rotation(i * 90, primary_axis)
            symmetry_ = symmetry.RotationSymmetry(rotation_)
            if not symmetry_.check_symmetry(self.adsorbate):
                rot_vec = i * 90 * alignment.vector
                matrix = transform.Rotation.from_rotvec(rot_vec, degrees=True)
                vec = matrix.apply(self.site.surface_norm)
                orientations.append(
                    AdsorbateOrientation(
                        f"{alignment.description} {i + 1}",
                        [alignment.vector, vec],
                    )
                )

        return orientations + self._create_reverse_orientations(
            alignment, orientations
        )

    def _create_vertical_orientations(self) -> list[AdsorbateOrientation]:
        """Create the vertical adsorbate orientations for a site.

        Returns:
            The list of AdsorbateOrientation instances representing the
            vertical adsorbate orientations.

        """
        orientations = []
        secondary_axis = axisfinder.find_secondary_axis(self.adsorbate)
        no_secondary_axis = norm(secondary_axis) == 0
        for i, alignment in enumerate(self.site.alignments):
            if i != 0 and (no_secondary_axis or self.force_symmetry):
                break

            orientations.append(
                AdsorbateOrientation(
                    f"vertical {i+1}",
                    [self.site.surface_norm, alignment.vector],
                )
            )

        reverse_orientations = []

        if not self.force_symmetry:
            reverse_orientations.extend(
                self._create_reverse_orientations(
                    (self.site.surface_norm, "vertical"), orientations
                )
            )

        return orientations + reverse_orientations

    def _create_reverse_orientations(
        self,
        alignment: sitefinder.SiteAlignment | tuple,
        orientations: Iterable[AdsorbateOrientation],
    ) -> list[AdsorbateOrientation]:
        """Create mirrored adsorbate orientations.

        Args:
            alignment: The alignment for the site. This can be supplied as
                either a :class:`.sitefinder.SiteAlignment` instance or as a
                2-tuple whose first and second elements are the alignment
                vector and description, respectively.
            orientations: An iterable of :class:`AdsorbateOrientation`
                instances representing the adsorbate orientations to be
                reversed.

        Returns:
            A list of :class:`AdsorbateOrientation` instances representing the
            reversed adsorbate orientations.

        """
        if isinstance(alignment, sitefinder.SiteAlignment):
            vector = alignment.vector
            description = alignment.description
        else:
            vector, description = alignment

        secondary_axis = axisfinder.find_secondary_axis(self.adsorbate)

        # Deal with linear adsorbates
        if norm(secondary_axis) == 0:
            primary_axis = axisfinder.find_primary_axis(self.adsorbate)
            secondary_axis = cross(primary_axis, [1, 0, 0])
            if norm(secondary_axis) == 0:
                secondary_axis = cross(primary_axis, [0, 1, 0])
            secondary_axis = secondary_axis / norm(secondary_axis)

        rotation_ = symmetry.Rotation(180, secondary_axis)
        symmetry_ = symmetry.RotationSymmetry(rotation_)

        reverse_orientations = []

        if not symmetry_.check_symmetry(self.adsorbate):
            vec = -vector
            start = len(orientations)
            for i, orientation in enumerate(orientations):
                reverse_orientations.append(
                    AdsorbateOrientation(
                        f"{description} {start + i + 1}",
                        [vec, orientation.vectors[1]],
                    )
                )

        return reverse_orientations
