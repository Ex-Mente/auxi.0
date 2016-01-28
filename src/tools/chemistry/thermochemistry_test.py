# -*- coding: utf-8 -*-
"""
This module provides testing code for the thermo module.

@author: Johan Zietsman
"""
__version__ = "0.0.2"

import os
import sys
from auxi.tools.chemistry import thermochemistry as thermo
import unittest


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):

    def test_Cp(self):
        self.assertEqual(thermo.Cp("Al2O3[S1]", 1000.0), 0.00036892922607564924)

    def test_H(self):
        self.assertEqual(thermo.H("Al2O3[S1]", 1000.0), -4.192397399191783)

    def test_S(self):
        self.assertEqual(thermo.S("Al2O3[S1]", 1000.0), 0.0005987306605872277)

    def test_G(self):
        self.assertEqual(thermo.G("Al2O3[S1]", 1000.0), -4.954671339718413)


# =============================================================================
# Display documentation and run tests.
# =============================================================================

if __name__ == '__main__':
    os.system("cls")
    unittest.main()
