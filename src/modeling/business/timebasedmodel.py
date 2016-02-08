# -*- coding: utf-8 -*-
"""
This module provides a time based model class that represents a
time based business model.
A time based model contains and executes entities.\n

@name: time based model
@author: Ex Mente Technologies (Pty) Ltd
"""

from datetime import datetime
from auxi.core.namedobject import NamedObject
from auxi.modeling.business.clock import Clock
from auxi.modeling.business.clock import TimePeriod
from auxi.modeling.business.entity import Entity
from auxi.modeling.financial.des.generalledgerstructure import GeneralLedgerStructure

__version__ = "0.2.0"

# TODO: initialise accounts by json file
# TODO: get_account by path.


class TimeBasedModel(NamedObject):
    """Represents an time based model class."""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self,
                 name,
                 description=None,
                 start_datetime=datetime.now(),
                 period_duration=TimePeriod.month,
                 period_count=60):
        """Initialise the object.

        :param name: The name.
        :param description: The description.
        :param start_datetime: The start datetime of the model.
        :param period_duration: The duration of the model's time period. e.g. month, day etc.
        :param start_datetime: The number of periods to execute the model for.
        """
        self.clock = Clock(
            "Clock",
            start_datetime=start_datetime,
            timestep_period_duration=period_duration)
        self.period_count = period_count
        self.entities = []
        super().__init__(name, description=description)

    def _update_childrens_parent_path(self):
        for e in self.entities:
            e.set_parent_path(self.name)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self._update_childrens_parent_path()

    def create_entity(self, name, gl_structure, description=None):
        """Create an entity in the model.

        :param name: The entity name.
        :param gl_structure: The entity's general ledger structure.
        :param description: The entity description.

        :returns: The created entity.
        """
        new_entity = Entity(name, gl_structure, description=description)
        self.entities.append(new_entity)
        return new_entity

    def remove_entity(self, name):
        """Remove an entity from the model.

        :param name: The name of the entity to remove.
        """
        entity_to_remove = None
        for e in self.entities:
            if e.name == name:
                entity_to_remove = e
        if entity_to_remove is not None:
            self.entities.remove(entity_to_remove)

    def prepare_to_run(self):
        """Prepare the model for execution.
        """
        self.clock.reset()
        for e in self.entities:
            e.prepare_to_run(self.clock, self.period_count)

    def run(self):
        """Execute the model.
        """
        self.prepare_to_run()
        for i in range(0, self.period_count):
            self.clock.tick()
            for e in self.entities:
                e.run(self.clock)
