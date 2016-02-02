# -*- coding: utf-8 -*-
"""
This module provides testing code for the auxi.modeling.financial.des.transactiontemplate module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from auxi.modeling.financial.des.transactiontemplate import TransactionTemplate

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """Tester for the auxi.modeling.financial.des.transactiontemplate class."""

    def setUp(self):
        self.object = TransactionTemplate("NameA",
                                          description="DescriptionA",
                                          dt_account="Bank",
                                          cr_account="Sales")

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.dt_account, "Bank")
        self.assertEqual(self.object.cr_account, "Sales")


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(TransactionTemplate)

if __name__ == '__main__':
    unittest.main()
