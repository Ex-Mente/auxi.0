# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.business.activity module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from datetime import datetime
from auxi.modeling.business.clock import Clock
from auxi.modeling.business.activity import Activity

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
      Tester for the auxi.modeling.business.activity class.
    """

    def setUp(self):
        self.object = Activity("NameA",
                               description="DescriptionA",
                               start=datetime(2016, 2, 1),
                               end=datetime(2017, 2, 1),
                               interval=3)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.start_date, datetime(2016, 2, 1))
        self.assertEqual(self.object.end_date, datetime(2017, 2, 1))
        self.assertEqual(self.object.interval, 3)

    def test_set_path(self):
        self.object.set_path("entityA/componentA")
        self.assertEqual(self.object.path, "entityA/componentA/NameA")

    def test_set_name(self):
        self.object.set_path("entityA/componentA")
        self.object.name = "NameAt"
        self.assertEqual(self.object.name, "NameAt")
        self.assertEqual(self.object.path, "entityA/componentA/NameAt")

    def test__meet_exection_criteria(self):
        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        self.object.prepare_to_run(clock, 13)
        self.assertEqual(self.object._meet_execution_criteria(3), False)
        self.assertEqual(self.object._meet_execution_criteria(4), True)
        self.assertEqual(self.object._meet_execution_criteria(40), False)

    def test_prepare_to_run(self):
        clock = Clock("NameA", start_datetime=datetime(2016, 1, 1))
        self.object.prepare_to_run(clock, 18)
        self.assertEqual(self.object.start_period_ix, 1)
        self.assertEqual(self.object.end_period_ix, 13)


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(Currency)

if __name__ == '__main__':
    unittest.main()
