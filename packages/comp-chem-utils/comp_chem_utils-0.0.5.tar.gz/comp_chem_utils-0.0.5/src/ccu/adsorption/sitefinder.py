"""Classes for locating and distinguishing adsorption sites.

Specifically, this module provides the :class:`AdsorptionSite`,
:class:`.SiteFinder`, and :class:`MOFSiteFinder` classes.
"""

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from collections.abc import Sequence
from typing import ClassVar

import ase
import numpy as np
from numpy import cross
from numpy import dot
from numpy.linalg import norm


# TODO: Convert to NamedTuple
class SiteAlignment:
    """An alignment that an adsorbate can assume on a site.

    Attributes:
        vector: A :class:`.numpy.array` representing the alignment vector as a
            unit vector.
        description: A description of the site alignment.

    """

    def __init__(
        self, alignment_vector: Sequence[float], description: str
    ) -> None:
        """Create a site alignment.

        Args:
            alignment_vector: A 3-element sequence of floats representing a
                direction in space.
            description: A description of the alignment.

        """
        vector = np.array(alignment_vector)
        self.vector = vector / norm(vector)
        self.description = description


# TODO: Convert to NamedTuple
class AdsorptionSite:
    """An adsorption site.

    Attributes:
        location: A :class:`.numpy.array` representing the location of the
            adsorption site.
        description: A description of the adsorption site as a string.
        alignments: A list of :class:`SiteAlignment` objects defining
            alignments for the site.
        surface_norm: A :class:`.numpy.array` representing the unit normal
            vector for the surface hosting the adsorption site.

    """

    def __init__(
        self,
        location: Sequence[float],
        description: str,
        alignments: Iterable[SiteAlignment],
        surface_norm: Sequence[float],
    ) -> None:
        """Initialize an adsorption site.

        Args:
            location: A 3-element sequence of floats identify the adsorption
                site in space.
            description: A description of the adsorption site.
            alignments: A list of alignments characterizing the site.
            surface_norm: A 3-element sequence representing the direction of
                the site surface norm.

        """
        self.location = np.array(location)
        self.description = description
        self.alignments = alignments
        vector = np.array(surface_norm)
        self.surface_norm = vector / norm(vector)


class MOFSite(AdsorptionSite):
    """An adsorption site within a MOF.

    Attributes:
        location: A :class:`.numpy.array` representing the location of the
            adsorption site.
        description: A description of the adsorption site as a string.
        alignments: A list of :class:`SiteAlignment` objects defining
            alignments for the site.
        surface_norm: A :class:`.numpy.array` representing the normal vector
            for the surface hosting the adsorption site.
        intermediate_alignments: A bool indicating whether or not to
            consider intermediate alignments.

    """

    def __init__(
        self,
        location: Sequence[float],
        description: str,
        alignment_atoms: Iterable[ase.Atom],
        site_anchor: Sequence[float],
        surface_norm: Sequence[float],
        intermediate_alignments: bool = False,
    ) -> None:
        """Create a site on a metal-organic framework.

        Args:
            location: A :class:`.numpy.array` representing the location of the
                adsorption site.
            description: A description of the adsorption site as a string.
            alignment_atoms: A list of :class:`.atom.Atom` instances, which, in
                concert with ``site_anchor`` can be used to generate alignment
                directions.
            site_anchor: A 3-element sequence of floats representing a
                reference location in space to be used to generate alignment
                directions. The generated alignments will constitute every
                direction from from the site anchor to an alignment atom.
            surface_norm: A :class:`.numpy.array` representing the normal
                vector for the surface hosting the adsorption site.
            intermediate_alignments: A bool indicating whether or not to
                consider intermediate alignments. Defaults to False.

        """
        self.intermediate_alignments = intermediate_alignments
        alignments = self.create_alignments(alignment_atoms, site_anchor)
        super().__init__(location, description, alignments, surface_norm)

    def create_alignments(
        self, alignment_atoms: Iterable[ase.Atom], site_anchor: Sequence[float]
    ) -> list[SiteAlignment]:
        """Creates the :class:`SiteAlignment` objects for a ``MOFSite``.

        Args:
            alignment_atoms: An iterable containing :class:`.atom.Atom`
                instances which will be used to define alignment directions.
            site_anchor: A sequence of 3 floats representing a reference
                location using for defining alignment directions. This is
                usually the position of the metal atom in the site.

        Returns:
            A list of :class:`SiteAlignment` instances representing the
            alignments for a :class:`MOFSite` instance.

        """
        alignments = []
        colinear_vectors = []
        added_elements = []
        for atom in alignment_atoms:
            vector = atom.position - site_anchor
            vector = vector / norm(vector)
            colinear_vectors.append(vector)
            description = f"colinear with {atom.symbol}"
            if atom.symbol not in added_elements:
                alignments.append(SiteAlignment(vector, description))
                added_elements.append(atom.symbol)

        if self.intermediate_alignments:
            alignments.extend(
                self.create_intermediate_alignments(colinear_vectors)
            )

        return alignments

    def create_intermediate_alignments(
        self, colinear_vectors: list[Sequence[float]]
    ) -> list[SiteAlignment]:
        """Create intermediate alignments.

        Args:
            colinear_vectors: 3-float sequences representing the direction
                of the intermediate alignments.

        Returns:
            A list of :class:`SiteAlignment` instances representing the
            intermediate alignments for a :class:`MOFSite` instance.

        """
        # TODO! Order collinear alignments by angle and define intermediate
        # TODO! alignments as bisectors
        parallel_line = 0.5 * (colinear_vectors[0] + colinear_vectors[1])
        parallel_line = parallel_line / norm(parallel_line)

        perpendicular_line = (
            colinear_vectors[0]
            - dot(colinear_vectors[0], parallel_line) * parallel_line
        )
        perpendicular_line = perpendicular_line / norm(perpendicular_line)
        return [
            SiteAlignment(parallel_line, "parallel"),
            SiteAlignment(perpendicular_line, "perpendicular"),
        ]


