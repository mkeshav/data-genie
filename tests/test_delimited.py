import sys
import os

import pytest
import random

from genie_pkg.delimited_genie import generate, anonymise_columns
import csv
import math

type_choices = ['int', 'float', 'str', 'special_string']


def test_csv():
    # Run all the tests in a loop to have better confidance of randomisation.
    for i in range(2, 5):
        ncols = random.randint(1, 10)
        default_specs = [(random.choice(type_choices),
                          random.randint(5, 15)) for i in range(ncols)]
        colspecs = default_specs + [('email', 15, 'mail.com'),
                                    ('date', '%d/%m/%Y', 3), 
                                    ('cc_mastercard',),
                                    ('geo_coord', (40.84, -73.87,),)]
        delimiter=random.choice([',', '|'])
        data = generate(colspecs, nrows=1, delimiter=delimiter)
        for d in data:
            decoded = d.decode()
            csv_data = list(csv.reader(decoded.splitlines(), delimiter=delimiter))[0]
            assert len(csv_data) == len(colspecs) + 1 # +1 is because geo_coord will produce 2 values


def test_anonymise():
    input_encoding = 'windows-1252' 
    row = 'FReNG,£Ni,£iFthtR¥ubOswUPh,mQWJoypv,F¢MFcR,-37.814,144.963'.encode(input_encoding)

    anonymous_col_specs = [(1, 'float'), (4, 'int'), (5, 'geo_coord', (40.84, -73.87,), 1000)]
    anonymised = anonymise_columns(
        row, anonymous_col_specs, encoding=input_encoding)
    decoded = anonymised.decode(input_encoding)
    csv_data = list(csv.reader(decoded.splitlines()))[0]
    assert isinstance(int(csv_data[4]), int) == True
    assert isinstance(float(csv_data[1]), float) == True
    assert math.isclose(float(csv_data[5]), 40.84, abs_tol=0.010)