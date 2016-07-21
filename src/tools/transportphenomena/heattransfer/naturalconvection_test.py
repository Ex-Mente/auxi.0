#!/usr/bin/env python3
"""
This module contains all the code used to test the testee module.
"""


import unittest
from os.path import realpath, dirname

from auxi.tools.transportphenomena.heattransfer import naturalconvection as testee
from auxi.tools.materialphysicalproperties.gases import air


__version__ = '0.3.0'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


MODULE_PATH = dirname(realpath(__file__))


class IsothermalFlatSurface_RegionTester(unittest.TestCase):

    def setUp(self):
        self.region = testee.IsothermalFlatSurface.Region(
            "r1", -90, True, -60, True, None, False, 4, False)

    def test_constructor(self):
        self.assertEqual(self.region.theta_min, -90)
        self.assertTrue(self.region.theta_min_incl, True)
        self.assertEqual(self.region.theta_max, -60)
        self.assertTrue(self.region.theta_max_incl)
        self.assertIsNone(self.region.Ra_min)
        self.assertFalse(self.region.Ra_min_incl)
        self.assertEqual(self.region.Ra_max, 4)
        self.assertFalse(self.region.Ra_max_incl)

    def test_contains_point(self):
        # testing theta < min boundary
        self.assertFalse(self.region.contains_point(-91, 3))
        # testing theta > max boundary
        self.assertFalse(self.region.contains_point(-59, 3))
        # testing Ra > max boundary
        self.assertFalse(self.region.contains_point(-75, 5))
        # testing all within boundary
        self.assertTrue(self.region.contains_point(-75, 3))

    @unittest.skip("Todo: Implement Test. I do not know how to.")
    def test_plot_region(self):
        self.assertFalse(True)


class IsothermalFlatSurfaceTester(unittest.TestCase):

    def setUp(self):
        self.model = testee.IsothermalFlatSurface(air)

        self.L = 0.4
        self.theta = 0.0
        self.Ts = 313.0
        self.Tf = 283.0

    def test_constructor(self):
        self.assertEqual(self.model.references, None)
        self.assertEqual(len(self.model.equation_dict), 22)
        self.assertEqual(len(self.model.regions), 22)

    def test_Nu_x(self):
        Nu_x = self.model.Nu_x(self.L, self.theta, self.Ts, T=self.Tf)
        self.assertAlmostEqual(Nu_x, 64.1972833727)

    def test_Nu_L(self):
        Nu_L = self.model.Nu_L(self.L, self.theta, self.Ts, T=self.Tf)
        self.assertAlmostEqual(Nu_L, 85.5963778303)

    def test_h_x(self):
        h_x = self.model.h_x(self.L, self.theta, self.Ts, T=self.Tf)
        self.assertAlmostEqual(h_x, 4.21863186596)

    def test_h_L(self):
        h_L = self.model.h_L(self.L, self.theta, self.Ts, T=self.Tf)
        self.assertAlmostEqual(h_L, 5.62484248795)

    def test_plot_regions(self):
        pass

if __name__ == '__main__':
    unittest.main()
