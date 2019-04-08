from genie_pkg.australia import Australia

def test_state():
    a = Australia()
    assert a.get_state() in ["VIC", "NSW", "ACT", "QLD", "SA", "NT"]