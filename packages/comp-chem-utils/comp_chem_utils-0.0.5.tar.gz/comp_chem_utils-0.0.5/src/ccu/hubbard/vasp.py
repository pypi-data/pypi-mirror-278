"""This module defines the `get_hubbard_u` function."""

from collections.abc import Iterable
from copy import deepcopy
from csv import DictWriter
import logging
import pathlib
import re
import shutil

import ase
from ase.calculators.vasp.setups import setups_defaults
from ase.calculators.vasp.vasp import Vasp
import numpy as np
from numpy.polynomial import polynomial

logger = logging.getLogger(__name__)


def archive_results(
    grid: list[float],
    chi_ij0: list[float],
    chi_ij: list[float],
    *,
    data_file: str = "hubbard",
) -> None:
    """Save hubbard calculation data to a .csv file in a plot-friendly format.

    Args:
        grid: A list of numbers representing perturbations (e.g., the x-axis).
        chi_ij0: The list values for the non-self consistent response function.
        chi_ij: The list values for the self consistent response function.
        data_file: The filename under which to save the data. Defaults to "hubbard".

    """
    logger.info("Archiving results in: %s", data_file)
    logger.debug("grid: %s", ", ".join(str(x) for x in grid))
    logger.debug("X_ij0: %s", ", ".join(str(x) for x in chi_ij0))
    logger.debug("X_ij: %s", ", ".join(str(x) for x in chi_ij))
    with pathlib.Path(f"{data_file}.csv").open("w", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=["x", "X_ij0", "X_ij"])
        writer.writeheader()
        for x, ij, ij0 in zip(grid, chi_ij0, chi_ij, strict=True):
            writer.writerow({"x": x, "X_ij0": ij, "X_ij": ij0})
    logger.info("Successfully archived results in: %s", data_file)


