import pytest
import os
from nagausspy import open_file, GaussianCom, GaussianLog

ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]
@pytest.fixture
def logfile():
    flog = os.path.join(ACTUAL_PATH, "data/output_freq.log")
    return flog

@pytest.fixture
def comfile():
    flog = os.path.join(ACTUAL_PATH, "data/nincs4_square.com")
    return flog

def test_open(comfile, logfile):
    assert isinstance(open_file(comfile), GaussianCom)
    assert isinstance(open_file(logfile), GaussianLog)
