#!/usr/bin/env python3
"""
This module provides physical property data sets and models for coals and
cokes.
"""

from sys import modules
from os.path import realpath, dirname, join
from math import exp

from auxi.tools.materialphysicalproperties.core import Model
from auxi.tools.chemistry.stoichiometry import molar_mass as mm
from auxi.tools.physicalconstants import R

__version__ = '0.3.3'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Johan Zietsman'
__credits__ = ['Johan Zietsman']
__maintainer__ = 'Johan zietsman'
__email__ = 'johan.zietsman@ex-mente.co.za'
__status__ = 'Planning'


def _path(relative_path):
    path = modules[__name__].__file__
    path = realpath(path)
    path = dirname(path)
    return join(path, relative_path)


class DafThermoTy(Model):
    """
    An abstract model that describes a thermochemical property of dry ash-free
    (daf) coal as a function of composition and temperature.
    """

    def __init__(self, material, proprty, symbol, display_symbol, units,
               references, datasets):
        state_schema = {'T': {'required': True, 'type': 'float', 'min': 0.0},
                        'y_C': {'required': True, 'type': 'float', 'min': 0.0,
                        'max': 1.0},
                        'y_H': {'required': True, 'type': 'float', 'min': 0.0,
                        'max': 1.0},
                        'y_O': {'required': True, 'type': 'float', 'min': 0.0,
                        'max': 1.0},
                        'y_N': {'required': True, 'type': 'float', 'min': 0.0,
                        'max': 1.0},
                        'y_S': {'required': True, 'type': 'float', 'min': 0.0,
                        'max': 1.0}}
        super().__init__(material, proprty, symbol, display_symbol, units,
                         state_schema, references, datasets)

    def _calc_a(self, y_C, y_H, y_O, y_N, y_S):
        """
        Calculate the mean atomic weight for the specified element mass
        fractions.
        
        :param y_C: Carbon mass fraction
        :param y_H: Hydrogen mass fraction
        :param y_O: Oxygen mass fraction
        :param y_N: Nitrogen mass fraction
        :param y_S: Sulphur mass fraction
       
        :returns: [kg/kmol] mean atomic weight

        See equation at bottom of page 538 of Merrick1983a.
        """

        return 1 / (y_C/mm("C") + y_H/mm("H") + y_O/mm("O") + y_N/mm("N") +
                    y_S/mm("S"))


class DafCpTy(DafThermoTy):
    """
    A model that describes the heat capacity of dry ash-free (daf) coal as
    a function of composition and temperature.
    """

    def __init__(self):
        super().__init__('Dry Ash-free Coal', 'Heat Capacity', 'Cp',
                         'C_p', 'J/kg/K', ['Merrick1983a', 'Merrick1983b'],
                         None)

    def _calc_g1(self, z):
        """
        Calculate the g1 parameter.

        :param z: dimensionless temperature
        """

        return exp(z) / ((exp(z) - 1.0) / z) ** 2.0

    def calculate(self, **state):
        """
        Calculate the heat capacity at the specified temperature and
        composition using equation 10 in Merrick1983b.

        :param T: [K] temperature
        :param y_C: Carbon mass fraction
        :param y_H: Hydrogen mass fraction
        :param y_O: Oxygen mass fraction
        :param y_N: Nitrogen mass fraction
        :param y_S: Sulphur mass fraction

        :returns: [J/kg/K] heat capacity

        The **state parameter contains the keyword argument(s) specified above
        that are used to describe the state of the material.
        """

        T = state['T']
        y_C = state['y_C']
        y_H = state['y_H']
        y_O = state['y_O']
        y_N = state['y_N']
        y_S = state['y_S']

        a = self._calc_a(y_C, y_H, y_O, y_N, y_S) / 1000  # kg/mol
        result = (R/a) * (self._calc_g1(380/T) + 2*self._calc_g1(1800/T))
        return result


class DafHTy(DafThermoTy):
    """
    A model that describes the enthalpy of dry ash-free (daf) coal as a
    function of composition and temperature.
    """

    def __init__(self):
        super().__init__('Dry Ash-free Coal', 'Enthalpy', 'H', 'H', 'J/kg',
                         ['Merrick1983a', 'Merrick1983b'], None)

    def _calc_g0(self, z):
        """
        Calculate the g0 parameter.

        :param z: dimensionless temperature
        """

        return 1 / (exp(z) - 1)

    def calculate(self, **state):
        """
        Calculate the enthalpy at the specified temperature and composition
        using equation 9 in Merrick1983b.

        :param T: [K] temperature
        :param y_C: Carbon mass fraction
        :param y_H: Hydrogen mass fraction
        :param y_O: Oxygen mass fraction
        :param y_N: Nitrogen mass fraction
        :param y_S: Sulphur mass fraction

        :returns: [J/kg] enthalpy

        The **state parameter contains the keyword argument(s) specified above
        that are used to describe the state of the material.
        """

        T = state['T']
        y_C = state['y_C']
        y_H = state['y_H']
        y_O = state['y_O']
        y_N = state['y_N']
        y_S = state['y_S']

        a = self._calc_a(y_C, y_H, y_O, y_N, y_S) / 1000  # kg/mol
        result = (R/a) * (380*self._calc_g0(380/T) + 3600*self._calc_g0(1800/T))
        return result


if __name__ == '__main__':
    composition = {'y_C': 0.8271423317,
                   'y_H': 0.0442564668,
                   'y_O': 0.1034694128,
                   'y_N': 0.020228025,
                   'y_S': 0.0049037636}

    cp = DafCpTy()
    h = DafHTy()

    def H(T):
        return h.calculate(T=T, **composition)

    def Cp(T):
        return cp.calculate(T=T, **composition)

    dT = 1
    for T in range(0, 810, 10):
        TK = T + 273.15
        dH = (H(TK + dT/2) - H(TK - dT/2))/dT
        print(T, Cp(TK), dH, H(TK))
