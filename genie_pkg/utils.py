import string

from random import getrandbits, choice
from ipaddress import IPv4Address, IPv6Address, IPv4Network

def generate_email_id(width, domain):
    actual_length = width - len(domain) - 1 # 1 for @
    if actual_length <= 0:
        minimum_expected_length = len(domain) + 2 # 1 for @
        raise Exception("With the domain {0}, Minimum length you should pass is {1}".format(domain, minimum_expected_length))

    local_part = [choice(string.ascii_letters) for i in range(0, actual_length)]
    return ''.join(local_part) + '@' + domain

def generate_ip(v=4):
    if v == 4:
        bits = getrandbits(32) # generates an integer with 32 random bits
        return str(IPv4Address(bits))
    elif v == 6:
        bits = getrandbits(128) # generates an integer with 128 random bits
        # .compressed contains the short version of the IPv6 address
        # str(addr) always returns the short address
        # .exploded is the opposite of this, always returning the full address with all-zero groups and so on
        return IPv6Address(bits).compressed

def generate_ipv4_in_subnet(subnet_cidr):
    subnet = IPv4Network(subnet_cidr)
    # subnet.max_prefixlen contains 32 for IPv4 subnets and 128 for IPv6 subnets
    # subnet.prefixlen is 24 in this case, so we'll generate only 8 random bits
    bits = getrandbits(subnet.max_prefixlen - subnet.prefixlen)
    return str(IPv4Address(subnet.network_address + bits))