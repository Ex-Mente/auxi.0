#!/usr/bin/env python3
"""
This module provides class and functions for basic business activities.
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

from auxi.modelling.business.structure import Activity

__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class BasicActivity(Activity):
    """
    An activity class that provides the most basic activity functionality:
    periodically create a transaction between two specified accounts.

    :param name: The name.
    :param dt_account: The debit account.
    :param cr_account: The credit account.
    :param amount: The amount of an activity.
    :param start: The datetime the activity should be started.
    :param end: The datetime the activity should be run until.
    :param interval: The interval of the activity.
    :param description: The description.
    """

    def __init__(self, name,
                 dt_account,
                 cr_account,
                 amount=0,
                 start=datetime.min,
                 end=datetime.max,
                 interval=1,
                 description=None):
        """
        """
        super(BasicActivity, self).__init__(
            name,
            description=description,
            start=start,
            end=end,
            interval=interval)
        self.interval = interval
        self.amount = amount
        self.dt_account = dt_account
        self.cr_account = cr_account

    def _meet_execution_criteria(self, ix_period):
        return super(BasicActivity, self)._meet_execution_criteria(
            ix_period) and self.amount > 0

    def run(self, clock, generalLedger):
        """
        Execute the activity at the current clock cycle.

        :param clock: The clock containing the current execution time and
          period information.
        :param generalLedger: The general ledger into which to create the
          transactions.
        """

        if not self._meet_execution_criteria(clock.timestep_ix):
            return

        generalLedger.create_transaction(
            self.description if self.description is not None else self.name,
            description='',
            tx_date=clock.get_datetime(),
            dt_account=self.dt_account,
            cr_account=self.cr_account,
            source=self.path,
            amount=self.amount)

    def get_referenced_accounts(self):
        """
        Retrieve the general ledger accounts referenced in this instance.

        :returns: The referenced accounts.
        """

        return [self.dt_account, self.cr_account]

'''
class BasicEquipment(Activity):
    """
    An activity class that provides a basic activity functionality for
    a purchase of equipment. This includes the purchase and depreciation
    thereafter.

    :param name: The name.
    :param description: The description.
    :param bank_account: The asset account that is decreased.
    :param equipment_account: The fixed asset account that is increased.
    :param depreciation_account: The expense account that is increased.
    :param purchase_amount: The purchase amount. The default amount is 0.
    :param writeoff_amount: The writeoff amount. The default amount is 0.
    :param depreciation_rate: The rate of depreciation as fraction of the whole
      (e.g. 0.15 = 15%). The default value is 0.0.
    :param start: The datetime the activity should be started.
    :param lifetime: The amount of months the equipment can exists before
      writing it off.
    :param interval: The interval of the activity.
    """

    def __init__(self, name,
                 bank_account,
                 loan_account,
                 interest_account,
                 purchase_amount=0,
                 writeoff_amount=0,
                 depreciation_rate=0.0,
                 start=datetime.min,
                 lifetime=60,
                 interval=1,
                 description=None):
        """
        """
        super(BasicEquipment, self).__init__(
            name,
            description=description,
            start=start,
            end=start + relativedelta(months=duration),
            interval=interval)
        self.bank_account = bank_account
        self.loan_account = loan_account
        self.interest_account = interest_account
        self._amount = amount
        self.duration = duration
        self.interest_rate = interest_rate

        self._months_executed = 0
        self._amount_left = amount
'''


class BasicLoanActivity(Activity):
    """
    An activity class that provides the most basic activity functionality for
    a loan:
    Creates a loan transaction and periodically create transactions to consider
    the interest and to pay the interest.

    :param name: The name.
    :param description: The description.
    :param bank_account: The asset account that is increased.
    :param loan_account: The liability account that is decreased.
    :param interest_account: The expense account the interest is
      added to.
    :param amount: The loan amount. The default amount is 0
    :param interest_rate: The interest rate as a fraction of the whole
      (e.g. 0.15 = 15%). The default value is 0.0
    :param start: The datetime the activity should be started.
    :param duration: The duration of the loan in months.
    :param interval: The interval of the activity.
    """

    def __init__(self, name,
                 bank_account,
                 loan_account,
                 interest_account,
                 amount=0,
                 interest_rate=0.0,
                 start=datetime.min,
                 duration=60,
                 interval=1,
                 description=None):
        """
        """
        super(BasicLoanActivity, self).__init__(
            name,
            description=description,
            start=start,
            end=start + relativedelta(months=duration+1),
            interval=interval)
        self.bank_account = bank_account
        self.loan_account = loan_account
        self.interest_account = interest_account
        self._amount = amount
        self.duration = duration
        self.interest_rate = interest_rate

        self._months_executed = 0
        self._amount_left = amount

    def _update_montly_payment_(self):
        int_rate = self._montly_interest_rate
        val = (self.amount * int_rate)
        val = val / (1 - (1 / pow((1 + int_rate), self.duration)))
        self._monthly_payment = val

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value
        self._update_montly_payment_()

    @property
    def interest_rate(self):
        return self._interest_rate

    @interest_rate.setter
    def interest_rate(self, value):
        self._interest_rate = value
        self._montly_interest_rate = value / 12.0
        self._update_montly_payment_()

    def _meet_execution_criteria(self, ix_period):
        return super(BasicLoanActivity, self)._meet_execution_criteria(
            ix_period) and self.amount > 0 and self.duration > 0

    def prepare_to_run(self, clock, period_count):
        """
        Prepare the activity for execution.

        :param clock: The clock containing the execution start time and
          execution period information.
        :param period_count: The total amount of periods this activity will be
          requested to be run for.
        """

        super(BasicLoanActivity, self).prepare_to_run(clock, period_count)

        self._months_executed = 0
        self._amount_left = self.amount

    def run(self, clock, generalLedger):
        """
        Execute the activity at the current clock cycle.

        :param clock: The clock containing the current execution time and
          period information.
        :param generalLedger: The general ledger into which to create the
          transactions.
        """

        if not self._meet_execution_criteria(clock.timestep_ix):
            return

        if self.description is None:
            tx_name = self.name
        else:
            tx_name = self.description

        if self._months_executed == 0:
            generalLedger.create_transaction(
                tx_name,
                description='Make a loan',
                tx_date=clock.get_datetime(),
                dt_account=self.bank_account,
                cr_account=self.loan_account,
                source=self.path,
                amount=self.amount)
        else:
            curr_interest_amount = (self._amount_left *
                                    self.interest_rate) / 12.0

            generalLedger.create_transaction(
                tx_name,
                description='Consider interest',
                tx_date=clock.get_datetime(),
                dt_account=self.interest_account,
                cr_account=self.loan_account,
                source=self.path,
                amount=curr_interest_amount)

            generalLedger.create_transaction(
                tx_name,
                description='Pay principle',
                tx_date=clock.get_datetime(),
                dt_account=self.loan_account,
                cr_account=self.bank_account,
                source=self.path,
                amount=self._monthly_payment)

            self._amount_left += curr_interest_amount - self._monthly_payment

        self._months_executed += self.interval

    def get_referenced_accounts(self):
        """
        Retrieve the general ledger accounts referenced in this instance.

        :returns: The referenced accounts.
        """

        return [
            self.bank_account,
            self.loan_account,
            self.interest_account]


if __name__ == "__main__":
    import unittest
    from auxi.modelling.business.basic_test import BasicActivityUnitTester
    from auxi.modelling.business.basic_test import BasicLoanActivityUnitTester
    unittest.main()
