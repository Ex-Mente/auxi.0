#!/usr/bin/env python3
"""
This module provides testing code for the
auxi.modelling.business.basic module.
"""

import unittest
from datetime import datetime
from dateutil import relativedelta

from auxi.core.time import Clock
from auxi.modelling.business.basic import BasicActivity
from auxi.modelling.business.basic import BasicLoanActivity
from auxi.modelling.financial.des import GeneralLedger
from auxi.modelling.financial.des import GeneralLedgerStructure

__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class BasicActivityUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.business.basic.BasicActivity class.
    """

    def setUp(self):
        self.object = BasicActivity("NameA",
                                    description="DescriptionA",
                                    dt_account="Bank",
                                    cr_account="Sales",
                                    amount=5000,
                                    start=datetime(2016, 2, 1),
                                    end=datetime(2017, 2, 1),
                                    interval=3)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.start_datetime, datetime(2016, 2, 1))
        self.assertEqual(self.object.end_datetime, datetime(2017, 2, 1))
        self.assertEqual(self.object.interval, 3)
        self.assertEqual(self.object.amount, 5000)
        self.assertEqual(self.object.dt_account, "Bank")
        self.assertEqual(self.object.cr_account, "Sales")

    def test__meet_exection_criteria(self):
        """
        Test that the activity only meets the execution criteria when
        it's amount is greater than 0.
        """

        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        self.object.prepare_to_run(clock, 13)
        self.assertEqual(self.object._meet_execution_criteria(5), True)
        self.object.amount = 0
        self.assertEqual(self.object._meet_execution_criteria(5), False)

    def test_run(self):
        """
        Test that the activity run method creates a transaction with an amount
        of 5000.
        """

        structure = GeneralLedgerStructure("NameA", description="DescriptionA")
        gl = GeneralLedger("NameA", structure, description="DescriptionA")
        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        clock.tick()
        clock.tick()
        self.object.prepare_to_run(clock, 20)
        self.object.run(clock, gl)
        self.assertEqual(len(gl.transactions), 1)
        self.assertEqual(gl.transactions[0].amount, 5000)

    def test_get_referenced_accounts(self):
        """
        Test that the activity run method get_referenced_accounts accounts
        matches the debit and credit accounts self.object was initialised with.
        """

        result = self.object.get_referenced_accounts()
        self.assertEqual(self.object.dt_account, result[0])
        self.assertEqual(self.object.cr_account, result[1])


class BasicLoanActivityUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.business.basic.BasicLoanActivity class.
    """

    def setUp(self):
        self.gl_structure = GeneralLedgerStructure(
            "GL Structure",
            description="General Ledger Structure")
        self.gl_structure["Account Payable"].create_account(
            "Capital Loan",
            "0000")
        self.gl_structure["Expense"].create_account(
            "Interest Expense",
            "0000")

        self.gl = GeneralLedger(
            "GL",
            self.gl_structure,
            description="General Ledger")

        self.clock = Clock("NameA", start_datetime=datetime(2016, 2, 1))

        self.object = BasicLoanActivity(
            "Capital Loan",
            bank_account="Bank/Default",
            loan_account="Account Payable/Capital Loan",
            interest_account="Expense/Interest Expense",
            amount=180000,
            interest_rate=0.15,
            start=datetime(2016, 2, 1),
            duration=36,
            interval=1,
            description="Loan for Capital")

    def test_constructor(self):
        self.assertEqual(self.object.name, "Capital Loan")
        self.assertEqual(self.object.bank_account, "Bank/Default")
        self.assertEqual(
            self.object.loan_account, "Account Payable/Capital Loan")
        self.assertEqual(
            self.object.interest_account, "Expense/Interest Expense")
        self.assertEqual(self.object.amount, 180000)
        self.assertEqual(self.object.interest_rate, 0.15)
        self.assertEqual(self.object.start_datetime, datetime(2016, 2, 1))
        self.assertEqual(self.object.end_datetime, datetime(2019, 3, 1))
        self.assertEqual(self.object.duration, 36)
        self.assertEqual(self.object.interval, 1)
        self.assertEqual(self.object.description, "Loan for Capital")

    def test__meet_exection_criteria(self):
        """
        Test that the activity only meets the execution criteria when
        it's amount is greater than 0 and its duration is greater than 0.
        """

        self.object.prepare_to_run(self.clock, 13)
        self.assertEqual(self.object._meet_execution_criteria(5), True)
        self.object.amount = 0
        self.assertEqual(self.object._meet_execution_criteria(5), False)
        self.object.amount = 180000
        self.object.duration = 0
        self.assertEqual(self.object._meet_execution_criteria(5), False)

    def test_run_first_month(self):
        """
        Test that the activity run method creates a transaction with an amount
        of 180000 on the first month. No other transactions
        """

        self.object.prepare_to_run(self.clock, 1)
        self.object.run(self.clock, self.gl)
        self.assertEqual(len(self.gl.transactions), 1)
        self.assertEqual(self.gl.transactions[0].amount, 180000)

    def test_run_third_month(self):
        """
        Test that the activity run method accrued the interest correctly.
        """

        self.clock.tick()
        self.object.prepare_to_run(self.clock, 61)
        self.clock.tick()
        self.object.run(self.clock, self.gl)
        self.clock.tick()
        self.object.run(self.clock, self.gl)
        self.clock.tick()
        self.object.run(self.clock, self.gl)
        self.assertEqual(len(self.gl.transactions), 5)
        # Test the intreset rate for the first month
        # loan amount = 180000
        # First month's interest should be (180000 * 0.15) / 12 = 2250
        self.assertEqual(self.gl.transactions[1].amount, 2250)
        # Principle payment is 6239.76 (see below)
        # The interest payed the previous month is 2250
        # Making the total amount payed to the loan 6239.76 - 2250 = 3,989.76
        # New amount to calculate interest from: 180000 - 3,989.76 = 176,010.24
        # 2nd month's interest should be 176,010.24 * 0.15) / 12 = 2,200.13
        self.assertEqual("%.2f" % self.gl.transactions[3].amount, "2200.13")
        # Test the monthly principle payment
        # interest rate = 0.15: per month 0.0125.
        # loan amount = 180000
        # duration of the loan = 36
        # payment = (180000*0.0125) / (1-(1/pow((1+0.0125), 36))) = 6239.76
        self.assertEqual("%.2f" % self.gl.transactions[2].amount, "6239.76")
        self.assertEqual("%.2f" % self.gl.transactions[4].amount, "6239.76")

    def test_run_last_month(self):
        """
        Test that the activity run method creates settled the loan on the
        loans' last month and that the transactions
        """

        self.clock.tick()
        self.object.prepare_to_run(self.clock, 61)
        for i in range(0, 60):
            self.object.run(self.clock, self.gl)
            self.clock.tick()
        # Test the number of transaction that was created during the
        # loan's lifetime.
        # 2 transactions per months should be created + the initial loan amount
        # transaction. 36*2 + 1 = 73
        last_tx_ix = len(self.gl.transactions)
        self.assertEqual(len(self.gl.transactions), 73)
        # The transactions should have run only run for 36 months
        # (the duration of the loan)
        r = relativedelta.relativedelta(
            self.gl.transactions[last_tx_ix-1].tx_date,
            self.gl.transactions[0].tx_date)
        self.assertEqual(r.years * 12 + r.months, 36)

    def test_get_referenced_accounts(self):
        """
        Test that the activity run method get_referenced_accounts accounts
        matches the debit and credit accounts self.object was initialised with.
        """

        result = self.object.get_referenced_accounts()
        self.assertEqual(self.object.bank_account, result[0])
        self.assertEqual(self.object.loan_account, result[1])
        self.assertEqual(self.object.interest_account, result[2])


if __name__ == '__main__':
    unittest.main()
