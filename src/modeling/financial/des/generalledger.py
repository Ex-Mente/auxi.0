# -*- coding: utf-8 -*-
"""
This module provides a general ledger class that a stores a
structure of accounts and list of transactions between these accounts.\n

@name: general ledger
@author: Ex Mente Technologies (Pty) Ltd
"""

from datetime import datetime
from auxi.core.namedobject import NamedObject
from auxi.modeling.financial.des.transaction import Transaction

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class GeneralLedger(NamedObject):
    """Represents the account structure of a general ledger."""
    transactions = []

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, structure, description=None):
        """Initialise the object.

        :param name: The name.
        :param structure: The general ledger structure.
        :param description: The description.
        """
        super().__init__(name, description)
        self.structure = structure

    def create_transaction(self, name, description=None,
                           tx_datetime=datetime.min,
                           dt_account=None, cr_account=None,
                           source=None, amount=0.00):
        """Create a transaction in the general ledger.

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
