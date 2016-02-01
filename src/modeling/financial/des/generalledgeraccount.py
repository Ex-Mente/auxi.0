# -*- coding: utf-8 -*-
"""
This module provides a general ledger account class and an account type enum.\n

@name: transaction
@author: Ex Mente Technologies (Pty) Ltd
"""

from enum import Enum
from auxi.core.namedobject import NamedObject


__version__ = "0.2.0"


class AccountType(Enum):
    asset = 1
    equity = 2
    expense = 3
    liability = 4
    revenue = 5


class GeneralLedgerAccount(NamedObject):
    """Represents an account of a general ledger.
    """
    accounts = []

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None,
                 number=None,
                 account_type=AccountType.revenue):
        """Initialise the object."""
        super().__init__(name, description)
        self.number = number
        self.account_type = account_type

    def create_account(self, name, description=None, number=None):
        """Create a sub account in the account.

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
        """Remove an account from the account's sub accounts.

        :param name: The name of the account to remove.
        """
        acc_to_remove = None
        for a in self.accounts:
            if a.name == name:
                acc_to_remove = a
        if acc_to_remove is not None:
            self.accounts.remove(acc_to_remove)
