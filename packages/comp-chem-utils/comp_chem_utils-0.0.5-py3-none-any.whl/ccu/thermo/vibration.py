"""Standardized functions for vibrational calculations."""

import logging
import pathlib

from ase import Atoms
from ase.constraints import FixAtoms
from ase.vibrations.vibrations import Vibrations
from numpy.linalg import norm

logger = logging.getLogger(__name__)


def run_vibration(atoms: Atoms, *, label="vib") -> None:
    """Run a vibrational calculation and log the output.

    The equilibrium structure is saved as ``final.traj``

    Args:
        atoms: An :class:`.atoms.Atoms` object with an attached calculator
            with which to run the vibration calculation.
        label: A string used to name the summary and trajectory files.
            Defaults to ``"vib"``. If the default value is used, the output
            will be logged in ``vib.txt``.

    Raises:
        RuntimeError: Unable to perform vibrational calculation due to missing
            forces.

    """
    logger.debug("Running vibration calculation")
    forces = atoms.get_forces(apply_constraint=True)
    atoms.write("final.traj")

    if forces is None:
        msg = "Unable to perform vibrational calculation due to missing forces"
        raise RuntimeError(msg)

    logger.info(">>> BEGIN print full force")

    for force, atom in zip(forces, atoms, strict=True):
        logger.info("%s %s: %s, %s, %s", atom.index, atom.symbol, *force)

    logger.info("norm of force: %s", norm(forces))
    logger.info("max force: %s", norm(max(forces, key=norm)))
    logger.info("<<< END print full force")

    fixed = []
    if atoms.constraints:
        for constraint in atoms.constraints:
            if isinstance(constraint, FixAtoms):
                fixed = constraint.index
                break

    logger.debug("Fixed indices: %s", fixed)

    to_vibrate = [atom.index for atom in atoms if atom.index not in fixed]
    logger.debug("Indices to vibrate: %s", to_vibrate)

    vib = Vibrations(
        atoms=atoms, nfree=4, name=label, delta=0.015, indices=to_vibrate
    )
    vib.run()

    with pathlib.Path(f"{label}.txt").open(mode="w", encoding="utf-8") as file:
        vib.summary(log=file)

    for mode in range(len(to_vibrate) * 3):
        vib.write_mode(mode)

    zpe = vib.get_zero_point_energy()

    logger.debug("Successfully ran vibration calculation. ZPE: %s", zpe)
