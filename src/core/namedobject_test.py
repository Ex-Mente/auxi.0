# -*- coding: utf-8 -*-
"""
This module provides testing code for the named object module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
import jsonpickle
from auxi.core.namedobject import NamedObject

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """Tester for the auxi.core.Object class."""

    def setUp(self):
        self.object = NamedObject("NameA", "DescriptionA")

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")

    def test__str__(self):
        obj = NamedObject("NameB", "DescriptionB")
        self.assertNotEqual(str(obj), str(self.object))

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
