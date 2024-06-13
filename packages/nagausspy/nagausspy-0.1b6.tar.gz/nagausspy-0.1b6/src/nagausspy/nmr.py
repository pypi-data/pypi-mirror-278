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
Results of the NMR calculation
"""
from collections import defaultdict
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from .frequency import _wide_spetra
from .geometry import GaussianGeometry
from typing import Dict, List, Tuple


class NMR(object):
    """
    Object sotring the results of the Magnetic shielding tensor for
    the NMR calculations

    Parameters
    ----------
    openfile : buffer
        Buffer from were the data will be read
    geometry : GaussianGeometry
        Geometry with the same atoms as the ones in the results

    """

    def __init__(self, openfile, geometry: GaussianGeometry):
        self._nucleus = defaultdict(lambda: [])

        # populate the nucleus before turning it into a "normal" dict
        for index, atom in enumerate(geometry):
            self._nucleus[atom.atomname].append(index)
        self._nucleus = dict(self._nucleus)

        self._tensors = np.zeros((len(geometry), 3, 3))
        self._eigenvalues = np.zeros((len(geometry), 3))
        self._isotropic = np.zeros(len(geometry))
        self._anisotropic = np.zeros(len(geometry))

        self._read_data(openfile)

    def _read_data(self, openfile):
        for index in range(len(self._isotropic)):
            # Read the first line
            splitted = next(openfile).strip().split()
            self._isotropic[index] = float(splitted[4])
            self._anisotropic[index] = float(splitted[7])

            # Start reading the tensor the indexes for the matrix are
            # read such that X->0 Y->1 Z->2

            # *X line
            splitted = next(openfile).strip().split()
            self._tensors[index, :, 0] = np.float_(splitted[1::2])

            # *Y line
            splitted = next(openfile).strip().split()
            self._tensors[index, :, 1] = np.float_(splitted[1::2])

            # *Z line
            splitted = next(openfile).strip().split()
            self._tensors[index, :, 2] = np.float_(splitted[1::2])

            # Read the eigenvalues
            splitted = next(openfile).strip().split()
            self._eigenvalues[index, :] = np.float_(splitted[1:])

    @property
    def tensors(self) -> np.ndarray:
        """
        Returns the tensors for all the nucleus. This can be filtered
        using the nucleus property as mask.
        """
        return self._tensors

    @property
    def nucleus(self) -> Dict[str, List[int]]:
        """
        Dictionary with the index of each nucleus, this can be used to
        filter the other properties.
        """
        return self._nucleus

    @property
    def isotropic(self) -> np.ndarray:
        """
        Returns the isotropìc displacements for all the nucleus. This can
        be filtered using the nucleus property as mask.
        """
        return self._isotropic

    @property
    def anisotropic(self) -> np.ndarray:
        """
        Returns the anisotropìc displacements for all the nucleus. This can
        be filtered using the nucleus property as mask.
        """
        return self._anisotropic

    @property
    def eigenvalues(self) -> np.ndarray:
        """
        Returns the tensors' eigenvalues for all the nucleus. This can be
        filtered using the nucleus property as mask.
        """
        return self._eigenvalues

    def generate_spectra(self, intensities="isotropic", npoints=3000,
                         delta_limits=(None, None), funct="gaussian",
                         nucleus=None, ref=0, wide=20) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genereates a wide espectra from the nmr data.

        Parameters
        ----------
        intensities : str (optional)
            Which kind of intensities will be plotted. the options are
            "isotropic" and "anisotropic". Default = "isotropic"
        npoints : int (optional)
            THe number of points to generate. Default=3000
        delta_limits : tuple(int or None, int or None) (optional)
            The limits for the lower and higher displacements. If None
            the limit will be deduced from the values of the data.
            Default (None, None)
        funct : WideningFunction compatible or str
            The function to be used to widen the peaks. If a string,
            the the matching preset function will be used. The posible
            values are:
                - gaussian: Gaussian widening
                - delta : Deltas on the frecuencies
                          (the npoints parameter will be ignored)
            Default = 'gaussian'
        nucleus : str or None (optional)
            The nucleus to representcalculate the espectra. If None
            all will be calculated. Default None
        ref : float (optional)
            Value of the displacement for the reference. Default 0
        wide : float (optional)
            FWHM of the function (not applicable for delta) in ppm. Default 20.

        Returns
        -------
        x : numpy.ndarray
            The values of the frecuencies axis
        y : numpy.ndarray
            The value of the intensity for each frequency.

        """

        mask = []
        delta_limits = list(delta_limits)
        if nucleus is None:
            mask = list(range(len(self.anisotropic)))
        else:
            mask = self.nucleus[nucleus]

        if intensities == "isotropic":
            ppm = self.isotropic
        elif intensities == "anisotropic":
            ppm = self.anisotropic

        ppm = ppm[mask]
        ppm = ref - ppm
        intensities = np.ones_like(ppm)

        if delta_limits[0] is None:
            delta_limits[0] = ppm.min() - 3*wide

        if delta_limits[1] is None:
            delta_limits[1] = ppm.max() + 3*wide

        return _wide_spetra(ppm, intensities, wide, funct, npoints,
                            delta_limits[0], delta_limits[1])

    def represent_spectra(self, ax=None, plot_options=None, **kwargs):
        """
        Represents the nmr spectra

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
            ax.set_xlabel(r"$\delta$  (ppm)")
            ax.set_ylabel("Intensity (a.u.)")
        return ax
