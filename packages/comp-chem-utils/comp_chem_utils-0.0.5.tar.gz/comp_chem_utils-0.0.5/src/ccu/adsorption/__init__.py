r"""Utilities for adsorption studies.

Example:
    Generate adsorbate complexes for all |CO2RR| intermediates on Au

    >>> from ase.build import bulk
    >>> import numpy as np
    >>>
    >>> from ccu.adsorption.adsorbatecomplex import AdsorbateComplexFactory
    >>> from ccu.adsorption.adsorbates import CO2RR_ADSORBATES
    >>> from ccu.adsorption.sitefinder import AdsorptionSite
    >>> from ccu.adsorption.sitefinder import SiteAlignment
    >>>
    >>> catalyst = bulk("Au") * 3
    >>> catalyst.center(vacuum=10, axis=2)
    >>> norm_vector = np.array([0, 0, 1])
    >>> surface_atom = max(catalyst, key=lambda atom: atom.position[2])
    >>> alignment = SiteAlignment(norm_vector, "vertical")
    >>> site = AdsorptionSite(
    ...     location=surface_atom.position,
    ...     description="on-top",
    ...     alignments=[alignment],
    ...     surface_norm=norm_vector,
    ... )
    >>> for adsorbate in CO2RR_ADSORBATES:
    ...     factory = AdsorbateComplexFactory(adsorbate, catalyst)
    ...     for complex in factory(site):
    ...

"""
