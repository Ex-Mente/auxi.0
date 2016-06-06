#!/usr/bin/env python3
"""
This module provides classes representing the accounting double entry system.
"""

from datetime import datetime

from enum import Enum

from auxi.core.objects import NamedObject
from auxi.core.reporting import ReportFormat


__version__ = '0.2.1'
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

AT = AccountType


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
        self._parent_path = ""
        self.path = name
        self.number = number
        self.account_type = account_type
        self.accounts = []
        super(GeneralLedgerAccount, self).__init__(name, description)

    def __getitem__(self, key):
        return [a for a in self.accounts if a.name == key][0]

    def __missing__(self, key):
        return None

    def set_parent_path(self, value):
        """
        Set the parent path and the path from the new parent path.

        :param value: The path to the object's parent
        """

        self._parent_path = value
        self.path = value + r'/' + self.name
        self._update_childrens_parent_path()

    def _update_childrens_parent_path(self):
        for a in self.accounts:
            a.set_parent_path(self.path)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        if self._parent_path != "":
            self.path = self._parent_path + r'/' + self.name
        else:
            self.path = self.name
        self._update_childrens_parent_path()

    def create_account(self, name, number=None, description=None):
        """
        Create a sub account in the account.

        :param name: The account name.
        :param description: The account description.
        :param number: The account number.

        :returns: The created account.
        """

        new_account = GeneralLedgerAccount(name, description, number,
                                           self.account_type)
        new_account.set_parent_path(self.path)
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

    def get_child_account(self, account_name):
        """
        Retrieves a child account.
        This could be a descendant nested at any level.

        :param account_name: The name of the account to retrieve.

        :returns: The child account, if found, else None.
        """

        if(r'/' in account_name):
            accs_in_path = account_name.split(r'/', 1)

            curr_acc = self[accs_in_path[0]]
            if curr_acc is None:
                return None
            return curr_acc.get_child_account(accs_in_path[1])
            pass
        else:
            return self[account_name]
        return None


