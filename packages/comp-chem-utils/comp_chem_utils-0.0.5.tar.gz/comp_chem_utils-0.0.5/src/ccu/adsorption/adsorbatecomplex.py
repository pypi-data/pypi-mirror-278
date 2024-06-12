"""Classes for producing catalyst-adsorbate complexes.

Specifically, this module provides the :class:`AdsorbateComplex` and
:class:`AdsorbateComplexFactory` classes.
"""

from collections.abc import Iterator
from pathlib import Path
from typing import Literal
from typing import overload

import ase
from ase.io import read
import numpy as np
from numpy import dot
from numpy import ndarray
from numpy.linalg import norm

from ccu.adsorption import adsorbateorientation
from ccu.adsorption import adsorbates
from ccu.adsorption import sitefinder
from ccu.structure import axisfinder
from ccu.structure import geometry


# TODO: Add metadata to Atoms.info
class AdsorbateComplex:
    """An adsorbate complex.

    Attributes:
        adsorbate_description: A description of the adsorbate.
        structure_description: A description of the surface structure.
        site_description: A description of the adsorption site.
        orientation_description: A description of the adsorbate orientation.
        structure: The :class:`.atoms.Atoms` object representing the adsorbate
            complex.

    """

    def __init__(
        self,
        adsorbate_description: str,
        site_description: str,
        orientation_description: str,
        structure_description: str,
        structure: ase.Atoms,
    ) -> None:
        """Initialize an instance from its attributes.

        Args:
            adsorbate_description: A description of the adsorbate.
            site_description: A description of the adsorption site.
            orientation_description: A description of the adsorbate
                orientation.
            structure_description: A description of the surface structure.
            structure: The :class:`.atoms.Atoms` object representing the
                adsorbate complex.

        """
        self.structure_description = structure_description
        self.adsorbate_description = adsorbate_description
        self.site_description = site_description
        self.orientation_description = orientation_description
        self.structure = structure

    def write(self, destination: Path | None = None) -> Path:
        """Write the ``AdsorbateComplex`` object to an ASE ``.traj`` file.

        Args:
            destination: A :class:`Path` indicating the directory in
                which to write the ``.traj`` file. Defaults to the current
                working directory.

        Returns:
            A :class:`Path` indicating the filename of the written ``.traj``
            file.

        """
        if destination is None:
            destination = Path.cwd()

        if self.orientation_description == "":
            description = (
                self.structure_description.replace(" ", "_"),
                self.adsorbate_description.replace(" ", "_"),
                self.site_description.replace(" ", "_"),
            )
        else:
            description = (
                self.structure_description.replace(" ", "_"),
                self.adsorbate_description.replace(" ", "_"),
                self.site_description.replace(" ", "_"),
                self.orientation_description.replace(" ", "_"),
            )

        filename = "_".join(description)
        index = 0
        while destination.joinpath(f"{filename}_{index}.traj").exists():
            index += 1

        self.structure.write(destination.joinpath(f"{filename}_{index}.traj"))
        return filename


