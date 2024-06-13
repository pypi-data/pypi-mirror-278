import pytest
import os
from nagausspy import (check_geometry_equivalence, GaussianCom,
                       clasify_geometries)


ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]

@pytest.fixture
def geometry1():
    fcom = os.path.join(ACTUAL_PATH, "data/conf1_comp.com")
    return GaussianCom(fcom).geometry

@pytest.fixture
def geometry2():
    fcom = os.path.join(ACTUAL_PATH, "data/conf2_comp.com")
    return GaussianCom(fcom).geometry

@pytest.fixture
def geometry3():
    fcom = os.path.join(ACTUAL_PATH, "data/conf3_comp.com")
    return GaussianCom(fcom).geometry

def test_equal(geometry1, geometry2, geometry3):
    assert (check_geometry_equivalence(geometry1, geometry2,
                                       [2, 3, 7], [11, 19]))

    assert not (check_geometry_equivalence(geometry1, geometry3,
                                           [2, 3, 7], [11, 19]))

    assert not (check_geometry_equivalence(geometry1, geometry3,
                                           [2, 3, 7], [11, 19]))

    assert not (check_geometry_equivalence(geometry3, geometry2,
                                           [2, 3, 7], [11, 19]))
def test_network(geometry1, geometry2, geometry3):
    entrada = {
        "geom1": geometry1,
        "geom2": geometry2,
        "geom3": geometry3,
    }
    expected_out = {
        0: ["geom1", "geom2"],
        1: ["geom3"]
    }

    assert expected_out == clasify_geometries(entrada, [2, 3, 7], [11, 19])
