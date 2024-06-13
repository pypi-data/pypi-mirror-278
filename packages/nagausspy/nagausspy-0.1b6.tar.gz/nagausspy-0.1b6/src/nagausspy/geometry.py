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

import re
from collections import defaultdict
import numpy as np
from scipy.spatial.distance import cdist
from typing import List, Optional
from gaddlemaps.components import AtomGro, Residue

class GaussianAtom(object):
    """
    Stores the info of an atom, with a similar interface to AtomGro
    """
    ATOMIC_NUMBERS = {1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6:
                      "C", 7: "N", 8: "O", 9: "F", 10: "Ne", 11: "Na",
                      12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S",
                      17: "Cl", 18: "Ar", 19: "K", 20: "Ca", 21: "Sc",
                      22: "Ti", 23: "V", 24: "Cr", 25: "Mn", 26: "Fe",
                      27: "Co", 28: "Ni", 29: "Cu", 30: "Zn", 31:
                      "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br",
                      36: "Kr", 37: "Rb", 38: "Sr", 39: "Y", 40: "Zr",
                      41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru", 45:
                      "Rh", 46: "Pd", 47: "Ag", 48: "Cd", 49: "In",
                      50: "Sn", 51: "Sb", 52: "Te", 53: "I", 54: "Xe",
                      55: "Cs", 56: "Ba", 57: "La", 58: "Ce", 59:
                      "Pr", 60: "Nd", 61: "Pm", 62: "Sm", 63: "Eu",
                      64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho", 68:
                      "Er", 69: "Tm", 70: "Yb", 71: "Lu", 72: "Hf",
                      73: "Ta", 74: "W", 75: "Re", 76: "Os", 77: "Ir",
                      78: "Pt", 79: "Au", 80: "Hg", 81: "Tl", 82:
                      "Pb", 83: "Bi", 84: "Po", 85: "At", 86: "Rn",
                      87: "Fr", 88: "Ra", 89: "Ac", 90: "Th", 91:
                      "Pa", 92: "U", 93: "Np", 94: "Pu", 95: "Am", 96:
                      "Cm", 97: "Bk", 98: "Cf", 99: "Es", 100: "Fm",
                      101: "Md", 102: "No", 103: "Lr", 104: "Rf", 105:
                      "Db", 106: "Sg", 107: "Bh", 108: "Hs", 109:
                      "Mt", 110: "Ds", 111: "Rg", 112: "Cn", 113:
                      "Nh", 114: "Fl", 115: "Mc", 116: "Lv", 117:
                      "Ts", 118: "Og"}

    DEFAULT_COLORMAP = defaultdict(lambda: "black",
                                   {"N":"blue", "C":"dark grey", "S":"yellow",
                                    "O":"red", "Ni":"green", "H":"white", "B":
                                    "magenta", "Mg":"green", "Na": "orange"})

    def __init__(self, atomnumber: int, position: List[float]):
        self.atomnumber: int = atomnumber
        self.position: np.ndarray = np.array(position)
        self._color = None

    def __str__(self) -> str:
        out = " {:15s} {:13.6f} {:13.6f} {:13.6f}".format(self.atomname,
                                                          *self.position)
        return out

    def __repr__(self) -> str:
        out = " {:2s} Atom at {:8.5f} {:8.5f} {:8.5f}".format(self.atomname,
                                                              *self.position)
        return out

    @property
    def color(self) -> str:
        """
        The color to represent
        """
        if self._color is None:
            return self.DEFAULT_COLORMAP[self.atomname]
        return self._color

    @color.setter
    def color(self, value: str):
        self._color = value

    @property
    def atomname(self) -> str:
        """
        The atomname corresponding to the input atomnumber
        """
        return self.ATOMIC_NUMBERS[self.atomnumber]

    @property
    def xyz_str(self) -> str:
        """
        Representation of tyhe atom in xyz format
        """
        out = "{:>3s}{:15.5f}{:15.5f}{:15.5f}".format(self.atomname,
                                                      *self.position)
        return out


