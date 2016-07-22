#!/usr/bin/env python3
"""
This module provides physical property data sets and models for slags.
"""

from sys import modules
from os.path import realpath, dirname, join
from math import exp

from auxi.tools.materialphysicalproperties.core import Model, DataSet
from auxi.tools.chemistry.stoichiometry import amount_fractions

__version__ = '0.3.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Markus Erwee, Johan Zietsman'
__credits__ = ['Markus Erwee', 'Johan Zietsman']
__maintainer__ = 'Johan zietsman'
__email__ = 'johan.zietsman@ex-mente.co.za'
__status__ = 'Planning'


def _path(relative_path):
    path = modules[__name__].__file__
    path = realpath(path)
    path = dirname(path)
    return join(path, relative_path)


class UrbainViscosityTx(Model):
    """
    A model that describes the variation in the dynamic viscosity of liquid
    slag as a function of temperature and composition expressed in mole
    fraction.
    """

    def __init__(self):
        state_schema = {'T': {'required': True, 'type': 'float', 'min': 0.0},
                        'x': {'required': True, 'type': 'dict'}}
        super().__init__('Slag', 'Dynamic Viscosity', 'mu', '\\mu', 'Pa.s',
                         state_schema, None, None)

    def calculate(self, **state):
        """
        Calculate dynamic viscosity at the specified temperature and
        composition:

        :param T: [K] temperature
        :param x: [mole fraction] composition dictionary , e.g. \
        {'SiO2': 0.25, 'CaO': 0.25, 'MgO': 0.25, 'FeO': 0.25}

        :returns: [Pa.s] dynamic viscosity

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """

        T = state['T']
        x = state['x']

        # normalise mole fractions
        x_total = sum(x.values())
        x = {compound: x[compound]/x_total for compound in x.keys()}

        xg = x.get('SiO2', .00) + x.get('P2O5', 0.0)
        xm = x.get('CaO', 0.0) + x.get('MgO', 0.0) + x.get('Na2O', 0.0) + \
            x.get('K2O', 0.0) + 3.0*x.get('CaF2', 0.0) + x.get('FeO', 0.0) + \
            x.get('MnO', 0.0) + 2.0*x.get('TiO2', 0.0) + 2.0*x.get('ZrO2', 0.0)

        xa = x.get('Al2O3', 0.0) + x.get('Fe2O3', 0.0) + x.get('B2O3', 0.0)

        # Note 2*XFeO1.5 = XFe2O3

        norm = 1.0 + x.get('CaF2', 0.0) + x.get('Fe2O3', 0.0) + \
            x.get('TiO2', 0.0) + x.get('ZrO2', 0.0)

        xg_norm = xg / norm
        xm_norm = xm / norm
        xa_norm = xa / norm

        alpha = xm_norm / (xm_norm + xa_norm)

        B0 = 13.8 + 39.9355*alpha - 44.049*alpha**2.0
        B1 = 30.481 - 117.1505*alpha + 129.9978*alpha**2.0
        B2 = -40.9429 + 234.0846*alpha - 300.04*alpha**2.0
        B3 = 60.7619 - 153.9276*alpha + 211.1616*alpha**2.0

        B = B0 + B1*xg_norm + B2*xg_norm**2.0 + B3*xg_norm**3.0

        A = exp(-0.2693*B - 11.6725)

        result = A*T*exp(1000.0*B/T)  # [P]

        return result / 10.0  # [Pa.s]


class UrbainViscosityTy(UrbainViscosityTx):
    """
    A model that describes the variation in the dynamic viscosity of liquid
    slag as a function of temperature and composition expressed in mass
    fraction.
    """

    def __init__(self):
        super().__init__()
        state_schema = {'T': {'required': True, 'type': 'float', 'min': 0.0},
                        'y': {'required': True, 'type': 'dict'}}
        self._create_validator(state_schema)

    def calculate(self, **state):
        """
        Calculate dynamic viscosity at the specified temperature and
        composition:

        :param T: [K] temperature
        :param y: [mass fraction] composition dictionary , e.g. \
        {'SiO2': 0.25, 'CaO': 0.25, 'MgO': 0.25, 'FeO': 0.25}

        :returns: [Pa.s] dynamic viscosity

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """

        T = state['T']
        y = state['y']
        x = amount_fractions(y)
        return super().calculate(T=T, x=x)


