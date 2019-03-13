#!/usr/bin/env python3
"""
This module provides testing code for classes in the chem module.
"""

import unittest

from auxi.modelling.process.core import Model


__version__ = '0.3.6'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Johan Zietsman'
__credits__ = ['Johan Zietsman']
__maintainer__ = 'Johan Zietsman'
__email__ = 'johan.zietsman@ex-mente.co.za'
__status__ = 'Planning'


class ModelTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.process.core.Model class.
    """

    def test_constructor(self):
        Model('Test Model', 'Test model.')


if __name__ == '__main__':
    unittest.main()
