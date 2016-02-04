# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.business.entity module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from datetime import datetime
from auxi.modeling.business.clock import Clock
from auxi.modeling.business.component import Component
from auxi.modeling.business.entity import Entity
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
      Tester for the auxi.modeling.entity.component class.
    """

    def setUp(self):
        self.gl_structure = GeneralLedgerStructure("NameA", description="DescriptionA")

        self.object = Entity("EntityA",
                             gl_structure=self.gl_structure,
                             description="DescriptionA",
                             period_count=24)
        # Set up the needed objects
        comp1 = self.object.create_component("ComponentA1", description="ca1")
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
        comp1.activities.append(basic_activity)

        self.clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))

    def test_constructor(self):
        self.assertEqual(self.object.name, "ComponentA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.gl.structure.name, self.gl_structure.name)
        self.assertEqual(self.object.period_count, 24)

    def test_set_parent_path(self):
        self.object.set_parent_path("modelA")
        self.assertEqual(self.object.path, "modelA/EntityA")

    def test_set_name(self):
        self.object.set_parent_path("modelA")
        self.object.name = "NameAt"
        self.assertEqual(self.object.name, "NameAt")
        self.assertEqual(self.object.components[0].path,
                         "modelA/EntityA/NameAt/ComponentA1")
        self.assertEqual(self.object.components[0].activities[0].path,
                         "modelA/EntityA/NameAt/ComponentA1/BasicActivityA")

    def test_create_component(self):
        new_comp = self.object.create_component("ComponentA2",
                                                description="ca2")
        self.assertEqual(new_comp.name, "ComponentA2")
        self.assertEqual(new_comp.description, "ca2")

        self.assertEqual(new_comp, self.object.components[1])

    def test_remove_component(self):
        self.object.create_component("ComponentA2",
                                     description="ca2")
        self.object.remove_account("ComponentA2")
        self.assertEqual(len(self.object.components), 1)

    def test_prepare_to_run(self):
        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        self.object.prepare_to_run(clock, 18)
        self.assertEqual(
            self.object.components[0].activities[0].start_period_ix, 2)
        self.assertEqual(
            self.object.components[0].activities[0].end_period_ix, 14)

    def test_run(self):
        self.object.prepare_to_run(self.clock, 20)
        self.clock.tick()
        self.clock.tick()
        self.object.run(self.clock)
        self.assertEqual(len(self.object.gl.transactions), 1)
        self.assertEqual(self.object.gl.transactions[0].amount, 5000)

    def test__perform_year_end_procedure_gross_profit_and_income_summary(self):
        pass

    def test__perform_year_end_procedure_gross_profit(self):
        pass

    def test__perform_year_end_procedure_income_summary(self):
        pass

    def test__perform_year_end_procedure_income_tax(self):
        pass

    def test__perform_year_end_procedure_retained_earnings(self):
        gls = self.object.gl.structure
        year_end_datetime = datetime(2017, 2, 1)
        # Test for == 0 case
        income_summary = 0
        self._perform_year_end_procedure_retained_earnings(
            year_end_datetime, income_summary)
        self.assertEqual(len(self.object.gl.transactions), 0)

        # Test for > 0 case
        income_summary = 1000
        self._perform_year_end_procedure_retained_earnings(
            year_end_datetime, income_summary)
        self.assertEqual(len(self.object.gl.transactions), 1)
        self.assertEqual(self.object.gl.transactions[0].dt_account,
                         gls.retainedearnings_account.name)
        self.assertEqual(self.object.gl.transactions[0].cr_account,
                         gls.retainedearnings_account.name)
        self.assertEqual(self.object.gl.transactions[0].yearEndDate,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[0].amount,
                         income_summary)
        self.assertEqual(self.object.gl.transactions[0].is_closing_dt_account,
                         True)

        # Test for < 0 case
        income_summary = -300
        self._perform_year_end_procedure_retained_earnings(
            year_end_datetime, income_summary)
        self.assertEqual(len(self.object.gl.transactions), 2)
        self.assertEqual(self.object.gl.transactions[1].dt_account,
                         gls.retainedearnings_account.name)
        self.assertEqual(self.object.gl.transactions[1].cr_account,
                         gls.retainedearnings_account.name)
        self.assertEqual(self.object.gl.transactions[1].yearEndDate,
                         year_end_datetime)
        self.assertEqual(self.object.gl.transactions[1].amount,
                         income_summary)
        self.assertEqual(self.object.gl.transactions[1].is_closing_dt_account,
                         True)

    def test__perform_year_end_procedure(self):
        pass

# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(Component)

if __name__ == '__main__':
    unittest.main()
