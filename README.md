# Data Genie

Genie that can satisfy your data wish

# Install
python3 -m pip install data-genie-mkeshav

# Usage
```
from genie_pkg import fw
colspecs = [('f1', 4, 'float'), ('f2', 3, 'int'), ('f3', 10, 'str')]
nrows = 10
encoding = 'windows-1252'
fw.generate(colspecs, nrows, encoding)
```