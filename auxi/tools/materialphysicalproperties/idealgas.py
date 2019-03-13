#!/usr/bin/env python3
"""
This module provides tools for calculating physical properties of an ideal gas.
"""
from matplotlib.backends.backend_pdf import PdfPages
import webbrowser
import matplotlib.pyplot as plt
import numpy as np


from auxi.tools.materialphysicalproperties.core import Model
from auxi.tools.physicalconstants import R
from auxi.tools.chemistry.stoichiometry import molar_mass as mm


__version__ = "0.3.6"
__license__ = "LGPL v3"
__copyright__ = "Copyright 2016, Ex Mente Technologies (Pty) Ltd"
__author__ = "Johan Zietsman"
__credits__ = ["Johan Zietsman"]
__maintainer__ = "Johan Zietsman"
__email__ = "johan.zietsman@ex-mente.co.za"
__status__ = "Planning"


class BetaT(Model):
    """
    A model that describes the variation in the thermal expansion coefficient
    of an ideal gas as a function of temperature.
    """

    def __init__(self):
        state_schema = {"T": {"required": True, "type": "float", "min": 0.0}}
        super().__init__("Ideal Gas", "Thermal Expansion Coefficient", "beta",
                         "\\beta", "1/K", state_schema, None, None)

    def calculate(self, **state):
        """
        Calculate the thermal expansion coefficient at the specified
        temperature:

        :param T: [K] temperature

        :returns: [1/K] thermal expansion coefficient

        The **state parameter contains the keyword argument(s) specified above
        that are used to describe the state of the material.
        """
        super().calculate(**state)
        return 1.0 / state["T"]


class RhoT(Model):
    """
    A model that describes the variation in density of an ideal gas as a
    function of temperature.

    :param molar_mass: [g/mol] average molar mass of the gas
    :param P: [Pa] pressure
    """

    def __init__(self, molar_mass, P):
        state_schema = {"T": {"required": True, "type": "float", "min": 0.0}}
        super().__init__("Ideal Gas", "Density", "rho", "\\rho", "kg/m3",
                         state_schema, None, None)

        self.mm = molar_mass / 1000.0
        """[kg/mol] average molar mass of the gas"""
        self.P = P
        """[Pa] pressure"""

    def calculate(self, **state):
        """
        Calculate the density at the specified temperature.

        :param T: [K] temperature

        :returns: [kg/m3] density

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """
        super().calculate(**state)
        return self.mm * self.P / R / state["T"]

    def plot(self, datasets, path, show=False):
        with PdfPages(path) as pdf:
            x_min = 1.0e100
            x_max = -1.0e100

            for ds in datasets.values():
                x_vals = ds.data["T"].tolist()
                y_vals = ds.data[self.symbol].tolist()
                plt.plot(
                    x_vals, y_vals, "o", alpha=0.4, markersize=4, label=ds.name)

                x_min = min(min(x_vals), x_min)
                x_max = max(max(x_vals), x_max)

            x_min = max(x_min, self.state_schema["T"]["min"])

            x_vals2 = np.linspace(x_min, x_max, 80)
            fx = [self(T=x) for x in x_vals2]
            plt.plot(x_vals2, fx, linewidth=0.3, label="model")

            plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 4))
            plt.legend(loc=0)
            plt.title("$%s$ vs $T$" % self.display_symbol)
            plt.xlabel("$T$ (K)")

            plt.ylabel("$%s$ (%s)" % (self.display_symbol, self.units))

            fig = plt.gcf()
            pdf.savefig(fig)
            plt.close()

        if show:
            webbrowser.open_new(path)


class RhoTP(Model):
    """
    A model that describes the variation in density of an ideal gas as a
    function of temperature and pressure.

    :param molar_mass: [g/mol] average molar mass of the gas
    """

    def __init__(self, molar_mass):
        state_schema = {"T": {"required": True, "type": "float", "min": 0.0},
                        "P": {"required": True, "type": "float", "min": 0.0}}
        super().__init__("Ideal Gas", "Density", "rho", "\\rho", "kg/m3",
                         state_schema, None, None)

        self.mm = molar_mass / 1000.0
        """[kg/mol] average molar mass of the gas"""

    def calculate(self, **state):
        """
        Calculate the density at the specified temperature and pressure.

        :param T: [K] temperature
        :param P: [Pa] pressure

        :returns: [kg/m3] density

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """
        super().calculate(**state)
        return self.mm * state["P"] / R / state["T"]


class RhoTPx(Model):
    """
    A model that describes the variation in density of an ideal gas as a
    function of temperature, pressure, and molar composition.
    """

    def __init__(self):
        state_schema = {"T": {"required": True, "type": "float", "min": 0.0},
                        "P": {"required": True, "type": "float", "min": 0.0},
                        "x": {"required": True, "type": "dict"}}
        super().__init__("Ideal Gas", "Density", "rho", "\\rho", "kg/m3",
                         state_schema, None, None)

    def calculate(self, **state):
        """
        Calculate the density at the specified temperature, pressure, and
        composition.

        :param T: [K] temperature
        :param P: [Pa] pressure
        :param x: [mole fraction] dictionary of compounds and mole fractions

        :returns: [kg/m3] density

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """
        super().calculate(**state)
        mm_average = 0.0
        for compound, molefraction in state["x"].items():
            mm_average += molefraction * mm(compound)
        mm_average /= 1000.0

        return mm_average * state["P"] / R / state["T"]


if __name__ == "__main__":
    import unittest
    from idealgas_test import *
    unittest.main()
