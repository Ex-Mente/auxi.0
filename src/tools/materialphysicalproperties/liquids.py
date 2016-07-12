# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:13:03 2016

@author: Marno Grewar
"""

from sys import modules
from os.path import realpath, dirname, join

from auxi.tools.materialphysicalproperties.core import DataSet
from auxi.tools.materialphysicalproperties.polynomial import PolynomialModelT
from auxi.modelling.process.materials.core import Material

__version__ = '0.2.3'
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

h2o_dataset = DataSet(_path('data/dataset-h2o-lienhard2015.csv'))

h2o_dict = {}
h2o_dict['rho'] = PolynomialModelT.read(_path('data/h2o-rho.json'))
h2o_dict['Cp'] = PolynomialModelT.read(_path('data/h2o-cp.json'))
h2o_dict['mu'] = PolynomialModelT.read(_path('data/h2o-mu.json'))
h2o_dict['k'] = PolynomialModelT.read(_path('data/h2o-k.json'))
h2o_dict['beta'] = PolynomialModelT.read(_path('data/h2o-beta.json'))

h2o = Material('Water', h2o_dict)
