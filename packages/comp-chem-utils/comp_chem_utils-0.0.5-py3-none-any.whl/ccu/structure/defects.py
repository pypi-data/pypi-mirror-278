"""Functions for creating defects within structures."""

from collections.abc import Iterable
from itertools import combinations
from itertools import permutations

from ase import Atoms
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.io.ase import AseAtomsAdaptor


def _convert_symbols(*, structure: Atoms, sites: list[int | str]) -> list[int]:
    """Convert chemical symbols into structure indices."""
    symbols: dict[str, list[int]] = {}
    for atom in structure:
        if atom.symbol not in symbols:
            symbols[atom.symbol] = []
        symbols[atom.symbol].append(atom.index)

    integer_sites: set[int] = set()
    for site in sites:
        if isinstance(site, int):
            integer_sites.add(site)
        else:
            integer_sites.update(symbols[site])

    return list(integer_sites)


def _validate_occupancies(
    *, sites: list[int], occupancies: list[tuple[str, int]]
) -> bool:
    """Ensure that occupancies do not exceed sites.

    Args:
        sites: The indices of sites to permute.
        occupancies: A list of 2-tuples, whose first entry indicates
            the chemical symbol of a dopant and whose second entry indicates
            the number of sites to fill with that dopant.

    Returns:
        True if the number of occupanies do not exceed the number sites.
        False, otherwise.
    """
    num_sites = len(sites)
    num_sites_to_replace = sum(x for _, x in occupancies)
    return num_sites_to_replace <= num_sites


def _convert_occupancies_to_occupants(
    *, occupancies: list[tuple[str, int]]
) -> list[str]:
    """Convert occupancies and counts into a list of chemical symbols."""
    occupants: list[str] = []
    for occupant, occupant_count in occupancies:
        occupants.extend([occupant] * occupant_count)

    return occupants


def _filter_for_uniqueness(structures: list[Atoms]) -> list[Atoms]:
    """Filter out duplicate structures."""
    unique_structures: list[Atoms] = []
    duplicates: list[int] = []
    for i, structure1 in enumerate(structures):
        match = i in duplicates
        if not match:
            for j in range(i + 1, len(structures)):
                matcher = StructureMatcher()
                if matcher.fit(
                    struct1=AseAtomsAdaptor.get_structure(structure1),
                    struct2=AseAtomsAdaptor.get_structure(structures[j]),
                ):
                    match = True
                    duplicates.append(j)

            unique_structures.append(structure1)
    return unique_structures


def permute(
    *,
    structure: Atoms,
    sites: Iterable[int | str] | None = None,
    occupancies: Iterable[tuple[str, int]] | None = None,
) -> list[Atoms]:
    """Create permutations of a structure considering a number of sites.

    Args:
        structure: an `ase.atoms.Atoms` object to permutate.
        sites: an optional list of integers and strings representing the sites
            to permute. Integers are interpreted as structure indices. Strings
            are interpreted as all sites of a given element. Defaults to all
            the indices of the structure.
        occupancies: an optional list of tuples whose first elements are
            strings representing chemical symbols and whose second elements are
            integers indicating the number of sites to fill with the given
            element. Empty strings can be passed to denote vacancy defects.
            Defaults to the occupancies of the sites defined in ``sites``.

    Example:
        Permute all atoms in a structure

        >>> from ase import Atoms
        >>> from ase.build import bulk

        >>> from ccu.structure.defects import permute

        >>> permuted_nios = permute(structure=bulk("NiO", "rocksalt", a=0.352) * 2)

    Example:
        Permute all atoms in a set of sites of a structure

        >>> from ase import Atoms
        >>> from ase.build import bulk

        >>> from ccu.structure.defects import permute

        >>> permuted_nios = permute(
        ...     structure=bulk("NiO", "rocksalt", a=0.352) * 2,
        ...     sites=[0, 1, 2],
        ... )

    Example:
        Create Ni-M bimetallics

        >>> from ase import Atoms
        >>> from ase.build import bulk

        >>> from ccu.structure.defects import permute

        >>> ni = bulk("Ni", "fcc", a=0.352) * 2
        >>> metals = ["Co", "Cr", "Cu", "Fe", "Ti"]
        >>> bimetallics = [ni]
        >>> for metal in metal:
        ...     for atom in ni:
        ...         bimetallics.extend(
        ...             permute(structure=ni, occupancies=(metal, atom.index + 1))
        ...         )

    """
    if sites is None:
        sites = list(range(len(structure)))

    sites = _convert_symbols(structure=structure, sites=sites)

    if occupancies is None:
        symbols = [structure.symbols[i] for i in sites]
        occupancies = [
            (symbol, symbols.count(symbol)) for symbol in set(symbols)
        ]

    if not _validate_occupancies(sites=sites, occupancies=occupancies):
        msg = (
            "Number of sites to replace specified via ``occupancies`` exceeds "
            "the number of sites specified via ``sites``."
        )
        raise ValueError(msg)

    occupants = _convert_occupancies_to_occupants(occupancies=occupancies)

    occupant_orderings = set(permutations(occupants))

    permutated_structures: list[Atoms] = []

    for site_subset in combinations(sites, r=len(occupants)):
        for occupant_ordering in occupant_orderings:
            new_structure = Atoms(structure)
            for site, occupant in zip(
                site_subset, occupant_ordering, strict=False
            ):
                if occupant:
                    new_structure.symbols[site] = occupant
                else:
                    del new_structure[site]
            permutated_structures.append(new_structure)

    # Find unique structure permutations
    unique_structures = _filter_for_uniqueness(permutated_structures)

    return unique_structures