class Transaction(NamedObject):
    """
    Represents a financial transaction between two general ledger accounts.

    :param name: The name.
    :param description: The description.
    :param tx_date: The transaction's date.
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
                 tx_date=datetime.min.date(),
                 dt_account=None, cr_account=None,
                 source=None, amount=0.00,
                 is_closing_dt_account=False,
                 is_closing_cr_account=False):
        super(Transaction, self).__init__(name, description)
        self.tx_date = tx_date
        self.dt_account = dt_account
        self.cr_account = cr_account
        self.source = source
        self.amount = amount
        self.is_closing_dt_account = is_closing_dt_account
        self.is_closing_cr_account = is_closing_cr_account


class TransactionTemplate(NamedObject):
    """
    Represents a template for how a transaction is to be created.

    :param name: The name of the transaction.
    :param description: The description of the transaction.
    :param dt_account: The account to debit.
    :param cr_account: The account to credit.
    """

    def __init__(self, name, dt_account, cr_account, description=None):
        """
        """
        super(TransactionTemplate, self).__init__(name, description)
        self.dt_account = dt_account
        self.cr_account = cr_account


class GeneralLedgerStructure(NamedObject):
    """
    The account structure of a general ledger.

    :param name: The name.
    :param description: The description.
    """

    # TODO: add _acc_ name abbr. descriptions

    def __init__(self, name, description=None):
        super(GeneralLedgerStructure, self).__init__(name, description)
        self.accounts = []

        ca = self._create_account_

        # create income statement account categories
        self._acci_unalloc_inc_ = ca("Unallocated Income Statement", "I05",
                                     AT.revenue)
        self._acci_sales_ = ca("Sales", "I10", AT.revenue)
        self._acci_cos_ = ca("Cost of Sales", "I15", AT.expense)
        self._acci_oth_inc_ = ca("Other Income", "I20", AT.revenue)
        self._acci_exp_ = ca("Expense", "I25", AT.expense)
        self._acci_tax_ = ca("Tax", "I30", AT.expense)
        self._acci_divs_ = ca("Dividends", "I35", AT.expense)

        # create balance sheet account categories
        self._accb_sh_cap_ = ca("Share Capital", "B10", AT.asset)
        self._accb_ret_inc_ = ca("Retained Income", "B15", AT.equity)
        self._accb_shh_loan_ = ca("Shareholders Loan", "B20", AT.liability)
        self._accb_lt_borrow_ = ca("Long Term Borrowing", "B25", AT.liability)
        self._accb_oth_lt_lia_ = ca("Other Long Term Liabilities", "B30",
                                    AT.liability)
        self._accb_fixed_ass_ = ca("Fixed Assets", "B35", AT.asset)
        self._accb_investments_ = ca("Investments", "B40", AT.asset)
        self._accb_oth_fixed_ass_ = ca("Other Fixed Assets", "B45", AT.asset)
        self._accb_inventory_ = ca("Inventory", "B50", AT.asset)
        self._accb_acc_receivable_ = ca("Accounts Receivable", "B55", AT.asset)
        self._accb_bank_ = ca("Bank", "B60", AT.asset)
        self._accb_bank_.create_account("Default", "0000")
        self._accb_oth_curr_ass_ = ca("Other Current Assets", "B65", AT.asset)
        self._accb_acc_payable_ = ca("Account Payable", "B70", AT.liability)
        self._accb_taxation_ = ca("Taxation", "B75", AT.liability)
        self._accb_oth_curr_lia_ = ca("Other Current Liabilities", "B80",
                                      AT.liability)

        # create the year end sub accounts
        self._acci_gross_prof_ = self._acci_unalloc_inc_.create_account(
            "Gross Profit", "0000")
        self._acci_inc_sum_ = self._acci_unalloc_inc_.create_account(
            "Income Summary", "0010")
        self._accb_ret_earnings_acc_ = self._accb_ret_inc_.create_account(
            "Retained Earnings", "0000")
        self._acci_inc_tax_exp_acc_ = self._acci_tax_.create_account(
            "Income Tax Expense", "0000")

        self.tax_payment_account = "Bank/Default"

    def __getitem__(self, key):
        items = [a for a in self.accounts if a.name == key]
        if len(items) == 0:
            return None
        else:
            return items[0]

    def __missing__(self, key):
        return None

    def _create_account_(self, name, number, account_type):
        """
        Create an account in the general ledger structure.

        :param name: The account name.
        :param number: The account number.
        :param account_type: The account type.

        :returns: The created account.
        """

        new_acc = GeneralLedgerAccount(name, None, number, account_type)
        self.accounts.append(new_acc)
        return new_acc

    def get_account(self, account_name):
        """
        Retrieves an account from the general ledger structure
        given the account name.

        :param account_name: The account name.

        :returns: The requested account, if found, else None.
        """

        if(r'/' in account_name):
            accs_in_path = account_name.split(r'/', 1)

            curr_acc = self[accs_in_path[0]]
            if curr_acc is None:
                return None
            return curr_acc.get_child_account(accs_in_path[1])
            pass
        else:
            return self[account_name]
        return None

    def get_account_decendants(self, account):
        """
        Retrieves an account's decendants from the general ledger structure
        given the account name.

        :param account_name: The account name.

        :returns: The decendants of the account.
        """

        result = []
        for child in account.accounts:
            self._get_account_and_decendants_(child, result)
        return result

    def _get_account_and_decendants_(self, account, result):
        """
        Returns the account and all of it's sub accounts.

        :param account: The account.
        :param result: The list to add all the accounts to.
        """

        result.append(account)
        for child in account.accounts:
            self._get_account_and_decendants_(child, result)

    def validate_account_names(self, names):
        """
        Validates wether the accounts in a list of account names exists.

        :param names: The names of the accounts.

        :returns: The decendants of the account.
        """

        for name in names:
            if self.get_account(name) is None:
                raise ValueError("The account '{}' does not exist in the"
                                 "  general ledger structure.".format(name))

    def report(self, format=ReportFormat.printout, output_path=None):
        """
        Returns a report of this class.

        :param format: The format of the report.
        :param output_path: The path to the file the report is written to.
          If None, then the report is not written to a file.

        :returns: The decendants of the account.
        """

        rpt = GlsRpt(self, output_path)
        return rpt.render(format)


class GeneralLedger(NamedObject):
    """
    Represents the account structure of a general ledger.

    :param name: The name.
    :param structure: The general ledger structure.
    :param description: The description.
    """

    def __init__(self, name, structure, description=None):
        super(GeneralLedger, self).__init__(name, description)
        self.structure = structure
        self.transactions = []

    def create_transaction(self, name, description=None,
                           tx_date=datetime.min.date(),
                           dt_account=None, cr_account=None,
                           source=None, amount=0.00):
        """
        Create a transaction in the general ledger.

        :param name: The transaction's name.
        :param description: The transaction's description.
        :param tx_date: The date of the transaction.
        :param cr_account: The transaction's credit account's name.
        :param dt_account: The transaction's debit account's name.
        :param source: The name of source the transaction originated from.
        :param amount: The transaction amount.

        :returns: The created transaction.
        """

        new_tx = Transaction(name, description, tx_date,
                             dt_account, cr_account, source, amount)
        self.transactions.append(new_tx)
        return new_tx

    def transaction_list(self, start=datetime.min,
                         end=datetime.max,
                         format=ReportFormat.printout,
                         component_path="",
                         output_path=None):
        """
        Generate a transaction list report.

        :param start: The start date to generate the report for.
        :param end: The end date to generate the report for.
        :param format: The format of the report.
        :param component_path: The path of the component to filter the report's
          transactions by.
        :param output_path: The path to the file the report is written to.
          If None, then the report is not written to a file.

        :returns: The generated report.
        """

        rpt = TransactionList(self, start, end, component_path, output_path)
        return rpt.render(format)

    def balance_sheet(self, end=datetime.max,
                      format=ReportFormat.printout, output_path=None):
        """
        Generate a transaction list report.

        :param end: The end date to generate the report for.
        :param format: The format of the report.
        :param output_path: The path to the file the report is written to.
          If None, then the report is not written to a file.

        :returns: The generated report.
        """

        rpt = BalanceSheet(self, end, output_path)
        return rpt.render(format)

    def income_statement(self, start=datetime.min,
                         end=datetime.max,
                         format=ReportFormat.printout,
                         component_path="",
                         output_path=None):
        """
        Generate a transaction list report.

        :param start: The start date to generate the report for.
        :param end: The end date to generate the report for.
        :param format: The format of the report.
        :param component_path: The path of the component to filter the report's
          transactions by.
        :param output_path: The path to the file the report is written to.
          If None, then the report is not written to a file.

        :returns: The generated report.
        """

        rpt = IncomeStatement(self, start, end, component_path, output_path)
        return rpt.render(format)


from auxi.modelling.financial.reporting import GeneralLedgerStructure as GlsRpt
from auxi.modelling.financial.reporting import TransactionList
from auxi.modelling.financial.reporting import BalanceSheet
from auxi.modelling.financial.reporting import IncomeStatement


from auxi.modelling.financial.reporting import GeneralLedgerStructure as GlsRpt
from auxi.modelling.financial.reporting import TransactionList as TxList


if __name__ == "__main__":
    import unittest
    from auxi.modelling.financial.des_test import GeneralLedgerAccountUnitTester
    from auxi.modelling.financial.des_test import TransactionUnitTester
    from auxi.modelling.financial.des_test import TransactionTemplateUnitTester
    from auxi.modelling.financial.des_test import GeneralLedgerStructureUnitTester
    from auxi.modelling.financial.des_test import GeneralLedgerUnitTester
    unittest.main()