class AdsorbateComplexFactory:
    r"""An AdsorbateComplex factory.

    Given an adsorbate, a structure, and various configuration specifications
    (e.g., ``symmetric``, ``vertical``), an :class:`AdsorbateComplexFactory`
    determines all of the adsorption sites and corresponding adsorbate
    configurations.

    Attributes:
        _structure: An :class:`.atoms.Atoms` instance representing the surface
            structure.
        separation: The distance (in Angstroms) that the adsorbate should be
            placed from the surface. Defaults to 1.8.
        special_centres: A bool indicating whether atom-centred
            placement will be used in addition to centre-of-mass placement.
        symmetric: A bool indicating whether or not the adsorbate is to be
            treated as symmetric.
        vertical: A bool indicating whether or not to consider vertical
            adsorption sites.

    """

    def __init__(
        self,
        adsorbate: ase.Atoms,
        structure: ase.Atoms,
        separation: float = 1.8,
        special_centres: bool = False,
        symmetric: bool = False,
        vertical: bool = False,
    ) -> None:
        r"""Create an ``AdsorbateComplexFactor``.

        Args:
            adsorbate: The adsorbate in the complex.
            structure: The structure on which to place the adsorbate.
            separation: The distance (in Angstroms) that the adsorbate should
                be placed from the surface. Defaults to 1.8.
            special_centres: Whether or not to produce atom-centred
                placements. Defaults to False.
            symmetric: Whether or not to treat the adsorbate as symmetric.
                Defaults to False.
            vertical: Whether to produce vertical orientations. Defaults to
                False.

        Note:
            In addition to setting ``special centres`` to True, one must also
            specify the indices of the atomic centres in order to use
            atom-centred placement. Specifically, the ``"special_centres"``
            key in ``adsorbates``\ 's :attr:`.atoms.Atoms.info` dictionary
            must map to an iterable whose elements specify the indices of the
            atoms to be used to centre the adsorbate. If this key is not
            present in the info attribute, then the position of the atom in
            ``adsorbate`` with index 0 will be used to centre the adsorbate.

        """
        self._adsorbate = adsorbate
        self._structure = structure
        self.separation = separation
        self.symmetric = symmetric
        self.vertical = vertical
        self.special_centres = special_centres
        if special_centres and "special centres" not in adsorbate.info:
            self._adsorbate.info["special centres"] = (0,)

    @property
    def adsorbate(self) -> ase.Atoms:
        """The adsorbate to be placed."""
        return self._adsorbate.copy()

    @property
    def structure(self) -> ase.Atoms:
        """The structure on which to place the adsorbate."""
        return self._structure.copy()

    def next_complex(
        self, site: sitefinder.AdsorptionSite, adsorbate_tag: int = -99
    ) -> Iterator[AdsorbateComplex]:
        """Yield next adsorbate-surface complex for a given site.

        Args:
            site: A sitefinder.AdsorptionSite instance which represents the
                site for which to generate complexes.
            adsorbate_tag: An integer with which to tag the adsorbate to
                enable tracking. Defaults to -99.

        """
        orientations = self.adsorbate_orientations(site)

        for orientation in orientations:
            if len(self._adsorbate) > 1:
                oriented_adsorbate = self.orient_adsorbate(orientation)
            else:
                oriented_adsorbate = self.adsorbate

            # Tags to distinguish adsorbate from surface atoms (useful for
            # vibrational calculations)
            oriented_adsorbate.set_tags(adsorbate_tag)

            oriented_adsorbate.set_cell(self._structure.cell[:])

            centres: ndarray[np.floating] = [
                oriented_adsorbate.get_center_of_mass()
            ]

            if self.special_centres:
                for i in self._adsorbate.info["special centres"]:
                    new_centre: ndarray[np.floating] = (
                        oriented_adsorbate.positions[i]
                    )
                    if not any(
                        all(centre == new_centre) for centre in centres
                    ):
                        centres.append(new_centre)

            for centre in centres:
                adsorbate_to_place = oriented_adsorbate.copy()
                self.place_adsorbate(adsorbate_to_place, site, centre)

                # Add adsorbate to structure
                new_structure = self.structure
                new_structure.extend(adsorbate_to_place)

                adsorbate_complex = AdsorbateComplex(
                    self._adsorbate.info.get("name", "adsorbate"),
                    site.description,
                    orientation.description,
                    new_structure.info["description"],
                    new_structure,
                )

                yield adsorbate_complex

    def adsorbate_orientations(
        self, site: sitefinder.AdsorptionSite
    ) -> list[adsorbateorientation.AdsorbateOrientation]:
        """Generate all adsorbate orientations for a given adsorption site.

        Args:
            site: An :class:`ccu.adsorption.sitefinder.AdsorptionSite`
                for which to generate adsorbate orientations.

        Returns:
            A list of :class:`.adsorbateorientation.AdsorbateOrientation`
            instances.

        """
        orientation_factory = adsorbateorientation.AdsorbateOrientationFactory(
            site, self._adsorbate, self.symmetric, self.vertical
        )
        return orientation_factory.create_orientations()

    def orient_adsorbate(
        self, orientation: adsorbateorientation.AdsorbateOrientation
    ) -> ase.Atoms:
        """Orients the ``AdsorbateComplexFactory``'s adsorbate.

        Args:
            orientation: An
                :class:`.adsorbateorientation.AdsorbateOrientation` instance
                representing the orientation in which the adsorbate is to be
                directed.

        Returns:
            An :class:`.atoms.Atoms` instance representing the oriented
            adsorbate as a copy of the ``AdsorbateComplexFactory``'s adsorbate.

        Note:
            The adsorbate is oriented such that its primary axis is aligned
            with the primary orientation vector of the given
            :class:`.adsorbateorientation.AdsorbateOrientation` object and its
            secondary axis is in the plane defined by the primary axis of the
            adsorbate and the secondary orientation.

        """
        new_adsorbate = self.adsorbate

        axis1 = axisfinder.find_primary_axis(new_adsorbate)

        # No first orientation for zero-dimensional molecule
        if norm(axis1) == 0:
            return new_adsorbate

        atom1, _ = axisfinder.find_farthest_atoms(new_adsorbate)

        # Orient along primary orientation axis
        new_adsorbate.rotate(axis1, orientation.vectors[0], atom1.position)

        # Orient using secondary orientation axis
        axis2 = axisfinder.find_secondary_axis(new_adsorbate)

        # No second orientation for one-dimensional molecule
        if norm(axis2) == 0:
            return new_adsorbate

        parallel_component = (
            dot(orientation.vectors[0], orientation.vectors[1])
            * orientation.vectors[0]
        )
        perpendicular_component = orientation.vectors[1] - parallel_component
        atom1, _ = axisfinder.find_farthest_atoms(new_adsorbate)

        new_adsorbate.rotate(
            axis2, perpendicular_component, center=atom1.position
        )

        return new_adsorbate

    def place_adsorbate(
        self,
        adsorbate: ase.Atoms,
        site: sitefinder.AdsorptionSite,
        centre: np.array = None,
    ):
        """Place adsorbate on site.

        The adsorbate is placed on the specified site while respecting the
        minimum specified separation.

        Args:
            adsorbate: An :class:`.atoms.Atoms` instance representing
                the adsorbate to be moved.
            site: A :class:`.sitefinder.AdsorptionSite` instance
                representing the site on which the adsorbate is to be placed.
            centre: A :class:`numpy.array` designating the centre with which
                to align the adsorbate. Defaults to None.

        """
        if centre is None:
            centre = adsorbate.get_center_of_mass()

        adsorbate.positions += site.location - centre
        separation = geometry.calculate_separation(adsorbate, self._structure)
        while separation < self.separation:
            adsorbate.positions += 0.1 * site.surface_norm
            separation = geometry.calculate_separation(
                adsorbate, self._structure
            )


