r"""Calculate thermodynamic properties via a DFT-parametrized calculator.

This module defines classes for the calculation of thermodynamic data via
DFT-parametrized models. In this way, zero-point energies, chemical potentials,
and Gibbs free energies can be calculated without the need of expensive
vibrational calculations. That hard work has already been done!

In particular, this module defines two main classes:

* :class:`ChemPotDatabase`: a database for parametrization data.

* :class:`ChemPotCalculator`: a calculator for computing thermodynamic data
  from parametrization data in a :class:`ChemPotDatabase`.

Additionally, ``ccu`` ships with a pre-defined dataset for a number of
molecules. The dataset was produced from a set of DFT-D3 calculations and
includes zero-point energies calculated under the rigid rotator and harmonic
oscillator approximations. Calculated values are valid below 1100K. Chemical
potentials are calculated via :func:`calculate_chemical_potential` using
equation :eq:`chem-pot`.

.. admonition:: Examples

    List all molecules included in the pre-defined dataset.

    >>> from ccu.thermo.chempot import ChemPotDatabase
    >>> from ccu.thermo.chempot import load_zpe_data
    >>> zpe_data = load_zpe_data()
    >>> for molecule in zpe_data:
    ...     print(molecule)
    CH4
    ...

    Retrieve parametrization data for |CO2| valid at 350 K.

    >>> from ccu.thermo.chempot import ChemPotDatabase
    >>> database = ChemPotDatabase()
    >>> query = {"molecule": "CO2", "temperature": 350}
    >>> database.parameter_data.get(**query)[0]
    0.130...

    Retrieve the vibrational zero-point energy of |N2|.

    >>> from ccu.thermo.chempot import ChemPotDatabase
    >>> database = ChemPotDatabase()
    >>> database.zpe_data["N2"]
    0.15...

    Calculate the chemical potential of |H2O| at IUPAC STP (273.15 K, 1 bar).

    >>> from ccu.thermo.chempot import ChemPotCalculator
    >>> calc = ChemPotCalculator()
    >>> chem_pot, _ = calc.calculate("H2O")
    >>> chem_pot
    0.114...

    or simply,

    >>> from ccu.thermo.chempot import calculate
    >>> calculate("H2O")[0]
    0.114...

    Calculate the gibbs free energy of |CH4| at 900 K and 2.4 bar.

    >>> from ccu.thermo.chempot import calculate
    >>> sum(calculate("CH4", 900, 2.4))
    -0.759...

    Use a custom database to perform the above calculations.

    >>> from ccu.thermo.chempot import ChemPotCalculator
    >>> from ccu.thermo.chempot import ChemPotDatabase
    >>> from ccu.thermo.chempot import load_zpe_data
    >>> # specify the paths to your database files
    >>> parameter_data = load_parameter_data(..., external=True)
    >>> zpe_data = load_zpe_data(...)
    >>> # load the database into the calculator
    >>> database = ChemPotDatabase(
    ...     parameter_data=parameter_data, zpe_data=zpe_data
    ... )
    >>> calc = ChemPotCalculator(database)
    >>> # and then as above...

.. |CO2| replace:: CO\ :sub:`2`
"""

from csv import DictReader
from dataclasses import dataclass
from dataclasses import field
from functools import cached_property
from importlib import resources
import logging
import math
from pathlib import Path
from textwrap import wrap
from typing import Final
from typing import Literal
from typing import NamedTuple
import warnings

import click

from ccu.thermo import STP

logger = logging.getLogger(__name__)

k_b: Final[float] = 0.000086173354613780


class ChemPotDataPoint(NamedTuple):
    """A thermodynamic parameter, valid in a certain temperature range.

    Attributes:
        lower: The lower temperature bound of the range (inclusive) in which
            the data point is valid.
        molecule: The molecule to which that data point applies.
        term: The kind of term represented by the :class:`ChemPotDataPoint`.
            If ``"b"``, the data point corresonds to a y-intercept. If ``"m"``,
            then the data point corresponds to a slope-like term.
        upper: The upper temperature bound of the range (exclusive) in which
            the data point is valid.
        value: The value of the parameter.

    """

    lower: float
    molecule: str
    param: Literal["b", "m"]
    upper: float
    value: float


