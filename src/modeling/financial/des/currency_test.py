# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.financial.des.currency module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from auxi.modeling.financial.des.currency import Currency

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
      Tester for the auxi.modeling.financial.des.currency class.
    """

    def setUp(self):
        self.object = Currency("NameA",
                               description="DescriptionA",
                               symbol="R")

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.symbol, "R")


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(Currency)

if __name__ == '__main__':
    unittest.main()
