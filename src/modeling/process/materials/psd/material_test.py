# -*- coding: utf-8 -*-
"""
This module provides testing code for the psdmaterial module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
import os
import numpy
from auxi.modeling.process.materials.psd.material import Material
from auxi.modeling.process.materials.psd.material import MaterialPackage

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestMaterial(unittest.TestCase):
    """Tester for the pmpy.materials.psdmaterial.Material class."""

    def setUp(self):
        self.material = Material("material",
                                 os.path.join(psdmaterial.DEFAULT_DATA_PATH,
                                 r"psdmaterial.test.materiala.txt"))

    def test_constructor(self):
        self.assertEqual(self.material.name, "material")
        self.assertEqual(len(self.material.size_classes), 10)
        self.assertEqual(self.material.size_class_count, 10)
        self.assertEqual(len(self.material.assays), 2)

    def test_get_size_class_index(self):
        self.assertEqual(self.material.get_size_class_index(307.2E-3), 0)
        self.assertEqual(self.material.get_size_class_index(38.4E-3), 2)
        self.assertEqual(self.material.get_size_class_index(600.0E-6), 6)
        self.assertEqual(self.material.get_size_class_index(0.0E0), 9)

    def test_create_empty_assay(self):
        empty_assay = self.material.create_empty_assay()
        self.assertEqual(len(empty_assay), 10)
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
        self.assertEqual(self.material.get_assay_total("FeedA"),
                         1.0000000000000002)
        self.assertEqual(self.material.get_assay_total("MillCharge"),
                         0.99)

    def test_create_package(self):
        package = self.material.create_package("FeedA", 123.456, True)
        self.assertEqual(package.get_mass(), 123.45599999999999)


class TestMaterialPackage(unittest.TestCase):

    def setUp(self):
        self.materiala = Material("materiala",
                                 os.path.join(psdmaterial.DEFAULT_DATA_PATH,
                                 r"psdmaterial.test.materiala.txt"))
        self.materiala_package_a = self.materiala.create_package("FeedA",
                                                             1234.5, True)
        self.materiala_package_b = self.materiala.create_package("MillCharge",
                                                             2345.6, True)

    def test_constructor(self):
        size_class_masses = self.materiala.assays["FeedA"] * 123.4 / \
                          self.materiala.assays["FeedA"].sum()
        package = MaterialPackage(self.materiala, size_class_masses)
        self.assertEqual(package.get_mass(), 123.4)

    def test_add_operator_1(self):
        """other = MaterialPackage
        Test whether the add operator calculates the resulting package
        correctly.
        """

        package_a_plus_b = self.materiala_package_a + self.materiala_package_b

        self.assertEqual(self.materiala_package_a.get_mass(), 1234.5)

        self.assertEqual(self.materiala_package_b.get_mass(), 2345.5999999999995)

        self.assertEqual(package_a_plus_b.get_mass(), 3580.0999999999999)

    # def test_add_operator_2(self):
        # mix_package = self.mix.create_package(None, 0.0)
        # mix_package = mix_package + self.materiala_package_a
        # mix_package = mix_package + self.reductant_package_a

        # self.assertEqual(mix_package.get_mass(),
                         # self.materiala_package_a.get_mass() +
                         # self.reductant_package_a.get_mass())

        # self.assertRaises(Exception, self.add_incompatible_packages)

    # def add_incompatible_packages(self):
        # result = self.materiala_package_a + self.reductant_package_a
        # result = result * 1.0

    def test_add_operator_3(self):
        """other = tuple (size_class, mass)
        Test whether the add operator calculates the resulting package
        correctly. Results were checked against FactSage results. They are not
        exactly the same, since the magnetic and other non-cp contributions are
        omitted by the thermo module.
        """

        packageAplus75micron = self.materiala_package_a + (75.0E-6, 123.4)

        self.assertEqual(packageAplus75micron.get_mass(), 1357.8999999999999)

    def test_extract_1(self):
        temp_package_a = self.materiala_package_a.clone()
        mass = 432.1
        diff_package = temp_package_a.extract(mass)

        self.assertEqual(temp_package_a.get_mass(),
                         self.materiala_package_a.get_mass() - mass -0.00000000000025)

        self.assertEqual(diff_package.get_mass(), mass + 8.0E-14)

    def test_subtract_operator_2(self):
        temp_package_a = self.materiala_package_a.clone()
        size_class = 4.8E-3
        mass = 123.4
        diff_package = temp_package_a.extract((size_class, mass))

        self.assertEqual(temp_package_a.get_mass(),
                         self.materiala_package_a.get_mass() - mass -0.0000000000002)
        self.assertEqual(temp_package_a.get_size_class_mass(size_class),
                         self.materiala_package_a.get_size_class_mass(size_class) -
                         mass)

        self.assertEqual(diff_package.get_mass(), mass)
        self.assertEqual(diff_package.get_size_class_mass(size_class), mass)

    def test_subtract_operator_3(self):
        temp_package_a = self.materiala_package_a.clone()
        size_class = 4.8E-3
        mass = temp_package_a.get_size_class_mass(size_class)
        diff_package = temp_package_a.extract(str(size_class))

        self.assertEqual(temp_package_a.get_mass(),
                         self.materiala_package_a.get_mass() - mass + 1.0E-13)
        self.assertEqual(temp_package_a.get_size_class_mass(size_class),
                         self.materiala_package_a.get_size_class_mass(size_class) -
                         mass)

        self.assertEqual(diff_package.get_mass(), mass)
        self.assertEqual(diff_package.get_size_class_mass(size_class), mass)

    def test_multiply_operator(self):
        temp_package_a = self.materiala_package_a.clone()

        mul_package_1 = temp_package_a * 0.0
        self.assertEqual(mul_package_1.get_mass(), 0.0)
        self.assertTrue(numpy.all(mul_package_1.size_class_masses ==
                                  temp_package_a.size_class_masses * 0.0))

        mul_package_2 = temp_package_a * 1.0
        self.assertEqual(mul_package_2.get_mass(), temp_package_a.get_mass())
        self.assertTrue(numpy.all(mul_package_2.size_class_masses ==
                                  temp_package_a.size_class_masses))

        mul_package_2 = temp_package_a * 123.4
        self.assertEqual(mul_package_2.get_mass(),
                         temp_package_a.get_mass() * 123.4 -0.0000000000298)
        self.assertTrue(numpy.all(mul_package_2.size_class_masses ==
                                  temp_package_a.size_class_masses * 123.4))

    def test_clone(self):
        clone = self.materiala_package_a.clone()

        self.assertEqual(clone.get_mass(), self.materiala_package_a.get_mass())
        self.assertTrue(numpy.all(clone.size_class_masses ==
                                  self.materiala_package_a.size_class_masses))

    def test_get_mass(self):
        self.assertEqual(self.materiala_package_a.get_mass(), 1234.5)
        self.assertEqual(self.materiala_package_b.get_mass(), 2345.5999999999995)

    def test_get_assay(self):
        self.assertTrue(numpy.all(self.materiala_package_a.get_assay() -
                                  self.materiala.assays["FeedA"] /
                                  self.materiala.assays["FeedA"].sum() <
                                  1.0E-16))
        self.assertTrue(numpy.all(self.materiala_package_a.get_assay() -
                                  self.materiala.assays["FeedA"] /
                                  self.materiala.assays["FeedA"].sum() >
                                  -1.0E-16))

    def test_get_size_class_mass(self):
        assay = "FeedA"
        size_class = 4.8E-3
        for size_class in self.materiala.size_classes:
            index = self.materiala.get_size_class_index(size_class)
            mass = 1234.5 * self.materiala.assays[assay][index] / \
                   self.materiala.get_assay_total(assay)
            self.assertEqual(
                self.materiala_package_a.get_size_class_mass(size_class),
                mass)


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

#help(Material)
#help(MaterialPackage)

if __name__ == '__main__':
    unittest.main()
