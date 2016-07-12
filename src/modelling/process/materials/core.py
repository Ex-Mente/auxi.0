#!/usr/bin/env python3
"""
This module provides a material class that can do thermochemical calculations.
"""

import os
import sys
import copy
import numpy

from auxi.core.objects import Object, NamedObject
from auxi.tools.chemistry import stoichiometry as stoich
from auxi.tools.chemistry import thermochemistry as thermo

__version__ = '0.2.3'
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
    :param file_path: The location of the file containing the material's data.
    :param description: the material's description
    """

    def __init__(self, name, property_models=None,
                 description=None):
        super().__init__(name, description)

        if 'beta' in property_models:
            self.beta = property_models['beta']

        if 'Cp' in property_models:
            self.Cp = property_models['Cp']

        if 'k' in property_models:
            self.k = property_models['k']

        if 'mu' in property_models:
            self.mu = property_models['mu']

        if 'rho' in property_models:
            self.rho = property_models['rho']

    def beta(self, **state):
        raise NotImplementedError()

    def Cp(self, **state):
        raise NotImplementedError()

    def k(self, **state):
        raise NotImplementedError()

    def mu(self, **state):
        raise NotImplementedError()

    def rho(self, **state):
        raise NotImplementedError()


if __name__ == '__main__':
    import unittest
    from core_test import *
    unittest.main()
