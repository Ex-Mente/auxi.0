#!/usr/bin/env python3
"""
This module contains all the code used to test the testee module.
"""


import os
import unittest

from auxi.tools.chemistry import stoichiometry as testee


__version__ = '0.2.0rc3'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class TestFunctions(unittest.TestCase):

    def test_amount(self):
        """
        Test whether the amount of a compound is calculated correctly.
        """

        self.assertEqual(testee.amount('FeO', 1.0), 0.01391896932815919)

    def test_mass(self):
        """
        Test whether the mass of a compound is calculated correctly.
        """

        self.assertEqual(testee.mass('FeO', 1.0), 71.8444)

    def test_convert_compound(self):
        """
        Test whether compound conversions are calculated correctly.
        """

        mm_Fe = testee.molar_mass('Fe')
        mm_Fe2O3 = testee.molar_mass('Fe2O3')

        m_Fe = 1000.0
        m_Fe2O3 = testee.convert_compound(m_Fe, 'Fe', 'Fe2O3', 'Fe')
        self.assertEqual(m_Fe2O3, m_Fe / mm_Fe / 2.0 * mm_Fe2O3)
        m_Fe2O3 = testee.convert_compound(m_Fe, 'Fe', 'Fe2O3', 'O')
        self.assertEqual(m_Fe2O3, 0.0)

        mm_FeTiO3 = testee.molar_mass('FeTiO3')
        mm_FeO = testee.molar_mass('FeO')
        mm_TiO2 = testee.molar_mass('TiO2')

        m_FeTiO3 = 1000.0
        m_FeO = testee.convert_compound(m_FeTiO3, 'FeTiO3', 'FeO', 'Fe')
        self.assertEqual(m_FeO, m_FeTiO3 / mm_FeTiO3 * mm_FeO)
        m_TiO2 = testee.convert_compound(m_FeTiO3, 'FeTiO3', 'TiO2', 'Ti')
        self.assertEqual(m_TiO2, m_FeTiO3 / mm_FeTiO3 * mm_TiO2)
        self.assertEqual(m_FeO + m_TiO2, m_FeTiO3)

    def test_element_mass_fraction(self):
        self.assertEqual(testee.element_mass_fraction('FeO', 'Fe'), 0.7773048421310499)
        self.assertEqual(testee.element_mass_fraction('FeO', 'O'), 0.22269515786895014)
        self.assertEqual(testee.element_mass_fraction('FeO', 'Si'), 0.0)
        self.assertEqual(testee.element_mass_fraction('Fe2O3', 'Fe'), 0.699425505453753)
        self.assertEqual(testee.element_mass_fraction('Fe2O3', 'O'), 0.300574494546247)
        self.assertEqual(testee.element_mass_fraction('Fe2O3', 'Mn'), 0.0)
        self.assertEqual(testee.element_mass_fraction('SiO2', 'Si'), 0.4674349206032192)
        self.assertEqual(testee.element_mass_fraction('SiO2', 'O'), 0.5325650793967809)
        self.assertEqual(testee.element_mass_fraction('SiO2', 'Fe'), 0.0)
        self.assertEqual(testee.element_mass_fraction('Ca(OH)2', 'Ca'), 0.5409171324346751)
        self.assertEqual(testee.element_mass_fraction('Ca(OH)2', 'O'), 0.43187532155673136)
        self.assertEqual(testee.element_mass_fraction('Ca(OH)2', 'H'), 0.027207546008593562)
        self.assertEqual(testee.element_mass_fraction('Ca(OH)2', 'Fe'), 0.0)

    def test_element_mass_fractions(self):
        self.assertEqual(list(testee.element_mass_fractions('FeO', ['Fe', 'O', 'Si'])), [0.7773048421310499, 0.22269515786895014, 0.0])
        self.assertEqual(list(testee.element_mass_fractions('Fe2O3', ['Fe', 'O', 'Mn'])), [0.699425505453753, 0.300574494546247, 0.0])
        self.assertEqual(list(testee.element_mass_fractions('SiO2', ['Si', 'O', 'Fe'])), [0.4674349206032192, 0.5325650793967809, 0.0])
        self.assertEqual(list(testee.element_mass_fractions('Ca(OH)2', ['Ca', 'O', 'H', 'Fe'])), [0.5409171324346751, 0.43187532155673136, 0.027207546008593562, 0.0])

    def test_elements(self):
        compounds = ['Ar', 'Fe2O3', 'SiO2', 'Al2O3', 'SO3', 'CaO', 'Fe', 'Mn2O3']
        elements = testee.elements(compounds)
        self.assertEqual(elements, {'Al', 'Ar', 'Ca', 'Fe', 'Mn', 'O', 'S', 'Si'})
        compounds = ['CO2']
        elements = testee.elements(compounds)
        self.assertEqual(elements, {'O', 'C'})

    def test_molar_mass(self):
        self.assertEqual(testee.molar_mass('FeO'), 71.8444)
        self.assertEqual(testee.molar_mass('Fe2O3'), 159.6882)
        self.assertEqual(testee.molar_mass('SiO2'), 60.0843)
        self.assertEqual(testee.molar_mass('Ca(OH)2'), 74.09268)

    def test_testeeiometry_coefficient(self):
        self.assertEqual(testee.stoichiometry_coefficient('FeO', 'Fe'), 1.0)
        self.assertEqual(testee.stoichiometry_coefficient('FeO', 'O'), 1.0)
        self.assertEqual(testee.stoichiometry_coefficient('FeO', 'Si'), 0.0)
        self.assertEqual(testee.stoichiometry_coefficient('Fe2O3', 'Fe'), 2.0)
        self.assertEqual(testee.stoichiometry_coefficient('Fe2O3', 'O'), 3.0)
        self.assertEqual(testee.stoichiometry_coefficient('Fe2O3', 'Mn'), 0.0)
        self.assertEqual(testee.stoichiometry_coefficient('SiO2', 'Si'), 1.0)
        self.assertEqual(testee.stoichiometry_coefficient('SiO2', 'O'), 2.0)
        self.assertEqual(testee.stoichiometry_coefficient('SiO2', 'Fe'), 0.0)
        self.assertEqual(testee.stoichiometry_coefficient('Ca(OH)2', 'Ca'), 1.0)
        self.assertEqual(testee.stoichiometry_coefficient('Ca(OH)2', 'O'), 2.0)
        self.assertEqual(testee.stoichiometry_coefficient('Ca(OH)2', 'H'), 2.0)
        self.assertEqual(testee.stoichiometry_coefficient('Ca(OH)2', 'Fe'), 0.0)

    def test_stoichiometry_coefficients(self):
        self.assertEqual(testee.stoichiometry_coefficients('FeO', ['Fe', 'O', 'Si']), [1.0, 1.0, 0.0])
        self.assertEqual(testee.stoichiometry_coefficients('Fe2O3', ['Fe', 'O', 'Mn']), [2.0, 3.0, 0.0])
        self.assertEqual(testee.stoichiometry_coefficients('FeOFe2O3', ['Fe', 'O', 'Mn']), [3.0, 4.0, 0.0])
        self.assertEqual(testee.stoichiometry_coefficients('(FeO)(Fe2O3)', ['Fe', 'O', 'Mn']), [3.0, 4.0, 0.0])
        self.assertEqual(testee.stoichiometry_coefficients('SiO2', ['Si', 'O', 'Fe']), [1.0, 2.0, 0.0])
        self.assertEqual(testee.stoichiometry_coefficients('Ca(OH)2', ['Ca', 'O', 'H', 'Fe']), [1.0, 2.0, 2.0, 0.0])
        self.assertEqual(testee.stoichiometry_coefficients('CaAl2(Si2O7)(OH)2·H2O', ['Al', 'Ca', 'Si', 'O', 'H']), [2.0, 1.0, 2.0, 10.0, 4.0])


# =============================================================================
# Display documentation and run tests.
# =============================================================================

if __name__ == '__main__':
    os.system('cls')
    # help(stoich)
    unittest.main()
