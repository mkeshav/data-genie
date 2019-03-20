import string

from random import getrandbits, choice, uniform, randint
from ipaddress import IPv4Address, IPv6Address, IPv4Network
from datetime import datetime, timedelta
import time
import uuid


def generate_email_id(width, domain='dummy.com'):
    actual_length = width - len(domain) - 1  # 1 for @
    if actual_length < 1:
        minimum_expected_length = len(domain) + 2  # 1 for @ and 1 for .
        raise Exception("With the domain {0}, Minimum length you should pass is {1}".format(
            domain, minimum_expected_length))

    local_part = [choice(string.ascii_letters)
                  for i in range(0, actual_length)]
    return ''.join(local_part) + '@' + domain


def generate_ip(v=4):
    if v == 4:
        bits = getrandbits(32)  # generates an integer with 32 random bits
        return str(IPv4Address(bits))
    elif v == 6:
        bits = getrandbits(128)  # generates an integer with 128 random bits
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


def random_integer(start=1, max_value=999):
    return randint(start, max_value)


def random_float(start=1, max_value=999, decimal_places=2):
    return round(uniform(start, max_value), decimal_places)


def random_string(length=20):
    return ''.join([choice(string.ascii_letters) for i in range(0, length)])


def random_string_with_special_chars(length=20):
    special = ["¢", "£", "¥"]
    random_chars = [choice(string.ascii_letters + ''.join(special))
                    for i in range(0, length - 1)]
    return ''.join([choice(special)] + random_chars)


def random_date_from_today(format_string='%Y/%m/%d', delta_days=0):
    return (datetime.today() - timedelta(days=delta_days)).strftime(format_string)


def _current_milli_time(): return int(round(time.time() * 1000))


def random_bool():
    return choice(['true', 'false'])


def now_epoch():
    return _current_milli_time()


def guid():
    return str(uuid.uuid4())
