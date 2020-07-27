import pytest
import pandas as pd

from genie_pkg.dqc import QualityChecker

def test_validate_successful():
    df = pd.DataFrame([{'name': 'foo',
                       'dob': '1970-01-01'}])
    QualityChecker(df)

def test_validate_throws_exception():
    df = pd.DataFrame({'P' : []})
    with pytest.raises(Exception) as _:
        QualityChecker(df)


def test_run_success():
    check_spec = """
            apply checks {
                size is 1
                has columns ['name', 'dob']
                column dob has unique values
                column product is not null
                column age has positive values
                column gender in ['male', 'female', 'other']
                column dob is date
            }
            """
    df = pd.DataFrame([{'name': 'foo',
                        'dob': '1970-01-01',
                        'product': "mask",
                        'age': 1, 'gender': 'male'}])

    _assert_success(df.dqc.run(check_spec))

def test_columns_missing():
    check_spec = """
                apply checks {
                    has columns ['foo', 'bar']
                    column dob has unique values
                }
                """
    df = pd.DataFrame([{'name': 'foo',
                        'd': '1970-01-01'}])

    check_results = df.dqc.run(check_spec)
    failures = list(filter(lambda x: not x[1], check_results))
    assert len(failures) == 2

def test_quantile():
    a = [80, 24, 74, 30, 72, 69, 27, 12, 84, 41]
    b = [62, 8, 42, 59, 10, 28, 46, 65, 100, 40]

    df = pd.DataFrame({'field_A': a, 'field_B': b})

    check_spec = """
                apply checks {
                    column field_A quantile(0.5) == 55.0
                    column field_B quantile(0.1)>9.0
                    column field_A quantile(0.5) < 56.0
                }
                """
    _assert_success(df.dqc.run(check_spec))

def test_parse_error():
    df = pd.DataFrame([{'name': 'foo',
                        'd': '1970-01-01'}])
    check_spec = """
                apply checks {
                    foo
                }
                """

    with pytest.raises(Exception) as _:
        df.dqc.run(check_spec)

def _assert_success(results):
    failures = list(filter(lambda x: not x[1], results))
    assert len(failures) == 0
