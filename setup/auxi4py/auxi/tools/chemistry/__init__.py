"""auxi for Python Package

The purpose of this package is to make auxi's chemistry tools
available through a series of Python modules for easy access and use.

Python version:  3.4.0
auxi version: 0.1.0"""

__version__ = "0.1.0"

import os
import sys
from auxi.tools.chemistry import thermochemistry

module_path = os.path.dirname(sys.modules[__name__].__file__)
data_path = os.path.join(module_path, r"data")
#print(data_path)

thermochemistry.set_default_data_path(data_path)
#print(thermochemistry.get_data_file_path())
thermochemistry.load_data()
