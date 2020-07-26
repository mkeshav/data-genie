Data Quality Checks
====

This module supports writing data quality checks on pandas dataframe.

.. code-block:: python

   from genie_pkg.dqc import QualityChecker
    check_spec = """
            apply checks {
                size is 1
                has columns ['name', 'dob']
                column dob has unique values
                column product is not null
            }
            """
    df = pd.DataFrame([{'name': 'foo',
                        'dob': '1970-01-01'}])

    check_results = df.dqc.run(check_spec)
    failures = list(filter(lambda x: not x[1], check_results))
    assert len(failures) == 0

**Available checks**

- `size is <number>`
- `has columns ['c1', 'c2'...]`
- `column <column_name> has unique values`
- `column <column_name> is not null`
- `column <column_name> in ['c1', 'c2'...]`
- `column <column_name> has positive values`
- `column <column_name> quantile(<percentile>) (> | < | ==) <rhs>`
