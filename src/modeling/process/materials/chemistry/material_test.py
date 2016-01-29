# -*- coding: utf-8 -*-
"""
This module provides testing code for the chemmaterial module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
import os
import numpy
from auxi.modeling.process.materials.chemistry.material import Material
from auxi.modeling.process.materials.chemistry.material import MaterialPackage

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestMaterial(unittest.TestCase):
    """Tester for the pmpy.materials.chemmaterial.Material class."""

    def setUp(self):
        self.material = Material("material",
                                 os.path.join(chemmaterial.DEFAULT_DATA_PATH,
                                 r"chemmaterial.test.ilmenite.txt"))

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
        self.assertEqual(empty_assay.sum(), 0.0)
        self.assertEqual(empty_assay.sum(), 0.0)
        self.assertEqual(empty_assay.sum(), 0.0)

    def test_add_assay(self):
        new_assay = self.material.create_empty_assay()
        new_assay[0] = 0.5
        new_assay[2] = 0.5
        self.material.add_assay("new_assay", new_assay)
        self.assertEqual(
            numpy.all(self.material.assays["new_assay"] == new_assay),
            True)

    def test_get_assay_total(self):
        self.assertEqual(self.material.get_assay_total("IlmeniteA"),
                         0.99791999999999992)
        self.assertEqual(self.material.get_assay_total("IlmeniteB"),
                         0.99760999999999989)
        self.assertEqual(self.material.get_assay_total("IlmeniteC"),
                         1.0000200000000001)

    def test_create_package(self):
        package = self.material.create_package("IlmeniteA", 123.456, True)
        self.assertEqual(package.get_mass(), 123.456)


class TestMaterialPackage(unittest.TestCase):

    def setUp(self):
        self.ilmenite = Material("ilmenite",
                                 os.path.join(chemmaterial.DEFAULT_DATA_PATH,
                                 r"chemmaterial.test.ilmenite.txt"))
        self.ilmenite_package_a = self.ilmenite.create_package("IlmeniteA",
                                                             1234.5, True)
        self.ilmenite_package_b = self.ilmenite.create_package("IlmeniteB",
                                                             2345.6, True)
        self.ilmenite_package_c = self.ilmenite.create_package("IlmeniteC",
                                                             3456.7, True)
        self.reductant = Material("reductant",
                                  os.path.join(chemmaterial.DEFAULT_DATA_PATH,
                                  r"chemmaterial.test.reductant.txt"))
        self.reductant_package_a = self.reductant.create_package("ReductantA",
                                                               123.45, True)
        self.mix = Material("mix", os.path.join(chemmaterial.DEFAULT_DATA_PATH,
                                                r"chemmaterial.test.mix.txt"))

    def test_constructor(self):
        compound_masses = self.ilmenite.assays["IlmeniteB"] * 123.4 / \
                          self.ilmenite.assays["IlmeniteB"].sum()
        package = MaterialPackage(self.ilmenite, compound_masses)
        self.assertEqual(package.get_mass(), 123.4)

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

        self.assertEqual(self.ilmenite_package_a.get_mass(), 1234.5)

        self.assertEqual(self.ilmenite_package_b.get_mass(), 2345.6)

        self.assertEqual(self.ilmenite_package_c.get_mass(), 3456.7)

        self.assertEqual(package_a_plus_b.get_mass(), 3580.0999999999999)

        self.assertEqual(package_a_plus_c.get_mass(), 4691.1999999999989)

        self.assertEqual(package_b_plus_c.get_mass(), 5802.2999999999993)

        self.assertEqual(package_a_plus_b_plus_c.get_mass(), 7036.8)

    def test_add_operator_2(self):
        mix_package = self.mix.create_package(None, 0.0)
        mix_package = mix_package + self.ilmenite_package_a
        mix_package = mix_package + self.reductant_package_a

        self.assertEqual(mix_package.get_mass(),
                         self.ilmenite_package_a.get_mass() +
                         self.reductant_package_a.get_mass())

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

        self.assertEqual(temp_package_a.get_mass(),
                         self.ilmenite_package_a.get_mass() - mass)

        self.assertEqual(diff_package.get_mass(), mass + 8.0E-14)

    def test_subtract_operator_2(self):
        temp_package_a = self.ilmenite_package_a.clone()
        compound = "TiO2"
        mass = 123.4
        diff_package = temp_package_a.extract((compound, mass))

        self.assertEqual(temp_package_a.get_mass(),
                         self.ilmenite_package_a.get_mass() - mass + 2.0E-13)
        self.assertEqual(temp_package_a.get_compound_mass(compound),
                         self.ilmenite_package_a.get_compound_mass(compound) -
                         mass)

        self.assertEqual(diff_package.get_mass(), mass)
        self.assertEqual(diff_package.get_compound_mass(compound), mass)

    def test_subtract_operator_3(self):
        temp_package_a = self.ilmenite_package_a.clone()
        compound = "TiO2"
        mass = temp_package_a.get_compound_mass(compound)
        diff_package = temp_package_a.extract(compound)

        self.assertEqual(temp_package_a.get_mass(),
                         self.ilmenite_package_a.get_mass() - mass + 1.0E-13)
        self.assertEqual(temp_package_a.get_compound_mass(compound),
                         self.ilmenite_package_a.get_compound_mass(compound) -
                         mass)

        self.assertEqual(diff_package.get_mass(), mass)
        self.assertEqual(diff_package.get_compound_mass(compound), mass)

    def test_multiply_operator(self):
        temp_package_a = self.ilmenite_package_a.clone()

        mul_package_1 = temp_package_a * 0.0
        self.assertEqual(mul_package_1.get_mass(), 0.0)
        self.assertTrue(numpy.all(mul_package_1.compound_masses ==
                                  temp_package_a.compound_masses * 0.0))

        mul_package_2 = temp_package_a * 1.0
        self.assertEqual(mul_package_2.get_mass(), temp_package_a.get_mass())
        self.assertTrue(numpy.all(mul_package_2.compound_masses ==
                                  temp_package_a.compound_masses))

        mul_package_2 = temp_package_a * 123.4
        self.assertEqual(mul_package_2.get_mass(),
                         temp_package_a.get_mass() * 123.4 + 3.0E-11)
        self.assertTrue(numpy.all(mul_package_2.compound_masses ==
                                  temp_package_a.compound_masses * 123.4))

    def test_clone(self):
        clone = self.ilmenite_package_a.clone()

        self.assertEqual(clone.get_mass(), self.ilmenite_package_a.get_mass())
        self.assertTrue(numpy.all(clone.compound_masses ==
                                  self.ilmenite_package_a.compound_masses))

    def test_get_mass(self):
        self.assertEqual(self.ilmenite_package_a.get_mass(), 1234.5)
        self.assertEqual(self.ilmenite_package_b.get_mass(), 2345.6)
        self.assertEqual(self.ilmenite_package_c.get_mass(), 3456.7)

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
