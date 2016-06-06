#!/usr/bin/env python3
"""
This module provides testing code for classes in the thermo module.
"""

# TODO: material package uses materials 'assays' property.
#       Material does not have an 'assays' property,
#       only a raw_assays and converted_assays property.

import unittest

import numpy as np

from auxi.core.helpers import get_path_relative_to_module as get_path
from auxi.tools.chemistry import thermochemistry as thermo
from auxi.modelling.process.materials.thermo import Material, MaterialPackage

__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class ThermoMaterialUnitTester(unittest.TestCase):
    """
    Unit tester for the auxi.modelling.process.materials.thermo.Material class.
    """

    def setUp(self):
        thermo.default_data_path = 'data/nist'
        test_data_file_path = get_path(
            __file__, 'data/thermomaterial.test.ilmenite.txt')
        self.m = Material("material", test_data_file_path)

    def test_constructor(self):
        self.assertEqual(self.m.name, "material")
        self.assertEqual(len(self.m.compounds), 14)
        self.assertEqual(self.m.compound_count, 14)
        self.assertEqual(len(self.m.converted_assays), 3)

    def test_get_compound_index(self):
        self.assertEqual(self.m.get_compound_index("Al2O3[S]"), 0)
        self.assertEqual(self.m.get_compound_index("K2O[S]"), 6)
        self.assertEqual(self.m.get_compound_index("P4O10[S]"), 10)
        self.assertEqual(self.m.get_compound_index("V2O5[S]"), 13)

    def test_create_empty_assay(self):
        empty_assay = self.m.create_empty_assay()
        self.assertEqual(len(empty_assay), 14)
        self.assertEqual(empty_assay.sum(), 0.0)
        self.assertEqual(empty_assay.sum(), 0.0)
        self.assertEqual(empty_assay.sum(), 0.0)

    def test_add_assay(self):
        new_assay = self.m.create_empty_assay()
        new_assay[0] = 0.5
        new_assay[2] = 0.5
        self.m.add_assay("new_assay", new_assay)
        self.assertEqual(
            np.all(self.m.converted_assays["new_assay"] == new_assay), True)

    def test_get_assay_total(self):
        self.assertAlmostEqual(self.m.get_assay_total("IlmeniteA"), 0.99792)
        self.assertAlmostEqual(self.m.get_assay_total("IlmeniteB"), 0.99761)
        self.assertAlmostEqual(self.m.get_assay_total("IlmeniteC"), 1.00002)

    def test_create_package(self):
        pkg = self.m.create_package("IlmeniteA", 123.456, 0.87, 205.0, True)
        self.assertEqual(pkg.mass, 123.456)
        self.assertEqual(pkg.P, 0.87)
        self.assertEqual(pkg.T, 205.0)
        self.assertEqual(pkg.H, -278.35680682442677)


