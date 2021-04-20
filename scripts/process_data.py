import csv
from collections import defaultdict
import json

def _process_post_codes():
    d = defaultdict(lambda: defaultdict(dict))
    with open('./scripts/oz_postcodes.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers
        for row in reader:
            state = row[2]
            locality = row[1]
            postcode = row[0]
            latitude = row[4]
            longitude = row[3]
            p = d[state][postcode]
            if latitude != "NULL" and longitude != "NULL":
                center = {
                    "latitude": latitude,
                    "longitude": longitude
                }
                p["center"] = center

            ls = p.get("localities", [])
            ls.append(locality)
            p["localities"] = ls

    for k, v in d.items():
        for k1, _ in v.items():
            ls = d[k][k1]["localities"]
            d[k][k1]["localities"] = list(set(ls))

    return d


if __name__ == "__main__":
    with open('./genie_pkg/data/oz_postcodes.json', 'w') as f:
        json.dump(_process_post_codes(), f, sort_keys=True, indent=4)