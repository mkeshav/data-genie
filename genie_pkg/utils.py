import string

from random import getrandbits, choice, uniform, randint
from ipaddress import IPv4Address, IPv6Address, IPv4Network
from datetime import datetime, timedelta
import time
import uuid
import math


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

def random_geo_coords(center=(-37.814, 144.963,), radius=10000):
    '''
        Generate random geo co ordinates

        Args:
            center (tuple-> (lat, long)): geo center to start from (defaults to melbourne)
            radius (int): Radius in meters (defaults to 1000)

            When using geographic (lat,lon) coordinates, 
            then x0 (longitude) and y0 (latitude) will be in degrees but r will most 
            likely be in meters (or feet or miles or some other linear measurement). 
            First, convert the radius r into degrees as if you were located near the 
            equator. Here, there are about 111,300 meters in a degree.

            Second, after generating x and y as in step (1), 
            adjust the x-coordinate for the shrinking of the east-west distances:


        Returns:
            data: (float, float)
    '''

    r = radius/111300 #about 111300 meters in one degree
    x0,y0 = center
    u = float(uniform(0.0,1.0))
    v = float(uniform(0.0,1.0))
    w = r * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t) 
    y = w * math.sin(t)
    
    x_latitude  = x + x0
    y_longitude = y + y0
    #3th decimal provides accuracy upto 110m (https://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude)
    return (round(x_latitude, 3), round(y_longitude,3),)


