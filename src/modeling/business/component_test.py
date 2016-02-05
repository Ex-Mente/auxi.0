# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.business.component module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from datetime import datetime
from auxi.modeling.business.clock import Clock
from auxi.modeling.business.component import Component
from auxi.modeling.business.basicactivity import BasicActivity
from auxi.modeling.financial.des.generalledger import GeneralLedger
from auxi.modeling.financial.des.generalledgerstructure import GeneralLedgerStructure
from auxi.modeling.financial.des.transactiontemplate import TransactionTemplate

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
      Tester for the auxi.modeling.business.component class.
    """

    def setUp(self):
        self.object = Component("ComponentA",
                                description="DescriptionA")
        # Set up the needed objects
        self.object.components.append(
            Component("ComponentA1", description="ca1"))
        self.object.components.append(
            Component("ComponentA2", description="ca2"))
        self.tx_template = TransactionTemplate("NameA",
                                               description="DescriptionA",
                                               dt_account="Bank",
                                               cr_account="Sales")
        basic_activity = BasicActivity("BasicActivityA",
                                       description="DescriptionA",
                                       start=datetime(2016, 2, 1),
                                       end=datetime(2017, 2, 1),
                                       interval=3,
                                       amount=5000,
                                       tx_template=self.tx_template)
        self.object.components[0].activities.append(basic_activity)

    def test_constructor(self):
        self.assertEqual(self.object.name, "ComponentA")
        self.assertEqual(self.object.description, "DescriptionA")

    def test_set_parent_path(self):
        self.object.set_parent_path("entityA")
        self.assertEqual(self.object.path, "entityA/ComponentA")

    def test_set_name(self):
        self.object.set_parent_path("entityA")
        self.object.name = "NameAt"
        self.assertEqual(self.object.name, "NameAt")
        self.assertEqual(self.object.components[0].path,
                         "entityA/NameAt/ComponentA1")
        self.assertEqual(self.object.components[1].path,
                         "entityA/NameAt/ComponentA2")
        self.assertEqual(self.object.components[0].activities[0].path,
                         "entityA/NameAt/ComponentA1/BasicActivityA")

    def test_create_component(self):
        new_comp = self.object.create_component("ComponentTestCreate",
                                                description="catc")
        self.assertEqual(new_comp.name, "ComponentTestCreate")
        self.assertEqual(new_comp.description, "catc")

        self.assertEqual(new_comp, self.object.components[2])

    def test_remove_component(self):
        self.object.create_component("ComponentTestRemove",
                                     description="catr")
        self.object.remove_component("ComponentTestRemove")
        self.assertEqual(len(self.object.components), 2)

    def test_prepare_to_run(self):
        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        self.object.prepare_to_run(clock, 18)
        self.assertEqual(
            self.object.components[0].activities[0].start_period_ix, 2)
        self.assertEqual(
            self.object.components[0].activities[0].end_period_ix, 14)

    def test_run(self):
        structure = GeneralLedgerStructure("NameA", description="DescriptionA")
        gl = GeneralLedger("NameA", structure, description="DescriptionA")
        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        clock.tick()
        clock.tick()
        self.object.prepare_to_run(clock, 20)
        self.object.run(clock, gl)
        self.assertEqual(len(gl.transactions), 1)
        self.assertEqual(gl.transactions[0].amount, 5000)

# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(Component)

if __name__ == '__main__':
    unittest.main()
