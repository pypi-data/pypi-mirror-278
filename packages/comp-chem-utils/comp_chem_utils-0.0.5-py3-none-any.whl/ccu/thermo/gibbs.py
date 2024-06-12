"""Functions for calculating Gibbs free energies from vibrational data."""

import contextlib
import logging
import pathlib
import sys
from typing import Literal
from typing import TextIO
import warnings

import ase.io
from ase.thermochemistry import HarmonicThermo
from ase.thermochemistry import IdealGasThermo

from ccu.thermo import STP
from ccu.thermo import WAVENUMBER_TO_EV

logger = logging.getLogger(__name__)


def _alert_imaginary_frequencies(
    approximation: Literal["IDEAL_GAS", "HARMONIC"] = "HARMONIC",
    lower_frequency_threshold: int = 12,
) -> None:
    """Issue an appropriate warning when there are imaginary frequencies."""
    match approximation:
        case "IDEAL_GAS":
            warnings.warn(
                message=(
                    "There are imaginary frequencies other than those attributable to"
                    "translational/rotational degrees of freedom or movement along "
                    "the reaction coordinate. These were not taken into account. Try "
                    "to re-optimize the structure."
                ),
                category=UserWarning,
                stacklevel=1,
            )
        case "HARMONIC":
            logger.warning(
                " There are imaginary frequencies besides the reaction coordinate. "
                f"They have been normalized to {lower_frequency_threshold} cm^-1."
            )


def _normalize_frequencies(
    frequencies: list[complex],
    approximation: Literal["IDEAL_GAS", "HARMONIC"] = "HARMONIC",
    transition_state: bool = False,
    frequency_threshold: float = 12,
) -> list[float]:
    """Add real frequencies and normalize sub-threshold frequencies."""
    logger.debug("Normalizing frequencies")
    real_frequencies: list[float] = []
    for freq in frequencies:
        if freq.imag == 0:
            frequency = float(freq.real)
            real_frequencies.append(max(frequency, frequency_threshold))
        else:
            if transition_state:
                real_frequencies.append(frequency_threshold)

            _alert_imaginary_frequencies(
                approximation=approximation,
                lower_frequency_threshold=frequency_threshold,
            )
    logger.debug("Normalized frequencies")
    return real_frequencies


# TODO: Consider necessity with updates to HarmonicThermo
# `ignore_imaginary` parameter does some of this for us
def select_frequencies(
    vib_file: TextIO | None = None,
    geometry: Literal["linear", "nonlinear"] = "nonlinear",
    approximation: Literal["IDEAL_GAS", "HARMONIC"] = "HARMONIC",
    transition_state: bool = False,
    frequency_threshold: float = 12,
) -> list[float]:
    r"""Discard frequencies according to the geometry and approximations.

    Args:
        vib_file: An opened text file in which to save the vibrational data.
        geometry: A string indicating the geometry. One of ``"linear"`` or
            ``"nonlinear"``. Defaults to ``"nonlinear"``.
        approximation: A string indicating the approximation used in the
            treatment of the free energy. Defaults to ``"HARMONIC"``.
        transition_state: Whether the frequencies correspond to a transition
            state. Defaults to False.
        frequency_threshold: All frequencies below this value will be
            normalized to this value. Defaults to 12 cm\ :sup:`-1`.

    Returns:
        The appropriate frequencies for the system.

    """
    logger.debug("Selecting frequencies from %s")
    if vib_file:
        lines = vib_file.readlines()
    else:
        with pathlib.Path("vib.txt").open(encoding="utf-8") as file:
            lines = file.readlines()

    all_frequencies: list[complex] = []

    for line in lines:
        column: list[str] = line.split()
        if column[0].isdigit():
            all_frequencies.append(complex(column[-1].replace("i", "j")))

    to_discard = (
        (6 if approximation == "IDEAL_GAS" else 0)
        - (1 if geometry == "linear" else 0)
        + (1 if transition_state else 0)
    )

    logger.debug("Successfully selected frequencies")

    return _normalize_frequencies(
        frequencies=all_frequencies[to_discard:],
        approximation=approximation,
        transition_state=transition_state,
        frequency_threshold=frequency_threshold,
    )


def calculate_free_energy(
    log_file: TextIO | None = None,
    vib_file: TextIO | None = None,
    approximation: Literal["IDEAL_GAS", "HARMONIC"] = "HARMONIC",
    symmetry: int = 1,
    geometry: Literal["linear", "nonlinear"] = "nonlinear",
    transition_state: bool = False,
    frequency_threshold: float = 12,
    temperature: float = STP.temperature,
    pressure: float = STP.pressure,
    spin: int = 0,
    atoms_file: str = "in.traj",
) -> tuple[float, float, list[float]]:
    """Calculate the thermodynamic corrections in the specified approximation.

    Args:
        log_file: A file in which to log the results.
        vib_file: A file from which to read the frequencies.
        approximation: Which approximation to use. One of ``"IDEAL_GAS"`` or
            ``"HARMONIC"``. Defaults to ``"HARMONIC"``.
        symmetry: The symmetry number of the system. Defaults to 1.
        geometry: The geometry of the system. One of ``"linear"`` or
            ``"nonlinear"`` Defaults to ``"nonlinear"``.
        transition_state: Whether to treat the system as a transition state.
            Defaults to False.
        frequency_threshold: All frequencies below this value with be
            normalized to this value. Defaults to 12.
        temperature: The temperature for the system (in Kelvin). Note that this
            is only relevant if ``approximation="IDEAL_GAS"``. Defaults to
            273.15.
        pressure: The pressure for the system (in bar). Note that this is only
            relevant if ``approximation="IDEAL_GAS"``. Defaults to 1.0.
        spin: The spin for the system. Note that this is only relevant if
            ``approximation="IDEAL_GAS"``. Defaults to 0.
        atoms_file: A string pointing to the structure to which the vibrational
            calculations correspond. Defaults to ``"in.traj"``.

    Returns:
        A 3-tuple (``ts``, ``zpe``, ``freq``) where ``ts`` is the entropic
        correction (:math:`-TS`), ``zpe`` is the vibrational zero-point
        energy (:math:`ZPE`), and ``freq`` is a list of floats representing
        the frequencies used to calculate the zero-point energy.

    Note:
        The free energy of the system can be calculated using :eq:`gibbs-def`

    """
    logger.debug("Calculating free energy")
    freq = select_frequencies(
        vib_file=vib_file,
        approximation=approximation,
        geometry=geometry,
        transition_state=transition_state,
        frequency_threshold=frequency_threshold,
    )

    vib_energies = [f * WAVENUMBER_TO_EV for f in freq]
    with contextlib.redirect_stdout(log_file or sys.stdout):
        if approximation == "IDEAL_GAS":
            atoms = ase.io.read(atoms_file)
            thermo = IdealGasThermo(
                atoms=atoms,
                vib_energies=vib_energies,
                geometry=geometry,
                potentialenergy=0.0,
                symmetrynumber=symmetry,
                spin=spin,
            )
            free_energy: float = thermo.get_gibbs_energy(
                temperature, pressure * 100000, verbose=bool(log_file)
            )
        else:
            thermo = HarmonicThermo(
                vib_energies=vib_energies, potentialenergy=0.0
            )
            free_energy: float = thermo.get_helmholtz_energy(
                temperature, verbose=bool(log_file)
            )

    zpe = thermo.get_ZPE_correction()
    ts = free_energy - zpe
    logger.debug(
        "Successfully calculated free energy %s entropic correction %s and zero-point energy %s",
        free_energy,
        ts,
        zpe,
    )

    return ts, zpe, freq
