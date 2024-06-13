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

"""
Implements a class to read the basic info of a gaussian file
"""
import re
import enum
import numpy as np
from .geometry import GaussianGeometry, ComGeometry
from .frequency import GaussianFrequencies
from ._commandline import CommandLine
from .nmr import NMR
from typing import Optional, Tuple, Union, List
import MDAnalysis

class JobTypes(enum.Enum):
    """
    Different jobtypes available to read
    """
    OPTIMIZATION = 0
    FREQUENCIES = 1
    NMR = 2
    POPULATION = 3

class GaussianLog(object):
    """
    Reads the content of a Gaussian .log file
    """

    def __init__(self, filename: str):
        self.TRIGGERS = {
            re.compile("Input orientation:"): self._read_geom,
            re.compile("Standard orientation:"): self._read_geom,
            re.compile(("Full mass-weighted force "
                        "constant matrix:")): self._read_frequencies,
            re.compile("^ #"): self._read_command_lines,
            re.compile("Symbolic Z-matrix:"): self._read_initial,
            re.compile("Magnetic shielding tensor"): self._read_nmr,
            re.compile("Normal termination of Gaussian"): self._toogle_end,
            re.compile("SCF Done:"): self._read_scf_energy,
        }

        self._commandline = None
        self._initial_geometry = None
        self._optimization_steps = []
        self._frequencies = None
        self._nmr = None
        self._normal_termination = False

        self._job_types = set()

        self._filename = filename
        self._parse()

    def __repr__(self):
        return "Gaussian log file '{}".format(self._filename)


    def _parse(self):
        with open(self._filename, "r") as openfile:
            for line in openfile:
                for trigger, method in self.TRIGGERS.items():
                    if trigger.search(line):
                        method(openfile, line)
        # Copy the nergy of the -2 frame into the last one, if it is
        # an optimization as it is aduplicate
        if JobTypes.OPTIMIZATION in self._job_types:
            self.final_geometry.energy = self.optimization_steps[-2].energy

    def _read_nmr(self, openfile, _):
        self._job_types.add(JobTypes.NMR)
        self._nmr = NMR(openfile, self.final_geometry)

    def _toogle_end(self, *_):
        self._normal_termination = True

    def _read_command_lines(self, openfile, line):
        lines = [line.split("#")[1].strip()]

        line = next(openfile)
        while not line.strip().startswith("-"):
            lines.append(line.strip())
            line = next(openfile)
        self._commandline = CommandLine(" ".join(lines))
        # prevent future reading of more lines starting with #
        self.TRIGGERS[re.compile("^ #")] = lambda *args: None

    def _read_geom(self, openfile, _):
        if self._optimization_steps:
            self._job_types.add(JobTypes.OPTIMIZATION)
        self._optimization_steps.append(GaussianGeometry(openfile,
                                                         charge=self.charge,
                                                         multiplicity=self.multiplicity))

    def _read_scf_energy(self, _, line):
        energy = float(line.split("=")[1].split()[0])
        self.final_geometry.energy = energy


    def _read_initial(self, openfile, _):
        line = next(openfile).split()
        charge = int(line[2])
        multi = int(line[5])
        self._initial_geometry = ComGeometry(openfile, charge, multi)

    def _read_frequencies(self, openfile, _):
        molsize = len(self.initial_geometry.coordinates)
        self._frequencies = GaussianFrequencies(openfile, molsize)

    @property
    def initial_geometry(self) -> Optional[ComGeometry]:
        """
        The initial geometry of the simulation
        """
        return self._initial_geometry

    @property
    def optimization_steps(self) -> Tuple[GaussianGeometry, ...]:
        """
        Returns a tuple with the steps of the optimization
        """
        return tuple(self._optimization_steps)

    @property
    def filename(self) -> str:
        """
        The filename and path of the log file
        """
        return self._filename

    @property
    def frequencies(self) -> Optional[GaussianFrequencies]:
        """
        THe frequencies object storing, if any, the frequencies of the
        log file
        """
        return self._frequencies

    @property
    def nmr(self) -> Optional[NMR]:
        """
        The nmr results, if any.
        """
        return self._nmr

    @property
    def final_geometry(self) -> Optional[ComGeometry]:
        """
        The las geometry stored on the log file
        """
        if JobTypes.OPTIMIZATION in self._job_types:
            return self._optimization_steps[-1]
        return self.initial_geometry

    @property
    def commandline(self) -> Optional[CommandLine]:
        """
        The parsed commandline taht was used to run the log file.
        """
        return self._commandline

    @property
    def charge(self) -> int:
        """
        Charge of the system
        """
        return self.initial_geometry.charge

    @charge.setter
    def charge(self, value: int):
        self.initial_geometry.charge = value
        for geom in self.optimization_steps:
            geom.charge = value

    @property
    def multiplicity(self):
        """
        Multiplicity of the system
        """
        return self.initial_geometry.multiplicity

    @multiplicity.setter
    def multiplicity(self, value: int):
        self.initial_geometry.multiplicity = value
        for geom in self.optimization_steps:
            geom.multiplicity = value

    @commandline.setter
    def commandline(self, value: Union[CommandLine,str]):
        if isinstance(value, CommandLine):
            self._commandline = value
        else:
            self._commandline = CommandLine(value)

    @property
    def normal_termination(self) -> bool:
        """
        Wether the termiantion is normal
        """
        return self._normal_termination

    def write_gro_and_xtc(self, out_basename: str, box: Optional[list[float]]=None,
                          resname: str='mlog', find_energy_minima: bool=False,
                          numbered_names: bool=False, bond_scan: Optional[List[int]]=None):
        """
        Writes a .gro and .xtc with the opt steps to open with VMD.

        Parameters
        ----------
        out_basename: str
            The base name of the output .gro and .xtc files.
        box: list of float
            A list with 3 (lx, ly, lz) or 6 (lx, ly, lz, alpha, beta, gamma)
            floats with the simulation box information. If it is None the box is
            set to a cubic one with side lenght of 1 nm.
        resname: str
            The resname to assign to the atoms in the system (optional).
        numbered_names: bool
            If True an index will be set to each atom to allow a better
            differentiation in VMD.
        find_energy_minima: bool
            If True, only the configurations with local minima energy will be
            considered.
        bond_scan: list of int
            A list with 2 index of the atoms to compute the distance to filter
            the optimization steps.

        """

        n_atoms = len(self._optimization_steps[0])
        universe = MDAnalysis.Universe.empty(n_atoms, 1, 1, trajectory=True)
        universe.add_TopologyAttr('names')
        universe.add_TopologyAttr('resnames')
        if not isinstance(resname, str):
            raise IOError(f'resnames must be a string.')
        universe.atoms.residues[0].resname = resname
        # Set box
        if box is None:
            universe.dimensions = [10, 10, 10, 90, 90, 90]
        elif len(box) == 3:
            universe.dimensions = list(box) + [90, 90, 90]
        else:
            universe.dimensions = box

        # Initial Gro 
        for index, (atom_md, atom_log) in enumerate(zip(universe.atoms,
                                                        self._optimization_steps[0].atoms)):
            if numbered_names:
                name = atom_log.atomname + str(index)
            else:
                name = atom_log.atomname
            atom_md.position = atom_log.position
            atom_md.name = name
        universe.atoms.write(out_basename + '.gro')
        # Trajectory
        opt_steps = self.filter_optimization_steps(find_energy_minima, bond_scan)
        with MDAnalysis.Writer(out_basename + '.xtc', n_atoms) as writer:
            for opt in opt_steps:
                universe.atoms.positions = opt.coordinates
                writer.write(universe.atoms)

    def filter_optimization_steps(self, find_energy_minima: bool=False,
                                  bond_scan: Optional[List[int]]=None) -> List[GaussianGeometry]:
        """
        Filters the optimazation steps searching energy minima or bonds.

        Parameters
        ----------
        find_energy_minima: bool
            If True, only the configurations with local minima energy will be
            considered.
        atoms_index: list of int
            A list with 2 index of the atoms to compute the distance.
        """
        if find_energy_minima:
            filter_steps = energy_minima(self.optimization_steps)
        if bond_scan is not None:
            filter_steps = scan_configurations(self.optimization_steps, bond_scan)
        return filter_steps


