#!/usr/bin/env python3

from genie_pkg.dqc import QualityChecker
from genie_pkg.australia import Australia

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

    # Below line is to remove codacy from saying Quality checker is not used as it does not understand monkey patching
    QualityChecker(df)
    check_results = df.dqc.run(check_spec)
    failures = list(filter(lambda x: not x[2], check_results))
    if len(failures) > 0:
        raise Exception("WTF!!!")
    else:
        a = Australia()
        a.get_random_state()
        print("everything is awesome...")
