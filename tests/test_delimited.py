import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../genie_pkg")

import pytest
import random

from delimited_genie import generate,anonymise_columns
import csv

type_choices = ['int', 'float', 'str', 'special_string']

def test_csv():
    # Run all the tests in a loop to have better confidance of randomisation.
    for i in range(2, 5):
        ncols = random.randint(1, 10)
        default_specs = [(random.choice(type_choices), random.randint(5, 15)) for i in range(ncols)]
        colspecs =  default_specs + [('email', 'mail.com'),
                                    ('date', '%d/%m/%Y'),]
        data = generate(colspecs, nrows=1)
        for d in data:
            decoded = d.decode()
            csv_data = list(csv.reader(decoded.splitlines()))[0]
            assert len(csv_data) == len(colspecs)
                

def test_anonymise():
    input_encoding = 'windows-1252'
    row = 'FReNG,£Ni,£iFthtR¥ubOswUPh,mQWJoypv,F¢MFcR'.encode(input_encoding)

    anonymous_col_specs = [(1, 'int'), (4, 'float')]
    anonymised = anonymise_columns(row, anonymous_col_specs, encoding=input_encoding)
    decoded = anonymised.decode(input_encoding)
    csv_data = list(csv.reader(decoded.splitlines()))[0]
    assert isinstance(int(csv_data[1]), int) == True
    assert isinstance(float(csv_data[4]), float) == True