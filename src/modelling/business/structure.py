#!/usr/bin/env python3
"""
This module provides an classes used to create a business structure.
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import OrderedDict

from auxi.core.objects import NamedObject
from auxi.modelling.financial.des import AccountType
from auxi.modelling.financial.des import GeneralLedger


__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class Activity(NamedObject):
    """
    Represents an activity base class. An activity will typically
    represent a transaction activity in a business.

    :param name: The name.
    :param description: The description.
    :param start: The datetime the activity should be started.
    :param end: The datetime the activity should be run until.
    :param interval: The interval of the activity.
    """

    def __init__(self, name,
                 start=datetime.min, end=datetime.max,
                 interval=1,
                 description=None):
        self._parent_path = ""
        super(Activity, self).__init__(name, description)
        self.start_datetime = self._get_date_(start)
        self.end_datetime = self._get_date_(end)
        self.interval = interval
        self.start_period_ix = -1
        self.end_period_ix = -1
        self.period_count = -1

    def _get_date_(self, date):
        if type(date) is str:
            return datetime.strptime(date, '%Y-%m-%d')
        else:
            return date

    def set_parent_path(self, value):
        """
        Set the parent path and the path from the new parent path.

        :param value: The path to the object's parent
        """

        self._parent_path = value
        self.path = value + r'/' + self.name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.path = self._parent_path + r'/' + self.name

    def _meet_execution_criteria(self, ix_period):
        if self.interval != 0 and (ix_period+1) % self.interval != 0:
            return False
        return ix_period >= self.start_period_ix and \
            ix_period + self.interval  <= self.end_period_ix

    def prepare_to_run(self, clock, period_count):
        """
        Prepare the activity for execution.

        :param clock: The clock containing the execution start time and
          execution period information.
        :param period_count: The total amount of periods this activity will be
          requested to be run for.
        """

        if self.start_period_ix == -1 and self.start_datetime != datetime.min:
            # Set the Start period index
            for i in range(0, period_count):
                if clock.get_datetime_at_period_ix(i) > self.start_datetime:
                    self.start_period_ix = i
                    break
        if self.start_period_ix == -1:
            self.start_period_ix = 0
        if self.period_count == -1 and self.end_datetime != datetime.max:
            # Set the Start date
            for i in range(0, period_count):
                if clock.get_datetime_at_period_ix(i) > self.end_datetime:
                    self.period_count = i - self.start_period_ix
                    break
        if self.period_count != -1:
            self.end_period_ix = self.start_period_ix + self.period_count
        else:
            self.end_period_ix = self.start_period_ix + period_count

    def get_referenced_accouts(self):
        """
        Retrieve the general ledger accounts referenced in this instance.

        :returns: The referenced accounts.
        """

        return []


class Component(NamedObject):
    """
    Represents an component class. A component class that represents a
    component of an entity. A component has business activities

    :param name: The name.
    :param description: The description.
    """

    def __init__(self, name, gl, description=None):
        self._parent_path = ""
        self.path = name
        self.gl = gl
        self.components = []
        self.activities = []
        super(Component, self).__init__(name, description=description)

    def __getitem__(self, name):
        return self.get_component(name)

    def __call__(self, name):
        return self.get_activity(name)

    def set_parent_path(self, value):
        """
        Set the parent path and the path from the new parent path.

        :param value: The path to the object's parent.
        """

        self._parent_path = value
        self.path = value + r'/' + self.name
        self._update_childrens_parent_path()

    def _update_childrens_parent_path(self):
        for c in self.components:
            c.set_parent_path(self.path)
        for a in self.activities:
            a.set_parent_path(self.path)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.path = self._parent_path + r'/' + self.name
        self._update_childrens_parent_path()

    def create_component(self, name, description=None):
        """
        Create a sub component in the business component.

        :param name: The new component's name.
        :param description: The new component's description.

        :returns: The created component.
        """

        new_comp = Component(name, self.gl, description=description)
        new_comp.set_parent_path(self.path)
        self.components.append(new_comp)
        return new_comp

    def remove_component(self, name):
        """
        Remove a sub component from the component.

        :param name: The name of the component to remove.
        """

        component_to_remove = None
        for c in self.components:
            if c.name == name:
                component_to_remove = c
        if component_to_remove is not None:
            self.components.remove(component_to_remove)

    def get_component(self, name):
        """
        Retrieve a child component given its name.

        :param name: The name of the component.

        :returns: The component.
        """

        return [c for c in self.components if c.name == name][0]

    def add_activity(self, activity):
        """
        Add an activity to the component.

        :param activity: The activity.
        """

        self.gl.structure.validate_account_names(
            activity.get_referenced_accounts())
        self.activities.append(activity)
        activity.set_parent_path(self.path)

    def get_activity(self, name):
        """
        Retrieve an activity given its name.

        :param name: The name of the activity.

        :returns: The activity.
        """

        return [a for a in self.activities if a.name == name][0]

    def prepare_to_run(self, clock, period_count):
        """
        Prepare the component for execution.

        :param clock: The clock containing the execution start time and
          execution period information.
        :param period_count: The total amount of periods this activity will be
          requested to be run for.
        """

        for c in self.components:
            c.prepare_to_run(clock, period_count)
        for a in self.activities:
            a.prepare_to_run(clock, period_count)

    def run(self, clock, generalLedger):
        """
        Execute the component at the current clock cycle.

        :param clock: The clock containing the current execution time and
          period information.
        :param generalLedger: The general ledger into which to create the
          transactions.
        """

        for c in self.components:
            c.run(clock, generalLedger)
        for a in self.activities:
            a.run(clock, generalLedger)


class Entity(NamedObject):
    """
    Represents an entity class. An entity consists of business components
    e.g. Sales department. It executes its components and performs
    financial year end transcations.

    :param name: The name.
    :param gl_structure: The general ledger structure the entity's
      general ledger will be initialized with.
    :param description: The description.
    :param period_count: The number of periods the entity should be run for.
    """

    def __init__(self, name, gl_structure, description=None):
        self.gl = GeneralLedger(
            "General Ledger",
            gl_structure,
            description="General Ledger")
        self._parent_path = ""
        self.path = name
        self.components = []
        self.negative_income_tax_total = 0
        self._prev_year_end_datetime = datetime.min
        self._curr_year_end_datetime = datetime.min
        self._exec_year_end_datetime = datetime.min
        self.period_count = -1
        super(Entity, self).__init__(name, description=description)

    def __getitem__(self, key):
        return [c for c in self.components if c.name == key][0]

    def set_parent_path(self, value):
        """
        Set the parent path and the path from the new parent path.

        :param value: The path to the object's parent
        """

        self._parent_path = value
        self.path = value + r'/' + self.name
        self._update_childrens_parent_path()

    def _update_childrens_parent_path(self):
        for c in self.components:
            c.set_parent_path(self.path)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.path = self._parent_path + r'/' + self.name
        self._update_childrens_parent_path()

    def create_component(self, name, description=None):
        """
        Create a component in the business entity.

        :param name: The component's name.
        :param description: The component's description.

        :returns: The created component.
        """

        new_comp = Component(name, self.gl, description=description)
        new_comp.set_parent_path(self.path)
        self.components.append(new_comp)
        return new_comp

    def remove_component(self, name):
        """
        Remove a component from the entity.

        :param name: The name of the component to remove.
        """

        component_to_remove = None
        for c in self.components:
            if c.name == name:
                component_to_remove = c
        if component_to_remove is not None:
            self.components.remove(component_to_remove)

    def prepare_to_run(self, clock, period_count):
        """
        Prepare the entity for execution.

        :param clock: The clock containing the execution start time and
          execution period information.
        :param period_count: The total amount of periods this activity will be
          requested to be run for.
        """

        self.period_count = period_count

        self._exec_year_end_datetime = clock.get_datetime_at_period_ix(
            period_count)
        self._prev_year_end_datetime = clock.start_datetime
        self._curr_year_end_datetime = clock.start_datetime + relativedelta(
            years=1)

        # Remove all the transactions
        del self.gl.transactions[:]

        for c in self.components:
            c.prepare_to_run(clock, period_count)

        self.negative_income_tax_total = 0

    def run(self, clock):
        """
        Execute the entity at the current clock cycle.

        :param clock: The clock containing the current execution time and
          period information.
        """

        if clock.timestep_ix >= self.period_count:
            return

        for c in self.components:
            c.run(clock, self.gl)

        self._perform_year_end_procedure(clock)

    def _perform_year_end_procedure(self, clock):
        if clock.get_datetime() >= self._curr_year_end_datetime\
         or clock.timestep_ix == self.period_count:
            gls = self.gl.structure
            year_start_date = self._prev_year_end_datetime
            year_end_date = self._curr_year_end_datetime + \
                timedelta(seconds=-1)

            self._prev_year_end_datetime = self._curr_year_end_datetime
            self._curr_year_end_datetime += relativedelta(years=1)
            if self._curr_year_end_datetime > self._exec_year_end_datetime:
                self._curr_year_end_datetime = self._exec_year_end_datetime

            gross_profit_write_off_accs = OrderedDict()
            inc_summary_write_off_accs = OrderedDict()
            sales_accs = gls.get_account_decendants(gls._acci_sales_)
            cost_of_sales_accs = gls.get_account_decendants(gls._acci_cos_)
            year_taxes = []
            for tx in self.gl.transactions:
                if tx.tx_date >= year_start_date and\
                 tx.tx_date <= year_end_date:
                    year_taxes.append(tx)
            for tx in year_taxes:
                cr_acc = gls.get_account(tx.cr_account)
                dt_acc = gls.get_account(tx.dt_account)

                if cr_acc in sales_accs:
                    if cr_acc in gross_profit_write_off_accs:
                        gross_profit_write_off_accs[cr_acc] += tx.amount
                    else:
                        gross_profit_write_off_accs[cr_acc] = tx.amount
                elif dt_acc in sales_accs:
                    if dt_acc in gross_profit_write_off_accs:
                        gross_profit_write_off_accs[dt_acc] -= tx.amount
                    else:
                        gross_profit_write_off_accs[dt_acc] = -tx.amount

                elif cr_acc in cost_of_sales_accs:
                    if cr_acc in gross_profit_write_off_accs:
                        gross_profit_write_off_accs[cr_acc] += tx.amount
                    else:
                        gross_profit_write_off_accs[cr_acc] = tx.amount
                elif dt_acc in cost_of_sales_accs:
                    if dt_acc in gross_profit_write_off_accs:
                        gross_profit_write_off_accs[dt_acc] -= tx.amount
                    else:
                        gross_profit_write_off_accs[dt_acc] = -tx.amount

                elif cr_acc.account_type == AccountType.revenue:
                    if cr_acc in inc_summary_write_off_accs:
                        inc_summary_write_off_accs[cr_acc] += tx.amount
                    else:
                        inc_summary_write_off_accs[cr_acc] = tx.amount
                elif dt_acc.account_type == AccountType.revenue:
                    if dt_acc.account_type == AccountType.revenue:
                        inc_summary_write_off_accs[dt_acc] -= tx.amount
                    else:
                        inc_summary_write_off_accs[dt_acc] = -tx.amount

                elif cr_acc.account_type == AccountType.expense:
                    if cr_acc in inc_summary_write_off_accs:
                        inc_summary_write_off_accs[cr_acc] -= tx.amount
                    else:
                        inc_summary_write_off_accs[cr_acc] = -tx.amount
                elif dt_acc.account_type == AccountType.expense:
                    if dt_acc in inc_summary_write_off_accs:
                        inc_summary_write_off_accs[dt_acc] += tx.amount
                    else:
                        inc_summary_write_off_accs[dt_acc] = tx.amount

            inc_sum = self._perform_year_end_gross_profit_and_income_summary(
                year_end_date,
                gross_profit_write_off_accs,
                inc_summary_write_off_accs)
            inc_sum = self._perform_year_end_income_tax(
                year_end_date,
                inc_sum)
            self._perform_year_end_retained_earnings(
                year_end_date,
                inc_sum)

    def _perform_year_end_gross_profit_and_income_summary(
            self,
            year_end_datetime,
            gross_profit_write_off_accounts,
            income_summary_write_off_accounts):
        gls = self.gl.structure
        gross_profit = self._perform_year_end_gross_profit(
            year_end_datetime,
            gross_profit_write_off_accounts)
        income_summary_amount = self._perform_year_end_income_summary(
            year_end_datetime,
            gross_profit,
            income_summary_write_off_accounts)

        def create_tx(dt_account, cr_account):
            tx_name = "Settle the '" + gls._acci_gross_prof_.path +\
             "' Account"
            new_tx = self.gl.create_transaction(
                tx_name,
                description=tx_name,
                tx_date=year_end_datetime,
                dt_account=dt_account,
                cr_account=cr_account,
                source=self.path,
                amount=abs(gross_profit))
            new_tx.is_closing_cr_account = True

        if gross_profit > 0:
            create_tx(gls._acci_gross_prof_.path,
                      gls._acci_inc_sum_.path)
        elif gross_profit < 0:
            create_tx(gls._acci_inc_sum_.path,
                      gls._acci_gross_prof_.path)

        return income_summary_amount

    def _perform_year_end_gross_profit(self,
                                       year_end_datetime,
                                       gross_profit_write_off_accounts):
        gls = self.gl.structure
        gross_profit = 0

        for acc, amount in gross_profit_write_off_accounts.items():
            def create_tx(dt_account, cr_account):
                tx_name = "Settle the '" + acc.path + "' Account"
                new_tx = self.gl.create_transaction(
                    tx_name,
                    description=tx_name,
                    tx_date=year_end_datetime,
                    dt_account=dt_account,
                    cr_account=cr_account,
                    source=self.path,
                    amount=abs(amount))
                new_tx.is_closing_cr_account = True

            gross_profit += amount
            if amount > 0:
                create_tx(gls._acci_gross_prof_.path, acc.path)
            elif amount < 0:
                create_tx(acc.path, gls._acci_gross_prof_.path)
        return gross_profit

    def _perform_year_end_income_summary(self,
                                         year_end_datetime,
                                         gross_profit,
                                         income_summary_write_off_accounts):
        gls = self.gl.structure
        income_summary_amount = gross_profit

        for acc, amount in income_summary_write_off_accounts.items():
            def create_tx(dt_account, cr_account):
                tx_name = "Settle the '" + acc.path + "' Account"
                new_tx = self.gl.create_transaction(
                    tx_name,
                    description=tx_name,
                    tx_date=year_end_datetime,
                    dt_account=dt_account,
                    cr_account=cr_account,
                    source=self.path,
                    amount=abs(amount))
                new_tx.is_closing_cr_account = True

            if amount > 0:
                if acc.account_type == AccountType.expense:
                    income_summary_amount -= amount
                    create_tx(gls._acci_inc_sum_.path, acc.path)
                else:
                    income_summary_amount += amount
                    create_tx(acc.path, gls._acci_inc_sum_.path)
            elif amount < 0:
                if acc.account_type == AccountType.expense:
                    income_summary_amount -= amount
                    create_tx(acc.path, gls._acci_inc_sum_.path)
                else:
                    income_summary_amount += amount
                    create_tx(gls._acci_inc_sum_.path, acc.path)
        return income_summary_amount

    def _perform_year_end_income_tax(self,
                                     year_end_datetime,
                                     income_summary_amount):
        return income_summary_amount

    def _perform_year_end_retained_earnings(self,
                                            year_end_datetime,
                                            income_summary_amount):
        def create_tx(dt_account, cr_account):
            tx_name = "Settle the '" + gls._acci_inc_sum_.path +\
                      "' Account, adjust Retained Earnings accordingly."
            new_tx = self.gl.create_transaction(
                tx_name,
                description=tx_name,
                tx_date=year_end_datetime,
                dt_account=dt_account,
                cr_account=cr_account,
                source=self.path,
                amount=income_summary_amount)
            new_tx.is_closing_cr_account = True
        gls = self.gl.structure

        if income_summary_amount > 0:
            create_tx(gls._acci_inc_sum_.path,
                      gls._accb_ret_earnings_acc_.path)
        elif income_summary_amount < 0:
            create_tx(gls._accb_ret_earnings_acc_.path,
                      gls._acci_inc_sum_.path)


if __name__ == "__main__":
    import unittest
    from auxi.modelling.business.structure_test import ActivityUnitTester
    from auxi.modelling.business.structure_test import ComponentUnitTester
    from auxi.modelling.business.structure_test import EntityUnitTester
    unittest.main()