def energy_minima(optimization_steps: Tuple[GaussianGeometry]) -> List[GaussianGeometry]:
    """
    Filters the steps to keep only the local energy minima

    Parameters
    ----------
    optimization_steps: list of GaussianGeometry
        The steps to filter.
    """
    
    filter_steps = []
    for index in range(len(optimization_steps) - 1):
        old_opt, new_opt = optimization_steps[index:index+2]
        if old_opt.energy is None:
            continue
        if new_opt.energy > old_opt.energy:
            filter_steps.append(old_opt)
    return filter_steps


def scan_configurations(optimization_steps: Tuple[GaussianGeometry],
                        atoms_index: List[int]) -> List[GaussianGeometry]:
    """
    Filters the steps to keep those with different atomic distances.

    Parameters
    ----------
    optimization_steps: list of GaussianGeometry
        The steps to filter.
    atoms_index: list of int
        A list with 2 index of the atoms to compute the distance.
    """
    filter_steps = []
    for index in range(len(optimization_steps) - 1):
        old_opt, new_opt = optimization_steps[index:index+2]
        if old_opt.energy is None:
            continue
        old_bond = np.linalg.norm(old_opt[atoms_index[0]].position -
                                  old_opt[atoms_index[1]].position)
        new_bond = np.linalg.norm(new_opt[atoms_index[0]].position -
                                  new_opt[atoms_index[1]].position)
        if not np.isclose(new_bond, old_bond):
            filter_steps.append(old_opt)
    return filter_steps
