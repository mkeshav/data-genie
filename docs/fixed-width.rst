Fixed Width
============

This module supports generation of fixed width data. Mostly needed when dealing with output
from legacy Mainframe systems


.. code-block:: python

   from genie_pkg import fw_genie
   number_of_decimals = 3
   colspecs = [('f1', 4, 'float', 3), ('f2', 3, 'int'), ('f3', 10, 'str'), ('f3', 10, 'date', '%Y/%m/%d')]
   nrows = 10
   encoding = 'windows-1252'
   for d in fw_genie.generate(colspecs, nrows, encoding):
      do_something(d)

Fixed width supports below types

- float (If number of decimal places are not passed, it will default to 2)
- int
- date (Length will be ignored and date will be according to format specified. Make sure it is valid python datetime format)
- str