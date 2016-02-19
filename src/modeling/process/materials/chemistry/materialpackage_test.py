# -*- coding: utf-8 -*-
"""
This module provides testing code for the chemistry material module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
import os
import numpy
from auxi.modeling.process.materials.chemistry import material
from auxi.modeling.process.materials.chemistry.material import Material
from auxi.modeling.process.materials.chemistry.material import MaterialPackage

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestMaterialPackage(unittest.TestCase):
    """Tester for the auxi.modeling.process.materials.chemistry.material.Material class."""
    def setUp(self):
        self.ilmenite = Material("ilmenite",
                                 os.path.join(material.DEFAULT_DATA_PATH,
                                 r"chemmaterial.test.ilmenite.txt"))
        self.ilmenite_package_a = self.ilmenite.create_package("IlmeniteA",
                                                             1234.5, True)
        self.ilmenite_package_b = self.ilmenite.create_package("IlmeniteB",
                                                             2345.6, True)
        self.ilmenite_package_c = self.ilmenite.create_package("IlmeniteC",
                                                             3456.7, True)
        self.reductant = Material("reductant",
                                  os.path.join(material.DEFAULT_DATA_PATH,
                                  r"chemmaterial.test.reductant.txt"))
        self.reductant_package_a = self.reductant.create_package("ReductantA",
                                                               123.45, True)
        self.mix = Material("mix", os.path.join(material.DEFAULT_DATA_PATH,
                                                r"chemmaterial.test.mix.txt"))

    def test_constructor(self):
        compound_masses = self.ilmenite.assays["IlmeniteB"] * 123.4 / \
                          self.ilmenite.assays["IlmeniteB"].sum()
        package = MaterialPackage(self.ilmenite, compound_masses)
        self.assertAlmostEqual(package.get_mass(), 123.4,
                               places=10)

    def test_add_operator_1(self):
        """other = MaterialPackage
        Test whether the add operator calculates the resulting package
        correctly. Results were checked against FactSage results. They are not
        exactly the same, since the magnetic and other non-cp contributions are
        omitted by the thermo module.
        """

        package_a_plus_b = self.ilmenite_package_a + self.ilmenite_package_b
        package_a_plus_c = self.ilmenite_package_a + self.ilmenite_package_c
        package_b_plus_c = self.ilmenite_package_b + self.ilmenite_package_c
        package_a_plus_b_plus_c = self.ilmenite_package_a + \
                             self.ilmenite_package_b + \
                             self.ilmenite_package_c

        self.assertAlmostEqual(self.ilmenite_package_a.get_mass(), 1234.5,
                               places=10)

        self.assertAlmostEqual(self.ilmenite_package_b.get_mass(), 2345.6,
                               places=10)

        self.assertAlmostEqual(self.ilmenite_package_c.get_mass(), 3456.7,
                               places=10)

        self.assertAlmostEqual(package_a_plus_b.get_mass(), 3580.0999999999999,
                               places=10)

        self.assertAlmostEqual(package_a_plus_c.get_mass(), 4691.1999999999989,
                               places=10)

        self.assertAlmostEqual(package_b_plus_c.get_mass(), 5802.2999999999993,
                               places=10)

        self.assertAlmostEqual(package_a_plus_b_plus_c.get_mass(), 7036.8,
                               places=10)

    def test_add_operator_2(self):
        mix_package = self.mix.create_package(None, 0.0)
        mix_package = mix_package + self.ilmenite_package_a
        mix_package = mix_package + self.reductant_package_a

        self.assertAlmostEqual(mix_package.get_mass(),
                               self.ilmenite_package_a.get_mass() +
                               self.reductant_package_a.get_mass(),
                               places=10)

        self.assertRaises(Exception, self.add_incompatible_packages)

    def add_incompatible_packages(self):
        result = self.ilmenite_package_a + self.reductant_package_a
        result = result * 1.0

    def test_add_operator_3(self):
        """other = tuple (compound, mass)
        Test whether the add operator calculates the resulting package
        correctly. Results were checked against FactSage results. They are not
        exactly the same, since the magnetic and other non-cp contributions are
        omitted by the thermo module.
        """

        packageAplusAl2O3 = self.ilmenite_package_a + ("Al2O3", 123.4)

        self.assertEqual(packageAplusAl2O3.get_mass(), 1357.9)

    def test_extract_1(self):
        temp_package_a = self.ilmenite_package_a.clone()
        mass = 432.1
        diff_package = temp_package_a.extract(mass)

        self.assertAlmostEqual(temp_package_a.get_mass(),
                               self.ilmenite_package_a.get_mass() - mass,
                               places=10)

        self.assertAlmostEqual(diff_package.get_mass(), mass,
                               places=10)

    def test_subtract_operator_2(self):
        temp_package_a = self.ilmenite_package_a.clone()
        compound = "TiO2"
        mass = 123.4
        diff_package = temp_package_a.extract((compound, mass))

        self.assertAlmostEqual(temp_package_a.get_mass(),
                               self.ilmenite_package_a.get_mass() - mass,
                               places=10)
        self.assertAlmostEqual(temp_package_a.get_compound_mass(compound),
                               self.ilmenite_package_a.get_compound_mass(compound) -
                               mass,
                               places=10)

        self.assertEqual(diff_package.get_mass(), mass)
        self.assertEqual(diff_package.get_compound_mass(compound), mass)

    def test_subtract_operator_3(self):
        temp_package_a = self.ilmenite_package_a.clone()
        compound = "TiO2"
        mass = temp_package_a.get_compound_mass(compound)
        diff_package = temp_package_a.extract(compound)

        self.assertAlmostEqual(temp_package_a.get_mass(),
                               self.ilmenite_package_a.get_mass() - mass,
                               places=10)
        self.assertAlmostEqual(temp_package_a.get_compound_mass(compound),
                               self.ilmenite_package_a.get_compound_mass(compound) -
                               mass,
                               places=10)

        self.assertEqual(diff_package.get_mass(), mass)
        self.assertEqual(diff_package.get_compound_mass(compound), mass)

    def test_multiply_operator(self):
        temp_package_a = self.ilmenite_package_a.clone()

        mul_package_1 = temp_package_a * 0.0
        self.assertEqual(mul_package_1.get_mass(), 0.0)
        self.assertTrue(numpy.all(mul_package_1.compound_masses ==
                                  temp_package_a.compound_masses * 0.0))

        mul_package_2 = temp_package_a * 1.0
        self.assertAlmostEqual(mul_package_2.get_mass(),
                               temp_package_a.get_mass(),
                               places=10)
        self.assertTrue(numpy.all(mul_package_2.compound_masses ==
                                  temp_package_a.compound_masses))

        mul_package_2 = temp_package_a * 123.4
        self.assertAlmostEqual(mul_package_2.get_mass(),
                               temp_package_a.get_mass() * 123.4,
                               places=10)
        self.assertTrue(numpy.all(mul_package_2.compound_masses ==
                                  temp_package_a.compound_masses * 123.4))

    def test_clone(self):
        clone = self.ilmenite_package_a.clone()

        self.assertEqual(clone.get_mass(), self.ilmenite_package_a.get_mass())
        self.assertTrue(numpy.all(clone.compound_masses ==
                                  self.ilmenite_package_a.compound_masses))

    def test_get_mass(self):
        self.assertAlmostEqual(self.ilmenite_package_a.get_mass(), 1234.5,
                               places=10)
        self.assertAlmostEqual(self.ilmenite_package_b.get_mass(), 2345.6,
                               places=10)
        self.assertAlmostEqual(self.ilmenite_package_c.get_mass(), 3456.7,
                               places=10)

    def test_get_assay(self):
        self.assertTrue(numpy.all(self.ilmenite_package_a.get_assay() -
                                  self.ilmenite.assays["IlmeniteA"] /
                                  self.ilmenite.assays["IlmeniteA"].sum() <
                                  1.0E-16))
        self.assertTrue(numpy.all(self.ilmenite_package_a.get_assay() -
                                  self.ilmenite.assays["IlmeniteA"] /
                                  self.ilmenite.assays["IlmeniteA"].sum() >
                                  -1.0E-16))

    def test_get_compound_mass(self):
        assay = "IlmeniteA"
        compound = "TiO2"
        for compound in self.ilmenite.compounds:
            index = self.ilmenite.get_compound_index(compound)
            mass = 1234.5 * self.ilmenite.assays[assay][index] / \
                   self.ilmenite.get_assay_total(assay)
            self.assertEqual(
                self.ilmenite_package_a.get_compound_mass(compound),
                mass)

    def test_get_element_masses(self):
        x = self.ilmenite_package_a.get_element_masses()
        y = self.ilmenite_package_a.get_element_mass("Ti")


# =============================================================================
# Display documentation and run tests.
# =============================================================================
#os.system("cls")

#help(Material)
#help(MaterialPackage)

if __name__ == '__main__':
    unittest.main()
