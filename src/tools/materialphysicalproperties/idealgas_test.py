#!/usr/bin/env python3
"""
This module contains all the code used to test the testee module.
"""


import unittest
import random

from auxi.tools.materialphysicalproperties import idealgas as testee
from auxi.tools.physicalconstants import R
from auxi.tools.chemistry.stoichiometry import molar_mass as mm


__version__ = '0.3.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class BetaTTester(unittest.TestCase):
    """
    The tester for the BetaT class.
    """

    def test_construct(self):
        """
        Test whether a model is constructed successfully.
        """
        testee.BetaT()

    def test_calculate(self):
        """
        Test whether the property value is calculated successfully.
        """
        model = testee.BetaT()
        T = random.uniform(0.0, 3000.0)
        self.assertEqual(model.calculate(T=T), 1.0/T)
        T = random.uniform(0.0, 3000.0)
        self.assertEqual(model.calculate(T=T), 1.0/T)
        T = random.uniform(0.0, 3000.0)
        self.assertEqual(model.calculate(T=T), 1.0/T)

    def test_call(self):
        """
        Test whether the property value is calculated successfully via the
        __call__ magic method.
        """
        model = testee.BetaT()
        T = random.uniform(0.0, 3000.0)
        self.assertEqual(model(T=T), 1.0/T)
        T = random.uniform(0.0, 3000.0)
        self.assertEqual(model(T=T), 1.0/T)
        T = random.uniform(0.0, 3000.0)
        self.assertEqual(model(T=T), 1.0/T)


class RhoTTester(unittest.TestCase):
    """
    The tester for the RhoT class.
    """

    def test_create(self):
        """
        Test whether a model is created successfully.
        """
        mm = random.uniform(1.0, 200.0)
        P = random.uniform(1.0, 101325.0*5.0)

        testee.RhoT(mm, P)

    def test_calculate(self):
        """
        Test whether the property value is calculated successfully.
        """
        mm = random.uniform(1.0, 200.0)
        P = random.uniform(1.0, 101325.0*5.0)

        model = testee.RhoT(mm, P)

        T = random.uniform(0.0, 3000.0)
        self.assertAlmostEqual(model.calculate(T=T), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        self.assertAlmostEqual(model.calculate(T=T), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        self.assertAlmostEqual(model.calculate(T=T), mm*P/R/T/1000.0)

    def test_call(self):
        """
        Test whether the property value is calculated successfully via the
        __call__ magic method.
        """
        mm = random.uniform(1.0, 200.0)
        P = random.uniform(1.0, 101325.0*5.0)

        model = testee.RhoT(mm, P)

        T = random.uniform(0.0, 3000.0)
        self.assertAlmostEqual(model(T=T), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        self.assertAlmostEqual(model(T=T), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        self.assertAlmostEqual(model(T=T), mm*P/R/T/1000.0)


class RhoTPTester(unittest.TestCase):
    """
    The tester for the RhoTP class.
    """

    def test_create(self):
        """
        Test whether a model is created successfully.
        """
        mm = random.uniform(1.0, 200.0)

        testee.RhoTP(mm)

    def test_calculate(self):
        """
        Test whether the property value is calculated successfully.
        """
        mm = random.uniform(1.0, 200.0)

        model = testee.RhoTP(mm)

        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        self.assertAlmostEqual(model.calculate(T=T, P=P), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        self.assertAlmostEqual(model.calculate(T=T, P=P), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        self.assertAlmostEqual(model.calculate(T=T, P=P), mm*P/R/T/1000.0)

    def test_call(self):
        """
        Test whether the property value is calculated successfully via the
        __call__ magic method.
        """
        mm = random.uniform(1.0, 200.0)

        model = testee.RhoTP(mm)

        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        self.assertAlmostEqual(model(T=T, P=P), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        self.assertAlmostEqual(model(T=T, P=P), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        self.assertAlmostEqual(model(T=T, P=P), mm*P/R/T/1000.0)


class RhoTPxTester(unittest.TestCase):
    """
    The tester for the RhoTPx class.
    """

    def _create_x_and_mm(self):
        x = {}

        x['N2'] = random.uniform(0.0, 10.0)
        x['O2'] = random.uniform(0.0, 10.0)
        x['Ar'] = random.uniform(0.0, 10.0)
        x['H2O'] = random.uniform(0.0, 10.0)

        total = sum(x.values())

        x = {key: x[key]/total for key in x.keys()}

        molar_mass = sum([x[key]*mm(key) for key in x.keys()])

        return x, molar_mass

    def test_create(self):
        """
        Test whether a model is created successfully.
        """
        testee.RhoTPx()

    def test_calculate(self):
        """
        Test whether the property value is calculated successfully.
        """
        model = testee.RhoTPx()

        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        x, mm = self._create_x_and_mm()
        self.assertAlmostEqual(model.calculate(T=T, P=P, x=x), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        x, mm = self._create_x_and_mm()
        self.assertAlmostEqual(model.calculate(T=T, P=P, x=x), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        x, mm = self._create_x_and_mm()
        self.assertAlmostEqual(model.calculate(T=T, P=P, x=x), mm*P/R/T/1000.0)

    def test_call(self):
        """
        Test whether the property value is calculated successfully via the
        __call__ magic method.
        """
        model = testee.RhoTPx()

        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        x, mm = self._create_x_and_mm()
        self.assertAlmostEqual(model(T=T, P=P, x=x), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        x, mm = self._create_x_and_mm()
        self.assertAlmostEqual(model(T=T, P=P, x=x), mm*P/R/T/1000.0)
        T = random.uniform(0.0, 3000.0)
        P = random.uniform(1.0, 101325.0*5.0)
        x, mm = self._create_x_and_mm()
        self.assertAlmostEqual(model(T=T, P=P, x=x), mm*P/R/T/1000.0)


if __name__ == '__main__':
    unittest.main()
