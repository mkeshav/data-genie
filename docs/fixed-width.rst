Fixed Width
============

This module supports generation of fixed width data.Mostly needed when
dealing with output from legacy Mainframe systems


To generate completely random data

.. code-block:: python

   from genie_pkg import fw_genie
   number_of_decimals = 3
   colspecs = [
         (5, 'float', 3), (3, 'int'), (10, 'str'),
         (10, 'date', '%Y/%m/%d'),
         (15, 'email', 'mail.com'),
         (10, 'myval', 'returnasis')
      ]
   nrows = 10
   encoding = 'windows-1252'
   for d in fw_genie.generate(colspecs, nrows, encoding):
      do_something(d)

If you want to just anonymise some parts of your fixed
width data (Say to remove piis etc)

.. code-block:: python

   from genie_pkg import fw_genie
   input_encoding = 'utf-8'
   row = 'FReNG£Ni£iFthtR¥ubOswUPhmQWJoypvF¢MFcR'.encode(input_encoding)

   cols_anonymise_specs = [(0, 5, 'int'), (28, 38, 'float')]
   anonymised = fw_genie.anonymise_columns(row,  anonymous_col_specs=cols_anonymise_specs, encoding=input_encoding)
   do_something(anonymised)

Fixed width supports below types

- float (If number of decimal places are not passed, it will default to 2).
      *Length is inclusive of decimal places.*
- int
- date (Make sure format is valid python datetime format.
      If the length passed does not match what the format produces,
      exception will be raised.)
- str
- email (if domain is not passed, it will default to dummy.com).
      *Length is inclusive of domain you specify.*
- myval (value that you just want to return as is)
