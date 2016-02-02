# -*- coding: utf-8 -*-
"""
This module provides a currency class representing a currency.\n

@name: currency
@author: Ex Mente Technologies (Pty) Ltd
"""

from auxi.core.namedobject import NamedObject

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class Currency(NamedObject):
    """Represents a currency."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None, symbol=None):
        """Initialise the object.

        :param name: The name.
        :param description: The description.
        :param symbol: The symbol.
        """
        super().__init__(name, description)
