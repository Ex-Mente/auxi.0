# -*- coding: utf-8 -*-
"""
This module provides testing code for the object module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
import jsonpickle
from auxi.core.object import Object

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """Tester for the auxi.core.Object class."""

    def setUp(self):
        self.object = Object()

    def test___str__(self):
        str_o = str(self.object)
        new_o = jsonpickle.decode(str_o)
        self.assertEqual(str_o, str(new_o))


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(Object)

if __name__ == '__main__':
    unittest.main()
