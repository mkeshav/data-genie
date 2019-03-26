import string

from random import getrandbits, choice, uniform, randint, Random
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

def random_geo_coords(center=(-37.814, 144.963,), radius=10000, accuracy=3):
    '''
        Generate random geo co ordinates

        Args:
            center (tuple-> (lat, long)): geo center to start from (defaults to melbourne)
            radius (int): Radius in meters (defaults to 1000)
            accuracy (int): Coordinate accuracy (3 decimals means upto 110m)
            https://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude

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
    return (round(x_latitude, accuracy), round(y_longitude, accuracy),)


def _credit_card_digits(prefixes, length):
    rnd = Random()
    rnd.seed()

    prefix = choice(prefixes)
    digits = [str(rnd.choice(range(0, 10))) for n in range(length - 1 - len(prefix))]

    return prefix + digits

def check_digit_luhn_mod_10(digits):
    '''
        https://en.wikipedia.org/wiki/Luhn_algorithm
    '''
    
    reversed_digits = digits[::-1]
    calibrated_digits = []
    for i, d in enumerate(reversed_digits):
        if i % 2 == 0:
            m = int(d) * 2
            if m > 9:
                calibrated_digits.append(m-9)
            else:
                calibrated_digits.append(m)
        else:
            calibrated_digits.append(int(d))
    
    sum_of_digs = sum(calibrated_digits)
    return (sum_of_digs * 9) % 10

def random_mastercard_number():
    mastercard_prefixes = [
        ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]

    digs = _credit_card_digits(mastercard_prefixes, 16)
    cd = check_digit_luhn_mod_10(digs)
    return ''.join(digs + [str(cd)])