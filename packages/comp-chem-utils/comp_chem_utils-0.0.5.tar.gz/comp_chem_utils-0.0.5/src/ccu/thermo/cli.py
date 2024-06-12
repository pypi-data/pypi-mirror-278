"""CLI utilities for thermochemistry."""

from collections.abc import Callable
from itertools import product
import logging
import sys
from typing import Literal
from typing import TextIO
from typing import TypeVar

import click

from ccu.thermo import STP
from ccu.thermo import chempot
from ccu.thermo import gibbs

logger = logging.getLogger(__package__.split(".")[0])

DEFAULT_APPROXIMATION = "HARMONIC"
_T = TypeVar("_T")


@click.group(name=__package__.split(".")[-1])
def main():
    """Thermochemistry tools."""


def _name_energy_file() -> TextIO:
    """Name the energy file based on the approximation."""
    prefix = "harmonic"
    if ctx := click.get_current_context(silent=True):
        prefix = ctx.params.get("approximation", "") or prefix

    return f"{prefix.lower()}_free_energy.e"


def report_state(ctx: click.Context) -> None:
    """Report the value and source of CLI parameters."""
    logger.debug("Parameters and Sources".center(80, "-"))
    for k, v in ctx.params.items():
        value = getattr(v, "name", str(v))
        logger.debug(
            "%s=%s from %s", k, value, ctx.get_parameter_source(k).name
        )


