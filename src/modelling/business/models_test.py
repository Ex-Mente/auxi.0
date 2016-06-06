#!/usr/bin/env python3
"""
This module provides testing code for the classes in the
auxi.modelling.business.models module.
"""

import unittest
from datetime import datetime

from auxi.modelling.business.models import TimeBasedModel
from auxi.modelling.business.basic import BasicActivity
from auxi.core.time import TimePeriod
from auxi.modelling.financial.des import GeneralLedgerStructure

__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


# ToDo: Test default construction (should be steady state)

class TimeBasedModelUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.business.models.TimeBasedModel class.
    """

    def setUp(self):
        self.object = TimeBasedModel("TimeBasedModelA",
                                     description="TimeBasedModel A",
                                     start_datetime=datetime(2016, 2, 1),
                                     period_duration=TimePeriod.day,
                                     period_count=200)
        # Set up the needed objects
        self.gl_structure = GeneralLedgerStructure(
            "NameA",
            description="DescriptionA")
        entity = self.object.create_entity(
            "EntityA",
            self.gl_structure,
            description="DescriptionA")
        # Set up the needed objects
        comp1 = entity.create_component("ComponentA1", description="ca1")
        basic_activity = BasicActivity("BasicActivityA",
                                       description="DescriptionA",
                                       dt_account="Bank",
                                       cr_account="Sales",
                                       amount=5000,
                                       start=datetime(2016, 2, 1),
                                       end=datetime(2016, 2, 14),
                                       interval=1)
        comp1.activities.append(basic_activity)

    def test_constructor(self):
        self.assertEqual(self.object.name, "TimeBasedModelA")
        self.assertEqual(self.object.description, "TimeBasedModel A")
        self.assertEqual(self.object.clock.start_datetime,
                         datetime(2016, 2, 1))
        self.assertEqual(self.object.clock.timestep_period_duration,
                         TimePeriod.day)
        self.assertEqual(self.object.period_count, 200)

    def test_set_name(self):
        """
        Test wether the name changes when it is set, that the model's path is
        updated and that the model's children's paths are updated correctly.
        """
        self.object.name = "NameAt"
        self.assertEqual(self.object.name, "NameAt")
        self.assertEqual(
            self.object.entities[0].components[0].path,
            "NameAt/EntityA/ComponentA1")
        self.assertEqual(
            self.object.entities[0].components[0].activities[0].path,
            "NameAt/EntityA/ComponentA1/BasicActivityA")

    def test_create_entity(self):
        new_entity = self.object.create_entity(
            "EntityTestCreate",
            self.gl_structure,
            description="ec")
        self.assertEqual(new_entity.name, "EntityTestCreate")
        self.assertEqual(new_entity.description, "ec")

        self.assertEqual(new_entity, self.object.entities[1])

    def test_remove_entity(self):
        self.object.create_entity(
            "EntityTestRemove",
            self.gl_structure,
            description="er")
        self.object.remove_entity("EntityTestRemove")
        self.assertEqual(len(self.object.entities), 1)

    def test_prepare_to_run(self):
        """
        Test that the model's entities prepare_to_run is called when the
        model's prepare_to_run is called.
        """
        self.object.prepare_to_run()
        self.assertEqual(
            self.object.entities[0].components[0].activities[0].end_period_ix,
            14)

    def test_run(self):
        """
        Test that the model's entities run is called when the
        model's run is called. Also test that the model was run for the
        expected timeperiod.
        """
        self.object.run()
        # Test that the business entity has run for 13 days only
        # (as configured).
        self.assertEqual(len(self.object.entities[0].gl.transactions), 13)


if __name__ == '__main__':
    unittest.main()
