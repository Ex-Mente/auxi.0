#!/usr/bin/env python3
"""
This module provides physical property data sets and models for gases.
"""

from sys import modules
from os.path import realpath, dirname, join

from auxi.tools.materialphysicalproperties.core import DataSet
from auxi.tools.materialphysicalproperties.polynomial import PolynomialModelT
from auxi.tools.materialphysicalproperties.idealgas import \
    BetaT as IgBetaT, RhoT as IgRhoT
from auxi.modelling.process.materials.core import Material
from auxi.tools.materialphysicalproperties.core import StateOfMatter


__version__ = '0.3.0'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman, Marno Grewar'
__credits__ = ['Christoff Kok', 'Johan Zietsman', 'Marno Grewar']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


def _path(relative_path):
    path = modules[__name__].__file__
    path = realpath(path)
    path = dirname(path)
    return join(path, relative_path)


def _create_polynomial_model(symbol, degree):
    newmod = PolynomialModelT.create(air_dataset, symbol, degree)
    newmod.plot(air_dataset, _path('temp.pdf'), False)
    newmod.write(_path('data/air-%s.json' % symbol.lower()))


air_dataset = DataSet(_path('data/dataset-air-lienhard2015.csv'))

# _create_polynomial_model('Cp', 14)
# _create_polynomial_model('k', 8)
# _create_polynomial_model('mu', 8)
# _create_polynomial_model('rho', 14)

air_dict = {}
air_dict['rho'] = IgRhoT(28.9645, 101325.0)
air_dict['Cp'] = PolynomialModelT.read(_path(r'data/air-cp.json'))
air_dict['mu'] = PolynomialModelT.read(_path(r'data/air-mu.json'))
air_dict['k'] = PolynomialModelT.read(_path(r'data/air-k.json'))
air_dict['beta'] = IgBetaT()

air = Material("Air", StateOfMatter.gas, air_dict)
