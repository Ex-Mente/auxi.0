# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.financial.tax.ruleset module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from auxi.modeling.financial.tax.ruleset import RuleSet

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
      Tester for the auxi.modeling.financial.tax.ruleset class.
    """

    def setUp(self):
        self.object = RuleSet("NameA",
                              description="DescriptionA",
                              code="ZA")

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.code, "ZA")


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(Currency)

if __name__ == '__main__':
    unittest.main()
