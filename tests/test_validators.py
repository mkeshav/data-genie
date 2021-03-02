from genie_pkg.validators import *

import pytest

def test_valid_cc():
    cc = '5218933507687324'
    assert is_valid_cc(cc)
