from genie_pkg.australia import Australia
import pytest
import math

@pytest.fixture
def oz():
    return Australia()

def test_state(oz):
    assert oz.get_random_state() in ["VIC", "NSW", "ACT", "QLD", "SA", "NT"]

def test_postcode(oz):
    p = oz.get_random_postcode("VIC")
    assert int(p) >= 3000

def test_geo_coordinate(oz):
    x0, y0 = oz.get_random_geo_coordinate(state="VIC", postcode="3000")
    assert x0 is not None
    assert y0 is not None