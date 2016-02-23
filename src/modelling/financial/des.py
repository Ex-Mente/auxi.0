#!/usr/bin/env python3
"""
This module provides classes representing the accounting double entry system.
"""

from enum import Enum
from datetime import datetime

from auxi.core.objects import NamedObject

__version__ = '0.2.0rc4'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class AccountType(Enum):
    """
    Represents the type of general ledger account.
    """
    asset = 1
    equity = 2
    expense = 3
    liability = 4
    revenue = 5


class GeneralLedgerAccount(NamedObject):
    """
    Represents an account of a general ledger.

    :param name: The name.
    :param description: The description.
    :param number: The number.
    :param account_type: The type of account.
    """

    def __init__(self, name, description=None,
                 number=None,
                 account_type=AccountType.revenue):
        """
        """
        super().__init__(name, description)
        self.number = number
        self.account_type = account_type
        self.accounts = []

    def create_account(self, name, description=None, number=None):
        """
        Create a sub account in the account.

        :param name: The account name.
        :param description: The account description.
        :param number: The account number.

        :returns: The created account.
        """
        new_account = GeneralLedgerAccount(name, description, number,
                                           self.account_type)
        self.accounts.append(new_account)
        return new_account

    def remove_account(self, name):
        """
        Remove an account from the account's sub accounts.

        :param name: The name of the account to remove.
        """
        acc_to_remove = None
        for a in self.accounts:
            if a.name == name:
                acc_to_remove = a
        if acc_to_remove is not None:
            self.accounts.remove(acc_to_remove)


class Transaction(NamedObject):
    """
    Represents a financial transaction between two general ledger accounts.

    :param name: The name.
    :param description: The description.
    :param tx_datetime: The transaction's date and time.
    :param dt_account: The account to debit.
    :param cr_account: The account to credit.
    :param source: The source that created the transaction.
    :param amount: The transaction's amount.
    :param is_closing_dt_account: Specifies wether this is a closing debit
      account.
    :param is_closing_cr_account: Specifies wether this is a closing credit
      account.
    """

    def __init__(self, name, description=None,
                 tx_datetime=datetime.min,
                 dt_account=None, cr_account=None,
                 source=None, amount=0.00,
                 is_closing_dt_account=False,
                 is_closing_cr_account=False):
        """
        """
        super().__init__(name, description)
        self.tx_datetime = tx_datetime
        self.dt_account = dt_account
        self.cr_account = cr_account
        self.source = source
        self.amount = amount
        self.is_closing_dt_account = is_closing_dt_account
        self.is_closing_cr_account = is_closing_cr_account


class TransactionTemplate(NamedObject):
    """
    Represents a template for how a transaction is to be created.

    :param name: The name.
    :param description: The description.
    :param dt_account: The account to debit.
    :param cr_account: The account to credit.
    """

    def __init__(self, name, description=None,
                 dt_account=None, cr_account=None):
        """
        """
        super().__init__(name, description)
        self.dt_account = dt_account
        self.cr_account = cr_account


class GeneralLedgerStructure(NamedObject):
    """
    Represents the account structure of a general ledger.

    :param name: The name.
    :param description: The description.
    """

    def __init__(self, name, description=None):
        """
        """
        super().__init__(name, description)
        self.accounts = []
        self.create_account(
            "Bank",
            description="Bank",
            number="010",
            account_type=AccountType.asset)
        self.incometaxpayable_account = self.create_account(
            "IncomeTaxPayable",
            description="IncomeTaxPayable",
            number="010",
            account_type=AccountType.liability)
        self.incometaxexpense_account = self.create_account(
            "IncomeTaxExpense",
            description="IncomeTaxExpense",
            number="010",
            account_type=AccountType.expense)
        self.sales_account = self.create_account(
            "Sales",
            description="Sales",
            number="010",
            account_type=AccountType.revenue)
        self.costofsales_account = self.create_account(
            "CostOfSales",
            description="CostOfSales",
            number="010",
            account_type=AccountType.expense)
        self.gross_profit_account = self.create_account(
            "GrossProfit",
            description="GrossProfit",
            number="010",
            account_type=AccountType.revenue)
        self.incomesummary_account = self.create_account(
            "IncomeSummary",
            description="IncomeSummary",
            number="010",
            account_type=AccountType.revenue)
        self.retainedearnings_account = self.create_account(
            "RetainedEarnings",
            description="RetainedEarnings",
            number="010",
            account_type=AccountType.equity)
        self.tax_payment_account = "Bank"

    def create_account(self, name, description=None, number=None,
                       account_type=AccountType.revenue):
        """
        Create an account in the general ledger structure.

        :param name: The account name.
        :param description: The account description.
        :param number: The account number.
        :param account_type: The account type.

        :returns: The created account.
        """
        new_account = GeneralLedgerAccount(name, description, number,
                                           account_type)
        self.accounts.append(new_account)
        return new_account

    def remove_account(self, name):
        """
        Remove an account from the general ledger's accounts.

        :param name: The name of the account to remove.
        """
        acc_to_remove = None
        for a in self.accounts:
            if a.name == name:
                acc_to_remove = a
        if acc_to_remove is not None:
            self.accounts.remove(acc_to_remove)

    def _get_account_from_child(self, accounts, account_name):
        for a in accounts:
            if a.name == account_name:
                return a
            else:
                result = self._get_account_from_child(a.accounts, account_name)
                if result is not None:
                    return result
        return None

    def get_account(self, account_name):
        """
        Retrieves an account from the general ledger structure
        given the account name.

        :param account_name: The account name.

        :returns: The requested account, if found, else None.
        """
        for a in self.accounts:
            if a.name == account_name:
                return a
            else:
                result = self._get_account_from_child(a.accounts, account_name)
                if result is not None:
                    return result
        return None

    def get_account_and_decendants(self, account, result):
        """
        Returns the account and all of it's sub accounts.

        :param account: The account.
        :param result: The list to add all the accounts to.
        """
        result.append(account)
        for child in account.accounts:
            self.get_account_and_decendants(child, result)


class GeneralLedger(NamedObject):
    """
    Represents the account structure of a general ledger.

    :param name: The name.
    :param structure: The general ledger structure.
    :param description: The description.
    """

    def __init__(self, name, structure, description=None):
        """
        """
        super().__init__(name, description)
        self.structure = structure
        self.transactions = []

    def create_transaction(self, name, description=None,
                           tx_datetime=datetime.min,
                           dt_account=None, cr_account=None,
                           source=None, amount=0.00):
        """
        Create a transaction in the general ledger.

        :param name: The transaction's name.
        :param description: The transaction's description.
        :param tx_datetime: The date and time of the transaction.
        :param cr_account: The transaction's credit account's name.
        :param dt_account: The transaction's debit account's name.
        :param source: The name of source the transaction originated from.
        :param amount: The transaction amount.

        :returns: The created transaction.
        """
        new_tx = Transaction(name, description, tx_datetime,
                             dt_account, cr_account, source, amount)
        self.transactions.append(new_tx)
        return new_tx


if __name__ == "__main__":
    import unittest
    from auxi.modelling.financial.des_test import GeneralLedgerAccountUnitTester
    from auxi.modelling.financial.des_test import TransactionUnitTester
    from auxi.modelling.financial.des_test import TransactionTemplateUnitTester
    from auxi.modelling.financial.des_test import GeneralLedgerStructureUnitTester
    from auxi.modelling.financial.des_test import GeneralLedgerUnitTester
    unittest.main()
