# -*- coding: utf-8 -*-
"""
This module provides a component class that as a component of an entity.
A component has business activities.\n

@name: component
@author: Ex Mente Technologies (Pty) Ltd
"""

from auxi.core.namedobject import NamedObject
from auxi.modeling.financial.des.transactiontemplate import TransactionTemplate

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class Component(NamedObject):
    """Represents an component class."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, description=None):
        """Initialise the object.

        :param name: The name.
        :param description: The description.
        """
        self._parent_path = ""
        self.path = name
        self.components = []
        self.activities = []
        super().__init__(name, description=description)

    def set_parent_path(self, value):
        self._parent_path = value
        self.path = value + r'/' + self.name
        self._update_childrens_parent_path()

    def _update_childrens_parent_path(self):
        for c in self.components:
            c.set_parent_path(self.path)
        for a in self.activities:
            a.set_parent_path(self.path)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.path = self._parent_path + r'/' + self.name
        self._update_childrens_parent_path()

    def prepare_to_run(self, clock, period_count):
        """Prepare the component for execution.

        :param clock: The clock containing the execution start time and execution period information.
        :param period_count: The total amount of periods this activity will be requested to be run for.
        """
        for c in self.components:
            c.prepare_to_run(clock, period_count)
        for a in self.activities:
            a.prepare_to_run(clock, period_count)

    def run(self, clock, generalLedger):
        """Execute the component at the current clock cycle.

        :param clock: The clock containing the current execution time and period information.
        :param generalLedger: The general ledger into which to create the transactions.
        """
        for c in self.components:
            c.run(clock, generalLedger)
        for a in self.activities:
            a.run(clock, generalLedger)
