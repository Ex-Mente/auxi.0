# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:13:03 2016

@author: Marno Grewar
"""

from sys import modules
from os.path import realpath, dirname, join

from auxi.tools.materialphysicalproperties.core import DataSet
from auxi.tools.materialphysicalproperties.polynomial import PolynomialModelT
from auxi.tools.materialphysicalproperties.idealgas import \
    BetaT as IgBetaT, RhoT as IgRhoT

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

air_dataset = DataSet(_path(r'data\dataset-air-lienhard2015.csv'))

air_dict = {}
air_dict['rho'] = IgRhoT(28.9645, 101325.0)
air_dict['Cp'] = PolynomialModelT.read(_path(r'data/air-cp.json'))
air_dict['mu'] = PolynomialModelT.read(_path(r'data/air-mu.json'))
air_dict['k'] = PolynomialModelT.read(_path(r'data/air-k.json'))
air_dict['beta'] = IgBetaT()