class ThermoMaterialPackageUnitTester(unittest.TestCase):
    """
    Unit tester for the auxi.modelling.process.materials.thermo.MaterialPackage
    class.
    """

    def setUp(self):
        self.ilm = Material("ilmenite",
                            get_path(__file__,
                                     'data/thermomaterial.test.ilmenite.txt'))
        self.ilm_pkg_a = self.ilm.create_package("IlmeniteA", 1234.5, 0.8,
                                                 100.0, True)
        self.ilm_pkg_b = self.ilm.create_package("IlmeniteB", 2345.6, 0.9,
                                                 200.0, True)
        self.ilm_pkg_c = self.ilm.create_package("IlmeniteC", 3456.7, 1.0,
                                                 300.0, True)

        self.red = Material("reductant",
                            get_path(__file__,
                                     'data/thermomaterial.test.reductant.txt'))
        self.red_pkg_a = self.red.create_package("ReductantA", 123.45, 0.75,
                                                 400.0, True)

        self.mix = Material("mix",
                            get_path(__file__,
                                     'data/thermomaterial.test.mix.txt'))

    def test_constructor(self):
        compound_masses = self.ilm.converted_assays["IlmeniteB"] * 123.4 / \
                          self.ilm.converted_assays["IlmeniteB"].sum()
        package = MaterialPackage(self.ilm, compound_masses, 0.8, 300.0)
        self.assertAlmostEqual(package.mass, 123.4)
        self.assertEqual(package.P, 0.8)
        self.assertEqual(package.T, 300.0)
        self.assertAlmostEqual(package.H, -236.60618829889296)

    def test___str__(self):
        print(self.ilm_pkg_a.__str__())

    def test_add_operator_1(self):
        """
        Test whether the add operator calculates the resulting package
        correctly. Results were checked against FactSage results. They are not
        exactly the same, since the magnetic and other non-cp contributions are
        omitted by the thermo module.
        """

        pkg_ab = self.ilm_pkg_a + self.ilm_pkg_b
        pkg_ac = self.ilm_pkg_a + self.ilm_pkg_c
        pkg_bc = self.ilm_pkg_b + self.ilm_pkg_c
        pkg_abc = self.ilm_pkg_a + self.ilm_pkg_b + self.ilm_pkg_c

        self.assertAlmostEqual(self.ilm_pkg_a.mass, 1234.5)
        self.assertAlmostEqual(self.ilm_pkg_a.P, 0.8)
        self.assertAlmostEqual(self.ilm_pkg_a.T, 100.0)
        self.assertAlmostEqual(self.ilm_pkg_a.H, -2811.6976363963095)

        self.assertAlmostEqual(self.ilm_pkg_b.mass, 2345.6)
        self.assertAlmostEqual(self.ilm_pkg_b.P, 0.9)
        self.assertAlmostEqual(self.ilm_pkg_b.T, 200.0)
        self.assertAlmostEqual(self.ilm_pkg_b.H, -4550.3197620429773)

        self.assertAlmostEqual(self.ilm_pkg_c.mass, 3456.7)
        self.assertAlmostEqual(self.ilm_pkg_c.P, 1.0)
        self.assertAlmostEqual(self.ilm_pkg_c.T, 300.0)
        self.assertAlmostEqual(self.ilm_pkg_c.H, -8023.545629913353)

        self.assertAlmostEqual(pkg_ab.mass, 3580.1)
        self.assertAlmostEqual(pkg_ab.P, 0.8)
        self.assertAlmostEqual(pkg_ab.T, 165.93941355722774)
        self.assertAlmostEqual(pkg_ab.H, self.ilm_pkg_a.H + self.ilm_pkg_b.H)

        self.assertAlmostEqual(pkg_ac.mass, 4691.2)
        self.assertAlmostEqual(pkg_ac.P, 0.8)
        self.assertAlmostEqual(pkg_ac.T, 249.48206641333098)
        self.assertAlmostEqual(pkg_ac.H, self.ilm_pkg_a.H + self.ilm_pkg_c.H)

        self.assertAlmostEqual(pkg_bc.mass, 5802.3)
        self.assertAlmostEqual(pkg_bc.P, 0.9)
        self.assertAlmostEqual(pkg_bc.T, 260.56905390294497)
        self.assertAlmostEqual(pkg_bc.H, self.ilm_pkg_b.H + self.ilm_pkg_c.H)

        self.assertAlmostEqual(pkg_abc.mass, 7036.8)
        self.assertAlmostEqual(pkg_abc.P, 0.8)
        self.assertAlmostEqual(pkg_abc.T, 233.3038145723261)
        self.assertAlmostEqual(pkg_abc.H, self.ilm_pkg_a.H +
                               self.ilm_pkg_b.H + self.ilm_pkg_c.H)

    def test_add_operator_2(self):
        mixPackage = self.mix.create_package(None, 0.0)
        mixPackage = mixPackage + self.ilm_pkg_a
        mixPackage = mixPackage + self.red_pkg_a

        self.assertEqual(mixPackage.mass,
                         self.ilm_pkg_a.mass + self.red_pkg_a.mass)
        self.assertEqual(mixPackage.P, 1.0)
        self.assertAlmostEqual(mixPackage.T, 146.64409455076031)
        self.assertEqual(mixPackage.H, self.ilm_pkg_a.H + self.red_pkg_a.H)

        self.assertRaises(Exception, self.add_incompatible_packages)

    def add_incompatible_packages(self):
        result = self.ilm_pkg_a + self.red_pkg_a
        result = result * 1.0

    def test_add_operator_3(self):
        """
        other = tuple (compound, mass)

        Test whether the add operator calculates the resulting package
        correctly. Results were checked against FactSage results. They are not
        exactly the same, since the magnetic and other non-cp contributions are
        omitted by the thermo module.
        """

        pkg = self.ilm_pkg_a + ("Al2O3[S1]", 123.4)

        self.assertEqual(pkg.mass, 1357.9)
        self.assertEqual(pkg.P, 0.8)
        self.assertEqual(pkg.T, 100.0)
        self.assertEqual(pkg.H, self.ilm_pkg_a.H + thermo.H("Al2O3[S1]", 100.0,
                                                            123.4))

    def test_add_operator_4(self):
        """
        other = tuple (compound, mass, temperature)

        Test whether the add operator calculates the resulting package
        correctly. Results were checked against FactSage results. They are not
        exactly the same, since the magnetic and other non-cp contributions are
        omitted by the thermo module.
        """

        pkg = self.ilm_pkg_a + ("Al2O3[S1]", 123.4, 500.0)

        self.assertEqual(pkg.mass, 1357.9)
        self.assertEqual(pkg.P, 0.8)
        self.assertEqual(pkg.T, 151.60776535105211)
        self.assertEqual(pkg.H, self.ilm_pkg_a.H + thermo.H("Al2O3[S1]", 500.0,
                                                            123.4))

    def test_extract_1(self):
        pkg = self.ilm_pkg_a.clone()
        mass = 432.1
        diffPackage = pkg.extract(mass)

        self.assertEqual(pkg.mass, self.ilm_pkg_a.mass - mass)
        self.assertEqual(pkg.P, 0.8)
        self.assertEqual(pkg.T, 100.0)

        self.assertAlmostEqual(diffPackage.mass, mass)
        self.assertEqual(diffPackage.P, 0.8)
        self.assertEqual(diffPackage.T, 100.0)

        self.assertEqual(pkg.H + diffPackage.H, self.ilm_pkg_a.H)

    def test_extract_2(self):
        pkg = self.ilm_pkg_a.clone()
        compound = "TiO2[S1]"
        mass = 123.4
        diffPackage = pkg.extract((compound, mass))

        self.assertEqual(pkg.mass,
                         self.ilm_pkg_a.mass - mass + 2.0E-13)
        self.assertEqual(pkg.get_compound_mass(compound),
                         self.ilm_pkg_a.get_compound_mass(compound) - mass)
        self.assertEqual(pkg.P, 0.8)
        self.assertEqual(pkg.T, 100.0)

        self.assertEqual(diffPackage.mass, mass)
        self.assertEqual(diffPackage.get_compound_mass(compound), mass)
        self.assertEqual(diffPackage.P, 0.8)
        self.assertEqual(diffPackage.T, 100.0)

        self.assertEqual(pkg.H + diffPackage.H, self.ilm_pkg_a.H)

    def test_extract_3(self):
        pkg = self.ilm_pkg_a.clone()
        compound = "TiO2[S1]"
        mass = pkg.get_compound_mass(compound)
        diffPackage = pkg.extract(compound)

        self.assertAlmostEqual(pkg.mass, self.ilm_pkg_a.mass - mass)
        self.assertEqual(pkg.get_compound_mass(compound), self.ilm_pkg_a.get_compound_mass(compound) - mass)
        self.assertEqual(pkg.P, 0.8)
        self.assertEqual(pkg.T, 100.0)

        self.assertEqual(diffPackage.mass, mass)
        self.assertEqual(diffPackage.get_compound_mass(compound), mass)
        self.assertEqual(diffPackage.P, 0.8)
        self.assertEqual(diffPackage.T, 100.0)

        self.assertEqual(pkg.H + diffPackage.H, self.ilm_pkg_a.H)

    def test_multiply_operator(self):
        pkg = self.ilm_pkg_a.clone()

        mul1Package = pkg * 0.0
        self.assertEqual(mul1Package.mass, 0.0)
        self.assertTrue(np.all(mul1Package._compound_masses == pkg._compound_masses * 0.0))
        self.assertEqual(mul1Package.P, pkg.P)
        self.assertEqual(mul1Package.T, pkg.T)
        self.assertEqual(mul1Package.H, 0.0)

        mul2Package = pkg * 1.0
        self.assertEqual(mul2Package.mass, pkg.mass)
        self.assertTrue(np.all(mul2Package._compound_masses == pkg._compound_masses))
        self.assertEqual(mul2Package.P, pkg.P)
        self.assertEqual(mul2Package.T, pkg.T)
        self.assertEqual(mul2Package.H, pkg.H)

        mul2Package = pkg * 123.4
        self.assertEqual(mul2Package.mass, pkg.mass * 123.4 + 3.0E-11)
        self.assertTrue(np.all(mul2Package._compound_masses == pkg._compound_masses * 123.4))
        self.assertEqual(mul2Package.P, pkg.P)
        self.assertEqual(mul2Package.T, pkg.T)
        self.assertEqual(mul2Package.H, pkg.H * 123.4 - 6.0E-11)

    def test_clone(self):
        clone = self.ilm_pkg_a.clone()

        self.assertEqual(clone.mass, self.ilm_pkg_a.mass)
        self.assertTrue(np.all(clone._compound_masses == self.ilm_pkg_a._compound_masses))
        self.assertEqual(clone.P, self.ilm_pkg_a.P)
        self.assertEqual(clone.T, self.ilm_pkg_a.T)
        self.assertEqual(clone.H, self.ilm_pkg_a.H)

    def test_mass(self):
        self.assertEqual(self.ilm_pkg_a.mass, 1234.5)
        self.assertEqual(self.ilm_pkg_b.mass, 2345.6)
        self.assertEqual(self.ilm_pkg_c.mass, 3456.7)

    def test_get_assay(self):
        self.assertTrue(np.all(self.ilm_pkg_a.get_assay() - self.ilm.converted_assays["IlmeniteA"] / self.ilm.converted_assays["IlmeniteA"].sum() < 1.0E-16))
        self.assertTrue(np.all(self.ilm_pkg_a.get_assay() - self.ilm.converted_assays["IlmeniteA"] / self.ilm.converted_assays["IlmeniteA"].sum() > -1.0E-16))

    def test_get_compound_mass(self):
        assay = "IlmeniteA"
        compound = "TiO2[S1]"
        for compound in self.ilm.compounds:
            mass = 1234.5 * self.ilm.converted_assays[assay][self.ilm.get_compound_index(compound)] / self.ilm.get_assay_total(assay)
            self.assertEqual(self.ilm_pkg_a.get_compound_mass(compound), mass)

    def test_set_H(self):
        tempPackageA = self.ilm_pkg_a.clone()
        H = tempPackageA.H + 5.67
        tempPackageA.H = H

        self.assertEqual(tempPackageA.H, H)
        self.assertEqual(tempPackageA.T, 121.65612974840057)

    def test_get_H(self):
        self.assertEqual(self.ilm_pkg_a.H, self.ilm_pkg_a._H)

    def test_set_T(self):
        tempPackageA = self.ilm_pkg_a.clone()
        T = tempPackageA.T + 123.4
        tempPackageA.T = T

        self.assertEqual(tempPackageA.T, T)
        self.assertEqual(tempPackageA.H, -2778.3170030281622)

    def test_get_T(self):
        self.assertEqual(self.ilm_pkg_a.T, self.ilm_pkg_a._T)

    def test_get_P(self):
        self.assertEqual(self.ilm_pkg_a.P, self.ilm_pkg_a._P)

    def test_get_element_masses(self):
        x = self.ilm_pkg_a.get_element_masses()
        y = self.ilm_pkg_a.get_element_mass("Ti")


if __name__ == '__main__':
    unittest.main()
