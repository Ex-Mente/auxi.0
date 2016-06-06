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
from auxi.core.reporting import ReportFormat

__version__ = '0.2.1'
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

    def test_set_parent_path(self):
        self.object.set_parent_path("accyA/accyB")
        self.assertEqual(self.object.path, "accyA/accyB/NameA")

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

    def test_get_child_account(self):
        sub_acc = self.object.create_account(
            "TestA",
            description="TestA_Desc",
            number="011")
        sub_sub_acc = sub_acc.create_account(
            "TestA1",
            description="TestA1_Desc",
            number="012")
        result = self.object.get_child_account("TestA/TestA1")

        self.assertEqual(result.name, sub_sub_acc.name)
        self.assertEqual(result.description, sub_sub_acc.description)
        self.assertEqual(result.number, sub_sub_acc.number)
        self.assertEqual(result.account_type, sub_sub_acc.account_type)

        self.assertEqual(result, sub_sub_acc)


class TransactionUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.des.Transaction class.
    """

    def setUp(self):
        self.object = Transaction("NameA",
                                  description="DescriptionA",
                                  tx_date=datetime(2016, 2, 1).date(),
                                  dt_account="Bank",
                                  cr_account="Sales",
                                  source="PigeonSales",
                                  amount=100.00)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.dt_account, "Bank")
        self.assertEqual(self.object.tx_date, datetime(2016, 2, 1).date())
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
        self.assertNotEqual(self.object["Bank"], None)
        self.assertEqual(
            self.object['Unallocated Income Statement'].account_type,
            AccountType.revenue)
        self.assertEqual(self.object["Sales"].number, "I10")
        self.assertEqual(
            self.object["Sales"].account_type,
            AccountType.revenue)
        self.assertEqual(self.object["Cost of Sales"].number, "I15")
        self.assertEqual(
            self.object["Cost of Sales"].account_type,
            AccountType.expense)
        self.assertEqual(self.object["Other Income"].number, "I20")
        self.assertEqual(
            self.object["Other Income"].account_type,
            AccountType.revenue)
        self.assertEqual(self.object["Expense"].number, "I25")
        self.assertEqual(
            self.object["Expense"].account_type,
            AccountType.expense)
        self.assertEqual(self.object["Tax"].number, "I30")
        self.assertEqual(
            self.object["Tax"].account_type,
            AccountType.expense)
        self.assertEqual(self.object["Dividends"].number, "I35")
        self.assertEqual(
            self.object["Dividends"].account_type,
            AccountType.expense)
        self.assertEqual(self.object["Share Capital"].number, "B10")
        self.assertEqual(
            self.object["Share Capital"].account_type,
            AccountType.asset)
        self.assertEqual(self.object["Retained Income"].number, "B15")
        self.assertEqual(
            self.object["Retained Income"].account_type,
            AccountType.equity)
        self.assertEqual(self.object["Shareholders Loan"].number, "B20")
        self.assertEqual(
            self.object["Shareholders Loan"].account_type,
            AccountType.liability)
        self.assertEqual(self.object["Long Term Borrowing"].number, "B25")
        self.assertEqual(
            self.object["Long Term Borrowing"].account_type,
            AccountType.liability)
        self.assertEqual(
            self.object["Other Long Term Liabilities"].number,
            "B30")
        self.assertEqual(
            self.object["Other Long Term Liabilities"].account_type,
            AccountType.liability)
        self.assertEqual(self.object["Fixed Assets"].number, "B35")
        self.assertEqual(
            self.object["Fixed Assets"].account_type,
            AccountType.asset)
        self.assertEqual(self.object["Investments"].number, "B40")
        self.assertEqual(
            self.object["Investments"].account_type,
            AccountType.asset)
        self.assertEqual(self.object["Other Fixed Assets"].number, "B45")
        self.assertEqual(
            self.object["Other Fixed Assets"].account_type,
            AccountType.asset)
        self.assertEqual(self.object["Inventory"].number, "B50")
        self.assertEqual(
            self.object["Inventory"].account_type,
            AccountType.asset)
        self.assertEqual(self.object["Accounts Receivable"].number, "B55")
        self.assertEqual(
            self.object["Accounts Receivable"].account_type,
            AccountType.asset)
        self.assertEqual(self.object["Bank"].number, "B60")
        self.assertEqual(
            self.object["Bank"].account_type,
            AccountType.asset)
        self.assertEqual(self.object["Bank"]["Default"].number, "0000")
        self.assertEqual(
            self.object["Bank"]["Default"].account_type,
            AccountType.asset)
        self.assertEqual(self.object["Other Current Assets"].number, "B65")
        self.assertEqual(
            self.object["Other Current Assets"].account_type,
            AccountType.asset)
        self.assertEqual(self.object["Account Payable"].number, "B70")
        self.assertEqual(
            self.object["Account Payable"].account_type,
            AccountType.liability)
        self.assertEqual(self.object["Taxation"].number, "B75")
        self.assertEqual(
            self.object["Taxation"].account_type,
            AccountType.liability)
        self.assertEqual(
            self.object["Other Current Liabilities"].number,
            "B80")
        self.assertEqual(
            self.object["Other Current Liabilities"].account_type,
            AccountType.liability)

        self.assertEqual(
            self.object['Unallocated Income Statement']["Gross Profit"].number,
            "0000")
        self.assertEqual(
            self.object['Unallocated Income Statement']
            ["Gross Profit"].account_type,
            AccountType.revenue)
        self.assertEqual(
            self.object['Unallocated Income Statement']
            ["Income Summary"].number,
            "0010")
        self.assertEqual(
            self.object['Unallocated Income Statement']
            ["Income Summary"].account_type,
            AccountType.revenue)
        self.assertEqual(
            self.object['Retained Income']
            ["Retained Earnings"].number,
            "0000")
        self.assertEqual(
            self.object['Retained Income']
            ["Retained Earnings"].account_type,
            AccountType.equity)
        self.assertEqual(
            self.object['Tax']
            ["Income Tax Expense"].number,
            "0000")
        self.assertEqual(
            self.object['Tax']
            ["Income Tax Expense"].account_type,
            AccountType.expense)

        self.assertEqual(self.object.tax_payment_account, "Bank/Default")

    def test_get_account(self):
        self.object["Retained Income"].create_account(
            "TestA",
            number="010")
        acc = self.object["Bank"].create_account(
            "TestB",
            number="020")
        sub_acc = acc.create_account(
            "TestB1",
            description="TestB1_Desc",
            number="010")
        sub_acc.create_account(
            "TestB1.1",
            description="TestB1.1_Desc",
            number="010")
        orig = sub_acc.create_account(
            "TestB1.2",
            description="TestB1.1_Desc",
            number="011")
        result = self.object.get_account("Bank/TestB/TestB1/TestB1.2")

        self.assertEqual(result.name, orig.name)
        self.assertEqual(result.description, orig.description)
        self.assertEqual(result.number, orig.number)

    def test_get_account_decendants(self):
        # Set up this test.
        self.sales_fish_acc = self.object["Sales"].create_account(
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
        result = self.object.get_account_decendants(self.object["Sales"])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], self.sales_fish_acc)
        self.assertEqual(result[1], self.sales_barracuda_acc)
        self.assertEqual(result[2], self.sales_nemo_acc)

    def test_validate_account_name_valid(self):
        self.object.validate_account_names(
            ["Bank/Default", "Retained Income/Retained Earnings"])

    def test_validate_account_name_invalid(self):
        self.assertRaises(
            ValueError,
            self.object.validate_account_names,
            ["invalid_acc_name_a", "invalid_acc_name_b"])

    def test_report(self):
        report = self.object.report(ReportFormat.string)
        line1 = report.split("\n")[0]
        self.assertEqual(line1.replace(" ", ""), "TypeNumberNameDescription")


class GeneralLedgerUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.des.GeneralLedger class.
    """

    def setUp(self):
        self.structure = GeneralLedgerStructure("NameA",
                                                description="DescriptionA")
        self.structure["Retained Income"].create_account(
            "TestA",
            description="TestA_Desc",
            number="010")
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
            tx_date=datetime(2016, 2, 1).date(),
            dt_account="Bank",
            cr_account="Sales",
            source="Peanut Sales",
            amount=20.00)

        tx_list = self.object.transactions
        self.assertEqual(new_tx.name, tx_list[0].name)
        self.assertEqual(new_tx.tx_date, tx_list[0].tx_date)
        self.assertEqual(new_tx.dt_account, tx_list[0].dt_account)
        self.assertEqual(new_tx.cr_account, tx_list[0].cr_account)
        self.assertEqual(new_tx.source, tx_list[0].source)
        self.assertEqual(new_tx.amount, tx_list[0].amount)


if __name__ == '__main__':
    unittest.main()
