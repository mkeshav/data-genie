import random
import string
import datetime
from datetime import datetime, timedelta

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

def _generate_columns(colspecs):
    gen_fns = {
        'int': _generate_int,
        'str': _generate,
    }

    col_data = []
    for col in colspecs:
        field_name, length, data_type, *optional = col
        if data_type == 'date':
            f =  optional[0] if optional else '%Y/%m/%d' 
            data = _generate_date(f) #not passing delta days yet
        elif data_type == 'float':
            number_of_decimals = optional[0] if optional else 2 
            data = _generate_float(length, number_of_decimals)
        else:
            data = gen_fns.get(data_type, _generate)(length)

        col_data.append((field_name, data))

    return col_data


def generate(colspecs, nrows, encoding='utf-8'):
    for i in range(nrows):
        col_data = _generate_columns(colspecs)
        yield ''.join([c[1] for c in col_data]).encode(encoding)