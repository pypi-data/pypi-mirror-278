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
import enum
import numpy as np
import matplotlib.pyplot as plt
from .widening_functions import WideningFunction, gaussian, lorentzian
from typing import Tuple, Optional


class Units(enum.Enum):
    """
    Some conversion units. All of them are based on eV

    The KbT is the thermal energy at room temperature (278.15K)
    """
    eV = 1.
    Ha = 27.211385
    kCalmol = 0.0433634
    kJmol = 0.01036410
    KbT = 0.02569257


class GaussianFrequencies(object):
    """
    Stores the frequencies of a Gaussian raman spectroscopy
    """

    WIDENING = 20
    _TRANSLATIONS = {"Frequencies": "frequencies",
                     "Red. masses": "reduced_mass",
                     "Frc consts": "force_constants",
                     "IR Inten": "ir_intensities",
                     "Raman Activ": "raman_activity",
                     "Depolar (P)": "depolar_p",
                     "Depolar (U)": "depolar_u"}

    def __init__(self, openfile, molsize: int):

        self.TRIGGERS = {
            re.compile("Low frequencies ---"): self._load_low_freq,
            re.compile("Diagonal vibrational polarizability:"): self._load_polarizability,
            re.compile("                     1"): self._load_main,
            re.compile("- Thermochemistry -"): self._load_thermo,

        }

        self._mode_properties = {
            "frequencies": [],
            "reduced_mass": [],
            "force_constants": [],
            "ir_intensities": [],
            "raman_activity": [],
            "depolar_p": [],
            "depolar_u": [],
        }

        self._normal_modes = np.array([[[]]])
        self._low_frequencies = []
        self._polarizability = np.array([0, 0, 0])
        self._molsize = molsize
        self._thermo = None
        self._load_info(openfile)

    def __repr__(self):
        return ("Frequencies object with "
                "{} normal modes").format(len(self.frequencies))

    @property
    def frequencies(self) -> np.ndarray:
        """
        Returns all the frequencies
        """
        return self._mode_properties["frequencies"].copy()

    @property
    def reduced_mass(self) -> np.ndarray:
        """
        Returns the reduced mass of each of the normal modes
        """
        return self._mode_properties["reduced_mass"].copy()

    @property
    def force_constants(self) -> np.ndarray:
        """
        Returns the force constants of each normal mode
        """
        return self._mode_properties["force_constants"].copy()

    @property
    def ir_intensities(self) -> np.ndarray:
        """
        Returns the intensities of every normal node
        """
        return self._mode_properties["ir_intensities"].copy()

    @property
    def raman_activity(self) -> np.ndarray:
        """
        Returns the raman activity
        """
        return self._mode_properties["raman_activity"].copy()

    @property
    def normal_modes(self) -> np.ndarray:
        """
        Returns all the normal modes. First index the nromal mode,
        second the atom and third the component of the eigenvector
        """
        return self._normal_modes.copy()

    @property
    def low_frequencies(self) -> np.ndarray:
        """
        Returns the frequencies at k=0
        """
        return np.array(self._low_frequencies)

    @property
    def polarizability(self) -> np.ndarray:
        """
        Returns the polarizability on the 3 coordinate axes
        """
        return self._polarizability

    @property
    def thermochemistry(self) -> Optional['GaussianThermochemistry']:
        """
        The object storing all the thermochemistry related values
        """
        return self._thermo

    def _load_polarizability(self, line, openfile):
        line = next(openfile)
        self._polarizability = np.array([float(i) for i in line.split()])
        return

    def _load_main(self, line, openfile):
        self._normal_modes = []

        while line.strip():
            # The previous line should be the one with the indexes
            line = next(openfile) # This line has the atom types

            line = next(openfile)
            while len(line.split("--")) == 2:

                key = line.split("--")[0].strip()
                if key in self._TRANSLATIONS:
                    formated = self._TRANSLATIONS[key]

                    vals = [float(i) for i in line.split("--")[1].split()]

                    self._mode_properties[formated] += vals

                    line = next(openfile)

            # Determine if we have 1, 2, or 3  eigenvalues per line
            nset = int((len(line.split()) - 2) / 3)

            set2append = [np.zeros([self._molsize, 3]) for i in range(nset)]
            for molindex in range(self._molsize):
                line = next(openfile)
                for setindex in range(nset):
                    offset = 2+3*setindex
                    newval = np.array([float(i)
                                       for i in line.split()[offset:offset+3]])
                    set2append[setindex][molindex, :] = newval
            line = next(openfile)  # restart the loop
            self._normal_modes += set2append

        for key, val in self._mode_properties.items():
            self._mode_properties[key] = np.array(val)
        return

    def _load_low_freq(self, line, _):
        fields = line.split("---")[1].split()
        self._low_frequencies += [float(i) for i in fields]
        return

    def _load_thermo(self, _, openfile):
        self._thermo = GaussianThermochemistry(openfile)

    def _load_info(self, openfile):
        for line in openfile:
            for trigger, method in self.TRIGGERS.items():
                if trigger.search(line):
                    method(line, openfile)
                    if method == self._load_thermo:
                        return

    def generate_spectra(self, intensities="IR", npoints=3000, maxfreq=None,
                         funct="gaussian") -> Tuple[np.ndarray,np.ndarray]:
        """
        Generates a wided spectra from the readf requencies.

        Parameters
        ----------
        intensities : str (optional)
            Which kind of intensities will be plotted. the options are
            "IR", "ones", ,and "raman". Default = "IR"
        npoints : int (optional)
            THe number of points to generate. Default=300
        maxfreq : float or None (optional)
            The maximum frequencie of the scpectra. If None, a
            value of 1.1 times the highest freqeuncie normal mode
            will be chosen. Default = None
        funct : WideningFunction compatible or str
            The function to be used to widen the peaks. If a string,
            the the matching preset function will be used. The posible
            values are:
                - gaussian: Gaussian widening
                - delta : Deltas on the frecuencies
                          (the npoints parameter will be ignored)
            Default = 'gaussian'

        Returns
        -------
        x : numpy.ndarray
            The values of the frecuencies axis
        y : numpy.ndarray
            The value of the intensity for each frequency.
        """


        widen = self.WIDENING

        if intensities == "IR":
            data = self.ir_intensities
        elif intensities == "raman":
            data = self.raman_activity
        elif intensities == "ones":
            data = np.ones_like(self.ir_intensities)

        return _wide_spetra(self.frequencies, data, widen,
                            funct, npoints, 0, maxfreq)

    def represent_spectra(self, ax=None, plot_options=None, **kwargs):
        """
        Represents the read spectra

        Parameters
        ----------
        ax : matplotlib.Axes or None
            The axes were the plot will be made, if None a new axis
            will be generate.
        plot_options: dict or None (optional)
            Dict with options for the plot. Default None
        **kwargs : Any keyword argument of the function generate_spectra

        Returns
        -------
        ax : matplotlib.axes
            The axes were the plot was made

        """
        if plot_options is None:
            plot_options = {}

        # Save if the axes were generated of used as input
        generated_ax = False
        if ax is None:
            _, ax = plt.subplots()
            generated_ax = True

        ax.plot(*self.generate_spectra(**kwargs), **plot_options)

        # If the axes were generated by the function add some labels
        if generated_ax:
            ax.set_xlabel(r"Frequency (cm$^{-1}$)")
            ax.set_ylabel("Intensity (a.u.)")
        return ax

