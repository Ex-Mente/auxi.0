# -*- coding: utf-8 -*-
"""
This module provides a entity class rrepresenting a business entity.
an entity consists of business components e.g. Sales department.\n

@name: entity
@author: Ex Mente Technologies (Pty) Ltd
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
from auxi.core.namedobject import NamedObject
from auxi.modeling.business.component import Component
from auxi.modeling.financial.des.generalledgeraccount import AccountType
from auxi.modeling.financial.des.generalledger import GeneralLedger
from auxi.modeling.financial.tax.ruleset import RuleSet

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class Entity(NamedObject):
    """Represents an entity class."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, gl_structure, description=None):
        """Initialise the object.

        :param name: The name.
        :param gl_structure: The general ledger structure the entity's general ledger will be initialized with.
        :param description: The description.
        :param period_count: The number of periods the entity should be run for.
        """
        self.gl = GeneralLedger(
            "General Ledger",
            gl_structure,
            description="General Ledger")
        self._parent_path = ""
        self.path = name
        self.components = []
        self.tax_rule_set = RuleSet("Default")
        self.negative_income_tax_total = 0
        self._prev_year_end_datetime = datetime.min
        self._curr_year_end_datetime = datetime.min
        self._exec_year_end_datetime = datetime.min
        self.period_count = -1
        super().__init__(name, description=description)

    def set_parent_path(self, value):
        """Set the parent path and the path from the new parent path.

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
        """Create a component in the business entity.

        :param name: The account name.
        :param description: The account description.

        :returns: The created component.
        """
        new_comp = Component(name, description=description)
        self.components.append(new_comp)
        return new_comp

    def remove_component(self, name):
        """Remove a component from the entity.

        :param name: The name of the component to remove.
        """
        component_to_remove = None
        for c in self.components:
            if c.name == name:
                component_to_remove = c
        if component_to_remove is not None:
            self.components.remove(component_to_remove)

    def prepare_to_run(self, clock, period_count):
        """Prepare the component for execution.

        :param clock: The clock containing the execution start time and execution period information.
        :param period_count: The total amount of periods this activity will be requested to be run for.
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
        """Execute the component at the current clock cycle.

        :param clock: The clock containing the current execution time and period information.
        """
        if clock.timestep_ix >= self.period_count:
            return

        for c in self.components:
            c.run(clock, self.gl)

        self._perform_year_end_procedure(clock)

    def _perform_year_end_procedure(self, clock):
        pass

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
            tx_name = "Settle the '" + gls.gross_profit_account.name +\
             "' Account"
            new_tx = self.gl.create_transaction(
                tx_name,
                description=tx_name,
                tx_datetime=year_end_datetime,
                dt_account=dt_account,
                cr_account=cr_account,
                source=self.path,
                amount=abs(gross_profit))
            new_tx.is_closing_cr_account = True

        if gross_profit > 0:
            create_tx(gls.gross_profit_account.name,
                      gls.incomesummary_account.name)
        elif gross_profit < 0:
            create_tx(gls.incomesummary_account.name,
                      gls.gross_profit_account.name)

        return income_summary_amount

    def _perform_year_end_gross_profit(self,
                                       year_end_datetime,
                                       gross_profit_write_off_accounts):
        gls = self.gl.structure
        gross_profit = 0

        for acc, amount in gross_profit_write_off_accounts.items():
            def create_tx(dt_account, cr_account):
                tx_name = "Settle the '" + acc.name + "' Account"
                new_tx = self.gl.create_transaction(
                    tx_name,
                    description=tx_name,
                    tx_datetime=year_end_datetime,
                    dt_account=dt_account,
                    cr_account=cr_account,
                    source=self.path,
                    amount=abs(amount))
                new_tx.is_closing_cr_account = True

            gross_profit += amount
            if amount > 0:
                create_tx(gls.gross_profit_account.name, acc.name)
            elif amount < 0:
                create_tx(acc.name, gls.gross_profit_account.name)
        return gross_profit

    def _perform_year_end_income_summary(self,
                                         year_end_datetime,
                                         gross_profit,
                                         income_summary_write_off_accounts):
        gls = self.gl.structure
        income_summary_amount = gross_profit

        for acc, amount in income_summary_write_off_accounts.items():
            def create_tx(dt_account, cr_account):
                tx_name = "Settle the '" + acc.name + "' Account"
                new_tx = self.gl.create_transaction(
                    tx_name,
                    description=tx_name,
                    tx_datetime=year_end_datetime,
                    dt_account=dt_account,
                    cr_account=cr_account,
                    source=self.path,
                    amount=abs(amount))
                new_tx.is_closing_cr_account = True

            if amount > 0:
                if acc.account_type == AccountType.expense:
                    income_summary_amount -= amount
                    create_tx(gls.incomesummary_account.name, acc.name)
                else:
                    income_summary_amount += amount
                    create_tx(acc.name, gls.incomesummary_account.name)
            elif amount < 0:
                if acc.account_type == AccountType.expense:
                    income_summary_amount -= amount
                    create_tx(acc.name, gls.incomesummary_account.name)
                else:
                    income_summary_amount += amount
                    create_tx(gls.incomesummary_account.name, acc.name)
        return income_summary_amount

    def _perform_year_end_income_tax(self,
                                     year_end_datetime,
                                     income_summary_amount):
        pass

    def _perform_year_end_retained_earnings(self,
                                            year_end_datetime,
                                            income_summary_amount):
        def create_tx(dt_account, cr_account):
            tx_name = "Settle the '" + gls.incomesummary_account.name +\
                      "' Account, adjust Retained Earnings accordingly."
            new_tx = self.gl.create_transaction(
                tx_name,
                description=tx_name,
                tx_datetime=year_end_datetime,
                dt_account=dt_account,
                cr_account=cr_account,
                source=self.path,
                amount=income_summary_amount)
            new_tx.is_closing_cr_account = True
        gls = self.gl.structure

        if income_summary_amount > 0:
            create_tx(gls.incomesummary_account.name,
                      gls.retainedearnings_account.name)
        elif income_summary_amount < 0:
            create_tx(gls.retainedearnings_account.name,
                      gls.incomesummary_account.name)
