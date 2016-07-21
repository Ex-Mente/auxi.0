#!/usr/bin/env python3
"""
This module provides a material class that can do thermochemical calculations.
"""

from auxi.core.objects import NamedObject
from auxi.tools.materialphysicalproperties.core import StateOfMatter


__version__ = '0.3.0'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class Material(NamedObject):
    """
    Represents a material consisting of multiple chemical compounds, having
    the ability to do thermochemical calculations.

    :param name: A name for the material.
    :param state_of_matter: The material's state of matter, e.g. liquid.
    :param file_path: The location of the file containing the material's data.
    :param description: the material's description
    """

    def __init__(self, name, state_of_matter=StateOfMatter.unknown,
                 property_models=None, description=None):
        super().__init__(name, description)

        self.mstate = state_of_matter
        """State of matter."""

        if 'alpha' in property_models:
            self.alpha = property_models['alpha']

        if 'beta' in property_models:
            self.beta = property_models['beta']

        if 'Cp' in property_models:
            self.Cp = property_models['Cp']

        if 'k' in property_models:
            self.k = property_models['k']

        if 'mu' in property_models:
            self.mu = property_models['mu']

        if 'nu' in property_models:
            self.nu = property_models['nu']

        if 'rho' in property_models:
            self.rho = property_models['rho']

    def alpha(self, **state):
        """
        Calculate the alpha value given the material state.

        :param **state: material state

        :returns: float
        """

        return self.k(**state) / self.rho(**state) / self.Cp(**state)

    def beta(self, **state):
        """
        Calculate the alpha value given the material state.

        :param **state: material state

        :returns: float
        """
        raise NotImplementedError()

    def Cp(self, **state):
        """
        Calculate the Cp value given the material state.

        :param **state: material state

        :returns: float
        """
        raise NotImplementedError()

    def k(self, **state):
        """
        Calculate the k value given the material state.

        :param **state: material state

        :returns: float
        """
        raise NotImplementedError()

    def mu(self, **state):
        """
        Calculate the mu value given the material state.

        :param **state: material state

        :returns: float
        """
        raise NotImplementedError()

    def nu(self, **state):
        """
        Calculate the nu value given the material state.

        :param **state: material state

        :returns: float
        """
        return self.mu(**state) / self.rho(**state)

    def rho(self, **state):
        """
        Calculate the rho value given the material state.

        :param **state: material state

        :returns: float
        """
        raise NotImplementedError()


if __name__ == '__main__':
    import unittest
    from core_test import *
    unittest.main()
