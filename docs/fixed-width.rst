Fixed Width
============

This module supports generation of fixed width data. Mostly needed when dealing with output
from legacy Mainframe systems


.. code-block:: python

   from genie_pkg import fw_genie
   colspecs = [('f1', 4, 'float'), ('f2', 3, 'int'), ('f3', 10, 'str'), ('f3', 10, 'date', '%Y/%m/%d')]
   nrows = 10
   encoding = 'windows-1252'
   for d in fw_genie.generate(colspecs, nrows, encoding):
      do_something(d)

Fixed width supports below types

- float
- int
- date (Length will be ignored and date will be according to format specified. Make sure it is valid python datetime format)
- str