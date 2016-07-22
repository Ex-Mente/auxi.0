#!/usr/bin/env python3
"""
This module provides physical property data sets and models for liquids.
"""

from sys import modules
from os.path import realpath, dirname, join

from auxi.tools.materialphysicalproperties.core import DataSet
from auxi.tools.materialphysicalproperties.polynomial import PolynomialModelT
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
    newmod = PolynomialModelT.create(h2o_dataset, symbol, degree)
    newmod.plot(h2o_dataset, _path('temp.pdf'), False)
    newmod.write(_path('data/h2o-%s.json' % symbol.lower()))


h2o_dataset = DataSet(_path('data/dataset-h2o-lienhard2015.csv'))

# _create_polynomial_model('beta', 11)
# _create_polynomial_model('Cp', 10)
# _create_polynomial_model('k', 8)
# _create_polynomial_model('mu', 11)
# _create_polynomial_model('nu', 11)
# _create_polynomial_model('rho', 7)

h2o_dict = {}
h2o_dict['beta'] = PolynomialModelT.read(_path('data/h2o-beta.json'))
h2o_dict['Cp'] = PolynomialModelT.read(_path('data/h2o-cp.json'))
h2o_dict['k'] = PolynomialModelT.read(_path('data/h2o-k.json'))
h2o_dict['mu'] = PolynomialModelT.read(_path('data/h2o-mu.json'))
h2o_dict['nu'] = PolynomialModelT.read(_path('data/h2o-nu.json'))
h2o_dict['rho'] = PolynomialModelT.read(_path('data/h2o-rho.json'))

h2o = Material('Water', StateOfMatter.liquid, h2o_dict)
