# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.business.entity module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
import collections
from datetime import datetime
from dateutil.relativedelta import relativedelta
from auxi.modeling.business.clock import Clock
from auxi.modeling.business.entity import Entity
from auxi.modeling.business.basicactivity import BasicActivity
from auxi.modeling.financial.des.generalledgerstructure import GeneralLedgerStructure
from auxi.modeling.financial.des.transactiontemplate import TransactionTemplate

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
      Tester for the auxi.modeling.entity.component class.
    """

    def setUp(self):
        self.gl_structure = GeneralLedgerStructure(
            "NameA",
            description="DescriptionA")

        self.object = Entity("EntityA",
                             gl_structure=self.gl_structure,
                             description="DescriptionA")
        # Set up the needed objects
        comp1 = self.object.create_component("ComponentA1", description="ca1")
        self.tx_template = TransactionTemplate("NameA",
                                               description="DescriptionA",
                                               dt_account="Bank",
                                               cr_account="Sales")
        basic_activity = BasicActivity("BasicActivityA",
                                       description="DescriptionA",
                                       start=datetime(2016, 2, 1),
                                       end=datetime(2017, 2, 1),
                                       interval=1,
                                       amount=5000,
                                       tx_template=self.tx_template)
        comp1.activities.append(basic_activity)

        self.clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))

    def test_constructor(self):
        self.assertEqual(self.object.name, "EntityA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.gl.structure.name, self.gl_structure.name)
        self.assertEqual(len(self.object.tax_rule_set.rules), 0)
        self.assertEqual(self.object.period_count, -1)

    def test_set_parent_path(self):
        self.object.set_parent_path("modelA")
        self.assertEqual(self.object.path, "modelA/EntityA")

    def test_set_name(self):
        self.object.set_parent_path("modelA")
        self.object.name = "NameAt"
        self.assertEqual(self.object.name, "NameAt")
        self.assertEqual(self.object.components[0].path,
                         "modelA/NameAt/ComponentA1")
        self.assertEqual(self.object.components[0].activities[0].path,
                         "modelA/NameAt/ComponentA1/BasicActivityA")

    def test_create_component(self):
        new_comp = self.object.create_component("ComponentA2",
                                                description="ca2")
        self.assertEqual(new_comp.name, "ComponentA2")
        self.assertEqual(new_comp.description, "ca2")

        self.assertEqual(new_comp, self.object.components[1])

    def test_remove_component(self):
        self.object.create_component("ComponentA2",
                                     description="ca2")
        self.object.remove_component("ComponentA2")
        self.assertEqual(len(self.object.components), 1)

    def test_prepare_to_run(self):
        # Test the prepare to run method before any run has been performed
        self.object.gl.create_transaction(
            "TestA",
            description="TestA_Desc",
            tx_datetime=datetime(2016, 2, 1),
            dt_account="Bank",
            cr_account="Sales",
            source="Peanut Sales",
            amount=20.00)
        self.object.negative_income_tax_total = 99

        self.object.prepare_to_run(self.clock, 18)

        # Was the component's prepare to run executed?
        self.assertEqual(
            self.object.components[0].activities[0].start_period_ix, 2)
        self.assertEqual(
            self.object.components[0].activities[0].end_period_ix, 14)
        # Was the datetime's set correctly?
        self.assertEqual(
            self.object._exec_year_end_datetime,
            self.clock.get_datetime_at_period_ix(18))
        self.assertEqual(
            self.object._prev_year_end_datetime,
            self.clock.start_datetime)
        self.assertEqual(
            self.object._curr_year_end_datetime,
            self.clock.start_datetime + relativedelta(years=1))
        # Was the transactions cleared?
        self.assertEqual(len(self.object.gl.transactions), 0)
        # Was the negative tax income reset to 0?
        self.assertEqual(self.object.negative_income_tax_total, 0)

    def test_run(self):
        self.object.prepare_to_run(self.clock, 20)
        self.clock.tick()
        self.clock.tick()
        self.object.run(self.clock)
        self.assertEqual(len(self.object.gl.transactions), 1)
        self.assertEqual(self.object.gl.transactions[0].amount, 5000)

    def test__perform_year_end_gross_profit_and_income_summary(self):
        gls = self.object.gl.structure
        year_end_datetime = datetime(2017, 2, 1)
        # Create the accounts to write of dict
        income_summary_write_off_accounts = collections.OrderedDict([
            (gls.costofsales_account, 700),
            (gls.incometaxexpense_account, -300),
            (gls.sales_account, 70),
            (gls.accounts[0], -30)])
        gross_profit_write_off_accounts = collections.OrderedDict([
            (gls.sales_account, 70),
            (gls.accounts[0], -30)])
        # Test when there the gross profit is 0.
        # The gross profit account should not be settled:
        inc = self.object._perform_year_end_gross_profit_and_income_summary(
            year_end_datetime,
            {},
            income_summary_write_off_accounts)
        # The gross profit account should not be settled.
        # Only the 4 transactions from the income summary year end calcs
        # should be there
        self.assertEqual(len(self.object.gl.transactions), 4)
        # The income summary should be that of the income summary year end calc
        # method: -360 (See the income summary year end calc, in this case,
        # gross profit starts at 0 instead of 5000, thus -360 instead of 4640)
        self.assertEqual(inc, -360)

        # Test when there is gross profit.
        # The gross profit account should not be settled:
        del self.object.gl.transactions[:]  # Clear the tx list
        self.object._perform_year_end_gross_profit_and_income_summary(
            year_end_datetime,
            gross_profit_write_off_accounts, {})
        # The gross profit account should be settled.
        # Only the 2 transactions from the income summary year end calcs
        # should be there as well as the gross profit settle transaction
        self.assertEqual(len(self.object.gl.transactions), 3)
        # Make sure the gross profit settle transaction appears correct
        # When gross profit is positive:
        self.assertEqual(self.object.gl.transactions[2].dt_account,
                         gls.gross_profit_account.name)
        self.assertEqual(self.object.gl.transactions[2].cr_account,
                         gls.incomesummary_account.name)
        self.assertEqual(self.object.gl.transactions[2].tx_datetime,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[2].amount, 40)
        self.assertEqual(self.object.gl.transactions[2].is_closing_cr_account,
                         True)
        # When gross profit is negative:
        gross_profit_write_off_accounts = collections.OrderedDict([
            (gls.sales_account, -70),
            (gls.accounts[0], 30)])
        del self.object.gl.transactions[:]  # Clear the tx list
        self.object._perform_year_end_gross_profit_and_income_summary(
            year_end_datetime,
            gross_profit_write_off_accounts, {})
        self.assertEqual(self.object.gl.transactions[2].dt_account,
                         gls.incomesummary_account.name)
        self.assertEqual(self.object.gl.transactions[2].cr_account,
                         gls.gross_profit_account.name)
        self.assertEqual(self.object.gl.transactions[2].tx_datetime,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[2].amount, 40)
        self.assertEqual(self.object.gl.transactions[2].is_closing_cr_account,
                         True)


    def test__perform_year_end_gross_profit(self):
        gls = self.object.gl.structure
        year_end_datetime = datetime(2017, 2, 1)

        # Create the accounts to write of dict
        gross_profit_write_off_accounts = collections.OrderedDict([
            (gls.sales_account, 70),
            (gls.accounts[0], -30)])
        gross_profit = self.object._perform_year_end_gross_profit(
            year_end_datetime, gross_profit_write_off_accounts)
        self.assertEqual(len(self.object.gl.transactions), 2)
        # Expenses: 700-300 = 400
        # Other: 70-30 = 40
        # Total: gross_profit + Other - expenses: 5000 + 40 - 400 = 4640
        self.assertEqual(gross_profit, 40)

        # Test the "gls.sales_account: 70" transaction
        self.assertEqual(self.object.gl.transactions[0].dt_account,
                         gls.gross_profit_account.name)
        self.assertEqual(self.object.gl.transactions[0].cr_account,
                         gls.sales_account.name)
        self.assertEqual(self.object.gl.transactions[0].tx_datetime,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[0].amount, 70)
        self.assertEqual(self.object.gl.transactions[0].is_closing_cr_account,
                         True)

        # Test the "gls.accounts[0]: -30" transaction
        self.assertEqual(self.object.gl.transactions[1].dt_account,
                         gls.accounts[0].name)
        self.assertEqual(self.object.gl.transactions[1].cr_account,
                         gls.gross_profit_account.name)
        self.assertEqual(self.object.gl.transactions[1].tx_datetime,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[1].amount, 30)
        self.assertEqual(self.object.gl.transactions[1].is_closing_cr_account,
                         True)

    def test__perform_year_end_income_summary(self):
        gls = self.object.gl.structure
        year_end_datetime = datetime(2017, 2, 1)
        gross_profit = 5000

        # Create the accounts to write of dict
        income_summary_write_off_accounts = collections.OrderedDict([
            (gls.costofsales_account, 700),
            (gls.incometaxexpense_account, -300),
            (gls.sales_account, 70),
            (gls.accounts[0], -30)])
        income_summary_amount = self.object._perform_year_end_income_summary(
            year_end_datetime, gross_profit, income_summary_write_off_accounts)
        self.assertEqual(len(self.object.gl.transactions), 4)
        # Expenses: 700-300 = 400
        # Other: 70-30 = 40
        # Total: gross_profit + Other - expenses: 5000 + 40 - 400 = 4640
        self.assertEqual(income_summary_amount, 4640)

        # Test the "gls.costofsales_account: 700" transaction
        self.assertEqual(self.object.gl.transactions[0].dt_account,
                         gls.incomesummary_account.name)
        self.assertEqual(self.object.gl.transactions[0].cr_account,
                         gls.costofsales_account.name)
        self.assertEqual(self.object.gl.transactions[0].tx_datetime,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[0].amount, 700)
        self.assertEqual(self.object.gl.transactions[0].is_closing_cr_account,
                         True)

        # Test the "gls.incometaxexpense_account: -300" transaction
        self.assertEqual(self.object.gl.transactions[1].dt_account,
                         gls.incometaxexpense_account.name)
        self.assertEqual(self.object.gl.transactions[1].cr_account,
                         gls.incomesummary_account.name)
        self.assertEqual(self.object.gl.transactions[1].tx_datetime,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[1].amount, 300)
        self.assertEqual(self.object.gl.transactions[1].is_closing_cr_account,
                         True)

        # Test the "gls.sales_account: 70" transaction
        self.assertEqual(self.object.gl.transactions[2].dt_account,
                         gls.sales_account.name)
        self.assertEqual(self.object.gl.transactions[2].cr_account,
                         gls.incomesummary_account.name)
        self.assertEqual(self.object.gl.transactions[2].tx_datetime,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[2].amount, 70)
        self.assertEqual(self.object.gl.transactions[2].is_closing_cr_account,
                         True)

        # Test the "gls.accounts[0]: -30" transaction
        self.assertEqual(self.object.gl.transactions[3].dt_account,
                         gls.incomesummary_account.name)
        self.assertEqual(self.object.gl.transactions[3].cr_account,
                         gls.accounts[0].name)
        self.assertEqual(self.object.gl.transactions[3].tx_datetime,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[3].amount, 30)
        self.assertEqual(self.object.gl.transactions[3].is_closing_cr_account,
                         True)

    def test__perform_year_end_income_tax(self):
        # TODO
        pass

    def test__perform_year_end_retained_earnings(self):
        gls = self.object.gl.structure
        year_end_datetime = datetime(2017, 2, 1)
        # Test for == 0 case
        income_summary = 0
        self.object._perform_year_end_retained_earnings(
            year_end_datetime, income_summary)
        self.assertEqual(len(self.object.gl.transactions), 0)

        # Test for > 0 case
        income_summary = 1000
        self.object._perform_year_end_retained_earnings(
            year_end_datetime, income_summary)
        self.assertEqual(len(self.object.gl.transactions), 1)
        self.assertEqual(self.object.gl.transactions[0].dt_account,
                         gls.incomesummary_account.name)
        self.assertEqual(self.object.gl.transactions[0].cr_account,
                         gls.retainedearnings_account.name)
        self.assertEqual(self.object.gl.transactions[0].tx_datetime,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[0].amount,
                         income_summary)
        self.assertEqual(self.object.gl.transactions[0].is_closing_cr_account,
                         True)

        # Test for < 0 case
        income_summary = -300
        self.object._perform_year_end_retained_earnings(
            year_end_datetime, income_summary)
        self.assertEqual(len(self.object.gl.transactions), 2)
        self.assertEqual(self.object.gl.transactions[1].dt_account,
                         gls.retainedearnings_account.name)
        self.assertEqual(self.object.gl.transactions[1].cr_account,
                         gls.incomesummary_account.name)
        self.assertEqual(self.object.gl.transactions[1].tx_datetime,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[1].amount,
                         income_summary)
        self.assertEqual(self.object.gl.transactions[1].is_closing_cr_account,
                         True)

    def test__perform_year_end_procedure(self):
        pass

# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(Component)

if __name__ == '__main__':
    unittest.main()