def _get_structure_with_name(
    structure: Path, *, preserve_info: bool = False
) -> ase.Atoms:
    """Load an :class:`.atoms.Atoms` object from a file and stores filename.

    The plain text description is stored in the "info" dictionary of the
    structure under the key "description" and can be accessed as follows:
        atoms = _get_structure_with_name(structure)
        structure_description = atoms.info['structure']

    Args:
        structure: A :class:`Path` instance indicating the path to the
            structure to be loaded.
        preserve_info: Whether or not to preserve the structure information in
            the info dictionary. If False, the ``"structure"`` key will be set
            to the structure filename. Defaults to False.

    Returns:
        The loaded :class:`.atoms.Atoms` object.

    """
    atoms = read(structure)
    if not preserve_info or "structure" not in atoms.info:
        atoms.info["structure"] = structure.stem

    return atoms


@overload
def _get_finder(
    structure: ase.Atoms, *, finder: Literal["MOF"]
) -> sitefinder.MOFSiteFinder: ...


def _get_finder(
    structure: ase.Atoms, *, finder: str = "MOF"
) -> sitefinder.SiteFinder:
    match finder:
        case "MOF":
            return sitefinder.MOFSiteFinder(structure)
        case _:
            msg = f"{finder} finder not implemented"
            raise NotImplementedError(msg)


def generate_complexes(
    adsorbate: str,
    structure: Path,
    destination: Path | None = None,
    separation: float = 1.8,
    special_centres: bool = False,
    symmetric: bool = False,
    vertical: bool = False,
    *,
    finder: str = "MOF",
) -> list[tuple[AdsorbateComplex, Path]]:
    """Create adsorbate complexes and write them to a ``.traj`` file.

    Args:
        adsorbate: A string indicating the name of the adsorbate to place on
            the surface.
        structure: A :class:`Path` indicating the filename of the structure
            on which the adsorbate will be placed.
        destination: A :class:`Path` indicating the directory in which
            to write the ``.traj`` files. The directory is created if it does
            not exist. Defaults to the current working directory.
        separation: A float indicating how far (in Angstroms) the adsorbate
            should be placed from the surface. Defaults to 1.8.
        special_centres: A bool indicating whether atom-centred
            placement will be used in addition to centre-of-mass placement.
        symmetric: A bool indicating whether or not the adsorbate is to be
            treated as symmetric. Defaults to False.
        vertical: A bool indicating whether or not vertical adsorption
            configurations are to be generated. Defaults to False.
        finder: The type of :class:`ccu.adsorption.sitefinder.SiteFinder`.
            Defaults to ``"MOF"``.

    Returns:
        A list of 2-tuples (``complex_i``, ``path_i``) where ``complex_i`` is
        the ith :class:`AdsorbateComplex` and ``path_i`` is a :class:`Path`
        representing the filename under which ``complex_i`` was saved.

    """
    if destination is None:
        destination = Path.cwd()
    elif not destination.exists():
        destination.mkdir()

    adsorbate = adsorbates.get_adsorbate(adsorbate)
    structure = _get_structure_with_name(structure)
    structure_finder = _get_finder(structure, finder)
    placer = AdsorbateComplexFactory(
        adsorbate=adsorbate,
        structure=structure,
        separation=separation,
        special_centres=special_centres,
        symmetric=symmetric,
        vertical=vertical,
    )
    complexes = []
    for site in structure_finder.sites():
        for configuration in placer.next_complex(site):
            complexes.append((configuration, configuration.write(destination)))

    return complexes
