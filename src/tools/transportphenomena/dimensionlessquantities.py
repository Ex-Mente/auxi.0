#!/usr/bin/env python3
"""
This module provides functions to calculate dimensionless quantities used when
doing transport phenomena calculations.
"""


# TODO: Add mathematical formula to each function. See Gr for example.
# TODO: Test to make sure that math formulae appear correctly on readthedocs.
# TODO: Test to make sure that math formulae appear correctly in LaTeX.
# DECISION: Use the most compact set of parameters for each function, as long
#   as
#          it does not cause ambiguity.
#          For example,
#              'nu' instead of 'mu' and 'rho'
#              'Ts' and 'Tinf' instead of 'dT'


__version__ = '0.3.0'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman, Marno Grewar'
__credits__ = ['Christoff Kok', 'Johan Zietsman', 'Marno Grewar']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


def Gr(L: float, Ts: float, Tf: float, beta: float, nu: float, g: float):
    """
    Calculate the Grashof number.

    :param L: [m] heat transfer surface characteristic length.
    :param Ts: [K] heat transfer surface temperature.
    :param Tf: [K] bulk fluid temperature.
    :param beta: [1/K] fluid coefficient of thermal expansion.
    :param nu: [m2/s] fluid kinematic viscosity.

    :returns: float

    .. math::
        \\mathrm{Gr} = \\frac{g \\beta (Ts - Tinf ) L^3}{\\nu ^2}

    Characteristic dimensions:
        * vertical plate: vertical length
        * pipe: diameter
        * bluff body: diameter
    """

    return g * beta * (Ts - Tf) * L**3.0 / nu**2.0


def Pr(nu: float, alpha: float) -> float:
    """
    Calculate the Prandtl number.

    :param nu: [m2/s] fluid kinematic viscosity / momentum diffusivity.
    :param alpha: [m2/s] fluid thermal diffusivity.

    :returns: float
    """

    return nu / alpha


def Re(L: float, v: float, nu: float) -> float:
    """
    Calculate the Reynolds number.

    :param L: [m] surface characteristic length.
    :param v: [m/s] fluid velocity relative to the object.
    :param nu: [m2/s] fluid kinematic viscosity.

    :returns: float
    """

    return v * L / nu


def Ra(L: float, Ts: float, Tf: float, alpha: float, beta: float, nu: float
       ) -> float:
    """
    Calculate the Grashof number.

    :param L: [m] heat transfer surface characteristic length.
    :param Ts: [K] heat transfer surface temperature.
    :param Tf: [K] bulk fluid temperature.
    :param alpha: [m2/s] fluid thermal diffusivity.
    :param beta: [1/K] fluid coefficient of thermal expansion.
    :param nu: [m2/s] fluid kinematic viscosity.

    :returns: float

    Ra = Gr*Pr

    Characteristic dimensions:
        * vertical plate: vertical length
        * pipe: diameter
        * bluff body: diameter
    """

    return g * beta * (Ts - Tinf) * L**3.0 / (nu * alpha)


def Nu(L: float, h: float, k: float) -> float:
    """
    Calculate the Nusselt number.

    :param L: [m] heat transfer surface characteristic length.
    :param h: [W/K/m2] convective heat transfer coefficient.
    :param k: [W/K/m] fluid thermal conductivity.

    :returns: float
    """

    return h * L / k


def Sh(L: float, h: float, D: float) -> float:
    """
    Calculate the Sherwood number.

    :param L: [m] mass transfer surface characteristic length.
    :param h: [m/s] mass transfer coefficient.
    :param D: [m2/s] fluid mass diffusivity.

    :returns: float
    """

    return h * L / D
