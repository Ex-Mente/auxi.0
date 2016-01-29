# -*- coding: utf-8 -*-
"""
This module provides testing code for the modelling.thermochemistry module.

@author: Ex Mente Technologies (Pty) Ltd
"""


import unittest
import os
import numpy
from auxi.modeling.process.materials.thermochemistry.material import Material
from auxi.modeling.process.materials.thermochemistry.material import MaterialPackage

__version__ = "0.2.0"

# =============================================================================
# Types.
# =============================================================================


class TestMaterial(unittest.TestCase):
    """

    """
    def setUp(self):
        self.material = Material("material", os.path.join(thermomaterial.DEFAULT_DATA_PATH, r"thermomaterial.test.ilmenite.txt"))

    def test_constructor(self):
        self.assertEqual(self.material.name, "material")
        self.assertEqual(len(self.material.compounds), 14)
        self.assertEqual(self.material.compound_count, 14)
        self.assertEqual(len(self.material.assays), 3)

    def test_get_compound_index(self):
        self.assertEqual(self.material.get_compound_index("Al2O3[S1]"), 0)
        self.assertEqual(self.material.get_compound_index("K2O[S]"), 6)
        self.assertEqual(self.material.get_compound_index("P4O10[S]"), 10)
        self.assertEqual(self.material.get_compound_index("V2O5[S]"), 13)

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
        self.assertEqual(numpy.all(self.material.assays["new_assay"] == new_assay), True)

    def test_get_assay_total(self):
        self.assertEqual(self.material.get_assay_total("IlmeniteA"), 0.99791999999999992)
        self.assertEqual(self.material.get_assay_total("IlmeniteB"), 0.99760999999999989)
        self.assertEqual(self.material.get_assay_total("IlmeniteC"), 1.0000200000000001)

    def test_create_package(self):
        package = self.material.create_package("IlmeniteA", 123.456, 0.87, 205.0, True)
        self.assertEqual(package.get_mass(), 123.456)
        self.assertEqual(package.P, 0.87)
        self.assertEqual(package.T, 205.0)
        self.assertEqual(package.H, -278.35680682442677)


