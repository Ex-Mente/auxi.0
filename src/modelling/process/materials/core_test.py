#!/usr/bin/env python3
"""
This module provides testing code for classes in the chem module.
"""

import unittest

from auxi.modelling.process.materials.core import Material
from auxi.tools.materialphysicalproperties.gases import air_dict


__version__ = '0.3.0'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class MaterialTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.process.materials.core.Material class.
    """

    def test_constructor(self):
        Material('Test Material', air_dict, 'Test material.')

    def test_beta(self):
        m = Material('Test Material', air_dict, 'Test material.')

        T = 300.0
        self.assertEqual(m.beta(T=T), 1.0/T)

if __name__ == '__main__':
    unittest.main()
