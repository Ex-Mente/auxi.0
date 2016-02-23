#!/usr/bin/env python3
"""
This module provides classes to manage currencies.
"""

from auxi.core.objects import NamedObject

__version__ = '0.2.0rc4'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class Currency(NamedObject):
    """
    Represents a currency.

    :param name: The name.
    :param description: The description.
    :param symbol: The symbol.
    """

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None, symbol=None):
        """
        """
        super().__init__(name, description)
        self.symbol = symbol


class CurrencyTable(NamedObject):
    """
    Represents a currency table that is used to define the exchange rates of
    different currencies based on the default currency.

    :param name: The name.
    :param description: The description.
    """

    def __init__(self, name, description=None,
                 default_currency=Currency(
                    "USD", "United States Dollars", "$")):
        """
        """
        super().__init__(name, description)
        self.default_currency = default_currency
        self.table = {}
        self.table[self.default_currency] = "1.0"


if __name__ == "__main__":
    import unittest
    from auxi.modelling.financial.currencies_test import CurrencyUnitTester
    from auxi.modelling.financial.currencies_test import CurrencyTableUnitTester
    unittest.main()
