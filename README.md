[![PyPI version](https://badge.fury.io/py/data-genie-mkeshav.svg)](https://badge.fury.io/py/data-genie-mkeshav)
[![CircleCI](https://circleci.com/bb/mkeshav/data_genie.svg?style=svg)](https://circleci.com/bb/mkeshav/data_genie)

# Data Genie

Genie that can satisfy your data wish.
Supports generation of fixedwidth content (as of this writing.)

# Install
python3 -m pip install data-genie-mkeshav

# Usage (Fixed Width)
```
from genie_pkg import fw_genie
colspecs = [('f1', 4, 'float'), ('f2', 3, 'int'), ('f3', 10, 'str')]
nrows = 10
encoding = 'windows-1252'
for d in fw_genie.generate(colspecs, nrows, encoding):
    do_something(d)
```

# Usage (Json)
One json object (nested if necessary)

```
from genie_pkg import json_genie
template = '''
        {
            "k1": {{random_integer(1000)}},
            "k2": "{{random_string_with_special_chars(5)}}",
            "k3": {{random_string_list(2, 8)}},
            "k4": {{random_float(100, 2)}},
            "k5": {{random_bool()}},
            "k6": {{now_epoch()}},
            "k7": "{{random_string(5)}}",
            "k8": [
                {
                    "y1": {{random_integer(1000)}}
                },
                {
                    "y1": {{random_integer(1000)}}
                }
            ],
            "k9": {{random_integer_list(2, 100)}}
        }
    '''
d = json.loads(json_genie.generate(template))
do_something(d)
```

To Create a list of json objects
```
entries = []
for i in range(0, n):
    entries.insert(0, json.loads(json_genie.generate(template)))
        
json.dumps(entries)
```
Available template functions

- `random_integer(max_expected_value)`
- `random_string_with_special_chars(length_of_expected_string)`
- `random_string_list(size_of_list, length_of_expected_string)`
- `random_string(length_of_expected_string)`
- `random_float(max_expected_value, number_of_decimal_places)`
- `random_bool()`
- `now_epoch()`

## Inject Custom template functions
```
from json_genie import generate, generate_with_custom_template_function
fruit_choices = ['mango', 'apple', 'durian', 'jackfruit']
def favourite_fruit():
    return random.choice(fruit_choices)

template = '''
    {
        "k1": {{random_integer(1000)}},
        "k2": "{{favourite_fruit()}}"
    }
'''

t = Template(template)
t.globals['favourite_fruit'] = favourite_fruit

d = json.loads(generate_with_custom_template_function(t))
```