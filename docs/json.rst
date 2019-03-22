Json
====

This module supports generation of Json data.

.. code-block:: python

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

**Available template functions**

- `random_integer(start, max_expected_value)`
- `random_string_with_special_chars(length_of_expected_string)`
- `random_string_list(size_of_list, length_of_expected_string)`
- `random_string(length_of_expected_string)`
- `random_float(start, max_expected_value, number_of_decimal_places)`
- `random_bool()`
- `now_epoch()`
- `guid()`
- `random_choice_of(list_of_choices)`
- `date_with_format(valid_python_dateformat_string, delta_days)`
   Will return date formatted as format string. use delta days to go forwards
   and backwards from today.
- `random_email_id(length, domain)` Length is inclusive of domain
- `random_ipv4()`
- `random_geo(center: tuple(latitude, longitude), radius_in_meters)`
   center defaults to melbourne and radius to 10000

**Inject Custom template functions**

You can do this, or submit a PR if you think your
function will be useful for others

.. code-block:: python

   from json_genie import generate, generate_with_custom_template_function
   fruit_choices = ['mango', 'apple', 'durian', 'jackfruit']
   def favourite_fruit():
      return random.choice(fruit_choices)

   template = '''
      {
         "k1": {{random_integer(1000)}},
         "k2": "{{favourite_fruit()}}"
      }
   t = Template(template)
   t.globals['favourite_fruit'] = favourite_fruit

   d = json.loads(generate_with_custom_template_function(t))
