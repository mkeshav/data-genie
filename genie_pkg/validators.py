from genie_pkg.generators import check_digit_luhn_mod_10

def is_valid_cc(cc) -> bool:
    """Validates credit card.

    Args:
        cc ([str]): Credit card number

    Returns:
        [bool]: True if it is a valid cc
    """
    first_15_digits = cc[:-1]
    check_digit = cc[len(cc) - 1]
    return check_digit_luhn_mod_10(first_15_digits) == int(check_digit)