class TestMaterialPackage(unittest.TestCase):

    def setUp(self):
        self.ilmenite = Material("ilmenite", os.path.join(thermomaterial.DEFAULT_DATA_PATH, r"thermomaterial.test.ilmenite.txt"))
        self.ilmenitePackageA = self.ilmenite.create_package("IlmeniteA", 1234.5, 0.8, 100.0, True)
        self.ilmenitePackageB = self.ilmenite.create_package("IlmeniteB", 2345.6, 0.9, 200.0, True)
        self.ilmenitePackageC = self.ilmenite.create_package("IlmeniteC", 3456.7, 1.0, 300.0, True)
        self.reductant = Material("reductant", os.path.join(thermomaterial.DEFAULT_DATA_PATH, r"thermomaterial.test.reductant.txt"))
        self.reductantPackageA = self.reductant.create_package("ReductantA", 123.45, 0.75, 400.0, True)
        self.mix = Material("mix", os.path.join(thermomaterial.DEFAULT_DATA_PATH, r"thermomaterial.test.mix.txt"))

    def test_constructor(self):
        compound_masses = self.ilmenite.assays["IlmeniteB"] * 123.4 / self.ilmenite.assays["IlmeniteB"].sum()
        package = MaterialPackage(self.ilmenite, compound_masses, 0.8, 300.0)
        self.assertEqual(package.get_mass(), 123.4)
        self.assertEqual(package.P, 0.8)
        self.assertEqual(package.T, 300.0)
        self.assertEqual(package.H, -236.60618829889296)

    def test_add_operator_1(self):
        """other = MaterialPackage
        Test whether the add operator calculates the resulting package correctly.
        Results were checked against FactSage results. They are not exactly the same, since the magnetic and other non-cp contributions are omitted by the thermo module.
        """

        packageAplusB = self.ilmenitePackageA + self.ilmenitePackageB
        packageAplusC = self.ilmenitePackageA + self.ilmenitePackageC
        packageBplusC = self.ilmenitePackageB + self.ilmenitePackageC
        packageAplusBplusC = self.ilmenitePackageA + self.ilmenitePackageB + self.ilmenitePackageC

        self.assertEqual(self.ilmenitePackageA.get_mass(), 1234.5)
        self.assertEqual(self.ilmenitePackageA.P, 0.8)
        self.assertEqual(self.ilmenitePackageA.T, 100.0)
        self.assertEqual(self.ilmenitePackageA.H, -2811.6976363963095)

        self.assertEqual(self.ilmenitePackageB.get_mass(), 2345.6)
        self.assertEqual(self.ilmenitePackageB.P, 0.9)
        self.assertEqual(self.ilmenitePackageB.T, 200.0)
        self.assertEqual(self.ilmenitePackageB.H, -4550.3197620429773)

        self.assertEqual(self.ilmenitePackageC.get_mass(), 3456.7)
        self.assertEqual(self.ilmenitePackageC.P, 1.0)
        self.assertEqual(self.ilmenitePackageC.T, 300.0)
        self.assertEqual(self.ilmenitePackageC.H, -8023.545629913353)

        self.assertEqual(packageAplusB.get_mass(), 3580.0999999999999)
        self.assertEqual(packageAplusB.P, 0.8)
        self.assertEqual(packageAplusB.T, 165.93941355722774)
        self.assertEqual(packageAplusB.H, self.ilmenitePackageA.H + self.ilmenitePackageB.H)

        self.assertEqual(packageAplusC.get_mass(), 4691.1999999999989)
        self.assertEqual(packageAplusC.P, 0.8)
        self.assertEqual(packageAplusC.T, 249.48206641333098)
        self.assertEqual(packageAplusC.H, self.ilmenitePackageA.H + self.ilmenitePackageC.H)

        self.assertEqual(packageBplusC.get_mass(), 5802.2999999999993)
        self.assertEqual(packageBplusC.P, 0.9)
        self.assertEqual(packageBplusC.T, 260.56905390294497)
        self.assertEqual(packageBplusC.H, self.ilmenitePackageB.H + self.ilmenitePackageC.H)

        self.assertEqual(packageAplusBplusC.get_mass(), 7036.8)
        self.assertEqual(packageAplusBplusC.P, 0.8)
        self.assertEqual(packageAplusBplusC.T, 233.3038145723261)
        self.assertEqual(packageAplusBplusC.H, self.ilmenitePackageA.H + self.ilmenitePackageB.H + self.ilmenitePackageC.H)

    def test_add_operator_2(self):
        mixPackage = self.mix.create_package(None, 0.0)
        mixPackage = mixPackage + self.ilmenitePackageA
        mixPackage = mixPackage + self.reductantPackageA

        self.assertEqual(mixPackage.get_mass(), self.ilmenitePackageA.get_mass() + self.reductantPackageA.get_mass())
        self.assertEqual(mixPackage.P, 1.0)
        self.assertEqual(mixPackage.T, 146.64409455076031)
        self.assertEqual(mixPackage.H, self.ilmenitePackageA.H + self.reductantPackageA.H)

        self.assertRaises(Exception, self.add_incompatible_packages)

    def add_incompatible_packages(self):
        result = self.ilmenitePackageA + self.reductantPackageA
        result = result * 1.0

    def test_add_operator_3(self):
        """other = tuple (compound, mass)
        Test whether the add operator calculates the resulting package correctly.
        Results were checked against FactSage results. They are not exactly the same, since the magnetic and other non-cp contributions are omitted by the thermo module.
        """

        packageAplusAl2O3 = self.ilmenitePackageA + ("Al2O3[S1]", 123.4)

        self.assertEqual(packageAplusAl2O3.get_mass(), 1357.9)
        self.assertEqual(packageAplusAl2O3.P, 0.8)
        self.assertEqual(packageAplusAl2O3.T, 100.0)
        self.assertEqual(packageAplusAl2O3.H, self.ilmenitePackageA.H + thermo.H("Al2O3[S1]", 100.0, 123.4))

    def test_add_operator_4(self):
        """other = tuple (compound, mass, temperature)
        Test whether the add operator calculates the resulting package correctly.
        Results were checked against FactSage results. They are not exactly the same, since the magnetic and other non-cp contributions are omitted by the thermo module.
        """

        packageAplusAl2O3 = self.ilmenitePackageA + ("Al2O3[S1]", 123.4, 500.0)

        self.assertEqual(packageAplusAl2O3.get_mass(), 1357.9)
        self.assertEqual(packageAplusAl2O3.P, 0.8)
        self.assertEqual(packageAplusAl2O3.T, 151.60776535105211)
        self.assertEqual(packageAplusAl2O3.H, self.ilmenitePackageA.H + thermo.H("Al2O3[S1]", 500.0, 123.4))

    def test_extract_1(self):
        tempPackageA = self.ilmenitePackageA.clone()
        mass = 432.1
        diffPackage = tempPackageA.extract(mass)

        self.assertEqual(tempPackageA.get_mass(), self.ilmenitePackageA.get_mass() - mass)
        self.assertEqual(tempPackageA.P, 0.8)
        self.assertEqual(tempPackageA.T, 100.0)

        self.assertEqual(diffPackage.get_mass(), mass + 8.0E-14)
        self.assertEqual(diffPackage.P, 0.8)
        self.assertEqual(diffPackage.T, 100.0)

        self.assertEqual(tempPackageA.H + diffPackage.H, self.ilmenitePackageA.H)

    def test_extract_2(self):
        tempPackageA = self.ilmenitePackageA.clone()
        compound = "TiO2[S1]"
        mass = 123.4
        diffPackage = tempPackageA.extract((compound, mass))

        self.assertEqual(tempPackageA.get_mass(), self.ilmenitePackageA.get_mass() - mass + 2.0E-13)
        self.assertEqual(tempPackageA.get_compound_mass(compound), self.ilmenitePackageA.get_compound_mass(compound) - mass)
        self.assertEqual(tempPackageA.P, 0.8)
        self.assertEqual(tempPackageA.T, 100.0)

        self.assertEqual(diffPackage.get_mass(), mass)
        self.assertEqual(diffPackage.get_compound_mass(compound), mass)
        self.assertEqual(diffPackage.P, 0.8)
        self.assertEqual(diffPackage.T, 100.0)

        self.assertEqual(tempPackageA.H + diffPackage.H, self.ilmenitePackageA.H)

    def test_extract_3(self):
        tempPackageA = self.ilmenitePackageA.clone()
        compound = "TiO2[S1]"
        mass = tempPackageA.get_compound_mass(compound)
        diffPackage = tempPackageA.extract(compound)

        self.assertEqual(tempPackageA.get_mass(), self.ilmenitePackageA.get_mass() - mass + 1.0E-13)
        self.assertEqual(tempPackageA.get_compound_mass(compound), self.ilmenitePackageA.get_compound_mass(compound) - mass)
        self.assertEqual(tempPackageA.P, 0.8)
        self.assertEqual(tempPackageA.T, 100.0)

        self.assertEqual(diffPackage.get_mass(), mass)
        self.assertEqual(diffPackage.get_compound_mass(compound), mass)
        self.assertEqual(diffPackage.P, 0.8)
        self.assertEqual(diffPackage.T, 100.0)

        self.assertEqual(tempPackageA.H + diffPackage.H, self.ilmenitePackageA.H)

    def test_multiply_operator(self):
        tempPackageA = self.ilmenitePackageA.clone()

        mul1Package = tempPackageA * 0.0
        self.assertEqual(mul1Package.get_mass(), 0.0)
        self.assertTrue(numpy.all(mul1Package._compound_masses == tempPackageA._compound_masses * 0.0))
        self.assertEqual(mul1Package.P, tempPackageA.P)
        self.assertEqual(mul1Package.T, tempPackageA.T)
        self.assertEqual(mul1Package.H, 0.0)

        mul2Package = tempPackageA * 1.0
        self.assertEqual(mul2Package.get_mass(), tempPackageA.get_mass())
        self.assertTrue(numpy.all(mul2Package._compound_masses == tempPackageA._compound_masses))
        self.assertEqual(mul2Package.P, tempPackageA.P)
        self.assertEqual(mul2Package.T, tempPackageA.T)
        self.assertEqual(mul2Package.H, tempPackageA.H)

        mul2Package = tempPackageA * 123.4
        self.assertEqual(mul2Package.get_mass(), tempPackageA.get_mass() * 123.4 + 3.0E-11)
        self.assertTrue(numpy.all(mul2Package._compound_masses == tempPackageA._compound_masses * 123.4))
        self.assertEqual(mul2Package.P, tempPackageA.P)
        self.assertEqual(mul2Package.T, tempPackageA.T)
        self.assertEqual(mul2Package.H, tempPackageA.H * 123.4 - 6.0E-11)

    def test_clone(self):
        clone = self.ilmenitePackageA.clone()

        self.assertEqual(clone.get_mass(), self.ilmenitePackageA.get_mass())
        self.assertTrue(numpy.all(clone._compound_masses == self.ilmenitePackageA._compound_masses))
        self.assertEqual(clone.P, self.ilmenitePackageA.P)
        self.assertEqual(clone.T, self.ilmenitePackageA.T)
        self.assertEqual(clone.H, self.ilmenitePackageA.H)

    def test_get_mass(self):
        self.assertEqual(self.ilmenitePackageA.get_mass(), 1234.5)
        self.assertEqual(self.ilmenitePackageB.get_mass(), 2345.6)
        self.assertEqual(self.ilmenitePackageC.get_mass(), 3456.7)

    def test_get_assay(self):
        self.assertTrue(numpy.all(self.ilmenitePackageA.get_assay() - self.ilmenite.assays["IlmeniteA"] / self.ilmenite.assays["IlmeniteA"].sum() < 1.0E-16))
        self.assertTrue(numpy.all(self.ilmenitePackageA.get_assay() - self.ilmenite.assays["IlmeniteA"] / self.ilmenite.assays["IlmeniteA"].sum() > -1.0E-16))

    def test_get_compound_mass(self):
        assay = "IlmeniteA"
        compound = "TiO2[S1]"
        for compound in self.ilmenite.compounds:
            mass = 1234.5 * self.ilmenite.assays[assay][self.ilmenite.get_compound_index(compound)] / self.ilmenite.get_assay_total(assay)
            self.assertEqual(self.ilmenitePackageA.get_compound_mass(compound), mass)

    def test_set_H(self):
        tempPackageA = self.ilmenitePackageA.clone()
        H = tempPackageA.H + 5.67
        tempPackageA.H = H

        self.assertEqual(tempPackageA.H, H)
        self.assertEqual(tempPackageA.T, 121.65612974840057)

    def test_get_H(self):
        self.assertEqual(self.ilmenitePackageA.H, self.ilmenitePackageA._H)

    def test_set_T(self):
        tempPackageA = self.ilmenitePackageA.clone()
        T = tempPackageA.T + 123.4
        tempPackageA.T = T

        self.assertEqual(tempPackageA.T, T)
        self.assertEqual(tempPackageA.H, -2778.3170030281622)

    def test_get_T(self):
        self.assertEqual(self.ilmenitePackageA.T, self.ilmenitePackageA._T)

    def test_get_P(self):
        self.assertEqual(self.ilmenitePackageA.P, self.ilmenitePackageA._P)

    def test_get_element_masses(self):
        x = self.ilmenitePackageA.get_element_masses()
        print(self.ilmenitePackageA.material.elements)
        print(x)
        y = self.ilmenitePackageA.get_element_mass("Ti")
        print(y)


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

#help(Material)
#help(MaterialPackage)

if __name__ == '__main__':
    unittest.main()
