Parser Library for NOAA IGRA2 Derived Files (for Python 3.5)
--------------------------------

Installing
-------------------------------
If you're a python and pip user, you can install the current development version with:

```
sudo pip install git+https://github.com/coeusite/igra2_derived_parser.git
```

or install it locally with:

```
pip install --user git+https://github.com/coeusite/igra2_derived_parser.git
```

To upgrade the parser:
```
pip install --user --force-reinstall --upgrade git+https://github.com/coeusite/igra2_derived_parser.git
```

Dependency
------------------------------
This module depends on:
* pandas (0.18.1)
* numpy (1.11.1)

Please update these packages to the latest edition.


Using
------------------------------
Using the module should be pretty straightforward. Here's an example:

```
from igra2_derived_parser import IGRA2Parser

# file path to a zip file or a plain text
file_path = 'examples/CHM00056187-drvd.txt.zip'

igra2_drvd_parser = IGRA2Parser()
igra2_drvd_parser.load(file_path)

# amount of records
print(igra2_drvd_parser.length)
print(len(igra2_drvd_parser))

# get the i-th record, where i is zero-indexed.
print(igra2_drvd_parser.get_header(i))
print(igra2_drvd_parser.get_data(i))

# get dew point for the i-th record
print(igra2_drvd_parser.get_dew_point(i))

# you can access the data directly by:
igra2_drvd_parser._data[i]
igra2_drvd_parser._header.loc[i, :]
```

Developing
--------------------------------
Testing scripts have not been implemented yet.


Contact
--------------------------------
For further questions, please open an issue or contact CoeusITE (coeusite@gmail.com)