class GaussianGeometry(object):
    """
    Stores the geonetry of a gaussian geometry
    """

    TRIGGER = re.compile("-----------------------------------------------------"
                         "----------------")

    ATOMIC_NAMES = {value: key for key, value in
                    GaussianAtom.ATOMIC_NUMBERS.items()}

    SKIPTRIGGERS = 2
    NTRIGGERS = 3

    def __init__(self, openfile, charge: int=0, multiplicity: int=1):
        self.atoms: List[GaussianAtom] = []
        self._multiplicity = multiplicity
        self._charge = charge
        self._energy = None
        self._load_info(openfile)

    def __repr__(self) -> str:
        return "Geometry with {} atoms".format(self.natoms)

    def __str__(self) -> str:
        out = "{} {}\n".format(self.charge, self.multiplicity)
        out += "\n".join([str(i) for i in self])
        return out

    def __len__(self) -> int:
        return self.natoms

    def __getitem__(self, index) -> GaussianAtom:
        return self.atoms[index]

    def _load_info(self, openfile):
        triggered = 0
        for line in openfile:
            if self.TRIGGER.search(line):
                triggered += 1

                if triggered >= self.NTRIGGERS:
                    break

                continue
            if triggered < self.SKIPTRIGGERS:
                continue
            self._load_line(line)

    def _load_line(self, line: str):
        fields = line.split()
        self.atoms.append(GaussianAtom(int(fields[1]),
                                       [float(i) for i in fields[3:6]]))

    def xyz_str(self, title: Optional[str]=None) -> str:
        """
        Returns the string corresponding to the xyz representation of
        the geometry.

        Parameters
        ----------
        title : str, optional
             The title of the geometry that will appear in the xyz. If
             None a default one will be used.

        Returns
        -------
        xyz : str
            xyz representation of the geometry.
        """

        if title is None:
            title = "Geometry generated by NaGaussPy"
        out = "{}\n{}\n{}\n".format(self.natoms, title,
                                    "\n".join(a.xyz_str for a in self.atoms))
        return out

    def save_as_xyz(self, filename: str, title: Optional[str]=None):
        """
        Saves the geometry as an xyz in a file.

        Parameters
        ----------
        filename : str
            Filename tot he file where the data will be saved.
        title : str, optional
            The title of the geometry that will appear in the xyz. If
            None a default one will be used.

        """
        with open(filename, "w") as openfile:
            openfile.write(self.xyz_str(title=title))

        # Find the bonds

        dist_mat = cdist(self.coordinates, self.coordinates,
                         metric="sqeuclidean")
        dist_mat = dist_mat < cut**2

        for i in range(len(self)-1):
            for j in range(i+1, len(self)):
                if dist_mat[i][j]:
                    mlab.plot3d(*zip(self[i].position,
                                     self[j].position))

    def align_with(self, atom_index: List[int], position: np.ndarray):
        """
        Aligns the geometry ina way that 3 atoms are orientated as 3
        reference points.

        Parameters
        ----------
        atom_index : list
            The indexes of the 3a toms to use in the alignment
        position : np.array(3,3)
            The positions of the reference points in the alignment.
            Each row correspond to one point.


        """
        from gaddlemaps import calcule_base

        old_position = np.array([self[i].position for i in atom_index])

        sel_base, sel_app = calcule_base(position)
        mol_base, mol_app = calcule_base(old_position)

        delta = sel_app - mol_app
        self.coordinates += delta
        conversion_matrix = np.matmul(np.linalg.inv(sel_base), mol_base)
        self.coordinates = np.matmul(conversion_matrix, self.coordinates.T).T

    @classmethod
    def from_xyz(cls, filename: str):
        """
        Creates a geometry from an xyz datafile

        Parameters
        ----------
        filename : str
            XYZ file

        Returns
        -------
        xyz : GaussianGeometry
            The geometry represented on the xyz file
        """

        geometry = cls.__new__(cls)
        geometry.charge = 0
        geometry.multiplicity = 1
        geometry.atoms = []

        with open(filename) as _file:
            # Skip the number of atoms and title line
            _ = next(_file)
            _ = next(_file)

            for line in _file:
                if not line.strip():
                    continue
                atomname, *coords = line.split()[:4]
                coords = np.array([float(i) for i in coords])
                geometry.atoms.append(
                    GaussianAtom(cls.ATOMIC_NAMES[atomname], coords)
                    )
        return geometry

    @property
    def natoms(self) -> int:
        """
        The number of atoms in the system
        """
        return len(self.atoms)

    @property
    def energy(self) -> Optional[float]:
        """
        SCF energy of the configuration in Hartrees
        """
        return self._energy
    @energy.setter
    def energy(self, value: float):
        self._energy = value

    @property
    def charge(self) -> int:
        """
        Charge of the system
        """
        return self._charge
    @charge.setter
    def charge(self, value: int):
        self._charge = value

    @property
    def multiplicity(self) -> int:
        """
        Multiplicity of the system
        """
        return self._multiplicity
    @multiplicity.setter
    def multiplicity(self, value: int):
        self._multiplicity = value

    @property
    def coordinates(self) -> np.ndarray:
        """
        The coordinates of all the atoms
        """
        return np.array([i.position for i in self.atoms])

    @coordinates.setter
    def coordinates(self, newval: np.ndarray):
        if len(newval) == self.natoms:
            for index, coordinate in enumerate(newval):
                self.atoms[index].position = np.array(coordinate)
        else:
            text = ("The number of atoms do not match the dimension "
                    "of the current data ({})")
            raise ValueError(text.format(self.coordinates.shape))

    @property
    def atom_numbers(self) -> np.ndarray:
        """
        The atomic numbers of all the atoms
        """
        return np.array([i.atomnumber for i in self.atoms])

    @property
    def moleculegro(self) -> Residue:
        """
        The MoleculeGro version of the geometry.
        """
        atoms: List[AtomGro] = []
        index = 1
        for number, coordinates in zip(self.atom_numbers, self.coordinates):
            atoms.append(AtomGro([1, "MOL",
                                  GaussianAtom.ATOMIC_NUMBERS[number],
                                  index]+list(coordinates/10)))
            index += 1
        mol = sum(atoms[1:], atoms[0])
        return mol

    def __add__(self, other):
        if isinstance(other, GaussianGeometry):
            new = self.__new__(self.__class__)
            new.atoms = self.atoms + other.atoms
            new.charge = self.charge + other.charge
            new.multiplicity = self.multiplicity + other.multiplicity - 1
            return new

        return other + self
    
    @staticmethod
    def bond_distance(atom1: GaussianAtom, atom2: GaussianAtom) -> float:
        """Returns the bonding distance between 2 atoms in Angstroms.

        Args:
            atom1 (GaussianAtom): First Atom
            atom2 (GaussianAtom): Second Atom

        Returns:
            float: Distance Between atoms.
        """
        return np.linalg.norm(atom1.position - atom2.position) 
    
    @staticmethod
    def angle(atom1: GaussianAtom, atom2: GaussianAtom, atom3: GaussianAtom) -> float:
        """Return the angle between 3 atoms in degrees.

        Args:
            atom1 (GaussianAtom): First atom
            atom2 (GaussianAtom): Second (vertex) atom
            atom3 (GaussianAtom): Third Atom

        Returns:
            float: Angle formed between the atoms.
        """
        vec1 = atom1.position - atom2.position
        vec1 /= np.linalg.norm(vec1)
        vec2 = atom3.position - atom2.position
        vec2 /= np.linalg.norm(vec2)
        cos_angle = np.dot(vec1, vec2)
        angle = np.arccos(cos_angle) * 180 / np.pi
        return angle
    
    @staticmethod
    def dihedral_angle(atom1: GaussianAtom, atom2: GaussianAtom, atom3: GaussianAtom,
                 atom4: GaussianAtom) -> float:
        """Returns the proper dihedral angle formed between 4 atoms in degrees.

        Args:
            atom1 (GaussianAtom): First atom
            atom2 (GaussianAtom): Second Atom
            atom3 (GaussianAtom): Third Atom
            atom4 (GaussianAtom): Forth atom

        Returns:
            float: Dihedral angle in degrees.
        """
        # see https://en.wikipedia.org/wiki/Dihedral_angle#In_polymer_physics
        vectors = [
            atom2.position - atom1.position,
            atom3.position - atom2.position,
            atom4.position - atom3.position,
        ]
        reference1 = np.cross(vectors[0], vectors[1])
        reference1 /= np.linalg.norm(reference1)
        reference2 = np.cross(vectors[1], vectors[2])
        reference2 /= np.linalg.norm(reference2)
        
        cos_angle = np.dot(reference1, reference2)
        
        sin_angle = (vectors[1]/np.linalg.norm(vectors[1])).dot(np.cross(reference1, reference2))
        
        angle = np.arctan2(sin_angle, cos_angle) * 180 / np.pi
        
        return angle


