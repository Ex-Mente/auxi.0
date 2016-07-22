#!/usr/bin/env python3
"""
This module contains all the code used to test the testee module.
"""


import unittest
from os import remove
from os.path import realpath, dirname, join, isfile

from auxi.tools.materialphysicalproperties import polynomial as testee
from auxi.tools.materialphysicalproperties.core import DataSet


__version__ = '0.3.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


MODULE_PATH = dirname(realpath(__file__))


class PolynomialModelTTester(unittest.TestCase):
    """
    The tester for the PolynomialModelT class.
    """

    def _test_properties(self, model):
        self.assertEqual(model.material, 'Air')
        self.assertEqual(model.property, 'Density')
        self.assertEqual(model.symbol, 'rho')
        self.assertEqual(model.display_symbol, '\\rho')
        self.assertEqual(model.references, None)
        self.assertEqual(model.datasets, ['dataset-air-lienhard2015.csv'])

        coeffs = [2.207010112413834e-28, -1.8498386015487013e-24,
                  6.761238643515948e-21, -1.415594789179995e-17,
                  1.875696238757754e-14, -1.6406192076125332e-11,
                  9.591604317302061e-09, -3.714488392719117e-06,
                  0.0009239972475093591, -0.13882710545123356,
                  11.147387712425617]

        for c, cref in zip(model._coeffs, coeffs):
            self.assertAlmostEqual(c, cref)

    def test_create(self):
        """
        Test whether a model is created successfully from a data set.
        """
        dataset_path = join(MODULE_PATH, 'data/dataset-air-lienhard2015.csv')
        dataset = DataSet(dataset_path)
        model = testee.PolynomialModelT.create(dataset, 'rho', 10)
        self._test_properties(model)

    def test_read(self):
        """
        Test whether a model is created successfully by loading it from a json
        file.
        """
        model = testee.PolynomialModelT.read(join(MODULE_PATH,
                                             'data/air-rho.json'))
        self._test_properties(model)

    def test_write(self):
        """
        Test whether a model is successfully written to a json file.
        """
        dataset_path = join(MODULE_PATH, 'data/dataset-air-lienhard2015.csv')
        dataset = DataSet(dataset_path)

        json_path = join(MODULE_PATH, 'test.json')

        model = testee.PolynomialModelT.create(dataset, 'rho', 10)
        model.write(json_path)
        self.assertTrue(isfile(json_path))
        model = testee.PolynomialModelT.read(json_path)
        remove(json_path)
        self._test_properties(model)

    def test_construct(self):
        """
        Test whether a model is constructed successfully.
        """

        file_path = join(MODULE_PATH, 'data/air-rho.json')

        model = testee.PolynomialModelT.read(file_path)
        testee.PolynomialModelT(model.material, model.property, model.symbol,
                                model.display_symbol, model.units,
                                model.references, model.datasets,
                                model._coeffs)
        self._test_properties(model)

    def test_calculate(self):
        """
        Test whether the property value is calculated successfully.
        """
        file_path = join(MODULE_PATH, 'data/air-rho.json')
        model = testee.PolynomialModelT.read(file_path)

        T = 100.0
        # self.assertEqual(model.calculate(T=T), 3.6026669128620208)
        self.assertEqual(model.calculate(T=T), 3.6049798036305774)
        T = 200.0
        self.assertEqual(model.calculate(T=T), 1.7581685372604081)
        T = 300.0
        self.assertEqual(model.calculate(T=T), 1.1791874628593089)
        T = 400.0
        self.assertEqual(model.calculate(T=T), 0.87918802181468259)
        T = 500.0
        self.assertEqual(model.calculate(T=T), 0.70171039180794637)
        T = 600.0
        self.assertEqual(model.calculate(T=T), 0.59118824960721206)

    def test_plot(self):
        """
        Test whether the plots are created.
        """
        dataset_path = join(MODULE_PATH, 'data/dataset-air-lienhard2015.csv')
        dataset = DataSet(dataset_path)
        model = testee.PolynomialModelT.create(dataset, 'rho', 10)

        pdf_path = join(MODULE_PATH, 'test.pdf')

        model.plot(dataset, pdf_path)
        self.assertTrue(isfile(pdf_path))
        remove(pdf_path)

    def test_call(self):
        """
        Test whether the property value is calculated successfully via the
        __call__ magic method.
        """
        file_path = join(MODULE_PATH, 'data/air-rho.json')
        model = testee.PolynomialModelT.read(file_path)

        T = 100.0
        self.assertEqual(model(T=T), 3.6026669128620208)
        T = 200.0
        self.assertEqual(model(T=T), 1.7581685372604081)
        T = 300.0
        self.assertEqual(model(T=T), 1.1791874628593089)
        T = 400.0
        self.assertEqual(model(T=T), 0.87918802181468259)
        T = 500.0
        self.assertEqual(model(T=T), 0.70171039180794637)
        T = 600.0
        self.assertEqual(model(T=T), 0.59118824960721206)


if __name__ == '__main__':
    unittest.main()
