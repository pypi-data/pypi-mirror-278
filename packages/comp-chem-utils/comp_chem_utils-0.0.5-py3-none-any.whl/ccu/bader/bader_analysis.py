"""Analyze the results of a Bader charge calculation."""

import logging
from pathlib import Path
import subprocess

from ase.io import read

logger = logging.getLogger(__name__)


def main() -> None:  # noqa: C901, PLR0912
    """The main application logic."""
    pp = "/work/siahrostami_lab/tiago/VASP/PP/potpaw_PBE.54/"
    atoms = read("POSCAR")
    with Path("ACF.dat").open(mode="r", encoding="utf-8") as charge_file:
        output = subprocess.check_output(
            args=["awk", "'{print $5}'"], stdin=charge_file, encoding="utf-8"
        )
    with Path("baderchargecolumn.txt").open(
        mode="r", encoding="utf-8"
    ) as bader_file:
        bader_file.write(output)

    i = 0
    with Path("CHARGE_ANALYSIS.txt").open(mode="w", encoding="utf-8") as f:
        f.write(
            "index(from POSCAR)"
            + "\t"
            + "Chemical symbol"
            + "\t"
            + "\t"
            + "Z"
            + "\t"
            + "frozen"
            + "\t"
            + "valence"
            + "\t"
            + "Bader_valence"
            + "\t"
            + "Bader_charge (z-frozen-Bader_valence)"
            + "\n"
        )

        for atom in atoms.get_chemical_symbols():
            j = 0
            with Path("baderchargecolumn.txt").open(
                mode="r", encoding="utf-8"
            ) as g:
                for b in g:
                    try:
                        c1 = float(b)
                        if j >= i:
                            break
                        else:
                            j += 1
                    except ValueError as err:
                        logger.warning(err)

            with Path(pp + atom + "/POTCAR").open(encoding="utf-8") as h:
                count = 0
                z = 0
                for c in h:
                    for d in c.split(";"):
                        kappa = 5
                        if "ZVAL" in d.split(" "):
                            while True:
                                try:
                                    valence = float(d.split(" ")[kappa])
                                    break
                                except ValueError as err:
                                    logger.warning(err)
                                    kappa += 1
                        if count == 1:
                            try:
                                z += float(d.split(" ")[-1])
                            except ValueError as err:
                                logger.warning(err)
                                count = 0

                        if "occ.\n" in d.split(" "):
                            count = 1

                frozen = z - valence
                c = z - frozen - c1

            f.write(
                str(i)
                + 3 * "\t"
                + atom
                + 3 * "\t"
                + str(z)
                + "\t"
                + str(frozen)
                + "\t"
                + str(valence)
                + "\t"
                + str(c1)
                + 3 * "\t"
                + str(c)
                + "\n"
            )
            i += 1


if __name__ == "__main__":
    main()
