import pytest
import os
import numpy as np
from nagausspy import GaussianLog, CommandLine

ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]

@pytest.fixture
def optlog():
    flog = os.path.join(ACTUAL_PATH, "data/output.log")
    return GaussianLog(flog)

@pytest.mark.skip("Gives error")
def test_steps(optlog):
    assert len(optlog.optimization_steps) == 13
    assert optlog.final_geometry.energy == -3472.90032890