def load_parameter_data(
    *, filename: str | Path = "param_data.csv", external: bool = False
) -> list[ChemPotDataPoint]:
    """Load parametrized data from a file of comma-separated values.

    Args:
        filename: The file from which to load the data. Defaults to
            "param_data.csv".
        external: Whether to load the file from in external source. Defaults
            to False.

    Returns:
        A dictionary mapping molecule names to instances of
        :class:`ChemPotDataset`.

    Note:
        The fields of the CSV file must include those of a
        :class:`ChemPotDataPoint`, and the values for the keys "lower",
        "upper", and "value" must be able to be converted into floats.
    """
    adverb = "externally" if external else "internally"
    logger.debug("Loading parameter data %s from %s", adverb, filename)
    if external:
        source = Path(filename)
    else:
        source = resources.files(f"{__package__}._chempot_data").joinpath(
            filename
        )

    with source.open(mode="r", encoding="utf-8") as file:
        reader = DictReader(file)
        data = []
        for row in reader:
            row["lower"] = float(row["lower"])
            row["upper"] = float(row["upper"])
            row["value"] = float(row["value"])
            data.append(ChemPotDataPoint(**row))

    logger.debug(
        "Successfully loaded parameter data %s from %s", adverb, filename
    )
    return data


def load_zpe_data(
    *, filename: str | Path = "zpe_data.csv", external: bool = False
) -> dict[str, float]:
    """Load vibrational zero-point energy data from a CSV file.

    Args:
        filename: The file from which to load the data. Defaults to
            "zpe_data.csv".
        external: Whether to load the file from an external source. Defaults
            to False.

    Returns:
        A dictionary mapping molecule names to their vibrational zero-point
        energies.

    Note:
        The fields of the CSV file must include "molecule" and "zpe", and the values corresponding to "zpe" must be able to be converted into
        floats.
    """
    adverb = "externally" if external else "internally"
    logger.debug("Loading ZPE data %s from %s", adverb, filename)
    if external:
        source = Path(filename)
    else:
        source = resources.files(f"{__package__}._chempot_data").joinpath(
            filename
        )

    with source.open(mode="r", encoding="utf-8") as file:
        reader = DictReader(file)
        zpe_data = {}
        for row in reader:
            molecule = row["molecule"]
            zpe_data[molecule] = float(row["zpe"])

    logger.debug("Successfully loaded ZPE data %s from %s", adverb, filename)
    return zpe_data


def calculate_chemical_potential(
    b: float, m: float, temperature: float, pressure: float
) -> float:
    r"""Calculate the chemical potential from parametrized model.

    This equation is consistent with :math:numref:`chem-pot`.

    Args:
        b: The y-intercept.
        m: The "slope"-like term in the interpolation.
        temperature: The temperature at which to calculate the chemical
            potential.
        pressure: The pressure at which to calculate the chemical
            potential.

    Returns:
        The chemical potential at the conditions specified.
    """
    return b + m * temperature + k_b * temperature * math.log(pressure)


@dataclass(eq=True, frozen=True)
class ChemPotDatabase:
    """A database of parametrized thermochemical data.

    Attributes:
        parameter_data: A list of :class:`ChemPotDataPoint` representing
            thermodynamic data for a parametrization.
        zpe_data: A dictionary mapping molecule names to vibrational
            zero-point energies.

    Example:
        Retrieve b parameter data for |CO2| that is valid at 350 K.

        >>> from ccu.thermo.chempot import ChemPotDatabase
        >>> database = ChemPotDatabase()
        >>> # Note that the following returns a list
        >>> database.get(molecule="CO2", temperature=350, param="b")
        [ChemPotDataPoint(param='b', lower=350.0, upper=400.0, molecule='CO...

    Example:
        Retrieve ZPE data for |CO2|.

        >>> from ccu.thermo.chempot import ChemPotDatabase
        >>> database = ChemPotDatabase()
        >>> database.zpe_data["CO2"]
        0.306
    """

    parameter_data: list[ChemPotDataPoint] = field(
        default_factory=load_parameter_data
    )
    zpe_data: dict[str, float] = field(default_factory=load_zpe_data)

    def get(
        self,
        temperature: float | None = None,
        **query,
    ) -> list[ChemPotDataPoint]:
        """Retrieve values from the parametrization database.

        Args:
            temperature: The temperature to use as a search key. Defaults to
                None. Note, however, that specifying this instead results in
                all database entries with lower and upper values which bracket
                ``temperature`` to be used. If values with a specific lower or
                upper range are desired, use the keys ``"lower"`` and
                ``"upper"``, respectively.
            **query: Specify filtering criteria with which to search for
                entries. Any keys corresponding to fields in a
                :class:`ChemPotDataPoint` are valid.

        Raises:
            LookupError: You specified a key that is not a field of
                :class:`ChemPotDataPoint`.

        Returns:
            A list of every :class:`ChemDataPoint` with fields matching your
            query.

        Note:
            Although it doesn't affect the results returned, the order that
            keyword arguments are specied affects the speed in which results
            are returned. Except for temperature, filtering criteria is
            applied in the order it is supplied in the function call. If
            supplied, the ``temperature`` criteria is always applied first.
        """
        query_summary = (
            ", " + ", ".join(f"{k}={v}" for k, v in query.items())
            if query
            else ""
        )
        logger.debug(
            "Executing query: temperature=%s%s", temperature, query_summary
        )
        matching = []
        try:
            for entry in self.parameter_data:
                satisfies_query = True
                if temperature is not None:
                    satisfies_query = entry.lower <= temperature < entry.upper

                if satisfies_query:
                    for field, condition in query.items():
                        if getattr(entry, field) != condition:
                            satisfies_query = False
                            break

                if satisfies_query:
                    matching.append(entry)

        except AttributeError as err:
            msg = f"{err.name} is not a valid query field"
            raise LookupError(msg) from err
        logger.debug("%s matches found for query", len(matching))
        return matching


