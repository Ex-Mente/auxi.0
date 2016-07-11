# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:13:03 2016

@author: Marno Grewar
"""

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


air_dataset = DataSet('data/dataset-air-lienhard2015.csv')

air = {}
air['rho'] = IgRhoT(28.9645, 101325.0)
air['cp'] = PolynomialModelT.read('data/air-cp.json')
air['mu'] = PolynomialModelT.read('data/air-mu.json')
air['k'] = PolynomialModelT.read('data/air-k.json')
air['beta'] = IgBetaT()
