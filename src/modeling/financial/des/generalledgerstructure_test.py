# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.financial.generalledgerstructure module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from auxi.modeling.financial.des.generalledgeraccount import AccountType
from auxi.modeling.financial.des.generalledgerstructure import GeneralLedgerStructure

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
      Tester for the auxi.modeling.financial.des.generalledgerstructure class.
    """

    def setUp(self):
        self.object = GeneralLedgerStructure("NameA",
                                             description="DescriptionA")

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.accounts[0].name, "Bank")
        self.assertEqual(self.accounts[0].account_type, AccountType.asset)
        self.assertEqual(self.accounts[0].name, "IncomeTaxPayable")
        self.assertEqual(self.accounts[0].account_type, AccountType.liability)
        self.assertEqual(self.accounts[0].name, "IncomeTaxExpense")
        self.assertEqual(self.accounts[0].account_type, AccountType.expense)
        self.assertEqual(self.accounts[0].name, "Sales")
        self.assertEqual(self.accounts[0].account_type, AccountType.revenue)
        self.assertEqual(self.accounts[0].name, "CostOfSales")
        self.assertEqual(self.accounts[0].account_type, AccountType.expense)
        self.assertEqual(self.accounts[0].name, "GrossProfit")
        self.assertEqual(self.accounts[0].account_type, AccountType.revenue)
        self.assertEqual(self.accounts[0].name, "IncomeSummary")
        self.assertEqual(self.accounts[0].account_type, AccountType.revenue)
        self.assertEqual(self.accounts[0].name, "RetainedEarnings")
        self.assertEqual(self.accounts[0].account_type, AccountType.equity)
        self.assertEqual(self.m_taxPaymentAccount, None)

    def test_create_account(self):
        new_acc = self.object.create_account("TestA",
                                             description="TestA_Desc",
                                             number="011",
                                             account_type=AccountType.equity)
        self.assertEqual(new_acc.name, "TestA")
        self.assertEqual(new_acc.description, "TestA_Desc")
        self.assertEqual(new_acc.number, "011")
        self.assertEqual(new_acc.account_type, AccountType.equity)

        self.assertEqual(new_acc, self.object.accounts[0])

    def test_remove_account(self):
        self.object.create_account("TestA",
                                   description="TestA_Desc",
                                   number="011",
                                   account_type=AccountType.equity)
        self.object.remove_account("TestA")
        self.assertEqual(len(self.object.accounts), 0)

    def test_get_account(self):
        self.object.create_account("TestA",
                                   description="TestA_Desc",
                                   number="010",
                                   account_type=AccountType.equity)
        acc = self.object.create_account("TestB",
                                         description="TestB_Desc",
                                         number="020",
                                         account_type=AccountType.asset)
        sub_acc = acc.create_account("TestB1",
                                     description="TestB1_Desc",
                                     number="010")
        sub_acc.create_account("TestB1.1",
                               description="TestB1.1_Desc",
                               number="010")
        orig = sub_acc.create_account("TestB1.2",
                                      description="TestB1.1_Desc",
                                      number="011")
        result = self.object.get_account("TestB1.2")

        self.assertEqual(result, orig)


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(TransactionTemplate)

if __name__ == '__main__':
    unittest.main()
