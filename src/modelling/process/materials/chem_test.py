#!/usr/bin/env python3
"""
This module provides testing code for classes in the chem module.
"""

import unittest

from auxi.core.helpers import get_path_relative_to_module as get_path
from auxi.modelling.process.materials.chem import Material, MaterialPackage


__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class ChemMaterialUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.process.materials.chem.Material class.
    """

    def assertAlmostEqual(self, first, second, places=14, msg=None,
                          delta=None):
        if type(first) is list and type(second) is list:
            self.assertEqual(len(first), len(second))
            for f, s in zip(first, second):
                self.assertAlmostEqual(f, s)
        else:
            super(ChemMaterialUnitTester, self).assertAlmostEqual(
                first, second, places, msg, delta)

    def setUp(self):
        test_data_file_path = get_path(
            __file__, 'data/chemmaterial.test.ilmenite.txt')
        self.material = Material("material", test_data_file_path)

    def test_constructor(self):
        self.assertEqual(self.material.name, "material")
        self.assertEqual(len(self.material.compounds), 14)
        self.assertEqual(self.material.compound_count, 14)
        self.assertEqual(len(self.material.assays), 3)

    def test_get_compound_index(self):
        self.assertEqual(self.material.get_compound_index("Al2O3"), 0)
        self.assertEqual(self.material.get_compound_index("K2O"), 6)
        self.assertEqual(self.material.get_compound_index("P4O10"), 10)
        self.assertEqual(self.material.get_compound_index("V2O5"), 13)

    def test_create_empty_assay(self):
        empty_assay = self.material.create_empty_assay()
        self.assertEqual(len(empty_assay), 14)
        self.assertEqual(sum(empty_assay), 0.0)
        self.assertEqual(sum(empty_assay), 0.0)
        self.assertEqual(sum(empty_assay), 0.0)

    def test_add_assay(self):
        new_assay = self.material.create_empty_assay()
        new_assay[0] = 0.5
        new_assay[2] = 0.5
        self.material.add_assay("new_assay", new_assay)
        self.assertTrue(self.material.assays["new_assay"] == new_assay)

    def test_get_assay_total(self):
        self.assertAlmostEqual(self.material.get_assay_total("IlmeniteA"),
                               0.99791999999999992)
        self.assertAlmostEqual(self.material.get_assay_total("IlmeniteB"),
                               0.99760999999999989)
        self.assertAlmostEqual(self.material.get_assay_total("IlmeniteC"),
                               1.0000200000000001)

    def test_create_package(self):
        package = self.material.create_package("IlmeniteA", 123.456, True)
        self.assertEqual(package.get_mass(), 123.456)


class ChemMaterialPackageUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.process.materials.chemistry.material.Material
    class.
    """

    def setUp(self):
        path = get_path(__file__, 'data/chemmaterial.test.ilmenite.txt')
        self.ilm = Material("ilmenite", path)

        self.ilm_pkg_a = self.ilm.create_package("IlmeniteA", 1234.5, True)
        self.ilm_pkg_b = self.ilm.create_package("IlmeniteB", 2345.6, True)
        self.ilm_pkg_c = self.ilm.create_package("IlmeniteC", 3456.7, True)

        path = get_path(__file__, 'data/chemmaterial.test.reductant.txt')
        self.red = Material("reductant", path)

        self.red_pkg_a = self.red.create_package("ReductantA", 123.45, True)

        path = get_path(__file__, 'data/chemmaterial.test.mix.txt')
        self.mix = Material("mix", path)

    def test_constructor(self):
        m_sum = sum(self.ilm.assays["IlmeniteB"])
        compound_masses = [(m * 123.4) / m_sum
                           for m in self.ilm.assays["IlmeniteB"]]
        package = MaterialPackage(self.ilm, compound_masses)
        self.assertAlmostEqual(package.get_mass(), 123.4)

    def test_add_operator_1(self):
        """
        other = MaterialPackage

        Test whether the add operator calculates the resulting package
        correctly. Results were checked against FactSage results. They are not
        exactly the same, since the magnetic and other non-cp contributions are
        omitted by the thermo module.
        """

        pkg_a_plus_b = self.ilm_pkg_a + self.ilm_pkg_b
        pkg_a_plus_c = self.ilm_pkg_a + self.ilm_pkg_c
        pkg_b_plus_c = self.ilm_pkg_b + self.ilm_pkg_c
        pkg_a_plus_b_plus_c = self.ilm_pkg_a + self.ilm_pkg_b + \
            self.ilm_pkg_c

        self.assertAlmostEqual(self.ilm_pkg_a.get_mass(), 1234.5)

        self.assertAlmostEqual(self.ilm_pkg_b.get_mass(), 2345.6)

        self.assertAlmostEqual(self.ilm_pkg_c.get_mass(), 3456.7)

        self.assertAlmostEqual(pkg_a_plus_b.get_mass(), 3580.1)

        self.assertAlmostEqual(pkg_a_plus_c.get_mass(), 4691.2)

        self.assertAlmostEqual(pkg_b_plus_c.get_mass(), 5802.3)

        self.assertAlmostEqual(pkg_a_plus_b_plus_c.get_mass(), 7036.8)

    def test_add_operator_2(self):
        """
        Tests the scenario when a 'mix' is created and two packages
        'mixed' into the mix package.
        """
        mix_package = self.mix.create_package(None, 0.0)
        mix_package = mix_package + self.ilm_pkg_a
        mix_package = mix_package + self.red_pkg_a

        self.assertAlmostEqual(mix_package.get_mass(),
                               self.ilm_pkg_a.get_mass() +
                               self.red_pkg_a.get_mass(),
                               places=10)

        self.assertRaises(Exception, self.add_incompatible_packages)

    def add_incompatible_packages(self):
        result = self.ilm_pkg_a + self.red_pkg_a
        result = result * 1.0

    def test_add_operator_3(self):
        """other = tuple (compound, mass)
        Test whether the add operator calculates the resulting package
        correctly. Results were checked against FactSage results. They are not
        exactly the same, since the magnetic and other non-cp contributions are
        omitted by the thermo module.
        """

        packageAplusAl2O3 = self.ilm_pkg_a + ("Al2O3", 123.4)

        self.assertEqual(packageAplusAl2O3.get_mass(), 1357.9)

    def test_extract_1(self):
        temp_package_a = self.ilm_pkg_a.clone()
        mass = 432.1
        diff_package = temp_package_a.extract(mass)

        self.assertAlmostEqual(temp_package_a.get_mass(),
                               self.ilm_pkg_a.get_mass() - mass)

        self.assertAlmostEqual(diff_package.get_mass(), mass)

    def test_subtract_operator_2(self):
        temp_package_a = self.ilm_pkg_a.clone()
        compound = "TiO2"
        mass = 123.4
        diff_package = temp_package_a.extract((compound, mass))

        self.assertAlmostEqual(temp_package_a.get_mass(),
                               self.ilm_pkg_a.get_mass() - mass)
        self.assertAlmostEqual(temp_package_a.get_compound_mass(compound),
                               self.ilm_pkg_a.get_compound_mass(compound) -
                               mass)

        self.assertEqual(diff_package.get_mass(), mass)
        self.assertEqual(diff_package.get_compound_mass(compound), mass)

    def test_subtract_operator_3(self):
        temp_package_a = self.ilm_pkg_a.clone()
        compound = "TiO2"
        mass = temp_package_a.get_compound_mass(compound)
        diff_package = temp_package_a.extract(compound)

        self.assertAlmostEqual(temp_package_a.get_mass(),
                               self.ilm_pkg_a.get_mass() - mass)
        self.assertAlmostEqual(temp_package_a.get_compound_mass(compound),
                               self.ilm_pkg_a.get_compound_mass(compound) -
                               mass)

        self.assertEqual(diff_package.get_mass(), mass)
        self.assertEqual(diff_package.get_compound_mass(compound), mass)

    def test_multiply_operator(self):
        temp_package_a = self.ilm_pkg_a.clone()

        mul_package_1 = temp_package_a * 0.0
        self.assertEqual(mul_package_1.get_mass(), 0.0)
        self.assertTrue(mul_package_1.compound_masses == [0.0] *
                        len(temp_package_a.compound_masses))

        mul_package_2 = temp_package_a * 1.0
        self.assertAlmostEqual(mul_package_2.get_mass(),
                               temp_package_a.get_mass(),
                               places=10)
        self.assertTrue(mul_package_2.compound_masses ==
                        temp_package_a.compound_masses)

        mul_package_2 = temp_package_a * 123.4
        self.assertAlmostEqual(mul_package_2.get_mass(),
                               temp_package_a.get_mass() * 123.4)
        self.assertTrue(mul_package_2.compound_masses ==
                        [m * 123.4 for m in temp_package_a.compound_masses])

    def test_clone(self):
        clone = self.ilm_pkg_a.clone()

        self.assertEqual(clone.get_mass(), self.ilm_pkg_a.get_mass())
        self.assertTrue(clone.compound_masses ==
                        self.ilm_pkg_a.compound_masses)

    def test_get_mass(self):
        self.assertAlmostEqual(self.ilm_pkg_a.get_mass(), 1234.5)
        self.assertAlmostEqual(self.ilm_pkg_b.get_mass(), 2345.6)
        self.assertAlmostEqual(self.ilm_pkg_c.get_mass(), 3456.7)

    def test_get_assay(self):
        ass = self.ilm.assays["IlmeniteA"]
        ass_sum = sum(ass)
        for ix, val in enumerate(self.ilm_pkg_a.get_assay()):
            self.assertTrue(val-(ass[ix] / ass_sum) < 1.0E-16)
            self.assertTrue(val-(ass[ix] / ass_sum) > -1.0E-16)

    def test_get_compound_mass(self):
        assay = "IlmeniteA"
        compound = "TiO2"
        for compound in self.ilm.compounds:
            index = self.ilm.get_compound_index(compound)
            mass = 1234.5 * self.ilm.assays[assay][index] / \
                self.ilm.get_assay_total(assay)
            self.assertEqual(
                self.ilm_pkg_a.get_compound_mass(compound),
                mass)

    def test_get_element_masses(self):
        x = self.ilm_pkg_a.get_element_masses()
        y = self.ilm_pkg_a.get_element_mass("Ti")


if __name__ == '__main__':
    unittest.main()
