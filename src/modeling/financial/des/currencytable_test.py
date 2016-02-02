# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.financial.des.currencytable module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from auxi.modeling.financial.des.currency import Currency
from auxi.modeling.financial.des.currencytable import CurrencyTable

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
      Tester for the auxi.modeling.financial.des.currencytable class.
    """

    def setUp(self):
        self.default_currency = Currency("ZAR", "South African Rands", "R")
        self.object = CurrencyTable("NameA",
                                    description="DescriptionA",
                                    default_currency=self.default_currency)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.default_currency, self.default_currency)
        self.assertEqual(self.object.table[self.default_currency], "1.0")


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(Currency)

if __name__ == '__main__':
    unittest.main()
