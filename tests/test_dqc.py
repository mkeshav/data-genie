import pytest
import pandas as pd

from genie_pkg.dqc import QualityChecker
from hypothesis import given, settings
from hypothesis.strategies import composite, integers, lists, text, dates, just, one_of
import string
from typing import List
import json
from datetime import date


def test_validate_successful():
    df = pd.DataFrame([{'name': 'foo',
                       'dob': '1970-01-01'}])
    QualityChecker(df)


def test_validate_throws_exception():
    df = pd.DataFrame({'P' : []})
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


def test_date_validation_error_returns_false():
    df = pd.DataFrame([{'dob': 'foo'}])
    check_spec = """
                apply checks {
                    is_date(dob)
                }
                """

    failures = list(filter(lambda x: not x[1], df.dqc.run(check_spec)))
    assert len(failures) == 1


def _build_row_count(c:str, rhs: int):
    return f"row_count {c} {rhs}"


def _build_has_columns(columns: List[str]):
    return "has_columns({})".format(json.dumps(columns))


def _build_column_is_date(column: str):
    return "is_date({})".format(column)


def _build_column_is_not_null(column: str):
    return "is_not_null({})".format(column)


def _build_column_has_one_of(column: str, values: List[str]):
    return "has_one_of({}, {})".format(column, json.dumps(values))


def _build_column_has_positive_values(column: str):
    return "is_positive({})".format(column)


def _build_column_has_unique_values(column: str):
    return "is_unique({})".format(column)


def _build_quantile(column: str, q:float, c:str, rhs:float):
    return f"quantile({column}, {q}) {c} {rhs}"


def _build_value_length(column: str, rhs: int, ignore_nulls=None):
    if ignore_nulls is not None:
        return f"value_length({column}, ignore_nulls={ignore_nulls}) == {rhs}"
    else:
        return f"value_length({column}) == {rhs}"


def _build_percent_value_length(column: str, pass_percent_threshold: int, rhs: int, ignore_nulls=None):
    if ignore_nulls is not None:
        return f"percent_of_values_have_length({column}, pass_percent_threshold={pass_percent_threshold}, ignore_nulls={ignore_nulls}) == {rhs}"
    else:
        return f"percent_of_values_have_length({column}, pass_percent_threshold={pass_percent_threshold}) == {rhs}"

@composite
def generate_valid_checks(draw):
    row_count = draw(integers(min_value=20))
    columns = draw(lists(text(alphabet=string.ascii_letters+string.digits+'-_', min_size=1), min_size=1))
    column = draw(text(alphabet=string.ascii_letters, min_size=1))
    comparator = draw(one_of(just(">"), just("=="), just("<")))
    genders = ['female', 'male', 'other']
    bool = draw(one_of(just(False), just(True)))
    return [
        _build_row_count(comparator, row_count),
        _build_has_columns(columns),
        _build_column_is_date("dob"),
        _build_column_is_not_null(column),
        _build_column_has_one_of("gender", genders),
        _build_column_has_positive_values("age"),
        _build_column_has_unique_values("dob"),
        _build_quantile("field_A", 0.5, "==", 55.0),
        _build_quantile("field_A", 0.1, ">", 9.0),
        _build_quantile("field_A", 0.5, "<", 56.0),
        _build_value_length("post_code", 4),
        _build_value_length("post_code", 4, ignore_nulls=bool),
        _build_percent_value_length("post_code", 50, 4, ignore_nulls=bool),
    ]


@given(generate_valid_checks(),
       lists(dates(min_value=date(1970, 1, 1), max_value=date(2100, 1, 1)).map(str), min_size=10, max_size=10),
       lists(integers(min_value=10), min_size=10, max_size=10),
       just([80, 24, 74, 30, 72, 69, 27, 12, 84, 41]),
       just(['female', 'male', 'other', 'female', 'male', 'other', 'female', 'male', 'other', 'other']),
       lists(integers(min_value=1000, max_value=9999), min_size=10, max_size=10),)
@settings(max_examples=101)
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
                       'post_code': post_codes})

    successes = list(filter(lambda x: x[1], df.dqc.run(check_spec)))
    #is_date, is_positive, quantile, has_one_of
    assert len(successes) > 0


def test_value_length():
    df = pd.DataFrame({'post_code': ["3000", "0800", None, ""]})
    check_spec = """
                apply checks {
                    value_length(post_code, ignore_nulls=True) == 4
                    value_length(post_code, ignore_nulls=False) == 4
                    percent_of_values_have_length(post_code, pass_percent_threshold=50) == 4
                }
                """
    successes = list(filter(lambda x: x[1], df.dqc.run(check_spec)))
    assert len(successes) == 2
    failures = list(filter(lambda x: not x[1], df.dqc.run(check_spec)))
    assert len(failures) == 1
