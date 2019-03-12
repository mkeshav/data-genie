import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../genie_pkg")

import pytest
import random
import io

from fw_genie import generate, mutate_beyond_recognition
import pandas as pd

type_choices = ['int', 'float', 'str']

def test_fw():
    min_width = 4 #this is to make sure floats are valid
    ncols = random.randint(1, 10)
    nrows = random.randint(1, 3)
    default_specs = [(random.randint(min_width, 10), random.choice(type_choices),) for i in range(ncols)]
    colspecs =  default_specs + [(10, 'date', '%d/%m/%Y'), (10, 'float', 3), (15, 'email', 'mail.com')]
    data = generate(colspecs, nrows=1)
    expected_length = sum([c[0] for c in colspecs])
    for d in data:
        decoded = d.decode()
        assert len(decoded) == expected_length


def test_generate_bad_decode():
    #has to have atleast 1 special char for this test to work
    ncols = random.randint(1, 10)
    colspecs = [(random.randint(1, 10), random.choice(type_choices),) for i in range(ncols)]
    #run the test more than once
    for i in range(2, 5):
        for d in generate(colspecs + [(8, 'str')], nrows=1, encoding='windows-1252'):
            try:
                print(d.decode('utf-8'))
                assert False
            except UnicodeDecodeError as e:
                assert True


def test_generate_good_decode():
    ncols = random.randint(1, 10)
    colspecs = [(random.randint(1, 10), random.choice(type_choices),) for i in range(ncols)]
    for d in generate(colspecs + [(8, 'str')], nrows=1):
        try:
            print(d.decode())
            assert True
        except e:
            assert False


def test_mutate():
    colspecs = [(0, 5), (5, 8), (8, 11), (11, 14), (14, 20), (20, 28), (28, 38)]
    input_encoding = 'windows-1252'
    row = 'FReNG£Ni£iFthtR¥ubOswUPhmQWJoypvF¢MFcR'.encode(input_encoding)

    cols_mutate_spec = [(0, 5, 'int'), (28, 38, 'float')]
    mutated = mutate_beyond_recognition(row, row_colspecs=colspecs, mutable_col_specs=cols_mutate_spec, encoding=input_encoding)
    
    assert len(mutated) == len(row.decode(input_encoding))
    df = pd.read_fwf(io.StringIO(mutated), colspecs=colspecs,
                           encoding=input_encoding,
                           header=None, dtype=str)
    assert df.at[0,0] != 'FReNG'
    assert isinstance(float(df.at[0, 6]), float) == True