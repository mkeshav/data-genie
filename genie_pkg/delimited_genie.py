
import csv

from genie_pkg.generators import *


def _gen(data_type, optional):
    if data_type == 'email':
        data = generate_email_id(*optional)
    elif data_type == 'int':
        data = str(random_integer(*optional))
    elif data_type == 'float':
        data = str(random_float(*optional))
    elif data_type == 'date':
        data = random_date_from_today(*optional)
    elif data_type == 'special_string':
        data = random_string_with_special_chars(*optional)
    elif data_type == 'geo_coord':
        data = random_geo_coords(*optional)
    elif data_type == 'cc_mastercard':
        data = random_mastercard_number()
    elif data_type == 'cc_visacard':
        data = random_visacard_number(*optional)
    elif data_type == 'one_of':
        data = one_of(*optional)
    else:
        data = random_string(*optional)

    return data


def _generate_columns(colspecs):
    row_data = []
    for col in colspecs:
        data_type, *optional = col
        data = _gen(data_type, optional)
        if data_type == 'geo_coord':
            x0, y0 = data
            row_data.append(str(x0))
            row_data.append(str(y0))
        else:
            row_data.append(data)

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
        if data_type == 'geo_coord':
            x0, y0 = data
            anonymised_csv[col_index] = str(x0)
            anonymised_csv[col_index+1] = str(y0)
        else:
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
    for _ in range(nrows):
        row_data = _generate_columns(colspecs)
        yield delimiter.join(row_data).encode(encoding)
