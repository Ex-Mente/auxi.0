#!/usr/bin/env python3
"""
This module provides testing code for the
auxi.modelling.financial.currencies module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from auxi.modelling.financial.currency import Currency, CurrencyTable

__version__ = '0.2.0rc4'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


# =============================================================================
# Types.
# =============================================================================

class CurrencyUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.currencies.Currency class.
    """

    def setUp(self):
        self.object = Currency("NameA",
                               description="DescriptionA",
                               symbol="R")

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.symbol, "R")


class CurrencyTableUnitTester(unittest.TestCase):
    """
      Tester for the auxi.modelling.financial.des.currencytable class.
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
# help(CurrencyTable)

if __name__ == '__main__':
    unittest.main()