class SiteFinder(ABC):
    """An abstract base class for finding adsorption sites.

    Subclasses must define the abstract method "sites" which returns all
    adsorption sites for a given structure.
    """

    @abstractmethod
    def __init__(self, structure: ase.Atoms) -> None:
        """Create a site finder.

        Args:
            structure: The structure on which to find sites.

        """

    @abstractmethod
    def sites(self) -> Iterable[AdsorptionSite]:
        """Subclasses should override this method."""


class MOFSiteFinder(SiteFinder):
    """Find adsorption sites on MOF surfaces.

    Currently, the atoms bonded to the metal within the SBU must possess tags
    of 1 and the metal must possess a tag of 2 for the implementation to work
    correctly.

    Attributes:
        structure: An :class:`.atoms.Atoms` object representing a
            metal-organic framework.
        DEFAULT_SBU_TAG: The default tag for the secondary building unit central atom

    """

    DEFAULT_SBU_TAG: ClassVar[int] = 2

    def __init__(
        self, structure: ase.Atoms, *, between_linkers: bool = False
    ) -> None:
        """Create a :class:`ccu.adsorption.sitefinder.MOFSiteFinder`.

        Args:
            structure: The structure on which to find adsorption sites.
            between_linkers: Whether to include between linker sites. Defaults
                to False.

        """
        super().__init__(structure)
        self.structure = structure
        self.between_linkers = between_linkers

    def sites(self) -> list[AdsorptionSite]:
        """Determines all unique SBU adsorption sites for a given MOF.

        Note that the :class:`AdsorptionSite` instances are defined such that
        the first and second elements in their "alignment_atoms" attribute are
        linker atoms and the third element is the metal.

        Returns:
            A list of :class:`AdsorptionSite` instances representing the SBU
            adsorption sites of the given MOF.

        """
        sites = self.create_linker_sites()
        sites.append(self.create_metal_site())
        if self.between_linkers:
            sites.append(self.create_between_linker_site())

        return sites

    @property
    def adjacent_linkers(self) -> list[ase.Atom]:
        """``ase.Atom`` instances representing adjacent linker atoms."""
        linkers = [atom for atom in self.structure if atom.tag == 1]

        closest_linker = linkers[1]
        for linker in linkers[1:]:
            if norm(linkers[0].position - linker.position) < norm(
                linkers[0].position - closest_linker.position
            ):
                closest_linker = linker

        return [linkers[0], closest_linker]

    @property
    def sbu_metal(self) -> ase.Atom:
        """The metal atom within the SBU of the MOF."""
        for atom in self.structure:
            if atom.tag == MOFSiteFinder.DEFAULT_SBU_TAG:
                return atom

        msg = "No metal atom tagged. (Metal atom must be tagged with 2.)"
        raise ValueError(msg)

    @property
    def surface_norm(self) -> np.array:
        """The unit norm to the secondary building unit.

        The unit norm is defined relative to the plane determined by two
        adjacent linker atoms and the metal within the SBU.
        """
        # Calculate upwards-pointing norm vector
        vector1 = self.adjacent_linkers[0].position - self.sbu_metal.position
        vector2 = self.adjacent_linkers[1].position - self.sbu_metal.position
        norm_vector = cross(vector1, vector2)

        if dot(norm_vector, [0, 0, 1]) < 0:
            norm_vector = -norm_vector

        return norm_vector / norm(norm_vector)

    def create_linker_sites(self) -> list[MOFSite]:
        """Returns a list of adsorption sites centred on MOF linker atoms."""
        linkers = self.adjacent_linkers
        sbu_metal = self.sbu_metal
        surface_norm = self.surface_norm

        # Define unique linker sites
        linker_sites = [
            MOFSite(
                linkers[0].position,
                f"on {linkers[0].symbol} linker",
                linkers,
                sbu_metal.position,
                surface_norm,
                True,
            )
        ]
        if linkers[0].symbol != linkers[1].symbol:
            linker_sites.append(
                MOFSite(
                    linkers[1].position,
                    f"on {linkers[1].symbol} linker",
                    linkers,
                    sbu_metal.position,
                    surface_norm,
                    True,
                )
            )

        return linker_sites

    def create_metal_site(self) -> MOFSite:
        """Returns an adsorption site centred on the MOF metal atom."""
        sbu_metal = self.sbu_metal
        linkers = self.adjacent_linkers
        surface_norm = self.surface_norm

        return MOFSite(
            sbu_metal.position,
            f"on {sbu_metal.symbol}",
            linkers,
            sbu_metal.position,
            surface_norm,
            True,
        )

    def create_between_linker_site(self) -> MOFSite:
        """Returns an adsorption site centred between the MOF linker atoms."""
        sbu_metal = self.sbu_metal
        linkers = self.adjacent_linkers
        surface_norm = self.surface_norm

        return MOFSite(
            0.5 * (linkers[0].position + linkers[1].position),
            "between linkers",
            linkers,
            sbu_metal.position,
            surface_norm,
            True,
        )