class ChemPotCalculator:
    """A chemical potential calculator.

    Attributes:
        database: The underlying database used for calculations.

    Example:
        >>> from ccu.thermo.chempot import ChemPotCalculator
        >>>
        >>> calc = ChemPotCalculator()
        >>> calc.calculate("CO2", 298.15, 1.0)
        -0.581856

    """

    def __init__(self, database: ChemPotDatabase | None = None) -> None:
        """Initialize the calculator from a database.

        Args:
            database: The database to use for the calculator. Defaults to
                None, in which case the pre-defined database is used.
        """
        self.database = database or ChemPotDatabase()

    @cached_property
    def max_temperature(self, *, tol: float = 1e-5) -> float:
        """The maximum temperature supported by the underlying database.

        Args:
            tol: The amount by which to decrement the maximum reported
                upper limit in the underlying database.

        Note:
            This property represents the maximum temperature of **any** data
            point irrespective of the molecule or parameter ("b" **or** "m").
            Further, since the upper limit of an instance of
            :class:`ChemPotDataPoint` represents an *exclusive* upper limit,
            the maximum reported upper limit is decremented by a ``tol`` to
            ensure non-empty queries with this value.
        """
        max_temp = -math.inf
        max_temp = max(
            max_temp, *[d.upper for d in self.database.parameter_data]
        )

        return max_temp - tol

    def calculate(
        self, molecule: str, temperature: float, pressure: float
    ) -> tuple[float, float]:
        """Calculate the chemical potential of a molecule.

        Args:
            molecule: The molecule for which to calculate the chemical
                potential.
            temperature: The temperature at which to calculate the chemical
                potential.
            pressure: The pressure at which to calculated the chemical
                potential.

        Returns:
            A 2-tuple (``chem_pot``, ``zpe``) whose elements represent the
            calculated chemical potential and retrieved vibrational zero-point
            energy, respectively.
        """
        logger.debug(
            "Calculating chemical potential for molecule: %s at temperature "
            "%s K and pressure %s bar",
            molecule,
            temperature,
            pressure,
        )
        query_temp = temperature

        if temperature > self.max_temperature:
            msg = (
                f"Temperature above {self.max_temperature}K detected "
                f"({temperature}K)! This is outside of the reliable range. "
                "For the default database, values between 1000K and 1100K "
                "are still acceptable, but values above 1100K are unreliable!"
                "The parametrization values for the maximum temperature will "
                "be used."
            )
            warnings.warn(msg, stacklevel=1)
            query_temp = self.max_temperature

        try:
            query = {"temperature": query_temp, "molecule": molecule}
            result = self.database.get(**query)
            b = next(x for x in result if x.param == "b").value
            m = next(x for x in result if x.param == "m").value
        except StopIteration as err:
            msg = (
                f"Insufficient information for {molecule} at temperature "
                f"{query_temp} in database. Choose another molecule or a "
                "different temperature!"
            )
            raise NotImplementedError(msg) from err

        chemp_pot = calculate_chemical_potential(b, m, temperature, pressure)
        return chemp_pot


