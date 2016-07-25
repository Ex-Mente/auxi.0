#!/usr/bin/env python3
"""
This module provides tools for calculating material physical properties.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import webbrowser
from cerberus import Validator, ValidationError

from auxi.tools.materialphysicalproperties.core import Model


__version__ = '0.3.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Marno Grewar, Christoff Kok, Johan Zietsman'
__credits__ = ['Marno Grewar', 'Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Marno Grewar'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


def _formula_string(coeffs, variable="x"):
    """
    Create a string representation of a polynomial formula.
    """
    template0 = "%.3E"
    template1 = "%+.3E%s"
    templaten = "%+.3E%s^%.0f"

    result = ""
    for power, coeff in enumerate(reversed(coeffs)):
        if power == 0:
            result += template0 % coeff
        elif power == 1:
            result += " " + template1 % (coeff, variable)
        else:
            result += " " + templaten % (coeff, variable, power)
    return "$%s$" % result


class PolynomialModelT(Model):
    """
    A model that uses polynomial fits on experimental data to describe the
    variation of a specific material physical property as a function of
    temperature.

    :param material: the name of the material being described, e.g. "Air"
    :param proprty: the name of the property being described, e.g. "density"
    :param symbol: the symbol of the property being described, e.g. "rho"
    :param display symbol: the display symbol of the property being described,\
    e.g. "\rho"
    :param units: the units used to express the property, e.g. "kg/m3"
    :param references: a list of literature references on which this model\
    implementation is based, e.g. ['lienhard2015', 'smith2006']
    :param datasets: a list of data sets on which this model implementation is\
    based, e.g. ['dataset-air-lienhard2015.csv']
    :param coeffs: polynomial coefficients sorted from highest to lowest power
    """

    def create(dataset, symbol, degree):
        """
        Create a model object from the data set for the property specified by
        the supplied symbol, using the specified polynomial degree.

        :param dataset: a DataSet object
        :param symbol: the symbol of the property to be described, e.g. 'rho'
        :param degree: the polynomial degree to use

        :returns: a new PolynomialModelT object
        """

        x_vals = dataset.data['T'].tolist()
        y_vals = dataset.data[symbol].tolist()
        coeffs = np.polyfit(x_vals, y_vals, degree)

        result = PolynomialModelT(dataset.material,
                                  dataset.names_dict[symbol],
                                  symbol, dataset.display_symbols_dict[symbol],
                                  dataset.units_dict[symbol],
                                  None, [dataset.name], coeffs)

        result.state_schema['T']['min'] = float(min(x_vals))
        result.state_schema['T']['max'] = float(max(x_vals))

        return result

    def __init__(self, material, proprty, symbol, display_symbol, units,
                 references, datasets, coeffs):
        state_schema = {'T': {'required': True, 'type': 'float', 'min': 0.0}}
        super().__init__(material, proprty, symbol, display_symbol, units,
                         state_schema, references, datasets)
        self._coeffs = [float(x) for x in coeffs]

    def calculate(self, **state):
        """
        Calculate the material physical property at the specified temperature
        in the units specified by the object's 'property_units' property.

        :param T: [K] temperature

        :returns: physical property value
        """
        super().calculate(**state)
        return np.polyval(self._coeffs, state['T'])

    def plot(self, dataset, path, show=False):
        with PdfPages(path) as pdf:
            x_vals = dataset.data['T'].tolist()
            y_vals = dataset.data[self.symbol].tolist()
            plt.plot(x_vals, y_vals, 'ro', alpha=0.4, markersize=4)

            x_vals2 = np.linspace(min(x_vals), max(x_vals), 80)
            fx = np.polyval(self._coeffs, x_vals2)
            plt.plot(x_vals2, fx, linewidth=0.3, label='')

            plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 4))
            plt.legend(loc=3, bbox_to_anchor=(0, 0.8))
            plt.title('$%s$ vs $T$' % self.display_symbol)
            plt.xlabel('$T$ (K)')

            plt.ylabel('$%s$ (%s)' % (self.display_symbol, self.units))

            fig = plt.gcf()
            pdf.savefig(fig)
            plt.close()

        if show:
            webbrowser.open_new(path)


if __name__ == "__main__":
    import unittest
    from polynomial_test import *
    unittest.main()