def get_hubbard_u(
    calc,
    atoms: ase.Atoms | None = None,
    index: int = 0,
    grid: Iterable[float] | None = None,
    enforce_strict: bool = True,
    data_file: str = "hubbard",
) -> float:
    """Calculates the Hubbard U parameter of an atom according to [4]_.

       This method employs the linear response method.

    Args:
        calc: A pre-configured Vasp calculator instance set up to run the
            calculation.
        atoms: An ase.Atoms instance for which the calculation will be
            performed. Defaults to None.
        index: An int denoting the index of the atom for which the Hubbard
            parameter is to be calculated.
        grid: An iterable of integers specifying the shifting potentials (in
            eV) that will be applied for the SCF and non-SCF calculations.
            Defaults to
            ``[-0.2, -0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15, 0.2]``.
        enforce_strict: If True, then calculator parameters will be verified
            against the following checks:

            * ``ICHARG < 10``
            * ``LDAU``, ``LDAUU``, ``LDAUJ``, ``LDAUL`` are not (and won't
              be) set
            * ``LORBIT >= 11``
            * ``LMAXMIX >= 4``
            * ``NSW < 1``

        data_file: A string indicating the file name to save the raw data used
            to calculate the response function.

    Returns:
            The Hubbard U parameter in eV.

    Example:
            Calculate the Hubbard U parameter for nickel (without magnetization)
            in NiO similar to the tutorial here_:

    >>> from ase import Atoms
    >>> from ase.build import bulk
    >>> from ase.calculators.vasp.vasp import Vasp
    >>> from ase.cell import Cell
    >>>
    >>> positions = [
    ...     [0.0, 0.0, 0.0],
    ...     [4.035, 4.035, 4.035],
    ...     [2.0175, 2.0175, 4.035],
    ...     [6.0525, 6.0525, 8.07],
    ...     [2.0175, 4.035, 2.0175],
    ...     [6.0525, 8.07, 6.0525],
    ...     [4.035, 6.0525, 6.0525],
    ...     [8.07, 10.0875, 10.0875],
    ...     [4.035, 2.0175, 2.0175],
    ...     [8.07, 6.0525, 6.0525],
    ...     [6.0525, 4.035, 6.0525],
    ...     [10.0875, 8.07, 10.0875],
    ...     [6.0525, 6.0525, 4.035],
    ...     [10.0875, 10.0875, 8.07],
    ...     [8.07, 8.07, 8.07],
    ...     [12.105, 12.105, 12.105],
    ...     [2.0175, 2.0175, 2.0175],
    ...     [6.0525, 6.0525, 6.0525],
    ...     [4.035, 4.035, 6.0525],
    ...     [8.07, 8.07, 10.0875],
    ...     [4.035, 6.0525, 4.035],
    ...     [8.07, 10.0875, 8.07],
    ...     [6.0525, 8.07, 8.07],
    ...     [10.0875, 12.105, 12.105],
    ...     [6.0525, 4.035, 4.035],
    ...     [10.0875, 8.07, 8.07],
    ...     [8.07, 6.0525, 8.07],
    ...     [12.105, 10.0875, 12.105],
    ...     [8.07, 8.07, 6.0525],
    ...     [12.105, 12.105, 10.0875],
    ...     [10.0875, 10.0875, 10.0875],
    ...     [14.1225, 14.1225, 14.1225],
    ... ]
    >>> cell = Cell(
    ...     [[8.07, 4.035, 4.035], [4.035, 8.07, 4.035], [4.035, 4.035, 8.07]]
    ... )
    >>> nio = Atoms("Ni16O16", positions=positions, cell=cell, pbc=True)
    >>> magmoms = []
    >>> for i, atom in enumerate(nio):
    ...     if atom.symbol == "Ni":
    ...         factor = 1 if i % 2 == 0 else -1
    ...         magmoms.append(factor)
    ...     else:
    ...         magmoms.append(0)
    >>>
    >>> nio.set_initial_magnetic_moments(magmoms)
    >>> calc = Vasp(  # doctest:+SKIP
    ...     prec="Accurate",
    ...     ediff=1e-6,
    ...     ismear=0,
    ...     sigma=0.2,
    ...     ispin=2,
    ...     lorbit=11,
    ...     lmaxmix=4,
    ...     magmoms=magmoms,
    ...     atoms=atoms,
    ... )
    >>> index = atoms.get_chemical_symbols().index("Ni")
    >>> perturbations = [x / 100 for x in range(-20, 25, 5)]
    >>> get_hubbard_u(calc, atoms, index, perturbations)  # doctest:+SKIP
        5....

    .. _here: https://www.vasp.at/wiki/index.php/Calculate_U_for_LSDA%2BU

    .. [4] The linear response method outlined in |paper|_
    .. |paper| replace:: Cococcioni and de Gironcoli. Phys. Rev. B 71, 035105
                         (2005)
    .. _paper: https://journals.aps.org/prb/abstract/10.1103/PhysRevB.71.035105
    """
    _configure_for_hubbard(calc, atoms, index, enforce_strict)

    if grid is None:
        grid = [x / 100 for x in range(-20, 25, 5)]

    # Perform self-consistent calculation
    calc.get_potential_energy(atoms=atoms)
    chi_ij0 = []
    chi_ij = []
    for u in grid:
        # Run non-SCF Calculation
        chi_ij0.append(_response_calculation(calc, atoms, u, index, False))

        # Run SCF Calculation
        chi_ij.append(_response_calculation(calc, atoms, u, index, True))

    archive_results(
        grid=grid, chi_ij=chi_ij, chi_ij0=chi_ij0, data_file=data_file
    )

    # Linear fit
    chi_ij0_fit = polynomial.polyfit(list(grid), chi_ij0, 1)
    chi_ij_fit = polynomial.polyfit(list(grid), chi_ij, 1)
    hubbard_u = (1 / chi_ij_fit[1]) - (1 / chi_ij0_fit[1])

    logger.info("X_ij0: %", chi_ij0_fit[1])
    logger.info("X_ij: %s", chi_ij_fit[1])
    logger.info("Hubbard U calculated for atom %s: %s eV", index, hubbard_u)

    return hubbard_u


def _configure_for_hubbard(
    calc: Vasp,
    atoms: ase.Atoms = None,
    index: int = 0,
    enforce_strict: bool = True,
):
    """Configures a calculator for a linear response calculation."""
    if atoms is None:
        atoms = calc.atoms

    params = {}

    symbol = atoms.get_chemical_symbols()[index]
    if symbol in setups_defaults["recommended"]:  # generalize
        pp = symbol + setups_defaults["recommended"][symbol]
    else:
        pp = symbol

    # Add index: pp special to setups
    if calc.input_params["setups"] is None:
        setups = {index: pp}
        params["setups"] = setups
    elif index not in calc.input_params["setups"]:
        setups = {index: pp}
        setups.update(calc.input_params["setups"])
        params["setups"] = setups
    else:
        params["setups"] = calc.input_params["setups"]

    # Checks
    if enforce_strict:
        _verify_hubbard_parameters(calc)

    calc.set(
        atoms=atoms,
        ldautype=3,
        **params,
    )


