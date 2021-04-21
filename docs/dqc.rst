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

    # if you pass ignore_column_case=True, column names in dataframe will be case insensitive
    check_results = df.dqc.run(check_spec, ignore_column_case=False(default))
    failures = list(filter(lambda x: not x[1], check_results))
    assert len(failures) == 0

    # To check if your spec is valid or not. If it is bad, will return (error, False) else (None, True)
    QualityChecker.validate_spec(check_spec)


**Available simple checks**

- `row_count (> | < | ==) <rhs>`
- `has_columns(["c1", "c2"...], ignore_case=False|True default is False)`
- `is_unique(<column_name>)`
- `is_not_null(<column_name>)`
- `has_one_of(<column_name>, ["c1", "c2"...], ignore_case=False|True default is False))`
- `is_positive(<column_name>)`
- `quantile(<column_name>, <percentile>) (> | < | ==) <rhs>`
- `is_date(<column_name>, pass_percent_threshold=<1..100> default 100, ignore_nulls=False|True default is False)`
- `percent_of_values_have_length(<column_name>, pass_percent_threshold=<1..100> default 100, ignore_nulls=False|True default is False) == <rhs>` (handy for data like post_code or ipv4)


**Available complex checks**

- Apply checks on multiple columns of rows identified by the condition (supports strings only)

.. code-block:: python

    # Check column values using row identification. c1, c2, c3 and c4 are column names
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

    df = pd.DataFrame({"c1": "v1", "c2": "2", "c3": "v3"}, index=[0])
    # Returns [(check_name, None|column_name, True|False)]
    result = df.dqc.run(check_spec)
