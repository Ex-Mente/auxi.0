# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.financial.des.generalledger module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from datetime import datetime
from auxi.modeling.financial.des.generalledgeraccount import AccountType
from auxi.modeling.financial.des.generalledgerstructure import GeneralLedgerStructure
from auxi.modeling.financial.des.generalledger import GeneralLedger

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
      Tester for the auxi.modeling.financial.des.generalledger class.
    """

    def setUp(self):
        self.structure = GeneralLedgerStructure("NameA",
                                                description="DescriptionA")
        self.structure.create_account("TestA",
                                      description="TestA_Desc",
                                      number="010",
                                      account_type=AccountType.equity)
        self.object = GeneralLedger("NameA",
                                    self.structure,
                                    description="DescriptionA")

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.structure, self.object.structure)

    def test_create_transaction(self):
        new_tx = self.object.create_transaction("TestA",
                                                description="TestA_Desc",
                                                tx_datetime=datetime(2016, 2, 1),
                                                dt_account="Bank",
                                                cr_account="Sales",
                                                source="Peanut Sales",
                                                amount=20.00)

        self.assertEqual(new_tx.name, self.object.transactions[0].name)
        self.assertEqual(new_tx.tx_datetime, self.object.transactions[0].tx_datetime)
        self.assertEqual(new_tx.dt_account, self.object.transactions[0].dt_account)
        self.assertEqual(new_tx.cr_account, self.object.transactions[0].cr_account)
        self.assertEqual(new_tx.source, self.object.transactions[0].source)
        self.assertEqual(new_tx.amount, self.object.transactions[0].amount)


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(TransactionTemplate)

if __name__ == '__main__':
    unittest.main()
