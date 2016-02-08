# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.financial.des.generalledgerstructure module.

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
        self.assertEqual(self.object.accounts[0].name, "Bank")
        self.assertEqual(self.object.accounts[0].account_type,
                         AccountType.asset)
        self.assertEqual(self.object.accounts[1].name, "IncomeTaxPayable")
        self.assertEqual(self.object.accounts[1],
                         self.object.incometaxpayable_account)
        self.assertEqual(self.object.accounts[1].account_type,
                         AccountType.liability)
        self.assertEqual(self.object.accounts[2].name, "IncomeTaxExpense")
        self.assertEqual(self.object.accounts[2],
                         self.object.incometaxexpense_account)
        self.assertEqual(self.object.accounts[2].account_type,
                         AccountType.expense)
        self.assertEqual(self.object.accounts[3].name, "Sales")
        self.assertEqual(self.object.accounts[3],
                         self.object.sales_account)
        self.assertEqual(self.object.accounts[3].account_type,
                         AccountType.revenue)
        self.assertEqual(self.object.accounts[4].name, "CostOfSales")
        self.assertEqual(self.object.accounts[4],
                         self.object.costofsales_account)
        self.assertEqual(self.object.accounts[4].account_type,
                         AccountType.expense)
        self.assertEqual(self.object.accounts[5].name, "GrossProfit")
        self.assertEqual(self.object.accounts[5],
                         self.object.gross_profit_account)
        self.assertEqual(self.object.accounts[5].account_type,
                         AccountType.revenue)
        self.assertEqual(self.object.accounts[6].name, "IncomeSummary")
        self.assertEqual(self.object.accounts[6],
                         self.object.incomesummary_account)
        self.assertEqual(self.object.accounts[6].account_type,
                         AccountType.revenue)
        self.assertEqual(self.object.accounts[7].name, "RetainedEarnings")
        self.assertEqual(self.object.accounts[7],
                         self.object.retainedearnings_account)
        self.assertEqual(self.object.accounts[7].account_type,
                         AccountType.equity)
        self.assertEqual(self.object.tax_payment_account, "Bank")

    def test_create_account(self):
        orig_length = len(self.object.accounts)
        new_acc = self.object.create_account("TestA",
                                             description="TestA_Desc",
                                             number="011",
                                             account_type=AccountType.equity)
        self.assertEqual(new_acc.name, "TestA")
        self.assertEqual(new_acc.description, "TestA_Desc")
        self.assertEqual(new_acc.number, "011")
        self.assertEqual(new_acc.account_type, AccountType.equity)

        self.assertEqual(new_acc, self.object.accounts[orig_length])

    def test_remove_account(self):
        orig_length = len(self.object.accounts)
        self.object.create_account("TestA",
                                   description="TestA_Desc",
                                   number="011",
                                   account_type=AccountType.equity)
        self.object.remove_account("TestA")
        self.assertEqual(len(self.object.accounts), orig_length)

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

        self.assertEqual(result.name, orig.name)
        self.assertEqual(result.description, orig.description)
        self.assertEqual(result.number, orig.number)

    def test_get_account_and_decendants(self):
        # Set up this test.
        self.sales_fish_acc = self.object.accounts[3].create_account(
            "SalesFish",
            description="Sales of Fish",
            number="010")
        self.sales_barracuda_acc = self.sales_fish_acc.create_account(
            "SalesBarracuda",
            description="Sales of Barracudas",
            number="010")
        self.sales_nemo_acc = self.sales_fish_acc.create_account(
            "SalesNemo",
            description="Sales of Nemos",
            number="020")
        # perform the test.
        result = []
        self.object.get_account_and_decendants(
            self.object.accounts[3], result)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], self.object.accounts[3])
        self.assertEqual(result[1], self.sales_fish_acc)
        self.assertEqual(result[2], self.sales_barracuda_acc)
        self.assertEqual(result[3], self.sales_nemo_acc)

# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(TransactionTemplate)

if __name__ == '__main__':
    unittest.main()
