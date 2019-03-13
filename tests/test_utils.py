import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../genie_pkg")

from utils import generate_ip, generate_ipv4_in_subnet
import re
def test_ipv4():
    ipv4 = generate_ip()
    assert re.match('\d+\.\d+\.\d+\.\d+', ipv4)

def test_ipv6():
    ipv6 = generate_ip(v=6)
    v6_part_regex = r'[a-z0-9]{2,4}'
    assert re.match('{0}:{0}:{0}:{0}:{0}:{0}:{0}:{0}'.format(v6_part_regex), ipv6)


def test_ipv4_subnet():
    # network containing all addresses from 10.0.0.0 to 10.0.0.255
    ipv4 = generate_ipv4_in_subnet("10.0.0.0/24")
    assert re.match(r'10\.0\.0\.[0-9]{1,3}', ipv4)