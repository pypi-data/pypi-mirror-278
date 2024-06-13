import pytest
import os
from nagausspy import GaussianCom

ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]

@pytest.fixture
def freqcom():
    flog = os.path.join(ACTUAL_PATH, "data/nincs4_freq.com")
    return GaussianCom(flog)

def test_empty():
    assert len(GaussianCom().geometry) == 0

def test_len(freqcom):
    assert len(freqcom.geometry) == 13

def test_scf(freqcom):
    assert freqcom.commandline["scf"]["conver"].value == "9"

def test_save(freqcom):
    freqcom.save(os.path.join(ACTUAL_PATH, "data/test.com"))