@main.command(
    "gibbs",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    default=0,
    count=True,
    help="Controls the verbosity. 0: Show messages of level warning and "
    "higher. 1: Show messages of level info and higher. 2: Show all messages"
    "-useful for debugging.",
    show_default=True,
)
@click.option(
    "-T",
    "--transition-state",
    is_flag=True,
    default=False,
    help=(
        "Assume that the system is a transition state when calculating the "
        "free energy of the system. One imaginary vibrational mode "
        "(corresponding to the reaction coordinate) will be discarded."
    ),
    show_default=True,
)
@click.option(
    "-S",
    "--solution-phase",
    "frequency_threshold",
    default=False,
    flag_value=100,
    help=(
        "Assume that the system is in solution when calculating the free "
        "energy of the system. When activated, low vibrations are "
        r"shifted to 100 cm\ :sup:`-1`; otherwise, low vibrations are "
        r"shifted to 12 cm\ :sup:`-1`."
    ),
    show_default=True,
)
@click.option(
    "--frequency-threshold",
    "frequency_threshold",
    default=12,
    help=(
        "All vibrations less than this value will be shifted to this "
        r"value. Units in cm\ :sup:`-1`."
    ),
    hidden=True,
)
@click.option(
    "--ideal-gas",
    "approximation",
    is_eager=True,
    flag_value="IDEAL_GAS",
    help=(
        "Use the ideal gas limit to calculate the free energy. With :math:`N` "
        "atoms, :math:`3N - 6` vibrational modes will be considered "
        "(:math:`3N - 5` if the ``--linear`` flag is provided)."
    ),
    show_default=True,
)
@click.option(
    f"--{DEFAULT_APPROXIMATION.lower()}",
    "approximation",
    default=True,
    is_eager=True,
    flag_value=DEFAULT_APPROXIMATION,
    help=(
        f'Use the {DEFAULT_APPROXIMATION.lower().replace("_", " ")} limit to '
        'calculate the free energy. All vibrational modes will be considered.'
    ),
    show_default=True,
)
@click.option(
    "-Y",
    "--symmetry",
    default=1,
    help=(
        "Specify the symmetry number of the system. Note that this is only "
        "relevant under the ideal gas approximation."
    ),
    show_default=True,
)
@click.option(
    "--linear",
    "geometry",
    flag_value="linear",
    help=(
        "Specify that the system is linear. Note that this is only "
        "relevant under the ideal gas approximation."
    ),
    show_default=True,
)
@click.option(
    "--non-linear",
    "geometry",
    default=True,
    flag_value="nonlinear",
    help=(
        "Specify that the system is nonlinear. Note that this is only "
        "relevant under the ideal gas approximation."
    ),
    show_default=True,
)
@click.option(
    "-t",
    "--temperature",
    default=STP.temperature,
    help="Specify the temperature (in Kelvin).",
    show_default=True,
    type=float,
)
@click.option(
    "-p",
    "--pressure",
    default=STP.pressure,
    help=(
        "Specify the temperature (in bar). Note that this is only applicable "
        "for the ideal gas approximation."
    ),
    show_default=True,
    type=float,
)
@click.option(
    "-s",
    "--spin",
    default=0,
    help=(
        "Specify the spin. Note that this is only relevant for the gas-phase "
        "approximation."
    ),
    show_default=True,
)
@click.option(
    "--atoms-file",
    default="in.traj",
    help=(
        "The name of the file containing the structure corresponding to the "
        "vibrational frequencies. Note that this is only used in the ideal "
        "gas approximation."
    ),
    show_default=True,
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "--dg-file",
    default="dg_ase.log",
    help=(
        "The name of the file in which the save the quantity "
        ":math:`-TS + ZPE`."
    ),
    show_default=True,
    type=click.File(mode="w", encoding="utf-8"),
)
@click.option(
    "--freq-file",
    default="gibbs_freq_used.txt",
    help=(
        "The name of the file in which to save the frequencies used to "
        'calculate the free energy. Use "-" to print to the standard output.'
    ),
    show_default=True,
    type=click.File(mode="w", encoding="utf-8"),
)
@click.option(
    "--vib-file",
    default="vib.txt",
    help=(
        "The name of the file from which to read the frequencies used to "
        "calculate the free energy."
    ),
    show_default=True,
    type=click.File(mode="r", encoding="utf-8"),
)
@click.option(
    "--log-file",
    default="free_energy.log",
    help=(
        "The name of the file in which to save all the information used to "
        "calculate the free energy. Use ``-`` to print to the standard output."
    ),
    type=click.File(mode="w", encoding="utf-8"),
)
@click.option(
    "--energy-file",
    default=_name_energy_file,
    help=(
        "The name of the file in which to save the free energy. Use ``-`` to "
        "print to the standard output."
    ),
    type=click.File(mode="w", encoding="utf-8"),
)
@click.pass_context
def calculate_free_energy(
    ctx: click.Context,
    verbosity: int,
    transition_state: bool,
    frequency_threshold: float,
    approximation: Literal["IDEAL_GAS", "HARMONIC"],
    symmetry: int,
    geometry: Literal["linear", "nonlinear"],
    temperature: float,
    pressure: float,
    spin: int,
    atoms_file: str,
    dg_file: TextIO,
    freq_file: TextIO,
    vib_file: TextIO,
    log_file: TextIO,
    energy_file: TextIO,
) -> None:
    """Calculate the free energy of a system."""
    match verbosity:
        case 0:
            level = logging.WARNING
        case 1:
            level = logging.INFO
        case _:
            level = logging.DEBUG

    fh = logging.StreamHandler(log_file)
    fh.setLevel(level=level)
    gibbs.logger.addHandler(fh)

    if energy_file is None:
        energy_file = f"{approximation.lower()}_free_energy.e"

    report_state(ctx=ctx)

    ts, zpe, frequencies = gibbs.calculate_free_energy(
        log_file=log_file,
        vib_file=vib_file,
        approximation=approximation,
        symmetry=symmetry,
        geometry=geometry,
        transition_state=transition_state,
        frequency_threshold=frequency_threshold,
        temperature=temperature,
        pressure=pressure,
        spin=spin,
        atoms_file=atoms_file,
    )
    _ = energy_file.write(str(ts + zpe))
    logger.info("Free energy written to %s", energy_file.name)
    _ = dg_file.write(str(ts))
    logger.info(
        "%s free energy written " "to %s",
        approximation.capitalize().replace("_", " "),
        dg_file.name,
    )
    header = "Frequencies used for Gibbs Free energy calculation".center(
        80, "-"
    )
    freq_lines = [
        f"{header}\n",
        *[f"{freq}\n" for freq in frequencies],
        "-" * 80,
    ]
    _ = freq_file.writelines(freq_lines)
    logger.info("Frequencies written to %s", freq_file.name)
    click.echo(f"Free energy: {ts + zpe}")


def print_molecules(
    ctx,  # noqa: ARG001
    value,  # noqa: ARG001
    param: click.Parameter,
) -> None:
    """Name all species for which chempot is parameterized."""
    if param:
        database = chempot.ChemPotDatabase()
        for molecule in database.zpe_data:
            click.echo(molecule)

        sys.exit(0)


