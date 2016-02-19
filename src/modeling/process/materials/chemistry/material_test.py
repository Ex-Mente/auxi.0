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

class TestMaterial(unittest.TestCase):
    """Tester for the auxi.modeling.process.materials.chemistry.material.Material class."""

    def setUp(self):
        self.material = Material("material",
                                 os.path.join(material.DEFAULT_DATA_PATH,
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
        self.assertAlmostEqual(self.material.get_assay_total("IlmeniteA"),
                               0.99791999999999992,
                               places=10)
        self.assertAlmostEqual(self.material.get_assay_total("IlmeniteB"),
                               0.99760999999999989,
                               places=10)
        self.assertAlmostEqual(self.material.get_assay_total("IlmeniteC"),
                               1.0000200000000001,
                               places=10)

    def test_create_package(self):
        package = self.material.create_package("IlmeniteA", 123.456, True)
        self.assertEqual(package.get_mass(), 123.456)


# =============================================================================
# Display documentation and run tests.
# =============================================================================
#os.system("cls")

#help(Material)
#help(MaterialPackage)

if __name__ == '__main__':
    unittest.main()
