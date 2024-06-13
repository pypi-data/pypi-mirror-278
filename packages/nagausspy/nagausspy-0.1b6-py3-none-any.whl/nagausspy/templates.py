# nagausspy: NaFoMat tools for editing Gaussian Files
# Copyright (C) 2024  Hadrián Montes, NaFoMat

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
