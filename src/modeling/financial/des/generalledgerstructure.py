# -*- coding: utf-8 -*-
"""
This module provides a general ledger structure class which
structures a general ledger's accounts.\n

@name: general ledger structure
@author: Ex Mente Technologies (Pty) Ltd
"""

from auxi.core.namedobject import NamedObject
from auxi.modeling.financial.des.generalledgeraccount import AccountType
from auxi.modeling.financial.des.generalledgeraccount import GeneralLedgerAccount

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class GeneralLedgerStructure(NamedObject):
    """Represents the account structure of a general ledger."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None):
        """Initialise the object."""
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
        """Create an account in the general ledger structure.

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
        """Remove an account from the general ledger's accounts.

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
        """Retrieves an account from the general ledger structure
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
        result.append(account)
        for child in account.accounts:
            self.get_account_and_decendants(child, result)
