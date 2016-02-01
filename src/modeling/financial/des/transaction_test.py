# -*- coding: utf-8 -*-
"""
This module provides testing code for the auxi.modeling.financial.transactiontemplate module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from datetime import datetime
from auxi.modeling.financial.des.transaction import Transaction

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """Tester for the auxi.modeling.financial.des.transaction class."""

    def setUp(self):
        self.object = Transaction("NameA",
                                  description="DescriptionA",
                                  tx_datetime=datetime(2016, 2, 1),
                                  dt_account="Bank",
                                  cr_account="Sales",
                                  source="PigeonSales",
                                  amount=100.00)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.dt_account, "Bank")
        self.assertEqual(self.object.tx_datetime, datetime(2016, 2, 1))
        self.assertEqual(self.object.cr_account, "Sales")
        self.assertEqual(self.object.source, "PigeonSales")
        self.assertEqual(self.object.is_closing_cr_account, False)
        self.assertEqual(self.object.is_closing_dt_account, False)
        self.assertEqual(self.object.amount, 100.0)


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(TransactionTemplate)

if __name__ == '__main__':
    unittest.main()
