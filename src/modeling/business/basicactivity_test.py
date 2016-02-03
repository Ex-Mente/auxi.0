# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.business.basicactivity module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from datetime import datetime
from auxi.modeling.business.clock import Clock
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
      Tester for the auxi.modeling.business.basicactivity class.
    """

    def setUp(self):
        self.tx_template = TransactionTemplate("NameA",
                                               description="DescriptionA",
                                               dt_account="Bank",
                                               cr_account="Sales")
        self.object = BasicActivity("NameA",
                                    description="DescriptionA",
                                    start=datetime(2016, 2, 1),
                                    end=datetime(2017, 2, 1),
                                    interval=3,
                                    amount=5000,
                                    tx_template=self.tx_template)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.start_datetime, datetime(2016, 2, 1))
        self.assertEqual(self.object.end_datetime, datetime(2017, 2, 1))
        self.assertEqual(self.object.interval, 3)
        self.assertEqual(self.object.amount, 5000)
        self.assertEqual(self.object.tx_template, self.tx_template)

    def test__meet_exection_criteria(self):
        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        self.object.prepare_to_run(clock, 13)
        self.assertEqual(self.object._meet_execution_criteria(5), True)
        self.object.amount = 0
        self.assertEqual(self.object._meet_execution_criteria(5), False)
        self.object.amount = 5000

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

# help(BasicActivity)

if __name__ == '__main__':
    unittest.main()
