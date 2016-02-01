# -*- coding: utf-8 -*-
"""
This module provides testing code for the object module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
import os
import numpy
from auxi.core.object import Object

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """Tester for the auxi.core.Object class."""

    def setUp(self):
        self.object = Object()

    def test_constructor(self):
        print(self.object)

        str_o = str(self.object)
        new_o = jsonpickle.decode(str_o)
        print(new_o)
        print(type(new_o))
        #self.assertEqual(self.material.name, "material")
        #self.assertEqual(len(self.material.size_classes), 10)
        #self.assertEqual(self.material.size_class_count, 10)
        #self.assertEqual(len(self.material.assays), 2)



# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

#help(Object)

if __name__ == '__main__':
    unittest.main()
