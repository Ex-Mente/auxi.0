#!/usr/bin/env python3
"""
This module provides testing code for the
auxi.modelling.business.basic module.
"""

import unittest
from datetime import datetime

from auxi.core.time import Clock
from auxi.modelling.business.basic import BasicActivity
from auxi.modelling.business.basic import BasicLoanActivity
from auxi.modelling.financial.des import GeneralLedger
from auxi.modelling.financial.des import GeneralLedgerStructure

__version__ = '0.2.0rc6'
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

        self.clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))

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

        # self.assertEqual("Done", "Not Done")
        pass

    def test_run_last_month(self):
        """
        Test that the activity run method creates settled the loan on the
        loans' last month.
        """

        # self.assertEqual("Done", "Not Done")
        pass

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
