# -*- coding: utf-8 -*-
"""
This module provides testing code for the thermochemistry module.
"""

import unittest

from auxi.tools.chemistry import thermochemistry as thermo


__version__ = '0.2.0rc6'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


# TODO: Create tests for: write_compound_to_auxi_file, load_data_factsage,
#   load_data_auxi, list_compounds, molar_mass
# TODO: Test CpRecord, Phase and Compound classes sperately?

class ThermoFunctionTester(unittest.TestCase):
    """
    The function tester for the thermochemistry module.
    """

    def assertAlmostEqual(self, first, second, places=14, msg=None,
                          delta=None):
        if type(first) is list and type(second) is list:
            self.assertEqual(len(first), len(second))
            for f, s in zip(first, second):
                self.assertAlmostEqual(f, s)
        else:
            super(ThermoFunctionTester, self).assertAlmostEqual(
                first, second, places, msg, delta)

    def test_Cp(self):
        self.assertAlmostEqual(thermo.Cp("Al2O3[S]", 1000.0),
                               0.00034731792422193833)
        #                       0.00036892922607564924)

    def test_H(self):
        self.assertAlmostEqual(thermo.H("Al2O3[S]", 1000.0),
                               0.2957519136468089)
        #                       -4.192397399191783)

    def test_S(self):
        self.assertAlmostEqual(thermo.S("Al2O3[S]", 1000.0),
                               0.0005662425810664761)
        #                       0.0005987306605872277)

    def test_G(self):
        self.assertAlmostEqual(thermo.G("Al2O3[S]", 1000.0),
                               -0.42515982843797523)
        #                       0.0005662425810664761)


if __name__ == '__main__':
    unittest.main()
