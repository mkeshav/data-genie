import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../genie_pkg")

import pytest
import random

from fw import surprise_me, generate, type_choices

def test_fw():
    (colspecs, data) = surprise_me()
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
        s = generate(colspecs + [('s0', 8, 'str')], 1, 'windows-1252')[0]
        try:
            print(s.decode('utf-8'))
            assert False
        except UnicodeDecodeError as e:
            assert True


def test_generate_good_decode():
    ncols = random.randint(1, 10)
    colspecs = [('f'+str(i), random.randint(1, 10), random.choice(type_choices),) for i in range(ncols)]
    s = generate(colspecs + [('s0', 8, 'str')], 1)[0]
    try:
        print(s.decode())
        assert True
    except e:
        assert False