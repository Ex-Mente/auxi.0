# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.financial.tax.rule module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from auxi.modeling.financial.tax.rule import Rule

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
      Tester for the auxi.modeling.financial.tax.rule class.
    """

    def setUp(self):
        self.object = Rule("NameA",
                           description="DescriptionA")

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(Currency)

if __name__ == '__main__':
    unittest.main()
