#!/usr/bin/env python3
"""
This module provides testing code for the
auxi.modelling.business.activity module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
import collections
from datetime import datetime
from dateutil.relativedelta import relativedelta

from auxi.core.time import Clock
from auxi.modelling.business.structure import Activity
from auxi.modelling.business.structure import Component
from auxi.modelling.business.structure import Entity
from auxi.modelling.business.basic import BasicActivity
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


class ActivityUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.business.structure.Activity class.
    """

    def setUp(self):
        self.object = Activity("NameA",
                               description="DescriptionA",
                               start=datetime(2016, 2, 1),
                               end=datetime(2017, 2, 1),
                               interval=3)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.start_datetime, datetime(2016, 2, 1))
        self.assertEqual(self.object.end_datetime, datetime(2017, 2, 1))
        self.assertEqual(self.object.interval, 3)

    def test_get_path(self):
        self.object.set_parent_path("entityA/componentA")
        self.assertEqual(self.object.path, "entityA/componentA/NameA")

    def test_set_parent_path(self):
        self.object.set_parent_path("entityA/componentA")
        self.assertEqual(self.object.path, "entityA/componentA/NameA")

    def test_set_name(self):
        """
        Test wether the name changes when it is set
        and that the activity's path is updated correctly.
        """
        self.object.set_parent_path("entityA/componentA")
        self.object.name = "NameAt"
        self.assertEqual(self.object.name, "NameAt")
        self.assertEqual(self.object.path, "entityA/componentA/NameAt")

    def test__meet_exection_criteria(self):
        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        self.object.prepare_to_run(clock, 13)
        self.assertEqual(self.object._meet_execution_criteria(3), False)
        self.assertEqual(self.object._meet_execution_criteria(5), True)
        self.assertEqual(self.object._meet_execution_criteria(40), False)

    def test_prepare_to_run(self):
        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        self.object.prepare_to_run(clock, 18)
        self.assertEqual(self.object.start_period_ix, 2)
        self.assertEqual(self.object.end_period_ix, 14)

    def test_get_referenced_accounts(self):
        self.assertEqual(len(self.object.get_referenced_accouts()), 0)


class ComponentUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.business.structure.Component class.
    """

    def setUp(self):
        self.gl_structure = GeneralLedgerStructure(
            "NameA",
            description="DescriptionA")
        self.gl_structure["Sales"].create_account("Default", number="0000")
        self.gl = GeneralLedger(
            "NameA",
            self.gl_structure,
            description="DescriptionA")
        self.object = Component("ComponentA",
                                self.gl,
                                description="DescriptionA")
        # Set up the needed objects
        self.object.create_component("ComponentA1", description="ca1")
        self.object.create_component("ComponentA2", description="ca2")
        self.basic_activity = BasicActivity(
            "BasicActivityA",
            description="DescriptionA",
            dt_account="Bank/Default",
            cr_account="Sales/Default",
            amount=5000,
            start=datetime(2016, 2, 1),
            end=datetime(2017, 2, 1),
            interval=3)
        self.object["ComponentA1"].add_activity(self.basic_activity)

    def test_constructor(self):
        self.assertEqual(self.object.name, "ComponentA")
        self.assertEqual(self.object.description, "DescriptionA")

    def test_set_parent_path(self):
        self.object.set_parent_path("/entityA")
        self.assertEqual(self.object.path, "/entityA/ComponentA")

    def test_set_name(self):
        """
        Test wether the name changes when it is set, that the component's
        name changes and that the component's children's paths are updated
        correctly.
        """
        self.object.set_parent_path("entityA")
        self.object.name = "NameAt"
        self.assertEqual(self.object.name, "NameAt")
        self.assertEqual(self.object.components[0].path,
                         "entityA/NameAt/ComponentA1")
        self.assertEqual(self.object.components[1].path,
                         "entityA/NameAt/ComponentA2")
        self.assertEqual(self.object.components[0].activities[0].path,
                         "entityA/NameAt/ComponentA1/BasicActivityA")

    def test_create_component(self):
        new_comp = self.object.create_component("ComponentTestCreate",
                                                description="catc")
        self.assertEqual(new_comp.name, "ComponentTestCreate")
        self.assertEqual(new_comp.description, "catc")

        self.assertEqual(new_comp, self.object.components[2])

    def test_remove_component(self):
        self.object.create_component("ComponentTestRemove",
                                     description="catr")
        self.object.remove_component("ComponentTestRemove")
        self.assertEqual(len(self.object.components), 2)

    def test_get_component_exists(self):
        self.assertEqual(
            self.object.get_component("ComponentA1"),
            self.object["ComponentA1"])

    def test_get_component_not_exists(self):
        self.assertRaises(IndexError, self.object.get_component, "ComponentA3")

    def test_add_activity_valid_account_name(self):
        basic_activity2 = BasicActivity(
            "BasicActivityB",
            description="DescriptionB",
            dt_account="Bank/Default",
            cr_account="Sales/Default",
            amount=5000,
            start=datetime(2016, 2, 1),
            end=datetime(2017, 2, 1),
            interval=3)
        self.object["ComponentA2"].add_activity(basic_activity2)

        self.assertEqual(len(self.object["ComponentA2"].activities), 1)
        self.assertEqual(
            basic_activity2.path,
            "/ComponentA/ComponentA2/BasicActivityB")

    def test_add_activity_invalid_account_name(self):
        basic_activity2 = BasicActivity(
            "BasicActivityB",
            description="DescriptionB",
            dt_account="invalid_acc_name_a",
            cr_account="invalid_acc_name_b",
            amount=5000,
            start=datetime(2016, 2, 1),
            end=datetime(2017, 2, 1),
            interval=3)
        self.assertRaises(
            ValueError,
            self.object["ComponentA2"].add_activity, basic_activity2)

    def test_get_activity_exists(self):
        self.assertEqual(
            self.object["ComponentA1"].get_activity("BasicActivityA"),
            self.basic_activity)

    def test_get_activity_not_exists(self):
        self.assertRaises(
            IndexError,
            self.object["ComponentA1"].get_activity, "B")

    def test_prepare_to_run(self):
        """
        Test that the component run's its activities' prepare_to_run methods.
        """
        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        self.object.prepare_to_run(clock, 18)
        # The activity's start and end period indexes should be changed.
        self.assertEqual(
            self.object.components[0].activities[0].start_period_ix, 2)
        self.assertEqual(
            self.object.components[0].activities[0].end_period_ix, 14)

    def test_run(self):
        """
        Test that the component runs its activities.
        """
        # Set up the general ledger so that an activity can create a
        # transaction.
        structure = GeneralLedgerStructure("NameA", description="DescriptionA")
        gl = GeneralLedger("NameA", structure, description="DescriptionA")
        # Prepare the component for a run. Tick the clock to the correct place
        # for the activity to create a transaction.
        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        clock.tick()
        clock.tick()
        self.object.prepare_to_run(clock, 20)
        self.object.run(clock, gl)
        # If the activity has been run, then a transaction should have
        # been generated.
        self.assertEqual(len(gl.transactions), 1)


class EntityUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.entity.component class.
    """

    def setUp(self):
        self.gl_structure = GeneralLedgerStructure(
            "NameA",
            description="DescriptionA")
        self.sales_acc = self.gl_structure._acci_sales_.create_account(
            "sales_default",
            "0000")
        self.cos_acc = self.gl_structure._acci_cos_.create_account(
            "cos_default",
            "0000")
        self.reva_acc = self.gl_structure["Other Income"].create_account(
            "RevA",
            number="011")
        self.expa_acc = self.gl_structure["Expense"].create_account(
            "ExpenseA",
            number="011")

        self.object = Entity("EntityA",
                             gl_structure=self.gl_structure,
                             description="DescriptionA")
        # Set up the needed objects
        self.comp1 = self.object.create_component("ComponentA1",
                                                  description="ca1")
        basic_activity = BasicActivity("BasicActivityA",
                                       description="DescriptionA",
                                       dt_account="Bank",
                                       cr_account="Sales",
                                       amount=5000,
                                       start=datetime(2016, 2, 1),
                                       end=datetime(2017, 2, 1),
                                       interval=1)
        self.comp1.add_activity(basic_activity)

        self.clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))

    def test_constructor(self):
        self.assertEqual(self.object.name, "EntityA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.gl.structure.name, self.gl_structure.name)
        self.assertEqual(self.object.period_count, -1)

    def test_set_parent_path(self):
        self.object.set_parent_path("/modelA")
        self.assertEqual(self.object.path, "/modelA/EntityA")

    def test_set_name(self):
        """
        Test wether the name changes when it is set, that the entity's
        name changes and that the component's children's paths are updated
        correctly.
        """

        self.object.set_parent_path("modelA")
        self.object.name = "NameAt"
        self.assertEqual(self.object.name, "NameAt")
        self.assertEqual(self.object.components[0].path,
                         "modelA/NameAt/ComponentA1")
        self.assertEqual(self.object.components[0].activities[0].path,
                         "modelA/NameAt/ComponentA1/BasicActivityA")

    def test_getitem_exists(self):
        self.assertEqual(
            self.comp1,
            self.object["ComponentA1"])

    def test_getitem_not_exists(self):
        self.assertRaises(IndexError, self.object.__getitem__, "ComponentA3")

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
        """
        Test that the entity run's its component' prepare_to_run methods.
        """

        # Test the prepare to run method before any run has been performed
        self.object.gl.create_transaction(
            "TestA",
            description="TestA_Desc",
            tx_date=datetime(2016, 2, 1).date(),
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
        """
        Test that the entity runs its components.
        """

        self.object.prepare_to_run(self.clock, 20)
        self.clock.tick()
        self.clock.tick()
        self.object.run(self.clock)
        self.assertEqual(len(self.object.gl.transactions), 1)
        self.assertEqual(self.object.gl.transactions[0].amount, 5000)

    def test__perform_year_end_gross_profit_and_income_summary(self):
        """
        Test that the year end gross profit and income summary accounts
        are summed up correctly.
        """

        gls = self.object.gl.structure
        year_end_datetime = datetime(2017, 2, 1)
        # Create the accounts to write of dict
        income_summary_write_off_accounts = collections.OrderedDict([
            (self.cos_acc, 700),
            (gls._acci_inc_tax_exp_acc_, -300),
            (self.sales_acc, 70),
            (gls._accb_bank_["Default"], -30)])
        gross_profit_write_off_accounts = collections.OrderedDict([
            (self.sales_acc, 70),
            (gls._accb_bank_["Default"], -30)])
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
                         gls._acci_gross_prof_.path)
        self.assertEqual(self.object.gl.transactions[2].cr_account,
                         gls._acci_inc_sum_.path)
        self.assertEqual(self.object.gl.transactions[2].tx_date,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[2].amount, 40)
        self.assertEqual(self.object.gl.transactions[2].is_closing_cr_account,
                         True)
        # When gross profit is negative:
        gross_profit_write_off_accounts = collections.OrderedDict([
            (self.sales_acc, -70),
            (gls._accb_bank_["Default"], 30)])
        del self.object.gl.transactions[:]  # Clear the tx list
        self.object._perform_year_end_gross_profit_and_income_summary(
            year_end_datetime,
            gross_profit_write_off_accounts, {})
        self.assertEqual(self.object.gl.transactions[2].dt_account,
                         gls._acci_inc_sum_.path)
        self.assertEqual(self.object.gl.transactions[2].cr_account,
                         gls._acci_gross_prof_.path)
        self.assertEqual(self.object.gl.transactions[2].tx_date,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[2].amount, 40)
        self.assertEqual(self.object.gl.transactions[2].is_closing_cr_account,
                         True)

    def test__perform_year_end_gross_profit(self):
        """
        Test that the year end gross profit account is closed correctly.
        """

        gls = self.object.gl.structure
        year_end_datetime = datetime(2017, 2, 1)

        # Create the accounts to write of dict
        gross_profit_write_off_accounts = collections.OrderedDict([
            (self.sales_acc, 70),
            (gls._accb_bank_["Default"], -30)])
        gross_profit = self.object._perform_year_end_gross_profit(
            year_end_datetime, gross_profit_write_off_accounts)
        self.assertEqual(len(self.object.gl.transactions), 2)
        # Expenses: 700-300 = 400
        # Other: 70-30 = 40
        # Total: gross_profit + Other - expenses: 5000 + 40 - 400 = 4640
        self.assertEqual(gross_profit, 40)

        # Test the "self.sales_acc: 70" transaction
        self.assertEqual(self.object.gl.transactions[0].dt_account,
                         gls._acci_gross_prof_.path)
        self.assertEqual(self.object.gl.transactions[0].cr_account,
                         self.sales_acc.path)
        self.assertEqual(self.object.gl.transactions[0].tx_date,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[0].amount, 70)
        self.assertEqual(self.object.gl.transactions[0].is_closing_cr_account,
                         True)

        # Test the "gls._accb_bank_["Default"]: -30" transaction
        self.assertEqual(self.object.gl.transactions[1].dt_account,
                         gls._accb_bank_["Default"].path)
        self.assertEqual(self.object.gl.transactions[1].cr_account,
                         gls._acci_gross_prof_.path)
        self.assertEqual(self.object.gl.transactions[1].tx_date,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[1].amount, 30)
        self.assertEqual(self.object.gl.transactions[1].is_closing_cr_account,
                         True)

    def test__perform_year_end_income_summary(self):
        """
        Test that the year end income summary account is closed correctly.
        """

        gls = self.object.gl.structure
        year_end_datetime = datetime(2017, 2, 1)
        gross_profit = 5000

        # Create the accounts to write of dict
        income_summary_write_off_accounts = collections.OrderedDict([
            (self.cos_acc, 700),
            (gls._acci_inc_tax_exp_acc_, -300),
            (self.sales_acc, 70),
            (gls._accb_bank_["Default"], -30)])
        income_summary_amount = self.object._perform_year_end_income_summary(
            year_end_datetime, gross_profit, income_summary_write_off_accounts)
        self.assertEqual(len(self.object.gl.transactions), 4)
        # Expenses: 700-300 = 400
        # Other: 70-30 = 40
        # Total: gross_profit + Other - expenses: 5000 + 40 - 400 = 4640
        self.assertEqual(income_summary_amount, 4640)

        # Test the "self.cos_acc: 700" transaction
        self.assertEqual(self.object.gl.transactions[0].dt_account,
                         gls._acci_inc_sum_.path)
        self.assertEqual(self.object.gl.transactions[0].cr_account,
                         self.cos_acc.path)
        self.assertEqual(self.object.gl.transactions[0].tx_date,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[0].amount, 700)
        self.assertEqual(self.object.gl.transactions[0].is_closing_cr_account,
                         True)

        # Test the "gls._acci_inc_tax_exp_acc_: -300" transaction
        self.assertEqual(self.object.gl.transactions[1].dt_account,
                         gls._acci_inc_tax_exp_acc_.path)
        self.assertEqual(self.object.gl.transactions[1].cr_account,
                         gls._acci_inc_sum_.path)
        self.assertEqual(self.object.gl.transactions[1].tx_date,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[1].amount, 300)
        self.assertEqual(self.object.gl.transactions[1].is_closing_cr_account,
                         True)

        # Test the "self.sales_acc: 70" transaction
        self.assertEqual(self.object.gl.transactions[2].dt_account,
                         self.sales_acc.path)
        self.assertEqual(self.object.gl.transactions[2].cr_account,
                         gls._acci_inc_sum_.path)
        self.assertEqual(self.object.gl.transactions[2].tx_date,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[2].amount, 70)
        self.assertEqual(self.object.gl.transactions[2].is_closing_cr_account,
                         True)

        # Test the "gls._accb_bank_["Default"]: -30" transaction
        self.assertEqual(self.object.gl.transactions[3].dt_account,
                         gls._acci_inc_sum_.path)
        self.assertEqual(self.object.gl.transactions[3].cr_account,
                         gls._accb_bank_["Default"].path)
        self.assertEqual(self.object.gl.transactions[3].tx_date,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[3].amount, 30)
        self.assertEqual(self.object.gl.transactions[3].is_closing_cr_account,
                         True)

    def test__perform_year_end_income_tax(self):
        # TODO
        pass

    def test__perform_year_end_retained_earnings(self):
        """
        Test that the year end retained earnings account is closed correctly.
        """

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
                         gls._acci_inc_sum_.path)
        self.assertEqual(self.object.gl.transactions[0].cr_account,
                         gls._accb_ret_earnings_acc_.path)
        self.assertEqual(self.object.gl.transactions[0].tx_date,
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
                         gls._accb_ret_earnings_acc_.path)
        self.assertEqual(self.object.gl.transactions[1].cr_account,
                         gls._acci_inc_sum_.path)
        self.assertEqual(self.object.gl.transactions[1].tx_date,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[1].amount,
                         income_summary)
        self.assertEqual(self.object.gl.transactions[1].is_closing_cr_account,
                         True)

    def test__perform_year_end_procedure(self):
        """
        Test that all the year end accounts has been closed of correctly.
        """

        gls = self.object.gl.structure
        # Test when that no year end transactions are created in the
        # middle of a year
        self.object.prepare_to_run(self.clock, 28)
        self.clock.timestep_ix = 6
        # create the transactions
        self.object.gl.create_transaction(
            "Sales_tx",
            description="Sales tx",
            tx_date=self.clock.get_datetime_at_period_ix(
                self.clock.timestep_ix),
            dt_account=gls._accb_bank_["Default"].path,  # Bank account
            cr_account=self.sales_acc.path,
            source=self.object.path,
            amount=70)
        # create the transactions
        self.object.gl.create_transaction(
            "Cost_of_Sales_tx",
            description="Cost of Sales tx",
            tx_date=self.clock.get_datetime_at_period_ix(
                self.clock.timestep_ix),
            dt_account=self.cos_acc.path,
            cr_account=gls._accb_bank_["Default"].path,  # Bank account
            source=self.object.path,
            amount=30)
        self.object._perform_year_end_procedure(self.clock)
        # Only one transaction should have been created and no
        # year end transactions.
        self.assertEqual(len(self.object.gl.transactions), 2)

        # Test that the year end procedure, at the year end, creates
        #   - two gross profit transactions with values of 70 and 40
        #   - one gross profit and income summary settle transaction
        #      with a value of 70 - 30
        #   - one retained earnings transaction with a value of 70 - 30
        # Only the 2 transaction (sales tx, and cost of sales tx) and the
        # 4 'year end' transactions should have been created.)
        self.clock.timestep_ix = 12
        self.object._perform_year_end_procedure(self.clock)

        self.assertEqual(len(self.object.gl.transactions), 6)
        self.assertEqual(self.object.gl.transactions[2].amount, 70)
        self.assertEqual(self.object.gl.transactions[2].is_closing_cr_account,
                         True)
        self.assertEqual(self.object.gl.transactions[2].dt_account,
                         gls._acci_gross_prof_.path)
        self.assertEqual(self.object.gl.transactions[2].cr_account,
                         self.sales_acc.path)

        self.assertEqual(self.object.gl.transactions[3].amount, 30)
        self.assertEqual(self.object.gl.transactions[3].is_closing_cr_account,
                         True)
        self.assertEqual(self.object.gl.transactions[3].dt_account,
                         self.cos_acc.path)
        self.assertEqual(self.object.gl.transactions[3].cr_account,
                         gls._acci_gross_prof_.path)

        self.assertEqual(self.object.gl.transactions[4].amount, 40)
        self.assertEqual(self.object.gl.transactions[4].is_closing_cr_account,
                         True)
        self.assertEqual(self.object.gl.transactions[4].dt_account,
                         gls._acci_gross_prof_.path)
        self.assertEqual(self.object.gl.transactions[4].cr_account,
                         gls._acci_inc_sum_.path)

        self.assertEqual(self.object.gl.transactions[5].amount, 40)
        self.assertEqual(self.object.gl.transactions[5].is_closing_cr_account,
                         True)
        self.assertEqual(self.object.gl.transactions[5].dt_account,
                         gls._acci_inc_sum_.path)
        self.assertEqual(self.object.gl.transactions[5].cr_account,
                         gls._accb_ret_earnings_acc_.path)

        # Test for a new year
        self.clock.timestep_ix = 18
        # Test for when other revenue and expense accounts transactions
        # exists as well.

        # create a sales transactions
        self.object.gl.create_transaction(
            "SalesTx2",
            description="Sales tx2",
            tx_date=self.clock.get_datetime_at_period_ix(
                self.clock.timestep_ix),
            dt_account=gls._accb_bank_["Default"].path,  # Bank account
            cr_account=self.sales_acc.path,
            source=self.object.path,
            amount=45)
        self.object.gl.create_transaction(
            "SalesTx3",
            description="Sales tx3",
            tx_date=self.clock.get_datetime_at_period_ix(
                self.clock.timestep_ix),
            dt_account=gls._accb_bank_["Default"].path,  # Bank account
            cr_account=self.sales_acc.path,
            source=self.object.path,
            amount=35)
        self.object.gl.create_transaction(
            "Cost_of_Sales_tx2",
            description="Cost of Sales tx 2",
            tx_date=self.clock.get_datetime_at_period_ix(
                self.clock.timestep_ix),
            dt_account=self.cos_acc.path,
            cr_account=gls._accb_bank_["Default"].path,  # Bank account
            source=self.object.path,
            amount=15)
        self.object.gl.create_transaction(
            "Cost_of_Sales_tx3",
            description="Cost of Sales tx 3",
            tx_date=self.clock.get_datetime_at_period_ix(
                self.clock.timestep_ix),
            dt_account=self.cos_acc.path,
            cr_account=gls._accb_bank_["Default"].path,  # Bank account
            source=self.object.path,
            amount=5)
        # create the transactions
        self.object.gl.create_transaction(
            "revenueATx",
            description="revenue a tx",
            tx_date=self.clock.get_datetime_at_period_ix(
                self.clock.timestep_ix),
            dt_account=gls._accb_bank_["Default"].path,  # Bank account
            cr_account=self.reva_acc.path,
            source=self.object.path,
            amount=450)
        self.object.gl.create_transaction(
            "revenueATx2",
            description="revenue a tx2",
            tx_date=self.clock.get_datetime_at_period_ix(
                self.clock.timestep_ix),
            dt_account=gls._accb_bank_["Default"].path,  # Bank account
            cr_account=self.reva_acc.path,
            source=self.object.path,
            amount=350)
        # create the transactions
        self.object.gl.create_transaction(
            "expenseAtx",
            description="expense a tx",
            tx_date=self.clock.get_datetime_at_period_ix(
                self.clock.timestep_ix),
            dt_account=self.expa_acc.path,
            cr_account=gls._accb_bank_["Default"].path,  # Bank account
            source=self.object.path,
            amount=320)
        self.object.gl.create_transaction(
            "expenseAtx2",
            description="expense a tx2",
            tx_date=self.clock.get_datetime_at_period_ix(
                self.clock.timestep_ix),
            dt_account=self.expa_acc.path,
            cr_account=gls._accb_bank_["Default"].path,  # Bank account
            source=self.object.path,
            amount=180)

        # Test that the year end procedure, at the year end, creates
        #   - two gross profit transactions with values of 80 and 20
        #   - two income summary transactions with values of 800 and 500
        #   - one gross profit and income summary settle transaction
        #      with a value of 80 - 20
        #   - one retained earnings transaction with a value of
        #      800 - 500 + 80 - 20
        # Only the 6 transactions (2 sales tx, 2 cost of sales,
        # 2 revenue a and 2 expense a) and the 5 'year end' transactions
        # should have been created.)
        self.clock.timestep_ix = 24
        self.object._perform_year_end_procedure(self.clock)

        self.assertEqual(len(self.object.gl.transactions), 20)
        self.assertEqual(self.object.gl.transactions[14].amount, 80)
        self.assertEqual(self.object.gl.transactions[14].is_closing_cr_account,
                         True)
        self.assertEqual(self.object.gl.transactions[14].dt_account,
                         gls._acci_gross_prof_.path)
        self.assertEqual(self.object.gl.transactions[14].cr_account,
                         self.sales_acc.path)

        self.assertEqual(self.object.gl.transactions[15].amount, 20)
        self.assertEqual(self.object.gl.transactions[15].is_closing_cr_account,
                         True)
        self.assertEqual(self.object.gl.transactions[15].dt_account,
                         self.cos_acc.path)
        self.assertEqual(self.object.gl.transactions[15].cr_account,
                         gls._acci_gross_prof_.path)

        self.assertEqual(self.object.gl.transactions[16].amount, 800)
        self.assertEqual(self.object.gl.transactions[16].is_closing_cr_account,
                         True)
        self.assertEqual(self.object.gl.transactions[16].dt_account,
                         self.reva_acc.path)
        self.assertEqual(self.object.gl.transactions[16].cr_account,
                         gls._acci_inc_sum_.path)

        self.assertEqual(self.object.gl.transactions[17].amount, 500)
        self.assertEqual(self.object.gl.transactions[17].is_closing_cr_account,
                         True)
        self.assertEqual(self.object.gl.transactions[17].dt_account,
                         gls._acci_inc_sum_.path)
        self.assertEqual(self.object.gl.transactions[17].cr_account,
                         self.expa_acc.path)

        self.assertEqual(self.object.gl.transactions[18].amount, 60)
        self.assertEqual(self.object.gl.transactions[18].is_closing_cr_account,
                         True)
        self.assertEqual(self.object.gl.transactions[18].dt_account,
                         gls._acci_gross_prof_.path)
        self.assertEqual(self.object.gl.transactions[18].cr_account,
                         gls._acci_inc_sum_.path)

        self.assertEqual(self.object.gl.transactions[19].amount, 360)
        self.assertEqual(self.object.gl.transactions[19].is_closing_cr_account,
                         True)
        self.assertEqual(self.object.gl.transactions[19].dt_account,
                         gls._acci_inc_sum_.path)
        self.assertEqual(self.object.gl.transactions[19].cr_account,
                         gls._accb_ret_earnings_acc_.path)


if __name__ == '__main__':
    unittest.main()
