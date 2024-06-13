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
Implements a functor to configure widening functions and some spectra
widening functions.
"""
import numpy as np

class WideningFunction(object):
    """
    Creates a functor that behaves as a wideding function. This
    function is defined by a center, an intensity and a widening.

    Parameters
    ----------
    func : function
        Function to be used as a template for the widening. This
        function must take as arguments the x coordiante, the center, the
        intensity and the wide (in this particular order) and retun the
        value of the y coordinate in such point.
    center : float
        The coordiante of the center of the function
    intensity : float
        The value of the intensity of the function
    widening : float
        The wide of the function

    """

    def __init__(self, func, center, intensity, widening):
        self.func = func
        self.center = center
        self.intensity = intensity
        self.widening = widening

    def __call__(self, *args):
        """
        Calculates the value on the function in the point.

        Parameters
        ----------
        x : float or numpy.ndarray
            The value(s) were the function must be evaluated

        Returns
        -------
        y : float or numpy.ndarray (the same as the input)
            The values of the function in the input(s) points(s).

        """
        return self.func(args[0], self.center, self.intensity, self.widening)


def gaussian(x, center, intensity, widening):
    """
    Evaluates a gaussian distribution function in a point.

    Parameters
    ----------

    x : float or numpy.ndarray
        The point(s) where the function will be evaluated
    center : float
        The mean value of the distribution
    intensity : float
        The value of the integral of the density
    widening : float
        The standar deviation of the distribution

    Returns
    -------
    data : float or numpy.ndarray (the same as x)
        The function evaluated at the x points.
    """

    return intensity/np.sqrt(2*np.pi*widening**2)*np.exp(-(x-center)**2/(2*widening**2))

def lorentzian(x, center, intensity, widening):
    """
    Evaluates a gaussian distribution function in a point.

    Parameters
    ----------

    x : float or numpy.ndarray
        The point(s) where the function will be evaluated
    center : float
        The mean value of the distribution
    intensity : float
        The value of the integral of the density
    widening : float
        The HWHM

    Returns
    -------
    data : float or numpy.ndarray (the same as x)
        The function evaluated at the x points.
    """

    return (intensity/np.pi)*(widening/((x-center)**2+widening**2))
