"""
nagausspy: Basics tools for Gaussian
"""
from .templates import COMMANDLINES
from .reader import GaussianLog
from ._com import GaussianCom, GaussianConfig
from .geometry import GaussianGeometry
from .frequency import Units
from ._commandline import CommandLine
from .widening_functions import gaussian
from .analysis import check_geometry_equivalence, clasify_geometries


from . import frequency as frequency
from . import nmr as nmr
from . import reader as reader
from . import widening_functions as widening_functions
from . import templates
from . import analysis as analysis

def open_file(filename):
    """
    Opens a compatible gaussian file choosing the correct class by
    looking at the file extension.

    Parameters
    ----------
    filename : str
        The path to the file you want to open

    """

    extensions = {
        "com": GaussianCom,
        "log": GaussianLog
    }
    cut = filename.split(".")
    if len(cut) == 1:
        text = "It was not possible to determine the extension for file {}"
        raise ValueError(text.format(filename))

    extension = cut[-1].lower()

    if extension not in extensions:
        text = "Unknown extension {}"
        raise ValueError(text.format(extension))

    return extensions[extension](filename)

__version__ = "0.1-beta3"

__all__ = ["Units", "GaussianLog", "GaussianCom", "CommandLine", "gaussian",
           "COMMANDLINES", "open_file", "GaussianGeometry",
           "check_geometry_equivalence", "clasify_geometries", "frequency",
           "GaussianConfig", "nmr", "reader", "widening_functions", "templates",
           "analysis"]
