import random
import string

from genie_pkg.generators import random_date_from_today, one_of, generate_email_id
from genie_pkg import GenieException


def _generate_int(width):
    max_value = int(width * "9")
    return str(random.randint(1, max_value)).zfill(width)


def _generate_float(width, number_of_decimals=2):
    real_width = width - number_of_decimals - 1
    if real_width < 1:
        min_expected_length = number_of_decimals + 2
        raise GenieException(
            "With number of decimal places of {0}, Minimum length you should pass is {1}".format(number_of_decimals, min_expected_length))

    max_value = int(real_width * "9")
    data = random.uniform(1, max_value)
    float_format = f"{str(real_width+number_of_decimals)}.{number_of_decimals}f"
    return f"{data:{float_format}}".zfill(width)


def _get_encoding_special_chars(encoding='utf-8'):
    if encoding == 'ascii':
        return string.ascii_letters
    else:
        return ''.join(["¢", "£", "¥"])


def _generate(width, encoding):
    special = _get_encoding_special_chars(encoding)
    # random chars upto width - 1 to make sure there is atleast 1 special
    random_chars = [random.choice(
        f"{string.ascii_letters}{special}") for _ in range(0, width - 1)]
    return ''.join([random.choice(special)] + random_chars)


def _generate_date(length, format_string='%Y/%m/%d', delta_days=0):
    d = random_date_from_today(format_string, delta_days)
    if len(d) > length:
        raise GenieException(
            "Format {0}, does not produce date of length {1}".format(format_string, length))

    return d


def _gen(data_type, length, optional, encoding):
    if data_type == 'one_of':
        val = str(one_of(*optional))
        if len(val) == length:
            data = val
        else:
            raise GenieException(
                "Provided value {0} is not of length {1}".format(val, length))
    elif data_type == 'date':
        data = _generate_date(length, *optional)  # not passing delta days yet
    elif data_type == 'float':
        data = _generate_float(length, *optional)
    elif data_type == 'email':
        data = generate_email_id(length, *optional)
    elif data_type == 'int':
        data = _generate_int(length, *optional)
    else:
        data = _generate(length, encoding)

    return data


def _generate_columns(colspecs, encoding):
    row_data = []
    for col in colspecs:
        length, data_type, *optional = col
        row_data.append(_gen(data_type, length, optional, encoding))

    return row_data


def generate(colspecs, nrows, encoding='utf-8'):
    '''
        Generate fixedwidth data for the provided specification

        Args:
            colspecs (tuple-> (length, type, optional)): List of column specifications (similar to pandas)
            nrows (int): Number of desired rows.
            encoding (str): Required encoding

        Returns:
            data: Iterator over nrows.
    '''
    for _ in range(nrows):
        row_data = _generate_columns(colspecs, encoding)
        yield ''.join(row_data).encode(encoding)


def anonymise_columns(row: bytes, anonymous_col_specs, encoding='utf-8') -> bytes:
    '''
        Generate fixedwidth data for the provided specification

        Args:
            row (bytes): Encoded bytes of the row data
            anonymous_col_specs (tuple-> (from, to, type, optional)): List of offset specifications
            encoding (str): Required encoding

        Returns:
            data: Mutated row.
    '''
    anonymised = row.decode(encoding)
    for ac in anonymous_col_specs:
        start, end, data_type, *optional = ac
        before = anonymised[:start]
        after = anonymised[end:]
        length = end - start
        data = _gen(data_type, length, optional, encoding)
        anonymised = ''.join([before, data, after])

    return anonymised.encode(encoding)
