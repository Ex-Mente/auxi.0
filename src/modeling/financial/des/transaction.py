# -*- coding: utf-8 -*-
"""
This module provides a transaction class that stores information on a
transaction between two general ledger accounts.\n

@name: transaction
@author: Ex Mente Technologies (Pty) Ltd
"""

from datetime import datetime
from auxi.core.namedobject import NamedObject


__version__ = "0.2.0"


class Transaction(NamedObject):
    """Represents a financial transaction between
       two general ledger accounts.
    """

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None,
                 tx_datetime=datetime.min,
                 dt_account=None, cr_account=None,
                 source=None, amount=0.00,
                 is_closing_dt_account=False,
                 is_closing_cr_account=False):
        """Initialise the object."""
        super().__init__(name, description)
        self.tx_datetime = tx_datetime
        self.dt_account = dt_account
        self.cr_account = cr_account
        self.source = source
        self.is_closing_dt_account = is_closing_dt_account
        self.is_closing_cr_account = is_closing_cr_account
