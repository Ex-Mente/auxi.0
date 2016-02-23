#!/usr/bin/env python3
"""
This module provides testing code for the auxi.modelling.financial.des module.
"""

import unittest
from datetime import datetime

from auxi.modelling.financial.des import AccountType
from auxi.modelling.financial.des import GeneralLedgerAccount
from auxi.modelling.financial.des import Transaction
from auxi.modelling.financial.des import TransactionTemplate
from auxi.modelling.financial.des import GeneralLedgerStructure
from auxi.modelling.financial.des import GeneralLedger

__version__ = '0.2.0rc4'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class GeneralLedgerAccountUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.des.GeneralLedgerAccount class.
    """

    def setUp(self):
        self.object = GeneralLedgerAccount("NameA",
                                           description="DescriptionA",
                                           number="010",
                                           account_type=AccountType.asset)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.number, "010")
        self.assertEqual(self.object.account_type, AccountType.asset)

    def test_create_account(self):
        new_account = self.object.create_account("TestA",
                                                 description="TestA_Desc",
                                                 number="011")
        self.assertEqual(new_account.name, "TestA")
        self.assertEqual(new_account.description, "TestA_Desc")
        self.assertEqual(new_account.number, "011")
        self.assertEqual(new_account.account_type, self.object.account_type)

        self.assertEqual(new_account, self.object.accounts[0])

    def test_remove_account(self):
        num_accounts = len(self.object.accounts)
        self.object.create_account("TestA",
                                   description="TestA_Desc",
                                   number="011")
        self.object.remove_account("TestA")
        self.assertEqual(len(self.object.accounts), num_accounts)


class TransactionUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.des.Transaction class.
    """

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


class TransactionTemplateUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.des.TransactionTemplate class.
    """

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


class GeneralLedgerStructureUnitTester(unittest.TestCase):
    """
      Tester for the auxi.modelling.financial.des.generalledgerstructure class.
    """

    def setUp(self):
        self.object = GeneralLedgerStructure("NameA",
                                             description="DescriptionA")

    def test_constructor(self):
        """
        Test the the variables has been initialised and that the default
        accounts has been created.
        """
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


class GeneralLedgerUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.des.GeneralLedger class.
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
        new_tx = self.object.create_transaction(
            "TestA",
            description="TestA_Desc",
            tx_datetime=datetime(2016, 2, 1),
            dt_account="Bank",
            cr_account="Sales",
            source="Peanut Sales",
            amount=20.00)

        tx_list = self.object.transactions
        self.assertEqual(new_tx.name, tx_list[0].name)
        self.assertEqual(new_tx.tx_datetime, tx_list[0].tx_datetime)
        self.assertEqual(new_tx.dt_account, tx_list[0].dt_account)
        self.assertEqual(new_tx.cr_account, tx_list[0].cr_account)
        self.assertEqual(new_tx.source, tx_list[0].source)
        self.assertEqual(new_tx.amount, tx_list[0].amount)

# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(GeneralLedgerAccount)
# help(Transaction)
# help(TransactionTemplate)
# help(GeneralLedgerStructure)
# help(GeneralLedger)

if __name__ == '__main__':
    unittest.main()
