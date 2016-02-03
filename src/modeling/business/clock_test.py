# -*- coding: utf-8 -*-
"""
This module provides testing code for the
auxi.modeling.business.clock module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from datetime import datetime
from auxi.modeling.business.clock import TimePeriod
from auxi.modeling.business.clock import Clock

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
      Tester for the auxi.modeling.business.clock class.
    """

    def setUp(self):
        self.object = Clock("NameA",
                            description="DescriptionA",
                            start_datetime=datetime(2016, 2, 1),
                            timestep_period_duration=TimePeriod.year,
                            timestep_period_count=3)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.start_datetime, datetime(2016, 2, 1))
        self.assertEqual(self.object.timestep_period_duration, TimePeriod.year)
        self.assertEqual(self.object.timestep_period_count, 3)

    def test_tick(self):
        self.assertEqual(self.object.timestep_ix, 0)
        self.object.tick()
        self.assertEqual(self.object.timestep_ix, 1)

    def test_reset(self):
        self.object.tick()
        self.object.reset()
        self.assertEqual(self.object.timestep_ix, 0)

    def test_get_datetime_at_period_ix(self):
        self.assertEqual(self.object.get_datetime_at_period_ix(3),
                         datetime(2019, 2, 1))

    def test_get_datetime(self):
        self.object.tick()
        self.assertEqual(self.object.get_datetime(), datetime(2017, 2, 1))

# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(SalesRule)

if __name__ == '__main__':
    unittest.main()
