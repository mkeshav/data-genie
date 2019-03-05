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
```
from genie_pkg import json_genie
template = '''
        {
            "id": {{random_integer(1000)}},
            "k2": "{{random_string_with_special_chars(5)}}",
            "k3": {{random_string_list(2, 8)}}
        }
    '''
d = json.loads(json_genie.generate(template))
do_something(d)
```

Available template functions
- `random_integer(max_expected_value)`
- `random_string_with_special_chars(length_of_expected_string)`
- `random_string_list(size_of_list, length_of_expected_string)`