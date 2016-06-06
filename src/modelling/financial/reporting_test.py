#!/usr/bin/env python3
"""
This module provides testing code for the auxi.modelling.financial.des module.
"""

import unittest
from datetime import datetime

from auxi.modelling.financial.reporting import GeneralLedgerStructure
from auxi.modelling.financial.reporting import TransactionList
from auxi.modelling.financial.reporting import BalanceSheet
from auxi.modelling.financial.reporting import IncomeStatement

from auxi.modelling.financial.des import GeneralLedger
from auxi.modelling.financial.des import GeneralLedgerStructure as Gls


__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class GeneralLedgerStructureUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.reporting.GeneralLedgerStructure
    class.
    """

    def setUp(self):
        gls = Gls("NameA")
        self.object = GeneralLedgerStructure(
            data_source=gls, output_path=None)

    def test__generate_table_(self):
        table = self.object._generate_table_()
        self.assertEqual(table[0], ["Type", "Number", "Name", "Description"])
        # The general leger has 27 accounts
        self.assertEqual(len(table), 28)


class TransactionListUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.reporting.TransactionList
    class.
    """

    def setUp(self):
        gls = Gls("NameA")
        self.gl = GeneralLedger("NameA", gls)
        self.object = TransactionList(
            data_source=self.gl,
            start=datetime(2016, 4, 1),
            end=datetime(2016, 8, 1), output_path=None)

        self.gl.create_transaction(
            "tx1",
            description='1',
            tx_date=datetime(2016, 2, 1),
            dt_account="Bank\Default1",
            cr_account="Sales\Default1",
            source="test1",
            amount=1001)
        self.gl.create_transaction(
            "tx2",
            description='2',
            tx_date=datetime(2016, 3, 1),
            dt_account="Bank\Default2",
            cr_account="Sales\Default2",
            source="test2",
            amount=1002)
        self.gl.create_transaction(
            "tx3",
            description='3',
            tx_date=datetime(2016, 4, 2),
            dt_account="Bank\Default3",
            cr_account="Sales\Default3",
            source="test3",
            amount=1003)
        self.gl.create_transaction(
            "tx4",
            description='4',
            tx_date=datetime(2016, 5, 1),
            dt_account="Bank\Default4",
            cr_account="Sales\Default4",
            source="test4",
            amount=1004)
        self.gl.create_transaction(
            "tx5",
            description='5',
            tx_date=datetime(2016, 9, 1),
            dt_account="Bank\Default5",
            cr_account="Sales\Default5",
            source="test5",
            amount=1005)

    def test__generate_table_(self):
        table = self.object._generate_table_()
        self.assertEqual(table[0], [
            "Date", "Source", "Tx Name", "Debit Account",
            "Credit Account", "Amount", "Description"])
        # There should be 4 rows, 1 for the header, 2 for transactions
        # and 1 for the 'Total' column.
        self.assertEqual(len(table), 4)
        # The first 2 and last to transactions
        # in the GL falls outside the request start and end date. Thus, only
        # the 3rd and 4th transactions should appear in the report.
        # Test that the transaction names are correct.
        self.assertEqual(table[1][2], "tx3")
        self.assertEqual(table[2][2], "tx4")
        # Test that the transaction amounts are correct.
        self.assertEqual(table[1][5], '1003.00')
        self.assertEqual(table[2][5], '1004.00')
        # Test that the transaction sources are correct.
        self.assertEqual(table[1][1], "test3")
        self.assertEqual(table[2][1], "test4")
        # Test that the transaction dates are correct.
        self.assertEqual(table[1][0], datetime(2016, 4, 2))
        self.assertEqual(table[2][0], datetime(2016, 5, 1))
        # Test that the transaction dt accounts are correct.
        self.assertEqual(table[1][3], "Bank\Default3")
        self.assertEqual(table[2][3], "Bank\Default4")
        # Test that the transaction dt accounts are correct.
        self.assertEqual(table[1][4], "Sales\Default3")
        self.assertEqual(table[2][4], "Sales\Default4")
        # Test that the transaction descriptions are correct.
        self.assertEqual(table[1][6], "3")
        self.assertEqual(table[2][6], "4")


if __name__ == '__main__':
    unittest.main()
