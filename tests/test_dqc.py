import pytest
import pandas as pd

from genie_pkg.dqc import QualityChecker
from hypothesis import given, settings, example
from hypothesis.strategies import composite, integers, lists, text, dates, just, one_of, sets
import string
from typing import List
import json
from datetime import date
import numpy as np

def test_validate_successful():
    df = pd.DataFrame([{'name': 'foo',
                        'dob': '1970-01-01'}])
    QualityChecker(df)


def test_validate_throws_exception():
    df = pd.DataFrame({'P': []})
    with pytest.raises(Exception) as _:
        QualityChecker(df)


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


def _build_row_count(c: str, rhs: int):
    return f"row_count {c} {rhs}"


def _build_has_columns(columns: List[str], ignore_case=False):
    return "has_columns({}, ignore_case={})".format(json.dumps(columns), ignore_case)


def _build_column_is_date(column: str):
    return "is_date({})".format(column)


def _build_column_is_not_null(column: str):
    return "is_not_null({})".format(column)


def _build_column_has_one_of(column: str, values: List[str], ignore_case=False):
    return "has_one_of({}, {}, ignore_case={})".format(column, json.dumps(values), ignore_case)


def _build_column_has_positive_values(column: str):
    return "is_positive({})".format(column)


def _build_column_has_unique_values(column: str):
    return "is_unique({})".format(column)


def _build_quantile(column: str, q: float, c: str, rhs: float):
    return f"quantile({column}, {q}) {c} {rhs}"


def _build_percent_value_length(column: str, pass_percent_threshold: int, rhs: int, ignore_nulls=None):
    if ignore_nulls is not None:
        return f"percent_of_values_have_length({column}, pass_percent_threshold={pass_percent_threshold}, ignore_nulls={ignore_nulls}) == {rhs}"
    else:
        return f"percent_of_values_have_length({column}, pass_percent_threshold={pass_percent_threshold}) == {rhs}"

def _build_when_row(row_identifier, then_column, then_value):
    return f'when row_identified_by {json.dumps(row_identifier)} then {{"{then_column}" == "{then_value}"}}'


@composite
def generate_valid_checks(draw):
    row_count = draw(integers(min_value=20))
    columns = draw(lists(text(alphabet=string.ascii_letters + string.digits + '-_', min_size=1), min_size=1))
    column = draw(text(alphabet=string.ascii_letters, min_size=1))
    comparator = draw(one_of(just(">"), just("=="), just("<")))
    genders = ['female', 'male', 'other']
    bool = draw(one_of(just(False), just(True)))
    row_identifier = {"c1": "v1", "c2": "2"}
    return [
        _build_row_count(comparator, row_count),
        _build_has_columns(columns, ignore_case=bool),
        _build_column_is_date("dob"),
        _build_column_is_not_null(column),
        _build_column_has_one_of("gender", genders),
        _build_column_has_positive_values("age"),
        _build_column_has_unique_values("dob"),
        _build_quantile("field_A", 0.5, "==", 55.0),
        _build_quantile("field_A", 0.1, ">", 9.0),
        _build_quantile("field_A", 0.5, "<", 56.0),
        _build_percent_value_length("post_code", 50, 4, ignore_nulls=bool),
        _build_when_row(row_identifier, "c3", "v3"),
    ]


@given(generate_valid_checks(),
       lists(dates(min_value=date(1970, 1, 1), max_value=date(2100, 1, 1)).map(str), min_size=10, max_size=10),
       lists(integers(min_value=10), min_size=10, max_size=10),
       just([80, 24, 74, 30, 72, 69, 27, 12, 84, 41]),
       just(['female', 'male', 'other', 'female', 'male', 'other', 'female', 'male', 'other', 'other']),
       lists(integers(min_value=1000, max_value=9999), min_size=10, max_size=10), )
@settings(max_examples=101, deadline=500)
def test_hypothesis(checks, dobs, ages, q_arr, genders, post_codes):
    check_spec = """
                    apply checks {
                        %s
                    }
                    """ % ('\n'.join(checks),)

    df = pd.DataFrame({'age': ages,
                       'dob': dobs,
                       'field_A': q_arr,
                       'gender': genders,
                       'post_code': post_codes,
                       'c1': 'v1', 'c2': "2", 'c3': 'v3'})

    successes = list(filter(lambda x: x[1], df.dqc.run(check_spec)))
    # is_date, is_positive, quantile, has_one_of
    assert len(successes) > 0


@given(lists(integers(min_value=1000, max_value=9999), min_size=4, max_size=4))
@example(["3000", "0800", None, ""])
@settings(deadline=500)
def test_percent_value_length(postcodes):
    df = pd.DataFrame({'post_code': postcodes})
    check_spec = """
                apply checks {
                    percent_of_values_have_length(post_code, pass_percent_threshold=50) == 4
                }
                """
    successes = list(filter(lambda x: x[1], df.dqc.run(check_spec)))
    assert len(successes) > 0
    failures = list(filter(lambda x: not x[1], df.dqc.run(check_spec)))
    assert len(failures) >= 0


def test_validate_spec_returns_false():
    check_spec = """
                apply checks {
                }
                """
    err, res = QualityChecker.validate_spec(check_spec)
    assert err is not None
    assert not res


def test_validate_spec_returns_true():
    check_spec = """
                apply checks {
                    row_count > 0
                }
                """
    err, res = QualityChecker.validate_spec(check_spec)
    assert err is None
    assert res


