#!/usr/bin/env python3
"""
This module provides testing code for the
auxi.core.time module.
"""

import unittest
from datetime import datetime

from auxi.core.time import Clock, TimePeriod

__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class ClockUnitTester(unittest.TestCase):
    """
    Tester for the auxi.core.time.Clock class.
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


if __name__ == '__main__':
    unittest.main()
