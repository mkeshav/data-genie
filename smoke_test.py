#!/usr/bin/env python3

from genie_pkg.dqc import QualityChecker
import pandas as pd

if __name__ == '__main__':

    check_spec = """
             apply checks {
                 row_count > 0
                 has_columns(["name", "dob"])
             }
             """
    df = pd.DataFrame([{'name': 'foo',
                        'dob': '1970-01-01'}])

    check_results = df.dqc.run(check_spec)
    failures = list(filter(lambda x: not x[1], check_results))
    if len(failures) > 0:
        raise Exception("WTF!!!")
    else:
        print("everything is awesome...")
