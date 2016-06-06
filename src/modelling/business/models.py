#!/usr/bin/env python3
"""
This module provides classes to work with business models.
"""

from datetime import datetime

from auxi.core.objects import NamedObject
from auxi.core.time import Clock, TimePeriod
from auxi.core.helpers import get_date
from auxi.modelling.business.structure import Entity

__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class TimeBasedModel(NamedObject):
    """
    Represents an time based model class. An instance of this class is by
    default configured to run only once, thus functioning as a steady state
    model. The instance's time based parameters must be configured for it to
    function as a time based model.

    :param name: The name.
    :param description: The description.
    :param start_datetime: The start datetime of the model.
    :param period_duration: The duration of the model's time period.
      e.g. month, day etc.
    :param period_count: The number of periods to execute the model for.
    """

    def __init__(self,
                 name,
                 description=None,
                 start_datetime=datetime.now(),
                 period_duration=TimePeriod.year,
                 period_count=1):
        self.clock = Clock(
            "Clock",
            start_datetime=get_date(start_datetime),
            timestep_period_duration=period_duration)
        self.period_count = period_count
        self.entities = []
        super(TimeBasedModel, self).__init__(name, description=description)

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
        """
        Create an entity and add it to the model.

        :param name: The entity name.
        :param gl_structure: The entity's general ledger structure.
        :param description: The entity description.

        :returns: The created entity.
        """

        new_entity = Entity(name, gl_structure, description=description)
        self.entities.append(new_entity)
        return new_entity

    def remove_entity(self, name):
        """
        Remove an entity from the model.

        :param name: The name of the entity to remove.
        """

        entity_to_remove = None
        for e in self.entities:
            if e.name == name:
                entity_to_remove = e
        if entity_to_remove is not None:
            self.entities.remove(entity_to_remove)

    def prepare_to_run(self):
        """
        Prepare the model for execution.
        """

        self.clock.reset()
        for e in self.entities:
            e.prepare_to_run(self.clock, self.period_count)

    def run(self):
        """
        Execute the model.
        """

        self.prepare_to_run()
        for i in range(0, self.period_count):
            for e in self.entities:
                e.run(self.clock)
            self.clock.tick()

    def __getitem__(self, key):
        return [e for e in self.entities if e.name == key][0]


if __name__ == "__main__":
    import unittest
    from auxi.modelling.business.models_test import TimeBasedModelUnitTester
    unittest.main()