def _verify_hubbard_parameters(calc: Vasp):
    params = {"ldau_luj": None, "ldautype": 3}

    if (
        calc.int_params["icharg"] is not None
        and calc.int_params["icharg"] >= 10  # noqa: PLR2004
    ):
        params["icharg"] = None

    # LDAUU, LDAUJ should be None or np.zeros()
    for param in ("ldauu", "ldauj"):
        if calc.list_float_params[param] is None:
            continue
        length = len(calc.list_float_params[param])
        if (np.zeros(length) == calc.list_float_params[param]).all():
            params[param] = calc.list_float_params[param]
        params[param] = None

    if calc.bool_params.get("ldau"):
        params["ldau"] = None

    # LORBIT >= 11
    if calc.int_params["lorbit"] is None or calc.int_params["lorbit"] < 11:  # noqa: PLR2004
        params["lorbit"] = 11
    else:
        params["lorbit"] = calc.int_params["lorbit"]

    # LMAXMIX >= 4
    if calc.int_params["lmaxmix"] is None or calc.int_params["lmaxmix"] < 4:  # noqa: PLR2004
        params["lmaxmix"] = 4  # check if atom has f electrons
    else:
        params["lmaxmix"] = calc.int_params["lmaxmix"]

    # NSW < 1
    if calc.int_params["nsw"] is None or calc.int_params["nsw"] > 0:
        params["nsw"] = 0
    else:
        params["nsw"] = calc.int_params["nsw"]

    calc.set(**params)


def _response_calculation(
    calc: Vasp,
    atoms: ase.Atoms,
    shifting_potential: float,
    index: int,
    scf: bool = False,
) -> float:
    suffix = "SCF" if scf else "nonSCF"

    new_dir = pathlib.Path(calc.directory) / f"U_{shifting_potential}_{suffix}"
    new_dir.mkdir()
    shutil.copyfile(
        pathlib.Path(calc.directory) / "CHGCAR", new_dir / "CHGCAR"
    )
    shutil.copyfile(
        pathlib.Path(calc.directory) / "WAVECAR", new_dir / "WAVECAR"
    )

    new_calc = deepcopy(calc)
    new_calc.reset()
    ldaul = []
    ldauu = []
    ldauj = []
    icharg = 0 if scf else 11

    for i, _ in enumerate(calc.atoms_sorted):
        if i == calc.resort[index]:
            ldaul.append(2)
            ldauu.append(shifting_potential)
            ldauj.append(shifting_potential)
        else:
            ldaul.append(-1)
            ldauu.append(0)
            ldauj.append(0)

    new_calc.set(
        ldau=True,
        icharg=icharg,
        ldautype=3,
        ldaul=ldaul,
        ldauu=ldauu,
        ldauj=ldauj,
        directory=new_dir,
    )
    new_atoms = deepcopy(atoms)
    new_atoms.calc = new_calc
    _ = new_atoms.get_potential_energy()
    charges = get_ionic_charges(new_dir)
    return charges[calc.resort[index]]["d"]


def get_ionic_charges(directory: pathlib.Path | None) -> list:
    """Parses an OUTCAR directory for the charges.

    Args:
        directory: A string or pathlib.Path instance representing the
            directory containing the OUTCAR. Defaults to the current working
            directory.

    Returns:
        A list of dictionaries containing the s, p, and d orbital occupancies.
        The occupancies are ordered consistent with the POSCAR and POTCAR
        files. For example::

            [{"s": 0.1, "d": 0.32, "f": 0.812}]

    """
    if directory is None:
        directory = pathlib.Path.cwd()

    outcar = directory.joinpath("OUTCAR")

    with outcar.open(mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    header_re = re.compile(r"total charge")
    footer_re = re.compile(r"-+\n")

    for i, line in enumerate(reversed(lines)):
        if header_re.search(line):
            start = -i + 3
            break

    charges = []
    for line in lines[start:]:
        if footer_re.match(line):
            break

        chg = line.split()
        s = chg[1]
        p = chg[2]
        d = chg[3]

        charges.append({"s": float(s), "p": float(p), "d": float(d)})

    return charges
