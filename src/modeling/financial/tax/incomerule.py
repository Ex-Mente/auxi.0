# -*- coding: utf-8 -*-
"""
This module provides an income tax rule class for specifying a rule that
handle income taxes.\n

@name: income tax rule
@author: Ex Mente Technologies (Pty) Ltd
"""

from auxi.core.namedobject import NamedObject

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class IncomeRule(NamedObject):
    """Represents an income tax rule class."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None, percentage=1.0):
        """Initialise the object.

        :param name: The name.
        :param description: The description.
        :param percentage: The income tax percentage.
        """
        super().__init__(name, description)
        self.percentage = percentage
