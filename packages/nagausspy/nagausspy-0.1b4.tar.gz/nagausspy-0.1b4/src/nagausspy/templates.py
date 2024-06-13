from ._commandline import CommandLine
from typing import Dict

COMMANDLINES: Dict[str, CommandLine] = {
    "optimization": CommandLine(("opt B3LYP/6-311g(d,p) "
                                 "int=ultrafine scf=conver=9")),
    "frequency": CommandLine(("freq=raman B3LYP/6-311g(d,p) int=ultrafine "
                              "pop=(full,nbo) scf=conver=9")),
    "population": CommandLine(("B3LYP/6-311g(d,p) int=ultrafine prop "
                               "pop=(full,nbo,esp) scf=conver=9")),
    "nmr": CommandLine(("RHF/6-311G(d,p) nmr"))
}
