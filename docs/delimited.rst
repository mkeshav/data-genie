Delimited (CSV)
===============

This module supports generation of delimited data.

To generate completely random data

.. code-block:: python

   from genie_pkg import delimited_genie
   [('special_string', 13), ('int', 15), ('float', 7), ('float', 8), ('str', 9), ('str', 5), ('int', 5)]
   nrows = 10
   encoding = 'windows-1252'
   for d in delimited_genie.generate(colspecs, nrows, encoding):
      do_something(d)

If you want to just anonymise some parts of your
csv data (Say to remove piis etc)

.. code-block:: python

   from genie_pkg import delimited_genie
   input_encoding = 'utf-8'
   row = 'FReNG,£Ni,£iFthtR¥ubOswUPh,mQWJoypv,F¢MFcR'.encode(input_encoding)

   anonymous_col_specs = [(1, 'int'), (4, 'float')]
   anonymised = delimited_genie.anonymise_columns(row, anonymous_col_specs, encoding=input_encoding)
   do_something(anonymised)

CSV supports below types

- float (If number of decimal places are not passed, it will default to 2).
- int
- str
- special_string (With special characters)
- email (length, optional_domain) if domain is not passed,
      it will default to dummy.com.
      (*Length is inclusive of domain you specify.*)
- date (Make sure format is valid python datetime format.
      Optional delta days to go back or in future)
- geo_coord (center:tuple(lat,lng), radius_in_meters, accuracy_digits)
  center defaults to melbourne, radius = 10000 and accuracy_digits=3
- cc_mastercard (generates 16 digit valid mastercard number)
- cc_visacard (length) (length can be 16 or 13) (generates 16 digit by default)
