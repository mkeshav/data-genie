from genie_pkg.generators import *

def is_valid_cc(cc):
    first_15_digits = cc[:-1]
    check_digit = cc[len(cc) - 1]
    return check_digit_luhn_mod_10(first_15_digits) == int(check_digit)