class ComGeometry(GaussianGeometry):
    """
    Geometry of .com file or from the initial geometry of a log file
    """

    TRIGGER = re.compile(r"^\s*$")
    SKIPTRIGGERS = 0
    NTRIGGERS = 1

    def _load_line(self, line: str):
        fields = line.split()
        self.atoms.append(GaussianAtom(self.ATOMIC_NAMES[fields[0]],
                                       [float(i) for i in fields[1:4]]))

def colors_codes():
    """
    Defines a color code for diferent colors.

    Define some colors in rgb: Red, greem, blue, black, white, yellow, cian,
    magenta, brown, grey, light blue, light red, dark grey.

    Returns:
    --------
    colors : dictionary
        A dictionary with the colors names and its respective codes.
    """
    colors = {}
    colors['red'] = (1, 0, 0)
    colors['green'] = (0, 1, 0)
    colors['blue'] = (0, 0, 1)
    colors['black'] = (0, 0, 0)
    colors['white'] = (1, 1, 1)
    colors['yellow'] = (1, 1, 0)
    colors['cian'] = (0, 1, 1)
    colors['magenta'] = (1, 0, 1)
    colors['brown'] = (0.588, 0.294, 0)
    colors['grey'] = (0.5, 0.5, 0.5)
    colors['light red'] = tuple([i/255. for i in (255, 102, 102)])
    colors['light blue'] = tuple([i/255. for i in (153, 153, 255)])
    colors['dark grey'] = tuple([i/255. for i in (32, 32, 32)])
    colors['orange'] = tuple([i/255. for i in (255, 165, 0)])
    colors['orangered'] = tuple([i/255. for i in (255, 69, 0)])
    return colors
