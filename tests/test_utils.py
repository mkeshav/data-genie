import sys
import os

from genie_pkg.utils import *
import re


def test_ipv4():
    ipv4 = generate_ip()
    assert re.match('\d+\.\d+\.\d+\.\d+', ipv4)


def test_ipv6():
    ipv6 = generate_ip(v=6)
    v6_part_regex = r'[a-z0-9]{2,4}'
    assert re.match(
        '{0}:{0}:{0}:{0}:{0}:{0}:{0}:{0}'.format(v6_part_regex), ipv6)


def test_ipv4_subnet():
    # network containing all addresses from 10.0.0.0 to 10.0.0.255
    ipv4 = generate_ipv4_in_subnet("10.0.0.0/24")
    assert re.match(r'10\.0\.0\.[0-9]{1,3}', ipv4)


def test_random_geo():
    for i in range(5):
        l = list(random_geo_coords(radius=1000))
        assert len(l) == 1
        x0, y0 = l[0]
        assert math.isclose(x0, -37.814, abs_tol=0.010)
        assert math.isclose(y0, 144.963, abs_tol=0.010)