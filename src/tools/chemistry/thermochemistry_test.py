# -*- coding: utf-8 -*-
"""
This module provides testing code for the thermochemistry module.
"""

import unittest

from auxi.tools.chemistry import thermochemistry as thermo


__version__ = '0.2.1'
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

    def test_load_data_auxi(self):
        thermo.compounds.clear()
        thermo.load_data_auxi()
        self.assertEqual(len(thermo.compounds), 81)

    def test_compound_get_phase_list(self):
        phs = thermo.compounds["Ag"].get_phase_list()
        self.assertEqual(phs[0], "L")
        self.assertEqual(phs[1], "S")

    def test_phase___str__(self):
        phs = thermo.compounds["Ag"].get_phase_list()
        self.assertTrue(len(phs[0].__str__()) > 0)

    def test_cpRecord___str__(self):
        ph = thermo.compounds["Ag"]._phases['L']
        for t, cpr in ph._Cp_records.items():
            self.assertTrue(len(cpr.__str__()) > 0)
            break

    def test_get_datafile_references(self):
        refs = thermo.get_datafile_references()
        self.assertTrue("rao1985" in refs)
        self.assertTrue(len(refs["rao1985"]) > 0)

    def test_get_reference(self):
        self.assertEqual("rao1985", thermo.compounds["Ag"].reference)
        self.assertTrue(len(thermo.compounds["Ag"].get_reference()) > 0)

    def test_molar_mass(self):
        self.assertAlmostEqual(thermo.molar_mass("FeO"), 0.0718444)

    def test_Cp(self):
        self.assertAlmostEqual(thermo.Cp("Al2O3[S]", 1000.0),
                               0.00034731792422193833)
        #                       0.00036892922607564924)

    def test_H(self):
        self.assertAlmostEqual(thermo.H("Al2O3[S]", 1000.0),
                               -4.264869218634823)
        #                       -4.192397399191783)

    def test_S(self):
        self.assertAlmostEqual(thermo.S("Al2O3[S]", 1000.0),
                               0.0005662425810664761)
        #                       0.0005987306605872277)

    def test_G(self):
        self.assertAlmostEqual(thermo.G("Al2O3[S]", 1000.0),
                               -4.985780960719607)
        #                       0.0005662425810664761)


if __name__ == '__main__':
    unittest.main()
