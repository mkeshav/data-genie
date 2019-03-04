from pymonad import curry
import random
import string


@curry
def _generate_int(width):
    sn = str(random.randint(1, 1000))
    if len(sn) > width:
        sn = sn[:width]
    return sn.zfill(width)


@curry
def _generate_float(width):
    if width < 3:
        return ''.zfill(width)
    elif width == 3:
        return '0.0'
    else:        
        # 1 to 10 with 2 decimal places will make sure it is 4 in string length always
        return str(round(random.uniform(1, 10), 2)).zfill(width)


@curry
def _generate(width):
    special = ["¢", "£", "¥"]
    #random chars upto width - 1 to make sure there is atleast 1 special
    random_chars = [random.choice(string.ascii_letters + ''.join(special)) for i in range(0, width - 1)]
    return ''.join([random.choice(special)] + random_chars)


gen_fns = {
    'int': _generate_int,
    'float': _generate_float,
    'str': _generate,
}

type_choices = ['int', 'float', 'str']


def _generate_columns(colspecs):
    return [(col[0], gen_fns.get(col[2], _generate)(col[1])) for col in colspecs]


def generate(colspecs, nrows, encoding='utf-8'):
    data = []
    for i in range(nrows):
        col_data = _generate_columns(colspecs)
        data.insert(0, ''.join([c[1] for c in col_data]).encode(encoding))

    return data


def surprise_me():
    ncols = random.randint(1, 10)
    nrows = random.randint(1, 3)
    colspecs = [('f'+str(i), random.randint(1, 10), random.choice(type_choices),) for i in range(ncols)]
    return (colspecs, generate(colspecs, nrows))