class RiboudViscosityTx(Model):
    """
    A model that describes the variation in the dynamic viscosity of liquid
    slag as a function of temperature and composition expressed in mole
    fraction.
    """

    def __init__(self):
        state_schema = {'T': {'required': True, 'type': 'float', 'min': 0.0},
                        'x': {'required': True, 'type': 'dict'}}
        super().__init__('Slag', 'Dynamic Viscosity', 'mu', '\\mu', 'Pa.s',
                         state_schema, None, None)

    def calculate(self, **state):
        """
        Calculate dynamic viscosity at the specified temperature and
        composition:

        :param T: [K] temperature
        :param x: [mole fraction] composition dictionary , e.g. \
        {'SiO2': 0.25, 'CaO': 0.25, 'MgO': 0.25, 'FeO': 0.25}

        :returns: [Pa.s] dynamic viscosity

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """

        T = state['T']
        x = state['x']

        # create the slag constituent categories
        compounds_sio2 = ['SiO2', 'PO2.5', 'TiO2', 'ZrO2']
        compounds_cao = ['CaO', 'MgO', 'FeO1.5', 'FeO', 'MnO', 'BO1.5']
        compounds_al2o3 = ['Al2O3']
        compounds_caf2 = ['CaF2']
        compounds_na2o = ['Na2O', 'K2O']
        compounds_all = (compounds_sio2 + compounds_cao + compounds_al2o3 +
                         compounds_caf2 + compounds_na2o)

        # convert compounds with two cations to single cation equivalents
        if 'P2O5' in x:
            x['PO2.5'] = 2.0 * x['P2O5']
        if 'Fe2O3' in x:
            x['FeO1.5'] = 2.0 * x['Fe2O3']
        if 'B2O3' in x:
            x['BO1.5'] = 2.0 * x['B2O3']

        # normalise mole fractions, use only compounds in compounds_all
        x_total = sum([x.get(c, 0.0) for c in compounds_all])
        x = {c: x.get(c, 0.0)/x_total for c in compounds_all}

        # calculate the cateogry mole fractions
        x1 = sum([x.get(c, 0.0) for c in compounds_sio2])
        x2 = sum([x.get(c, 0.0) for c in compounds_cao])
        x3 = sum([x.get(c, 0.0) for c in compounds_al2o3])
        x4 = sum([x.get(c, 0.0) for c in compounds_caf2])
        x5 = sum([x.get(c, 0.0) for c in compounds_na2o])

        # TODO: Why is x1 not used? This looks suspicious.
        A = exp(-17.51 + 1.73*x2 + 5.82*x4 + 7.02*x5 - 33.76*x3)
        B = 31140.0 - 23896.0*x2 - 46356.0*x4 - 39159.0*x5 + 68833.0*x3

        result = A*T*exp(B/T)  # [P]

        return result / 10.0  # [Pa.s]


class RiboudViscosityTy(RiboudViscosityTx):
    """
    A model that describes the variation in the dynamic viscosity of liquid
    slag as a function of temperature and composition expressed in mass
    fraction.
    """

    def __init__(self):
        super().__init__()
        state_schema = {'T': {'required': True, 'type': 'float', 'min': 0.0},
                        'y': {'required': True, 'type': 'dict'}}
        self._create_validator(state_schema)

    def calculate(self, **state):
        """
        Calculate dynamic viscosity at the specified temperature and
        composition:

        :param T: [K] temperature
        :param y: [mass fraction] composition dictionary , e.g. \
        {'SiO2': 0.25, 'CaO': 0.25, 'MgO': 0.25, 'FeO': 0.25}

        :returns: [Pa.s] dynamic viscosity

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """

        T = state['T']
        y = state['y']
        x = amount_fractions(y)
        return super().calculate(T=T, x=x)


ds1 = DataSet(_path('data/dataset-slag-slagatlas1995.csv'))