class GaussianThermochemistry(object):
    """
    Stores the information about the thermochemistry after a frequencie calculation
    """

    MAX_MAGNITUDES = 4

    def __init__(self, openfile):

        self._TRIGGERS = {
            re.compile("Sum of electronic and zero-point Energies"): self._read_zero,
            re.compile("Sum of electronic and thermal Energies"): self._read_thermal,
            re.compile("Sum of electronic and thermal Enthalpies"): self._read_enthalpy,
            re.compile("Sum of electronic and thermal Free Energies"): self._read_free,
        }

        self._electronic_energy = None
        self._zero_point_energy = None
        self._thermal_energy = None
        self._enthalpy = None
        self._free_energy = None
        self._TS = None
        self._cv = None
        self._cv_rotational = None
        self._cv_translational = None
        self._cv_vibrational = None
        self._units = Units.Ha
        self._parse(openfile)
        self._parse_cv(openfile)

    def __repr__(self):
        if self._electronic_energy is None:
            string = ("Sum of electronic and zero-point Energies = {} {}\n"
                      "Sum of electronic and thermal Energies = {} {}\n"
                      "Sum of electronic and thermal Enthalpies = {} {}\n"
                      "Sum of electronic and thermal Free Energies = {} {}\n")
            string = string.format(self.zero_point_energy, self.units.name,
                                   self.thermal_energy, self.units.name,
                                   self.enthalpy, self.units.name,
                                   self.free_energy, self.units.name)
        else:
            string = ("Electronic energy = {} {}\n"
                      "Zero-point Energy = {} {}\n"
                      "Thermal Energy = {} {}\n"
                      "Thermal Enthalpy = {} {}\n"
                      "Thermal Free Energy = {} {}\n")
            string = string.format(self.electronic_energy, self.units.name,
                                   self.zero_point_energy, self.units.name,
                                   self.thermal_energy, self.units.name,
                                   self.enthalpy, self.units.name,
                                   self.free_energy, self.units.name)
            
        string += ("Total CV = {} {}/K\n"
                   "Translational CV = {} {}/K\n"
                   "Rotational CV = {} {}/K\n"
                   "Vibrational CV = {} {}/K\n")
        string = string.format(self.CV, self.units.name,
                               self.CV_translational, self.units.name,
                               self.CV_rotational, self.units.name,
                               self._cv_vibrational, self.units.name)
        return string

    def _parse(self, openfile):
        read_magnitudes = 0
        for line in openfile:
            for trigger, method in self._TRIGGERS.items():
                if trigger.search(line):
                    method(line)
                    read_magnitudes += 1
                if read_magnitudes == self.MAX_MAGNITUDES:
                    self._finish()
                    return

    def _read_zero(self, line):
        self._zero_point_energy = float(line.split("=")[1])
        return
    
    def _parse_cv(self, openfile):
        for line in openfile:
            if line.strip().startswith("E (Thermal)"):
                break
        next(openfile)
        units_factor = Units.kCalmol.value/(1000*Units.Ha.value)
        self._cv = float(next(openfile).split()[2]) * units_factor
        next(openfile)
        self._cv_translational = float(next(openfile).split()[2]) * units_factor
        self._cv_rotational = float(next(openfile).split()[2]) * units_factor
        self._cv_vibrational = float(next(openfile).split()[2]) * units_factor

        

    def _read_thermal(self, line):
        self._thermal_energy = float(line.split("=")[1])
        return

    def _read_enthalpy(self, line):
        self._enthalpy = float(line.split("=")[1])
        return

    def _read_free(self, line):
        self._free_energy = float(line.split("=")[1])

    def _finish(self):
        self._TS = self._enthalpy - self._free_energy

    def set_energy_reference(self, energy, units=Units.Ha):
        """
        Sets the energy reference to a dsired value taking into
        account the units.

        Parameters
        ----------
        energy : float
            Value of the energy reference.
        units : Units, optional
            Units of the energy reference value. Default Units.Ha

        """
        # If the energy reference already exist undo the reference
        if self._electronic_energy is not None:
            old_energy = self._electronic_energy
            self._electronic_energy = None
            self.set_energy_reference(old_energy, units=self.units)

        # transform to the proper units
        energy += units.value / self.units.value

        self._electronic_energy = energy
        self._zero_point_energy -= energy
        self._thermal_energy -= energy
        self._enthalpy -= energy
        self._free_energy -= energy
        self._TS -= energy

    @property
    def units(self):
        """
        Units of the values stored. Changing this value to another
        will change all the values stored
        """
        return self._units

    @units.setter
    def units(self, value):
        if self._electronic_energy is not None:
            self._electronic_energy *= self.units.value/value.value
        self._zero_point_energy *= self.units.value/value.value
        self._thermal_energy *= self.units.value/value.value
        self._enthalpy *= self.units.value/value.value
        self._free_energy *= self.units.value/value.value
        self._TS *= self.units.value/value.value
        
        self._cv *= self.units.value/value.value
        self._cv_translational *= self.units.value/value.value
        self._cv_rotational *= self.units.value/value.value
        self._cv_vibrational *= self.units.value/value.value
        
        self._units = value

    @property
    def electronic_energy(self):
        """
        SCF electronic energy taken from the reference
        """
        return self._electronic_energy

    @property
    def zero_point_energy(self):
        """
        Returns the corrected zero point energy
        """
        return self._zero_point_energy

    @property
    def thermal_energy(self):
        """
        The corrected thermal energy
        """
        return self._thermal_energy

    @property
    def enthalpy(self):
        """
        The corrected enthalpy
        """
        return self._enthalpy

    @property
    def free_energy(self):
        """
        The corrected Free energy
        """
        return self._free_energy

    @property
    def TS(self):
        """
        The product of the temperature and the
        increment of entropy
        """
        return self._TS
    
    @property
    def CV(self):
        """
        Total Heat capacity at constant volume
        """
        return self._cv
    
    @property
    def CV_translational(self):
        """
        Contribution to the Heat capacity at constant volume due to translation
        """
        return self._cv_translational
    
    @property
    def CV_rotational(self):
        """
        Contribution to the Heat capacity at constant volume due to rotations
        """
        return self._cv_rotational
    
    @property
    def CV_vibrational(self):
        """
        Contribution to the Heat capacity at constant volume due to vibrations
        """
        return self._cv_vibrational

    def __add__(self, other):
        if self.units.value != other.units.value:
            text = "Missmatch in the units of the thermochmistry {} and {}"
            text = text.format(self.units.name, other.units.name)
            raise ValueError(text)

        obj = self.__new__(self.__class__)
        obj._units = self.units
        obj._zero_point_energy = (self.zero_point_energy
                                  + other.zero_point_energy)
        obj._thermal_energy = (self.thermal_energy
                               + other.thermal_energy)
        obj._enthalpy = (self.enthalpy + other.enthalpy)
        obj._free_energy = (self.free_energy + other.free_energy)
        obj._TS = self.TS + other.TS
        obj._cv = self.CV + other.CV
        obj._cv_translational = self.CV_translational + other.CV_translational
        obj._cv_rotational = self.CV_rotational + other.CV_rotational
        obj._cv_vibrational = self.CV_vibrational + other.CV_vibrational

        if (self.electronic_energy is None) and (other.electronic_energy is None):
            obj._electronic_energy = None
        elif self.electronic_energy is None:
            obj._electronic_energy = other.electronic_energy
        elif other.electronic_energy is None:
            obj._electronic_energy = self.electronic_energy
        else:
            obj._electronic_energy = (self._electronic_energy
                                      + other._electronic_energy)
        return obj

    def __mul__(self, other):
        obj = self.__new__(self.__class__)
        obj._units = self.units
        obj._zero_point_energy = self.zero_point_energy * other
        obj._thermal_energy = self.thermal_energy * other
        obj._enthalpy = self.enthalpy* other
        obj._free_energy = self.free_energy * other
        obj._TS = self.TS * other
        obj._cv = self.CV * other
        obj._cv_translational = self.CV_translational * other
        obj._cv_rotational = self.CV_rotational * other
        obj._cv_vibrational = self.CV_vibrational * other

        obj._electronic_energy = self.electronic_energy
        if self.electronic_energy is not None:
            obj._electronic_energy *= other
        return obj

    def __truediv__(self, other):
        return self * (1./other)

    __div__ = __truediv__

    def __rmul__(self, other):
        return self*other

    def __sub__(self, other):
        return self + (-1*other)

def _wide_spetra(frequencies, data, widen, funct, npoints, minfreq, maxfreq):
    functions = {
        "gaussian": gaussian,
        "lorentzian": lorentzian
    }

    if maxfreq is None:
        maxfreq = np.max(frequencies * 1.1)

    if isinstance(funct, str):
        if funct == "delta":
            return _generate_delta_spectra(frequencies, data, maxfreq=maxfreq)
        else:
            funct = functions[funct]

    functs = [WideningFunction(funct, freq, intensity, widen)
              for freq, intensity in zip(frequencies, data)]

    # Create the array of x

    xdata = np.linspace(minfreq, maxfreq, npoints)
    ydata = sum(func(xdata) for func in functs)
    return xdata, ydata

def _generate_delta_spectra(frequencies, data, maxfreq):
    data = data[frequencies < maxfreq]
    frequencies = frequencies[frequencies < maxfreq]
    xdata = np.zeros(3*len(data))
    ydata = np.zeros(3*len(data))

    for i, value in enumerate(data):
        xdata[3*i:3*(i+1)] = frequencies[i]*np.ones(3)
        ydata[1+3*i] = value

    return xdata, ydata
