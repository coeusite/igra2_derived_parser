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

Using
------------------------------
Using the module should be pretty straightforward. Here's an example:

```
from igra2_derived_parser import IGRA2Parser

# file path to a zip file or a plain text
file_path = 'example/CHM00056187-drvd.txt.zip'

parser = IGRA2Parser()
parser.load(file_path)

# amount of records
print(parser.length)
print(len(parser))

# get the i-th record (i: 0-index)
print(parser.get_header(i))
print(parser.get_data(i))
```

Contact
--------------------------------
For further questions, please open an issue or contact CoeusITE (coeusite@gmail.com)
