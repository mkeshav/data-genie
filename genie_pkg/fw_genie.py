import random
import string
import datetime
from datetime import datetime, timedelta
from typing import NewType
import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), os.path.pardir ) )
from genie_pkg import utils

def _generate_int(width):
    max_value = int(width * "9")
    return str(random.randint(1, max_value)).zfill(width)

def _generate_float(width, number_of_decimals=2):
    real_width = width - number_of_decimals - 1
    if real_width < 1:
        min_expected_length = number_of_decimals + 2
        raise Exception(
            "With number of decimal places of {0}, Minimum length you should pass is {1}".format(number_of_decimals, min_expected_length))

    max_value = int(real_width * "9")
    data = random.uniform(1, max_value)
    float_format = f"{str(real_width+number_of_decimals)}.{number_of_decimals}f"
    return f"{data:{float_format}}".zfill(width)

def _generate(width):
    special = ["¢", "£", "¥"]
    #random chars upto width - 1 to make sure there is atleast 1 special
    random_chars = [random.choice(string.ascii_letters + ''.join(special)) for i in range(0, width - 1)]
    return ''.join([random.choice(special)] + random_chars)


def _generate_date(length, format_string='%Y/%m/%d', delta_days=0):
    d = utils.random_date_from_today(format_string, delta_days)
    if len(d) > length:
        raise Exception(
            "Format {0}, does not produce date of length {1}".format(format_string, length))

    return d

def _gen(data_type, length, optional):
    gen_fns = {
        'int': _generate_int,
        'str': _generate,
    }
    if data_type == 'myval':
        val = str(optional[0])
        if len(val) == length:
            data = val
        else:
            raise Exception("Provided value {0} is not of length {1}".format(val, length))
    if data_type == 'date':
        data = _generate_date(length, *optional) #not passing delta days yet
    elif data_type == 'float':
        data = _generate_float(length, *optional)
    elif data_type == 'email':
        data = utils.generate_email_id(length, *optional)
    else:
        data = gen_fns.get(data_type, _generate)(length)

    return data

def _generate_columns(colspecs):
    row_data = []
    for col in colspecs:
        length, data_type, *optional = col        
        row_data.append(_gen(data_type, length, optional))

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
    for i in range(nrows):
        row_data = _generate_columns(colspecs)
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
        data = _gen(data_type, length, optional)
        anonymised = ''.join([before, data, after])
    
    return anonymised.encode(encoding)