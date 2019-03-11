import random
import string
import datetime
from datetime import datetime, timedelta
from typing import NewType
import pandas as pd
import io

def _generate_int(width):
    max_value = int(width * "9")
    return str(random.randint(1, max_value)).zfill(width)

def _generate_float(width, number_of_decimals):
    if width < 4:
        return ''.zfill(width)
    else:
        real_width = width - number_of_decimals - 1
        max_value = int(real_width * "9")
        data = random.uniform(1, max_value)
        float_format = f"0{str(real_width+3)}.{number_of_decimals}f"
        return f"{data:{float_format}}"

def _generate(width):
    special = ["¢", "£", "¥"]
    #random chars upto width - 1 to make sure there is atleast 1 special
    random_chars = [random.choice(string.ascii_letters + ''.join(special)) for i in range(0, width - 1)]
    return ''.join([random.choice(special)] + random_chars)


def _generate_date(format_string, delta_days=0):
    return (datetime.today() - timedelta(days=delta_days)).strftime(format_string)

def _generate_email(width, domain):
    actual_length = width - len(domain) - 1
    local_part = [random.choice(string.ascii_letters) for i in range(0, actual_length)]
    return ''.join(local_part) + '@' + domain

def _gen(data_type, length, optional=None):
    gen_fns = {
        'int': _generate_int,
        'str': _generate,
    }
    if data_type == 'date':
        f =  optional[0] if optional else '%Y/%m/%d' 
        data = _generate_date(f) #not passing delta days yet
    elif data_type == 'float':
        number_of_decimals = optional[0] if optional else 2 
        data = _generate_float(length, number_of_decimals)
    elif data_type == 'email':
        domain = optional[0] if optional else 'gmail.com'
        data = _generate_email(length, domain)
    else:
        data = gen_fns.get(data_type, _generate)(length)

    return data

def _generate_columns(colspecs):
    row_data = []
    for col in colspecs:
        length, data_type, *optional = col        
        row_data.append(_gen(data_type, length, optional))

    return row_data


def _find_colindex_and_length(row_colspecs, colspec):
    for i, spec in enumerate(row_colspecs):
        start, end, _ = colspec
        if spec[0] == start:
            return (i, end - start)
    
    return None


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


def mutate_beyond_recognition(row: bytes, row_colspecs, mutable_col_specs, encoding='utf-8') -> str:
    '''
        Generate fixedwidth data for the provided specification

        Args:
            row (bytes): Encoded bytes of the row data
            row_colspecs ([(int, int)]): A list of pairs (tuples) giving the extents of the fixed-width fields of each line as half-open intervals (i.e., [from, to[ ). 
            mutable_col_specs (tuple-> (from, to, type, optional)): List of offset specifications
            encoding (str): Required encoding

        Returns:
            data: Mutated row.
    '''

    df = pd.read_fwf(io.BytesIO(row), colspecs=row_colspecs,
                           encoding=encoding,
                           header=None, dtype=str)
    

    for mc in mutable_col_specs:
        idx, length = _find_colindex_and_length(row_colspecs, mc)
        _, _, data_type, *optional = mc
        df.at[0,idx] = _gen(data_type, length, optional)

    return ''.join(df.iloc[0, :].values.astype(str).tolist())

