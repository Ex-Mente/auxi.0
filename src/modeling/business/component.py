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
        """Set the parent path and the path from the new parent path.

        :param value: The path to the object's parent
        """
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

    def create_component(self, name, description=None):
        """Create a component in the business entity.

        :param name: The account name.
        :param description: The account description.

        :returns: The created component.
        """
        new_comp = Component(name, description=description)
        self.components.append(new_comp)
        return new_comp

    def remove_component(self, name):
        """Remove a component from the entity.

        :param name: The name of the component to remove.
        """
        component_to_remove = None
        for c in self.components:
            if c.name == name:
                component_to_remove = c
        if component_to_remove is not None:
            self.components.remove(component_to_remove)

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
