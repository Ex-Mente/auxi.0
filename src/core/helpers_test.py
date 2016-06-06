#!/usr/bin/env python3
"""
This module contains code used to test core helpers classes.
"""

import unittest
import os
from datetime import datetime, date

from auxi.core.helpers import get_path_relative_to_module, get_date

__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class HelpersUnitTester(unittest.TestCase):
    """
    The unit tester for the helpers functions being tested.
    """

    def test_get_path_relative_to_module(self):
        path = get_path_relative_to_module(__file__, "test/test.txt")
        dr = os.path.dirname(__file__)
        self.assertEqual(
            path,
            os.path.join(dr, "test/test.txt"))

    def test_get_date(self):
        dt = date(2016, 4, 14)
        self.assertEqual(get_date(dt), dt)
        self.assertEqual(get_date("2016-04-14"), dt)


if __name__ == '__main__':
    unittest.main()