def _construct_lines_to_print(
    full_width: int, short_width: int, buffer: int
) -> tuple[list[str], list[str]]:
    """Construct the lines of the instruction text.

    Args:
        full_width: The full width of the instruction text. This is used to
            set the boxsize.
        short_width: The half width of the instruction text. This is used to
            wrap the upper text.
        buffer: The size of the margins. This is used as a starting point for
            setting the margins of all text.

    Returns:
        The wrapped instruction text.
    """
    text1 = (
        "Chemical potential \u0394\u03bc(0 → T) calculator",
        "Parametrized with PBE-D3 using Rigid "
        "Rotator/Translator and Harmonic "
        "Oscillator approximation",
        "Reliable for temperatures below 1100K",
    )
    description = []
    for x in text1:
        for line in wrap(x, short_width):
            description.append(f"{line: ^{full_width}}")

    description.insert(1, " " * full_width)
    description.insert(-1, " " * full_width)

    header1 = "INSTRUCTIONS:"
    header2 = "Example:"
    instruction_text = (
        "State your molecules, temperatures, and pressures separated by "
        "commas (no spaces), and this script will create all combinations "
        "of your parameters. For a single molecule/temperature/"
        "pressure, simply write the number."
    )
    instructions = []
    for line in wrap(instruction_text, full_width - 2 * buffer):
        instructions.append(f"{' ' * buffer + line: <{full_width}}")

    example_text = (
        "Molecule        : CO2,H2O",
        "Temperature (K) : 150,160,17",
        "Pressure (bar)  : 1,2,3",
    )
    examples = [
        f"{' ' * buffer + line: <{full_width}}" for line in example_text
    ]
    summary_text = (
        "Calculates CO2, H2O chemical potential for 150 K - 1,2,3 bar",
        "160 K - 1,2,3 bar",
        "170 K - 1,2,3 bar",
    )
    summary = [
        f"{line + ' ' * (buffer+2): >{full_width}}" for line in summary_text
    ]
    lines1 = [
        "#" * full_width,
        " " * full_width,
        *description,
        " " * full_width,
        "#" * full_width,
    ]

    lines2 = [
        f"{' ' * (buffer-2) + header1: <{full_width}}",
        *instructions,
        " " * full_width,
        " " * full_width,
        f"{' ' * (buffer-2) + header2: <{full_width}}",
        *examples,
        " " * full_width,
        *summary,
        " " * full_width,
        "_" * full_width,
    ]
    return lines1, lines2


def print_instructions() -> None:
    """Print instructions for using :mod:`chempot` interactively."""
    full_width = 80
    short_width = 40
    buffer = 4
    description, example = _construct_lines_to_print(
        full_width, short_width, buffer
    )

    for line in description:
        click.echo(f"#{line}#")

    click.echo(" " * full_width)
    click.echo(" " * full_width)
    click.echo(" " + "_" * (full_width))

    for line in example:
        click.echo(f"|{line}|")
    database = ChemPotDatabase()
    molecules = (
        f"Molecules available: {' '.join(x for x in database.zpe_data)}"
    )
    molecules = molecules.center(full_width)
    click.echo(molecules)


def calculate(
    molecule: str,
    temperature: float = STP.temperature,
    pressure: float = STP.pressure,
) -> tuple[float, float]:
    """Calculate molecular thermodynamic properties with the default data.

    Args:
        molecule: The name of the molecule for which the calculation will be
            performed. Must be one of
            :data:`ccu.thermo.chempot.MOLECULES`.
        temperature: The temperature (in Kelvin) at which to perform the
            calculation. Defaults to 298.15.
        pressure: The pressure (in bar) at which to perform the calculation.
            Defaults to 1.0.

    Returns:
        A 2-tuple (``chem_pot``, ``zpe``) corresponding to the calculated
        chemical potential and vibrational zero-point energy, respectively.

    Note:
        The model is only parametrized up to 1000K. Although values up to
        1100K may still be reliable, at temperatures higher than 1100K,
        results become unreliable.
    """
    calc = ChemPotCalculator()
    chem_pot = calc.calculate(molecule, temperature, pressure)
    zpe = calc.database.zpe_data[molecule]
    return chem_pot, zpe
