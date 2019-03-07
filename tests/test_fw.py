import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../genie_pkg")

import pytest
import random

from fw_genie import generate

type_choices = ['int', 'float', 'str']

def test_fw():
    ncols = random.randint(1, 10)
    nrows = random.randint(1, 3)
    colspecs = [('f'+str(i), random.randint(1, 10), random.choice(type_choices),) for i in range(ncols)] + [('date_field', 10, 'date',)]
    data = generate(colspecs, 1)
    expected_length = sum([c[1] for c in colspecs])
    for d in data:
        decoded = d.decode()
        assert len(decoded) == expected_length


def test_generate_bad_decode():
    #has to have atleast 1 special char for this test to work
    ncols = random.randint(1, 10)
    colspecs = [('f'+str(i), random.randint(1, 10), random.choice(type_choices),) for i in range(ncols)]
    #run the test more than once
    for i in range(2, 5):
        for d in generate(colspecs + [('s0', 8, 'str')], 1, 'windows-1252'):
            try:
                print(d.decode('utf-8'))
                assert False
            except UnicodeDecodeError as e:
                assert True


def test_generate_good_decode():
    ncols = random.randint(1, 10)
    colspecs = [('f'+str(i), random.randint(1, 10), random.choice(type_choices),) for i in range(ncols)]
    for d in generate(colspecs + [('s0', 8, 'str')], 1):
        try:
            print(d.decode())
            assert True
        except e:
            assert False