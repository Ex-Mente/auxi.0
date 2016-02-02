# -*- coding: utf-8 -*-
"""
This module provides a currency table class that a stores a
dictionary of currency with exchange rates based on the table's default currency.\n

@name: currency table
@author: Ex Mente Technologies (Pty) Ltd
"""

from auxi.core.namedobject import NamedObject
from auxi.modeling.financial.des.currency import Currency

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class CurrencyTable(NamedObject):
    """Represents a currency table that is used to define the exchange rates of
    different currencies based on the default currency."""
    table = {}

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None,
                 default_currency=Currency(
                    "USD", "United States Dollars", "$")):
        """Initialise the object.

        :param name: The name.
        :param description: The description.
        """
        super().__init__(name, description)
        self.default_currency = default_currency
        self.table[self.default_currency] = "1.0"
