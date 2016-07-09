"""
This module provides tools for calculating physical properties of an ideal gas.
"""


from auxi.tools.materialphysicalproperties.core import Model
from auxi.tools.physicalconstants import R
from auxi.tools.chemistry.stoichiometry import molar_mass as mm


__version__ = '0.2.3'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Johan Zietsman'
__credits__ = ['Johan Zietsman']
__maintainer__ = 'Johan Zietsman'
__email__ = 'johan.zietsman@ex-mente.co.za'
__status__ = 'Planning'


class BetaT(Model):
    """
    A model that describes the variation in the thermal expansion coefficient
    of an ideal gas as a function of temperature.
    """

    def __init__(self):
        super().__init__('Ideal Gas', 'Thermal Expansion Coefficient', 'beta',
                         '1/K', None, None)

    def __call__(self, T):
        return self.calculate(T)

    def calculate(self, T):
        """
        Calculate the thermal expansion coefficient at the specified
        temperature:

        :param T: [K] temperature

        :returns: [1/K] thermal expansion coefficient
        """
        return 1.0 / T


class RhoT(Model):
    """
    A model that describes the variation in density of an ideal gas as a
    function of temperature.

    :param molar_mass: [g/mol] average molar mass of the gas
    :param P: [Pa] pressure
    """

    def __init__(self, molar_mass, P):
        super().__init__('Ideal Gas', 'Density', 'rho', 'kg/m3', None, None)

        self.mm = molar_mass / 1000.0
        """[kg/mol] average molar mass of the gas"""
        self.P = P
        """[Pa] pressure"""

    def __call__(self, T):
        return self.calculate(T)

    def calculate(self, T):
        """
        Calculate the density at the specified temperature.

        :param T: [K] temperature

        :returns: [kg/m3] density
        """
        return self.mm * self.P / R / T


class RhoTP(Model):
    """
    A model that describes the variation in density of an ideal gas as a
    function of temperature and pressure.

    :param molar_mass: [g/mol] average molar mass of the gas
    """

    def __init__(self, molar_mass):
        super().__init__('Ideal Gas', 'Density', 'rho', 'kg/m3', None, None)

        self.mm = molar_mass / 1000.0
        """[kg/mol] average molar mass of the gas"""

    def __call__(self, T, P):
        return self.calculate(T, P)

    def calculate(self, T, P):
        """
        Calculate the density at the specified temperature and pressure.

        :param T: [K] temperature
        :param P: [Pa] pressure

        :returns: [kg/m3] density
        """
        return self.mm * P / R / T


class RhoTPx(Model):
    """
    A model that describes the variation in density of an ideal gas as a
    function of temperature, pressure, and molar composition.
    """

    def __init__(self):
        super().__init__('Ideal Gas', 'Density', 'rho', 'kg/m3', None, None)

    def __call__(self, T, P, x):
        return self.calculate(T, P, x)

    def calculate(self, T, P, x):
        """
        Calculate the density at the specified temperature, pressure, and
        composition.

        :param T: [K] temperature
        :param P: [Pa] pressure
        :param x: [mole fraction] dictionary of compounds and mole fractions

        :returns: [kg/m3] density
        """
        mm_average = 0.0
        for compound, molefraction in x.items():
            mm_average += molefraction * mm(compound)
        mm_average /= 1000.0

        return mm_average * P / R / T


if __name__ == "__main__":
    import unittest
    from idealgas_test import *
    unittest.main()
