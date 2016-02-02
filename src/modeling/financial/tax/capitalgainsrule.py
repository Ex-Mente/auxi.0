# -*- coding: utf-8 -*-
"""
This module provides a capital gains tax rule class for specifying a rule that
handle capital gains taxes.\n

@name: capital gains tax rule
@author: Ex Mente Technologies (Pty) Ltd
"""

from auxi.core.namedobject import NamedObject

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class CapitalGainsRule(NamedObject):
    """Represents a capital gains tax rule class."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None, percentage=1.0):
        """Initialise the object.

        :param name: The name.
        :param description: The description.
        :param percentage: The capital gains tax percentage.
        """
        super().__init__(name, description)
        self.percentage = percentage
