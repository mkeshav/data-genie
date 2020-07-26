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
            }
            """
    df = pd.DataFrame([{'name': 'foo',
                        'dob': '1970-01-01',
                        'product': "mask",
                        'age': 1, 'gender': 'male'}])

    check_results = df.dqc.run(check_spec)
    failures = list(filter(lambda x: not x[1], check_results))
    assert len(failures) == 0

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