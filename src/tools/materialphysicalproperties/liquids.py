# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:13:03 2016

@author: Marno Grewar
"""

from auxi.tools.materialphysicalproperties.core import DataSet
from auxi.tools.materialphysicalproperties.polynomial import PolynomialModelT

__version__ = '0.2.3'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman, Marno Grewar'
__credits__ = ['Christoff Kok', 'Johan Zietsman', 'Marno Grewar']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


h2o_dataset = DataSet('data/dataset-h2o-lienhard2015.csv')

h2o = {}
h2o['rho'] = PolynomialModelT.read('data/h2o-rho.json')
h2o['cp'] = PolynomialModelT.read('data/h2o-cp.json')
h2o['mu'] = PolynomialModelT.read('data/h2o-mu.json')
h2o['k'] = PolynomialModelT.read('data/h2o-k.json')
h2o['beta'] = PolynomialModelT.read('data/h2o-beta.json')