def _summarize_chempot(chem_pot, g, zpe, t, p, m) -> None:
    """Neatly summarize the results from chempot.

    Args:
        chem_pot: The calculated chemical potential.
        g: The calculated Gibbs free energy.
        zpe: The vibrational zero-point energy for the molecule.
        t: The temperature (in Kelvin) at which the free energy was
            calculated.
        p: The pressure (in bar) at which the free energy was calculated.
        m: The name of the molecule for which the calculation was performed.
    """
    # Formatting values
    g = round(g, 3)
    zpe = round(zpe, 3)
    delta_mu = "\u0394\u03bc"
    arrow = "\u2192"
    header = f" {m} // {t} K // {p} bar "

    # Measuring widths
    lhs = ["G", "zpe", f"{delta_mu}(0 {arrow} T)", "G"]
    rhs = [
        f"zpe + {delta_mu}(0 {arrow} T)",
        f"{zpe:.3f} eV",
        f"{chem_pot:.3f} eV",
        f"{g:.3f} eV",
    ]
    left_length = len(max(lhs))
    right_length = len(max(rhs))

    # Spacing text
    left_summary = [f"{x: >{left_length}}" for x in lhs]
    right_summary = [f"{x: >{right_length}}" for x in rhs]
    header = f"{header: ^{3+left_length+right_length}}"
    header_row = "=" * len(header)

    # Printing
    click.echo(header_row)
    click.echo(header)
    click.echo(header_row)

    for left, right in zip(left_summary, right_summary, strict=True):
        click.echo(f"{left} = {right}")

    footer_row = "-" * len(header)
    click.echo(footer_row)


def _process_prompted_values(
    convert_to: Callable[[str], _T] = str,
) -> list[str | float]:
    def _func(
        value: list[str | int] | str,
    ) -> _T:
        if isinstance(value, list):
            return value
        return [convert_to(x) for x in value.split(",")]

    return _func


@main.command(
    "chempot",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.argument(
    "molecules",
    nargs=-1,
    metavar="MOLECULE",
)
@click.option(
    "-t",
    "--temperature",
    "temperatures",
    default=[STP.temperature],
    help="Specify the temperature (in Kelvin).",
    multiple=True,
    show_default=True,
    type=float,
)
@click.option(
    "-p",
    "--pressure",
    "pressures",
    multiple=True,
    default=[STP.pressure],
    help="Specify the temperature (in bar).",
    show_default=True,
    type=float,
)
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    flag_value=True,
    help="Execute interactively.",
    type=float,
)
@click.option(
    "-l",
    "--list",
    is_eager=True,
    is_flag=True,
    flag_value=True,
    callback=print_molecules,
    expose_value=False,
    help="Print the list of all molecules for which chempot is "
    "parametrized",
)
def chempot_calculator(
    molecules: list[str],
    temperatures: list[float],
    pressures: list[float],
    interactive: bool,
) -> None:
    """Launch the chemical potential calculator parametrized with PBE-D3.

    MOLECULES are the molecules for which the chemical potential will be
    calculated.
    """
    if interactive:
        chempot.print_instructions()
        str_value_proc = _process_prompted_values()
        float_value_proc = _process_prompted_values(float)
        while True:
            molecules = click.prompt("Molecules", value_proc=str_value_proc)
            temperatures = click.prompt(
                "Temperatures",
                value_proc=float_value_proc,
                default=[STP.temperature],
                show_default=True,
            )
            pressures = click.prompt(
                "Pressures",
                value_proc=float_value_proc,
                default=[STP.pressure],
                show_default=True,
            )

            for m, t, p in product(molecules, temperatures, pressures):
                chem_pot, zpe = chempot.calculate(m, t, p)
                g = chem_pot + zpe
                _summarize_chempot(chem_pot, g, zpe, t, p, m)

            molecules.clear()
            temperatures.clear()
            pressures.clear()
    else:
        for m, t, p in product(molecules, temperatures, pressures):
            chem_pot, zpe = chempot.calculate(m, t, p)
            g = chem_pot + zpe
            _summarize_chempot(chem_pot, g, zpe, t, p, m)
