#!/usr/bin/env python3
"""
This module provides testing code for classes in the chem module.
"""

import unittest

from auxi.modelling.core import Project


__version__ = '0.3.5'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class ProjectTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.core.Project class.
    """

    def test_constructor(self):
        Model('Test Project', 'Test project.')


if __name__ == '__main__':
    unittest.main()
