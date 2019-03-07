from pymonad import curry
import random
import string
import datetime
from datetime import datetime, timedelta

def _generate_int(width):
    sn = str(random.randint(1, 1000))
    if len(sn) > width:
        sn = sn[:width]
    return sn.zfill(width)


def _generate_float(width):
    if width < 3:
        return ''.zfill(width)
    elif width == 3:
        return '0.0'
    else:        
        # 1 to 10 with 2 decimal places will make sure it is 4 in string length always
        return str(round(random.uniform(1, 10), 2)).zfill(width)


def _generate(width):
    special = ["¢", "£", "¥"]
    #random chars upto width - 1 to make sure there is atleast 1 special
    random_chars = [random.choice(string.ascii_letters + ''.join(special)) for i in range(0, width - 1)]
    return ''.join([random.choice(special)] + random_chars)


def _generate_date(format_string, delta_days=0):
    return (datetime.today() - timedelta(days=delta_days)).strftime(format_string)

def _generate_columns(colspecs):
    gen_fns = {
        'int': _generate_int,
        'float': _generate_float,
        'str': _generate,
    }

    col_data = []
    for col in colspecs:
        field_name, length, data_type, *date_format = col
        if data_type == 'date':
            f =  date_format if date_format else '%Y/%m/%d' 
            data = _generate_date(f)
        else:
            data = gen_fns.get(data_type, _generate)(length)
        col_data.append((field_name, data))

    return col_data


def generate(colspecs, nrows, encoding='utf-8'):
    for i in range(nrows):
        col_data = _generate_columns(colspecs)
        print(col_data)
        yield ''.join([c[1] for c in col_data]).encode(encoding)