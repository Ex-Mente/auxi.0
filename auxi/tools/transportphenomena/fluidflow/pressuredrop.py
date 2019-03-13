#!/usr/bin/env python3
"""
This module provides tools to calculate pressure drops in pipes and ducts.
"""

__version__ = "0.3.6"
__license__ = "LGPL v3"
__copyright__ = "Copyright 2016, Ex Mente Technologies (Pty) Ltd"
__author__ = "Johan Zietsman"
__credits__ = ["Willem Roos", "Johan Zietsman"]
__maintainer__ = "Johan Zietsman"
__email__ = "johan.zietsman@ex-mente.co.za"
__status__ = "Planning"


from math import log10, sqrt
from scipy.optimize import root


def color_warn(text):
    return f"\033[33m{text}\033[0m"


def f_l(Re_D):
    """
    Calculate the friction factor of laminar flow (l).

    :param Re_D: Reynolds number for the specified hydraulic diameter.
    :return: Friction factor.

    Source: lienhard2018, Fig. 7.6.
    """
    return 64 / Re_D


def f_ts(Re_D):
    """
    Calculate the friction factor of turbulent flow (t) in a smooth duct (s)
    for the provided conditions.

    :param Re_D: Reynolds number for the specified hydraulic diameter.
    :return: Friction factor.

    Source: lienhard2018, Eq. 7.42.
    """
    return 1 / (1.82 * log10(Re_D) - 1.64)**2


def f_tr_Haaland(Re_D, ɛ, D, warn=True):
    """
    Calculate the friction factor of turbulent flow (t) in a rough duct (r) for
    the provided conditions with Haaland's equation.

    :param Re_D: Reynolds number for the specified hydraulic diameter.
    :param ɛ: [m] Surface roughness.
    :param D: [m] Duct hydraulic diameter.
    :return: Friction factor.

    Source: lienhard2018, Eq. 7.50.
    """
    if warn:
        try:
            if (ɛ / D) < 0.0 or (ɛ / D) > 0.05:
                raise Warning(
                    f"ɛ/D '{ɛ / D:.3e}' out of range 0.0 <= ɛ/D <= 0.05.")
        except Warning as w:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            print(color_warn("WARNING: "), ex_value)

        try:
            if Re_D < 4000.0 or Re_D > 1.0E8:
                raise Warning(
                    f"Reynolds number '{Re_D:.3e}' out of range "
                    "4000 <= Re_D <= 1E8.")
        except Warning as w:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            print(color_warn("WARNING: "), ex_value)

    return 1 / (1.8 * log10((6.9 / Re_D) + (ɛ / D / 3.7)**1.11))**2


def f_tr_Colebrook(Re_D, ɛ, D):
    """
    Calculate the friction factor of turbulent flow (t) a rough duct (r) for
    the provided conditions with Colebrook's equation.

    :param Re_D: Reynolds number for the specified hydraulic diameter.
    :param ɛ: [m] Surface roughness.
    :param D: [m] Duct hydraulic diameter.
    :return: Friction factor.
    """

    def cb(f, Re_D, ɛ, D):
        """
        Calculate the Colebrook function in the form that the Darcy friction
        factor roots can be calculated.

        Source: cengel2018, Eq. 8-74.
        """
        term1 = ɛ / D / 3.7
        term2 = 2.51 / Re_D / sqrt(f)

        return -2 * log10(term1 + term2) - 1 / sqrt(f)

    # find the roots of the Colebrook equation
    return = root(cb, 0.02, args=(Re_D, ɛ, D)).x[0]


def D_h(A, P):
    """
    Calculate the hydraulic diameter of a duct.

    :param A: [m2] Internal cross sectional area of duct.
    :param P: [m] Internal perimeter of duct.
    :return: [m] Hydraulic diameter of duct.
    """
    return 4 * A / P


def Δp(f, L, D, ρ, v):
    """
    Calculate the pressure drop for turbulent flow in a duct.

    :param f: Duct Darcy friction factor.
    :param L: [m] Duct length.
    :param D: [m] Duct hydraulic diameter.
    :param ρ: [kg/m3] Fluid density.
    :param v: [m/s] Average fluid velocity.
    :return: [Pa] Pressure drop.

    Source: lienhard2018, Eq. 3.25.
    """
    return f * (L / D) * (ρ * v**2 / 2)
