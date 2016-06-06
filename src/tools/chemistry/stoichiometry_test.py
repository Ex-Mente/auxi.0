#!/usr/bin/env python3
"""
This module contains all the code used to test the testee module.
"""


import unittest

from auxi.tools.chemistry import stoichiometry as testee


__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class StoichFunctionTester(unittest.TestCase):
    """
    The function tester for the stoichiometry module.
    """

    def assertAlmostEqual(self, first, second, places=14, msg=None,
                          delta=None):
        if type(first) is list and type(second) is list:
            self.assertEqual(len(first), len(second))
            for f, s in zip(first, second):
                self.assertAlmostEqual(f, s)
        else:
            super(StoichFunctionTester, self).assertAlmostEqual(
                first, second, places, msg, delta)

    def test_invalid_characters(self):
        """
        Test whether an exception is raised when a compound formula contains an
        invalid character.
        """

        self.assertRaises(ValueError, testee.molar_mass, '(FeO)*(Fe2O3)')
        self.assertRaises(ValueError, testee.molar_mass, 'CaO1,5')
        self.assertRaises(ValueError, testee.stoichiometry_coefficients,
                          'CaO1,5', ['Ca', 'O'])

    def test_molar_mass(self):
        """
        Test whether the molar mass of a compound is calculated correctly.
        """

        func = testee.molar_mass

        self.assertAlmostEqual(func('FeO'), 71.8444)
        self.assertAlmostEqual(func('Fe2O3'), 159.6882)
        self.assertAlmostEqual(func('SiO2'), 60.0843)
        self.assertAlmostEqual(func('Ca(OH)2'), 74.09268)

    def test_amount(self):
        """
        Test whether the amount of a compound is calculated correctly.
        """

        func = testee.amount

        self.assertEqual(func('FeO', 1.0), 0.01391896932815919)

    def test_mass(self):
        """
        Test whether the mass of a compound is calculated correctly.
        """

        func = testee.mass

        self.assertEqual(func('FeO', 1.0), 71.8444)

    def test_convert_compound(self):
        """
        Test whether compound conversions are calculated correctly.
        """

        func = testee.convert_compound

        m_Fe = 1000.0
        m_Fe2O3 = func(m_Fe, 'Fe', 'Fe2O3', 'Fe')
        self.assertAlmostEqual(m_Fe2O3, 1429.7448294386247)
        m_Fe2O3 = func(m_Fe, 'Fe', 'Fe2O3', 'O')
        self.assertEqual(m_Fe2O3, 0.0)

        m_FeTiO3 = 1000.0
        m_FeO = func(m_FeTiO3, 'FeTiO3', 'FeO', 'Fe')
        self.assertAlmostEqual(m_FeO, 473.56341234801613)
        m_TiO2 = func(m_FeTiO3, 'FeTiO3', 'TiO2', 'Ti')
        self.assertAlmostEqual(m_TiO2, 526.4365876519838)
        self.assertAlmostEqual(m_FeO + m_TiO2, m_FeTiO3)

    def test_element_mass_fraction(self):
        """
        Test whether an element mass fraction is calculated correctly.
        """

        func = testee.element_mass_fraction

        self.assertAlmostEqual(func('FeO', 'Fe'), 0.7773048421310499)
        self.assertAlmostEqual(func('FeO', 'O'), 0.22269515786895014)
        self.assertAlmostEqual(func('FeO', 'Si'), 0.0)
        self.assertAlmostEqual(func('Fe2O3', 'Fe'), 0.699425505453753)
        self.assertAlmostEqual(func('Fe2O3', 'O'), 0.300574494546247)
        self.assertAlmostEqual(func('Fe2O3', 'Mn'), 0.0)
        self.assertAlmostEqual(func('SiO2', 'Si'), 0.4674349206032192)
        self.assertAlmostEqual(func('SiO2', 'O'), 0.5325650793967809)
        self.assertAlmostEqual(func('SiO2', 'Fe'), 0.0)
        self.assertAlmostEqual(func('Ca(OH)2', 'Ca'), 0.5409171324346751)
        self.assertAlmostEqual(func('Ca(OH)2', 'O'), 0.43187532155673136)
        self.assertAlmostEqual(func('Ca(OH)2', 'H'), 0.027207546008593562)
        self.assertAlmostEqual(func('Ca(OH)2', 'Fe'), 0.0)

    def test_element_mass_fractions(self):
        """
        Test whether a list of element mass fraction is calculated correctly.
        """

        func = testee.element_mass_fractions

        x_FeO = [0.7773048421310499, 0.22269515786895014, 0.0]
        self.assertAlmostEqual(list(func('FeO', ['Fe', 'O', 'Si'])), x_FeO)

        x_Fe2O3 = [0.699425505453753, 0.300574494546247, 0.0]
        self.assertAlmostEqual(list(func('Fe2O3', ['Fe', 'O', 'Mn'])), x_Fe2O3)

        x_SiO2 = [0.4674349206032192, 0.5325650793967809, 0.0]
        self.assertAlmostEqual(list(func('SiO2', ['Si', 'O', 'Fe'])), x_SiO2)

        x_CaO2H2 = [0.5409171324346751, 0.43187532155673136,
                    0.027207546008593562, 0.0]
        self.assertAlmostEqual(list(func('Ca(OH)2', ['Ca', 'O', 'H', 'Fe'])),
                               x_CaO2H2)

    def test_elements(self):
        """
        Test whether the set of elements in a list of compounds is calculated
        correctly.
        """

        func = testee.elements

        compounds = ['Ar', 'Fe2O3', 'SiO2', 'Al2O3', 'SO3', 'CaO', 'Fe',
                     'Mn2O3']
        elements = func(compounds)
        self.assertEqual(elements, {'Al', 'Ar', 'Ca', 'Fe', 'Mn', 'O', 'S',
                                    'Si'})

        compounds = ['CO2']
        elements = func(compounds)
        self.assertEqual(elements, {'O', 'C'})

    def test_stoichiometry_coefficient(self):
        """
        Test whether the stoichiometry coefficient of a specified element in a
        compound is calculated correctly.
        """

        func = testee.stoichiometry_coefficient

        self.assertAlmostEqual(func('FeO', 'Fe'), 1.0)
        self.assertAlmostEqual(func('FeO', 'O'), 1.0)
        self.assertAlmostEqual(func('FeO', 'Si'), 0.0)
        self.assertAlmostEqual(func('Fe2O3', 'Fe'), 2.0)
        self.assertAlmostEqual(func('Fe2O3', 'O'), 3.0)
        self.assertAlmostEqual(func('Fe2O3', 'Mn'), 0.0)
        self.assertAlmostEqual(func('SiO2', 'Si'), 1.0)
        self.assertAlmostEqual(func('SiO2', 'O'), 2.0)
        self.assertAlmostEqual(func('SiO2', 'Fe'), 0.0)
        self.assertAlmostEqual(func('Ca(OH)2', 'Ca'), 1.0)
        self.assertAlmostEqual(func('Ca(OH)2', 'O'), 2.0)
        self.assertAlmostEqual(func('Ca(OH)2', 'H'), 2.0)
        self.assertAlmostEqual(func('Ca(OH)2', 'Fe'), 0.0)

    def test_stoichiometry_coefficients(self):
        """
        Test whether the stoichiometry coefficients of a specified list of
        elements in a compound is calculated correctly.
        """

        func = testee.stoichiometry_coefficients

        self.assertEqual(func('FeO', ['Fe', 'O', 'Si']),
                         [1.0, 1.0, 0.0])
        self.assertEqual(func('Fe2O3', ['Fe', 'O', 'Mn']),
                         [2.0, 3.0, 0.0])
        self.assertEqual(func('FeOFe2O3', ['Fe', 'O', 'Mn']),
                         [3.0, 4.0, 0.0])
        self.assertEqual(func('(FeO)(Fe2O3)', ['Fe', 'O', 'Mn']),
                         [3.0, 4.0, 0.0])
        self.assertEqual(func('SiO2', ['Si', 'O', 'Fe']),
                         [1.0, 2.0, 0.0])
        self.assertEqual(func('Ca(OH)2', ['Ca', 'O', 'H', 'Fe']),
                         [1.0, 2.0, 2.0, 0.0])
        self.assertEqual(func('CaAl2(Si2O7)(OH)2.H2O',
                              ['Al', 'Ca', 'Si', 'O', 'H']),
                         [2.0, 1.0, 2.0, 10.0, 4.0])


if __name__ == '__main__':
    unittest.main()
