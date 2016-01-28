# -*- coding: utf-8 -*-
"""
This module contains a single class representing a Cp record of a chemical
compound phase.
"""
__version__ = "0.2.0"

import math
from auxi.core.object import Object


class CpRecord(Object):
    """A Cp equation record for a compound phase over a specific temperature
    range.

    :param dictionary: Dictionary containing the data required to initialise \
    the phase."""

    def __init__(self, dictionary):
        self.Tmin = dictionary["Tmin"]

        """The minimum temperature of the range covered by this record. [K]"""
        self.Tmax = dictionary["Tmax"]
        """The maximum temperature of the range covered by this record. [K]"""

        self._coefficients = list()
        """The coefficiencts of the terms in the Cp equation."""

        self._exponents = list()
        """The exponents of the terms in the Cp equation."""

        for t in dictionary["Terms"]:
            self._coefficients.append(t["Coefficient"])
            self._exponents.append(t["Exponent"])


    def __str__(self):
        result = "\t\tCp RECORD:" + "\n"
        result = result + "\t\t\tTmin: " + str(self.Tmin) + "\n"
        result = result + "\t\t\tTmax: " + str(self.Tmax) + "\n"
        for i in range(len(self._coefficients)):
            result = result + "\t\t\t{:.8e}".format(self._coefficients[i]) + " "
            result = result + str(self._exponents[i]) + "\n"
        return result


    def Cp(self, temperature):
        """Calculate the heat capacity of the compound phase.

        :param temperature: [K]

        :returns: Heat capacity. [J/mol/K]"""

        result = 0.0
        for c, e in zip(self._coefficients, self._exponents):
            result = result + c * temperature ** e
        return result


    def H(self, temperature):
        """Calculate the portion of enthalpy of the compound phase covered by
        this Cp record.

        :param temperature: [K]

        :returns: Enthalpy. [J/mol]"""

        result = 0.0
        if temperature < self.Tmax:
            T = temperature
        else:
            T = self.Tmax
        Tref = self.Tmin
        for c, e in zip(self._coefficients, self._exponents):
            # Analytically integrate Cp(T).
            if e == -1.0:
                result = result + c * (math.log(T) - math.log(Tref))
            else:
                result = result + c * (T ** (e + 1.0) - Tref ** (e + 1.0)) / (e + 1.0)
        return result


    def S(self, temperature):
        """Calculate the portion of entropy of the compound phase covered by
        this Cp record.

        :param temperature: [K]

        :returns: Entropy. [J/mol/K]"""

        result = 0.0
        if temperature < self.Tmax:
            T = temperature
        else:
            T = self.Tmax
        Tref = self.Tmin
        for c, e in zip(self._coefficients, self._exponents):
            # Create a modified exponent to analytically integrate Cp(T)/T instead of Cp(T).
            e_modified = e - 1.0
            if e_modified == -1.0:
                result = result + c * (math.log(T) - math.log(Tref))
            else:
                result = result + c * (T ** (e_modified + 1.0) - Tref ** (e_modified + 1.0)) / (e_modified + 1.0)
        return result
