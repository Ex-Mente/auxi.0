#!/usr/bin/env python3
"""
This module contains all the code used to test the testee module.
"""


import unittest
import csv
from os import remove
from os.path import realpath, dirname, join, isfile

from auxi.tools.materialphysicalproperties import core as testee


__version__ = '0.3.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


MODULE_PATH = dirname(realpath(__file__))


class DataSetTester(unittest.TestCase):
    """
    The tester for the DataSet class.
    """

    def test_create_template(self):
        mat_name = 'test'
        template_path = MODULE_PATH
        testee.DataSet.create_template(mat_name, template_path)
        file_path = join(MODULE_PATH, 'dataset-%s.csv' % mat_name)
        self.assertTrue(isfile(file_path))

        with open(file_path, newline='') as file:
            lines = csv.reader(file, delimiter=',', quotechar='"')
            ix = 0
            for l in lines:
                if ix == 0:
                    self.assertEqual(l[0], 'Name')
                    self.assertEqual(l[1], 'test')
                if ix == 7:
                    self.assertEqual(l[0], '100.0')
                    self.assertEqual(l[1], '0.0')
                    self.assertEqual(l[2], '10.0')
                    self.assertEqual(l[3], '100.0')
                if ix == 16:
                    self.assertEqual(l[0], '550.0')
                    self.assertEqual(l[1], '9.0')
                    self.assertEqual(l[2], '19.0')
                    self.assertEqual(l[3], '109.0')
                ix += 1
        remove(file_path)

    def _create_dataset(self):
        path = join(dirname(realpath(__file__)),
                    'data/dataset-air-lienhard2015.csv')
        return testee.DataSet(path)

    def test_construct(self):
        """
        Test whether a data set is constructed successfully from a file.
        """
        self._create_dataset()

    def test_name(self):
        """
        Test whether the data set name is successfully loaded.
        """
        ds = self._create_dataset()
        self.assertEqual(ds.name, 'dataset-air-lienhard2015.csv')

    def test_material(self):
        """
        Test whether the material name is successfully loaded.
        """
        ds = self._create_dataset()
        self.assertEqual(ds.material, 'Air')

    def test_description(self):
        """
        Test whether the data set description is successfully loaded.
        """
        ds = self._create_dataset()
        self.assertEqual(ds.description, 'Thermophysical properties of air at'
                         ' 1 atm pressure.')

    def test_reference(self):
        """
        Test whether the data set reference is successfully loaded.
        """
        ds = self._create_dataset()
        self.assertEqual(ds.reference, 'lienhard2015')

    def test_parameter_names(self):
        """
        Test whether the data set parameter names are successfully loaded.
        """
        ds = self._create_dataset()
        self.assertEqual(ds.col_names,
                         ['Temperature', 'Density', 'Heat Capacity',
                          'Dynamic Viscosity', 'Kinematic Viscosity',
                          'Thermal Conductivity', 'Thermal Diffusivity',
                          'Prandtl Number'])

    def test_parameter_units(self):
        """
        Test whether the data set parameter units are successfully loaded.
        """
        ds = self._create_dataset()
        self.assertEqual(ds.col_units,
                         ['K', 'kg/m3', 'J/kg/K', 'kg/m/s', 'm2/s', 'W/m/K',
                          'm2/s', 'None'])

    def test_parameter_symbols(self):
        """
        Test whether the data set parameter symbols are successfully loaded.
        """
        ds = self._create_dataset()
        self.assertEqual(ds.col_symbols,
                         ['T', 'rho', 'Cp', 'mu', 'nu', 'k', 'alpha', 'Pr'])


if __name__ == '__main__':
    unittest.main()
