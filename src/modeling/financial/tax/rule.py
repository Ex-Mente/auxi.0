# -*- coding: utf-8 -*-
"""
This module provides a tax rule class that serves as a base class
for tax rules.\n

@name: tax rule
@author: Ex Mente Technologies (Pty) Ltd
"""

from auxi.core.namedobject import NamedObject

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class Rule(NamedObject):
    """Represents a tax rule base class."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None):
        """Initialise the object.

        :param name: The name.
        :param description: The description.
        """
        super().__init__(name, description)
