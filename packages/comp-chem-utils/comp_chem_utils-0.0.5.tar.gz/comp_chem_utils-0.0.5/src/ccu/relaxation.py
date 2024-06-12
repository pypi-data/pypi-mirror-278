"""DFT-code agnostic standard relaxation workflow utilities.

.. admonition:: Example

    .. code-block:: python

        import logging
        from ase.build import bulk
        from ase.calculators import Vasp
        from ccu.adsorption.adsorbates import get_adsorbate
        from ccu.relaxation import run_relaxation

        logging.basicConfig(level=logging.DEBUG)

        atoms = bulk("Au") * 3
        atoms.center(vacuum=10, axis=2)
        surface_atom = max(atoms, key=lambda a: a.position[2])
        cooh = get_adsorbate("COOH")
        com = cooh.get_center_of_mass()
        site = surface_atom.position + [0, 0, 3]
        direction = site - com

        for atom in cooh:
            atom.position += direction

        atoms += cooh

        atoms.calc = Vasp(...)
        run_relaxation(atoms, run_chargemol=True)
"""

import logging
from pathlib import Path

from ase import Atoms
from numpy.linalg import norm
from pymatgen.command_line.bader_caller import BaderAnalysis
from pymatgen.command_line.chargemol_caller import ChargemolAnalysis

logger = logging.getLogger(__name__)


def run_relaxation(
    atoms: Atoms, *, run_bader: bool = False, run_chargemol: bool = False
) -> None:
    """Run a relaxation calculation and log the output.

    Args:
        atoms: An Atoms object with an attached calculator with which to run
            the relaxation calculation.
        run_bader: Whether or not to run Bader analysis afterwards.
        run_chargemol: Whether or not to run chargemol afterwards.

    """
    e = atoms.get_potential_energy()
    logger.info("final energy %s eV", e)

    with Path("final.e").open(mode="x", encoding="utf-8") as file:
        file.write(f"{e}\n")

    forces = atoms.get_forces()

    if forces is not None:
        f = str(norm(max(forces, key=norm)))
        logger.info("max force %s eV/Å", f)

    atoms.write("final.traj")

    if run_bader:
        _ = BaderAnalysis()
    if run_chargemol:
        _ = ChargemolAnalysis()
