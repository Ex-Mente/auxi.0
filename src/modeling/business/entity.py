# -*- coding: utf-8 -*-
"""
This module provides a entity class rrepresenting a business entity.
an entity consists of business components e.g. Sales department.\n

@name: entity
@author: Ex Mente Technologies (Pty) Ltd
"""

from datetime import datetime
from auxi.core.namedobject import NamedObject
from auxi.modeling.financial.des.generalledger import GeneralLedger
from auxi.modeling.financial.tax.ruleset import RuleSet

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class Entity(NamedObject):
    """Represents an entity class."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, gl_structure, description=None, period_count=-1):
        """Initialise the object.

        :param name: The name.
        :param gl_structure: The general ledger structure the entity's general ledger will be initialized with.
        :param description: The description.
        :param period_count: The number of periods the entity should be run for.
        """
        self.gl = GeneralLedger(
            "General Ledger",
            gl_structure,
            description="General Ledger")
        self._parent_path = ""
        self.path = name
        self.components = []
        self.tax_rule_set = RuleSet("Default")
        self.negative_income_tax_total = 0
        self._prev_year_end_datetime = datetime.min
        self._curr_year_end_datetime = datetime.min
        self._exec_year_end_datetime = datetime.min
        self.period_count = period_count
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
