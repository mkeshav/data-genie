from genie_pkg.generators import *
import re
import pytest


def test_ipv4():
    ipv4 = generate_ip()
    assert re.match(r'\d+\.\d+\.\d+\.\d+', ipv4)


def test_ipv6():
    ipv6 = generate_ip(v=6)
    v6_part_regex = r'[a-z0-9]{2,4}'
    assert re.match(
        '{0}:{0}:{0}:{0}:{0}:{0}:{0}:{0}'.format(v6_part_regex), ipv6)



def test_bad_ip_length():
    with pytest.raises(GenieException) as _:
        generate_ip(3)

def test_ipv4_subnet():
    # network containing all addresses from 10.0.0.0 to 10.0.0.255
    ipv4 = generate_ipv4_in_subnet("10.0.0.0/24")
    assert re.match(r'10\.0\.0\.[0-9]{1,3}', ipv4)


def test_random_geo():
    for i in range(5):
        x0, y0 = random_geo_coords(radius=1000)
        assert math.isclose(x0, -37.814, abs_tol=0.010)
        assert math.isclose(y0, 144.963, abs_tol=0.010)


def test_check_digit_luhn_mod_10_mc():
    assert check_digit_luhn_mod_10('7992739871') == 3
    assert check_digit_luhn_mod_10('536990340067168') == 0
    assert check_digit_luhn_mod_10('540436862055838') == 9
    assert check_digit_luhn_mod_10('532420806394835') == 7
    assert check_digit_luhn_mod_10('532420499852544') == 4


def test_check_digit_luhn_mod_10_visa():
    assert check_digit_luhn_mod_10('402400714020726') == 6
    assert check_digit_luhn_mod_10('433696811345131') == 9
    assert check_digit_luhn_mod_10('455604196816395') == 0
    assert check_digit_luhn_mod_10('453260352189118') == 4


def test_random_mastercard_number():
    assert random_mastercard_number() is not None


def test_random_visacard_number():
    cc = random_visacard_number(13)
    assert len(cc) == 13


def test_one_of():
    choices = [1, 2, 3]
    v = one_of(choices)
    assert v in choices


def test_one_of_throws_exception():
    with pytest.raises(Exception) as e_info:
        one_of('blah')
        assert False


def test_random_wonderland_text():
    text = random_wonderland_text(2)
    #funny regex may not work for all sentences. No use installing nltk for a test, hence no len assertion
    assert text is not None


def test_random_dob():
    assert random_dob(year=2019, month=1, day=1) == '01/01/2019'
    feb_born = random_dob(year=2019, month=2)
    assert int(feb_born.split('/')[1]) <= 28
    nonfeb_born = random_dob(year=2019, month=3)
    assert int(nonfeb_born.split('/')[1]) <= 30
    assert random_dob() is not None


def test_utc_epoch_start_and_end_ms_for():
    s, e = utc_epoch_start_and_end_ms_for(2019, 7, 22)
    ms_in_day = e - s
    assert ms_in_day + 10 == 24 * 60 * 60 * 1000

def test_utc_now_epoch():
    utc1 = utc_now_epoch_ms()
    utc2 = utc_now_epoch_ms()
    assert utc2 >= utc1