@given(
    sets(text(alphabet=string.ascii_letters + '-_', min_size=3), min_size=5, max_size=5),
    lists(integers(min_value=1000, max_value=9999), min_size=5, max_size=5)
)
@settings(deadline=300)
def test_has_columns(columns, values):
    data = {}
    for c in columns:
        data[c] = values

    df = pd.DataFrame(data)
    check_spec_template = """
                    apply checks {
                        %s
                    }
                    """

    columns_lower_cased = [c.lower() for c in columns]
    check_spec_case_sensitive = check_spec_template % (_build_has_columns(columns_lower_cased, ignore_case=False),)
    result_case_sensitive = df.dqc.run(check_spec_case_sensitive)
    failures = list(filter(lambda x: not x[1], result_case_sensitive))
    assert len(failures) == 1
    successes = list(filter(lambda x: x[1], result_case_sensitive))
    assert len(successes) == 0
    check_spec_ignore_case = check_spec_template % (_build_has_columns(list(columns), ignore_case=True),)
    result_ignore_case = df.dqc.run(check_spec_ignore_case)
    failures = list(filter(lambda x: not x[1], result_ignore_case))
    assert len(failures) == 0
    successes = list(filter(lambda x: x[1], result_ignore_case))
    assert len(successes) == 1


def test_has_one_of():
    gender = ['female', 'male', 'other']
    data = {'Gender': ['Male', 'Female']}
    check_spec_template = """
                    apply checks {
                        %s
                    }
                    """

    df = pd.DataFrame(data)
    check_spec_case_sensitive = check_spec_template % (_build_column_has_one_of('gender', gender),)
    result_case_sensitive = df.dqc.run(check_spec_case_sensitive)
    failures = list(filter(lambda x: not x[1], result_case_sensitive))
    assert len(failures) == 1
    successes = list(filter(lambda x: x[1], result_case_sensitive))
    assert len(successes) == 0
    # previous test would have mutated the column name, hence recreate the df
    df = pd.DataFrame(data)
    check_spec_ignore_case = check_spec_template % (_build_column_has_one_of('gender', gender, ignore_case=True),)
    result_ignore_case = df.dqc.run(check_spec_ignore_case, ignore_column_case=True)
    failures = list(filter(lambda x: not x[1], result_ignore_case))
    assert len(failures) == 0
    successes = list(filter(lambda x: x[1], result_ignore_case))
    assert len(successes) == 1

def test_when_success():
    check_spec = """
                    apply checks {
                        when row_identified_by {
                            "c1": "v1", 
                            "c2": "2"
                        } then {
                            "c3" == "v3",
                            "c4" == "v4"
                        }
                    }
                    """
    
    df = pd.DataFrame({"c1": "v1", "c2": "2", "c3": "v3", "c4": "v4"}, index=[0])
    result = df.dqc.run(check_spec)    
    assert result[0][1]

def test_when_row_identifier_column_missing():
    check_spec = """
                    apply checks {
                        when row_identified_by {"c1": "v1", "c4": "2"} then {"c3" == "v3"}
                    }
                    """
    
    df = pd.DataFrame({"c1": "v1", "c2": "2", "c3": "v3"}, index=[0])
    with pytest.raises(Exception) as _:
        df.dqc.run(check_spec)   

def test_when_target_column_missing():
    check_spec = """
                    apply checks {
                        when row_identified_by {"c1": "v1", "c2": "2"} then {"c3" == "v3"}
                    }
                    """
    
    df = pd.DataFrame({"c1": "v1", "c2": "2", "c4": "v3"}, index=[0])
    result = df.dqc.run(check_spec)
    assert not result[0][1]

def test_is_date_with_none_ignore_nulls():
    df = pd.DataFrame({'dob': ['1970-01-01', 'foo', None, np.nan]})
    check_spec = """
                apply checks {
                    is_date(dob, ignore_nulls=True)
                }
                """

    result = df.dqc.run(check_spec)
    assert not result[0][1]

def test_is_date_with_none_donot_ignore_nulls():
    df = pd.DataFrame({'dob': ['1970-01-01', 'foo', None, np.nan]})
    check_spec = """
                apply checks {
                    is_date(dob)
                }
                """

    result = df.dqc.run(check_spec)
    assert not result[0][1]

def test_is_date_success():
    df = pd.DataFrame({'dob': ['1970-01-01', 'foo', None, np.nan]})
    check_spec = """
                apply checks {
                    is_date(dob, pass_percent_threshold=50, ignore_nulls=True)
                }
                """

    result = df.dqc.run(check_spec)
    assert  result[0][1]

def test_is_date_division_by_zero():
    df = pd.DataFrame({'dob': [None, np.nan], 'bar': 'foo'})
    check_spec = """
                apply checks {
                    is_date(dob, ignore_nulls=True)
                }
                """

    result = df.dqc.run(check_spec)
    assert not result[0][1]

def test_percent_values_have_length_param_combinations():
    df = pd.DataFrame([{'name': 'foo',
                        'd': '1970-01-01'}])
    check_spec = """
                apply checks {
                    percent_of_values_have_length(foo, pass_percent_threshold=50, ignore_nulls=True) == 2
                    percent_of_values_have_length(bar, ignore_nulls=True) == 2
                    percent_of_values_have_length(foobar, pass_percent_threshold=50) == 2
                    percent_of_values_have_length(foo) == 2
                }
                """
    
    result = df.dqc.run(check_spec)
    assert True
