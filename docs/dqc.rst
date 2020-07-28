Data Quality Checks
====

This module supports writing data quality checks on pandas dataframe.

.. code-block:: python

   from genie_pkg.dqc import QualityChecker
    check_spec = """
            apply checks {
                row_count > 10
                has_columns(["name", "dob"])
            }
            """
    df = pd.DataFrame([{'name': 'foo',
                        'dob': '1970-01-01'}])

    check_results = df.dqc.run(check_spec)
    failures = list(filter(lambda x: not x[1], check_results))
    assert len(failures) == 0

**Available checks**

- `row_count (> | < | ==) <rhs>`
- `has_columns(["c1", "c2"...])`
- `is_unique(<column_name>)`
- `is_not_null(<column_name>)`
- `has_one_of(<column_name>, ["c1", "c2"...])`
- `is_positive(<column_name>)`
- `quantile(<column_name>, <percentile>) (> | < | ==) <rhs>`
- `is_date(<column_name>)`
- `value_length(<column_name>) == <rhs>` (handy for data like post_code or ipv4)
