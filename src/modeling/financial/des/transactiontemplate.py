# -*- coding: utf-8 -*-
"""
This module provides a transaction template class that serves as a template
for how a transaction is to be created.\n

@name: transaction template
@author: Ex Mente Technologies (Pty) Ltd
"""

from auxi.core.namedobject import NamedObject


__version__ = "0.2.0"


class TransactionTemplate(NamedObject):
    """Represents a template for how a transaction is to be created."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None,
                 dt_account=None, cr_account=None):
        """Initialise the object."""
        super().__init__(name, description)
        self.dt_account = dt_account
        self.cr_account = cr_account
