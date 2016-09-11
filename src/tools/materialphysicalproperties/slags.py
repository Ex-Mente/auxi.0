#!/usr/bin/env python3
"""
This module provides physical property data sets and models for slags.
"""

from sys import modules
from os.path import realpath, dirname, join
from math import exp

from auxi.tools.materialphysicalproperties.core import Model, DataSet
from auxi.tools.chemistry.stoichiometry import amount_fractions

__version__ = '0.3.3'
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

        xg = x.get('SiO2', 0.0) + x.get('P2O5', 0.0)
        xm = x.get('CaO', 0.0) + x.get('MgO', 0.0) + x.get('Na2O', 0.0) + \
            x.get('K2O', 0.0) + 3.0*x.get('CaF2', 0.0) + x.get('FeO', 0.0) + \
            x.get('MnO', 0.0) + 2.0*x.get('TiO2', 0.0) + 2.0*x.get('ZrO2', 0.0)

        xa = x.get('Al2O3', 0.0) + x.get('Fe2O3', 0.0) + x.get('B2O3', 0.0)

        norm = 1.0 + x.get('CaF2', 0.0) + 0.5*x.get('Fe2O3', 0.0) + \
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

class ModifiedUrbainViscosityTx(Model):
    """
    A model that describes the variation in the dynamic viscosity of liquid
    slag as a function of temperature and composition expressed in mole
    fraction. This "Modified" Urbain Model is more appropriate for Basic
    Oxygen Steelmaking Slags than the standard, generic UrbainViscosity model.
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

        xg = x.get('SiO2', 0.0) + x.get('P2O5', 0.0)
        xm = x.get('CaO', 0.0) + x.get('MgO', 0.0) + x.get('Na2O', 0.0) + \
            x.get('K2O', 0.0) + 3.0*x.get('CaF2', 0.0) + x.get('FeO', 0.0) + \
            x.get('MnO', 0.0) + 2.0*x.get('TiO2', 0.0) + 2.0*x.get('ZrO2', 0.0)

        xa = x.get('Al2O3', 0.0) + x.get('Fe2O3', 0.0) + x.get('B2O3', 0.0)

        alpha = xm/(xm+xa)
 
        BMgO0 = 13.2 + 15.9*alpha - 18.6*alpha**2
        BMgO1 = 30.5 - 51.1*alpha + 33*alpha**2
        BMgO2 = -40.4 + 138*alpha - 112*alpha**2
        BMgO3 = 60.8 - 99.8*alpha + 97.9*alpha**2
     
        BMgO = BMgO0 + BMgO1*xg + BMgO2*xg**2 + BMgO3*xg**3
     
        BCaO0 = 13.2 + 41.5*alpha - 45*alpha**2
        BCaO1 = 30.5 - 117.2*alpha + 130*alpha**2
        BCaO2 = -40.4 + 232.1*alpha - 298.6*alpha**2
        BCaO3 = 60.8 - 156.4*alpha + 213.6*alpha**2
     
        BCaO = BCaO0 + BCaO1*xg + BCaO2*xg**2 + BCaO3*xg**3
         
        BMnO0 = 13.2 + 20*alpha - 25.6*alpha**2
        BMnO1 = 30.5 + 26*alpha - 56*alpha**2
        BMnO2 = -40.4 - 110.3*alpha + 186.2*alpha**2
        BMnO3 = 60.8 + 64.3*alpha - 104.6*alpha**2
     
        BMnO = BMnO0 + BMnO1*xg + BMnO2*xg**2 + BMnO3*xg**3
     
        xCaO = x.get('CaO',0.0)
        xMgO = x.get('MgO',0.0)
     
# XMnO Calculated using Mills modification as documented in Slag Atlas 2nd ed
        xMnO = x.get('MnO',0.0)+x.get('FeO',0.0)+x.get('CrO',0.0)+\
        0.6*(x.get('Fe2O3',0.0)+x.get('Cr2O3',0.0))
     
        BGlobal = (xCaO*BCaO+xMgO*BMgO+xMnO*BMnO)/(xCaO+xMgO+xMnO)

        A = exp(-0.2693*BGlobal - 11.6725)

        result = A*T*exp(1000.0*BGlobal/T)  # [P]

        return result / 10.0  # [Pa.s]


class ModifiedUrbainViscosityTy(UrbainViscosityTx):
    """
    A model that describes the variation in the dynamic viscosity of liquid
    slag as a function of temperature and composition expressed in mass
    fraction. This "Modified" Urbain Model is more appropriate for Basic
    Oxygen Steelmaking Slags than the standard, generic UrbainViscosity model.
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
    fraction. The RiboudViscosity model is used most often for calculating
    the viscosity of mold fluxes (used for continuous casting of steel as 
    lubricant).
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
    fraction. The RiboudViscosity model is used most often for calculating
    the viscosity of mold fluxes (used for continuous casting of steel as 
    lubricant).
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