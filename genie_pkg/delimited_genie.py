
import csv
import sys
import os

from genie_pkg.utils import *


def _gen(data_type, optional):
    if data_type == 'email':
        data = generate_email_id(*optional)
    elif data_type == 'int':
        data = random_integer(*optional)
    elif data_type == 'float':
        data = random_float(*optional)
    elif data_type == 'date':
        data = random_date_from_today(*optional)
    elif data_type == 'special_string':
        data = random_string_with_special_chars(*optional)
    else:
        data = random_string(*optional)

    return str(data)


def _generate_columns(colspecs):
    row_data = []
    for col in colspecs:
        data_type, *optional = col
        row_data.append(_gen(data_type, optional))

    return row_data


def anonymise_columns(row: bytes, anonymous_col_specs, encoding='utf-8', delimiter=',') -> bytes:
    '''
        Generate delimited data for the provided specification

        Args:
            row (bytes): Encoded bytes of the row data
            anonymous_col_specs (tuple-> (from, to, type, optional)): List of offset specifications
            encoding (str): Required encoding
            delimiter (str): Defaults to ,

        Returns:
            data: Mutated row.
    '''
    lines = row.decode(encoding).splitlines()
    anonymised_csv = list(csv.reader(lines, delimiter=delimiter))[0]
    for ac in anonymous_col_specs:
        col_index, data_type, *optional = ac
        data = _gen(data_type, optional)
        anonymised_csv[col_index] = data
        anonymised = delimiter.join(anonymised_csv)

    return anonymised.encode(encoding)


def generate(colspecs, nrows, encoding='utf-8', delimiter=','):
    '''
        Generate fixedwidth data for the provided specification

        Args:
            colspecs (tuple-> (length, type, optional)): List of column specifications (similar to pandas)
            nrows (int): Number of desired rows.
            encoding (str): Required encoding
            delimiter (str): Defaults to ,

        Returns:
            data: Iterator over nrows.
    '''
    for i in range(nrows):
        row_data = _generate_columns(colspecs)
        yield delimiter.join(row_data).encode(encoding)
