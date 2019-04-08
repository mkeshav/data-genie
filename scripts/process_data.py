import csv
from collections import defaultdict
import json

def _process_post_codes():
    d = defaultdict(lambda: defaultdict(list))
    with open('./scripts/oz_postcodes.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers
        for row in reader:
            state = row[2]
            locality = row[1]
            postcode = row[0]
            d[state][postcode].append(locality)

    for k, v in d.items():
        for k1, v1 in v.items():
            d[k][k1] = list(set(v1))
    
    return d


if __name__ == "__main__":
    with open('./genie_pkg/data/oz_postcodes.json', 'w') as f:        
        json.dump(_process_post_codes(), f, sort_keys=True, indent=4)