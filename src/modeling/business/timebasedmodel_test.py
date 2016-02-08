# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.business.timebasedmodel module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from datetime import datetime
from auxi.modeling.business.timebasedmodel import TimeBasedModel
from auxi.modeling.business.basicactivity import BasicActivity
from auxi.modeling.business.clock import TimePeriod
from auxi.modeling.financial.des.generalledgerstructure import GeneralLedgerStructure
from auxi.modeling.financial.des.transactiontemplate import TransactionTemplate

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
      Tester for the auxi.modeling.business.timebasedmodel class.
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
        tx_template = TransactionTemplate("NameA",
                                          description="DescriptionA",
                                          dt_account="Bank",
                                          cr_account="Sales")
        basic_activity = BasicActivity("BasicActivityA",
                                       description="DescriptionA",
                                       start=datetime(2016, 2, 1),
                                       end=datetime(2016, 2, 14),
                                       interval=1,
                                       amount=5000,
                                       tx_template=tx_template)
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
        self.object.prepare_to_run()
        self.assertEqual(
            self.object.entities[0].components[0].activities[0].end_period_ix,
            14)

    def test_run(self):
        self.object.run()
        self.assertEqual(len(self.object.entities[0].gl.transactions), 13)
        self.assertEqual(self.object.entities[0].gl.transactions[0].amount,
                         5000)

# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(Component)

if __name__ == '__main__':
    unittest.main()
