# -*- coding: utf-8 -*-
"""
This module provides a tax rule set class that groups a collection of tax rules.
This is useful for distinguising between different countries' tax rules.\n

@name: tax rule set
@author: Ex Mente Technologies (Pty) Ltd
"""

from auxi.core.namedobject import NamedObject

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class RuleSet(NamedObject):
    """Represents a tax rule set base class."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None, code=None):
        """Initialise the object.

        :param name: The name.
        :param description: The description.
        :param code: The code identifying the rule set. E.g. ZA tax rules, or US tax rules.
        """
        super().__init__(name, description)
        self.code = code
