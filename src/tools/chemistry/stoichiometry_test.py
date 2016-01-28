# -*- coding: utf-8 -*-
"""
This module provides testing code for the stoichiometry module.

@author: Johan Zietsman
"""
__version__ = "0.2.0"


import os
from auxi.tools.chemistry import stoichiometry as stoich
# import stoich
import unittest


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):

    def test_amount(self):
        self.assertEqual(stoich.amount("FeO", 1.0), 0.01391896932815919)

    def test_mass(self):
        self.assertEqual(stoich.mass("FeO", 1.0), 71.8444)

    def test_convert_compound(self):
        mm_Fe = stoich.molar_mass("Fe")
        mm_Fe2O3 = stoich.molar_mass("Fe2O3")

        mass_Fe = 1000.0
        mass_Fe2O3 = stoich.convert_compound(mass_Fe, "Fe", "Fe2O3", "Fe")
        self.assertEqual(mass_Fe2O3, mass_Fe / mm_Fe / 2.0 * mm_Fe2O3)
        mass_Fe2O3 = stoich.convert_compound(mass_Fe, "Fe", "Fe2O3", "O")
        self.assertEqual(mass_Fe2O3, 0.0)

        mm_FeTiO3 = stoich.molar_mass("FeTiO3")
        mm_FeO = stoich.molar_mass("FeO")
        mm_TiO2 = stoich.molar_mass("TiO2")

        mass_FeTiO3 = 1000.0
        mass_FeO = stoich.convert_compound(mass_FeTiO3, "FeTiO3", "FeO", "Fe")
        self.assertEqual(mass_FeO, mass_FeTiO3 / mm_FeTiO3 * mm_FeO)
        mass_TiO2 = stoich.convert_compound(mass_FeTiO3, "FeTiO3", "TiO2", "Ti")
        self.assertEqual(mass_TiO2, mass_FeTiO3 / mm_FeTiO3 * mm_TiO2)
        self.assertEqual(mass_FeO + mass_TiO2, mass_FeTiO3)

    def test_element_mass_fraction(self):
        self.assertEqual(stoich.element_mass_fraction("FeO", "Fe"), 0.7773048421310499)
        self.assertEqual(stoich.element_mass_fraction("FeO", "O"), 0.22269515786895014)
        self.assertEqual(stoich.element_mass_fraction("FeO", "Si"), 0.0)
        self.assertEqual(stoich.element_mass_fraction("Fe2O3", "Fe"), 0.699425505453753)
        self.assertEqual(stoich.element_mass_fraction("Fe2O3", "O"), 0.300574494546247)
        self.assertEqual(stoich.element_mass_fraction("Fe2O3", "Mn"), 0.0)
        self.assertEqual(stoich.element_mass_fraction("SiO2", "Si"), 0.4674349206032192)
        self.assertEqual(stoich.element_mass_fraction("SiO2", "O"), 0.5325650793967809)
        self.assertEqual(stoich.element_mass_fraction("SiO2", "Fe"), 0.0)
        self.assertEqual(stoich.element_mass_fraction("Ca(OH)2", "Ca"), 0.5409171324346751)
        self.assertEqual(stoich.element_mass_fraction("Ca(OH)2", "O"), 0.43187532155673136)
        self.assertEqual(stoich.element_mass_fraction("Ca(OH)2", "H"), 0.027207546008593562)
        self.assertEqual(stoich.element_mass_fraction("Ca(OH)2", "Fe"), 0.0)

    def test_element_mass_fractions(self):
        self.assertEqual(list(stoich.element_mass_fractions("FeO", ["Fe", "O", "Si"])), [0.7773048421310499, 0.22269515786895014, 0.0])
        self.assertEqual(list(stoich.element_mass_fractions("Fe2O3", ["Fe", "O", "Mn"])), [0.699425505453753, 0.300574494546247, 0.0])
        self.assertEqual(list(stoich.element_mass_fractions("SiO2", ["Si", "O", "Fe"])), [0.4674349206032192, 0.5325650793967809, 0.0])
        self.assertEqual(list(stoich.element_mass_fractions("Ca(OH)2", ["Ca", "O", "H", "Fe"])), [0.5409171324346751, 0.43187532155673136, 0.027207546008593562, 0.0])

    def test_elements(self):
        compounds = ["Ar", "Fe2O3", "SiO2", "Al2O3", "SO3", "CaO", "Fe", "Mn2O3"]
        elements = stoich.elements(compounds)
        self.assertEqual(elements, {'Al', 'Ar', 'Ca', 'Fe', 'Mn', 'O', 'S', 'Si'})
        compounds = ["CO2"]
        elements = stoich.elements(compounds)
        self.assertEqual(elements, {'O', 'C'})

    def test_molar_mass(self):
        self.assertEqual(stoich.molar_mass("FeO"), 71.8444)
        self.assertEqual(stoich.molar_mass("Fe2O3"), 159.6882)
        self.assertEqual(stoich.molar_mass("SiO2"), 60.0843)
        self.assertEqual(stoich.molar_mass("Ca(OH)2"), 74.09268)

    def test_stoichiometry_coefficient(self):
        self.assertEqual(stoich.stoichiometry_coefficient("FeO", "Fe"), 1.0)
        self.assertEqual(stoich.stoichiometry_coefficient("FeO", "O"), 1.0)
        self.assertEqual(stoich.stoichiometry_coefficient("FeO", "Si"), 0.0)
        self.assertEqual(stoich.stoichiometry_coefficient("Fe2O3", "Fe"), 2.0)
        self.assertEqual(stoich.stoichiometry_coefficient("Fe2O3", "O"), 3.0)
        self.assertEqual(stoich.stoichiometry_coefficient("Fe2O3", "Mn"), 0.0)
        self.assertEqual(stoich.stoichiometry_coefficient("SiO2", "Si"), 1.0)
        self.assertEqual(stoich.stoichiometry_coefficient("SiO2", "O"), 2.0)
        self.assertEqual(stoich.stoichiometry_coefficient("SiO2", "Fe"), 0.0)
        self.assertEqual(stoich.stoichiometry_coefficient("Ca(OH)2", "Ca"), 1.0)
        self.assertEqual(stoich.stoichiometry_coefficient("Ca(OH)2", "O"), 2.0)
        self.assertEqual(stoich.stoichiometry_coefficient("Ca(OH)2", "H"), 2.0)
        self.assertEqual(stoich.stoichiometry_coefficient("Ca(OH)2", "Fe"), 0.0)

    def test_stoichiometry_coefficients(self):
        self.assertEqual(stoich.stoichiometry_coefficients("FeO", ["Fe", "O", "Si"]), [1.0, 1.0, 0.0])
        self.assertEqual(stoich.stoichiometry_coefficients("Fe2O3", ["Fe", "O", "Mn"]), [2.0, 3.0, 0.0])
        self.assertEqual(stoich.stoichiometry_coefficients("FeOFe2O3", ["Fe", "O", "Mn"]), [3.0, 4.0, 0.0])
        self.assertEqual(stoich.stoichiometry_coefficients("(FeO)(Fe2O3)", ["Fe", "O", "Mn"]), [3.0, 4.0, 0.0])
        self.assertEqual(stoich.stoichiometry_coefficients("SiO2", ["Si", "O", "Fe"]), [1.0, 2.0, 0.0])
        self.assertEqual(stoich.stoichiometry_coefficients("Ca(OH)2", ["Ca", "O", "H", "Fe"]), [1.0, 2.0, 2.0, 0.0])
        self.assertEqual(stoich.stoichiometry_coefficients("CaAl2(Si2O7)(OH)2·H2O", ["Al", "Ca", "Si", "O", "H"]), [2.0, 1.0, 2.0, 10.0, 4.0])


# =============================================================================
# Display documentation and run tests.
# =============================================================================

if __name__ == '__main__':
    os.system("cls")
    # help(stoich)
    unittest.main()
