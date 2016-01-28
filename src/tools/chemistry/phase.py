# -*- coding: utf-8 -*-
"""
This module contains a single class representing a phase of a chemical
compound.
"""
__version__ = "0.2.0"

import math
from auxi.core.namedobject import NamedObject
from auxi.tools.chemistry.cprecord import CpRecord


class Phase(NamedObject):
    """Represents a phase of a chemical compound.

    :param dictionary: Dictionary containing the data required to initialise \
    the phase."""

    def __init__(self, dictionary):
        self.name = dictionary["Symbol"]
        """The phase's name, e.g. solid, liquid, gas, etc."""

        self.symbol = dictionary["Symbol"]
        """The phase's symbol, e.g. S1 = solid 1, L = liquid, etc."""

        self.Tref = 298.15
        """The reference temperature of the phase. [K]"""

        self.DHref = dictionary["DHref"]
        """The formation enthalpy of the phase at Tref. [J/mol]"""

        self.Sref = dictionary["Sref"]
        """The standard entropy of the phase at Tref. [J/mol/K]"""

        self._Cp_records = dict()
        """A dictionary containing the phase's Cp records."""

        for k, v in dictionary["Cp_records"].items():
            self._Cp_records[k] = CpRecord(v)

    def __str__(self):
        result = "\tPHASE: " + self.name + "\n"
        result = result + "\t\tName: " + self.name + "\n"
        result = result + "\t\tSymbol: " + self.symbol + "\n"
        result = result + "\t\tTref: " + str(self.Tref) + "\n"
        result = result + "\t\tDHref: " + str(self.DHref) + "\n"
        result = result + "\t\tSref: " + str(self.Sref) + "\n"
        result = result + "\t\tCp record count:" + str(len(self._Cp_records)) + "\n"
        for k, v in self._Cp_records.items():
            result = result + str(v)
        return result

    def Cp(self, temperature):
        """Calculate the heat capacity of the compound phase at the specified
        temperature.

        :param temperature: [K]

        :returns: The heat capacity of the compound phase. [J/mol/K]
        """
        for Tmax in sorted(self._Cp_records.keys()):
            if temperature < Tmax:
                return self._Cp_records[Tmax].Cp(temperature)
        Tmax = max(self._Cp_records.keys())
        return self._Cp_records[Tmax].Cp(Tmax)

    def H(self, temperature):
        """Calculate the enthalpy of the compound phase at the specified
        temperature.

        :param temperature: [K]

        :returns: The enthalpy of the compound phase. [J/mol]
        """
        result = self.DHref
        for Tmax in sorted(self._Cp_records.keys()):
            result = result + self._Cp_records[Tmax].H(temperature)
            if temperature <= Tmax:
                return result
        # Extrapolate beyond the upper limit by using a constant heat capacity.
        Tmax = max(self._Cp_records.keys())
        result = result + self.Cp(Tmax)*(temperature - Tmax)
        return result

    def S(self, temperature):
        """Calculate the entropy of the compound phase at the specified
        temperature.

        :param temperature: [K]

        :returns: The entropy of the compound phase. [J/mol/K]
        """
        result = self.Sref
        for Tmax in sorted(self._Cp_records.keys()):
            result = result + self._Cp_records[Tmax].S(temperature)
            if temperature <= Tmax:
                return result
        # Extrapolate beyond the upper limit by using a constant heat capacity.
        Tmax = max(self._Cp_records.keys())
        result = result + self.Cp(Tmax)*math.log(temperature / Tmax)
        return result

    def G(self, temperature):
        """Calculate the heat capacity of the compound phase at the specified
        temperature.

        :param temperature: [K]

        :returns: The Gibbs free energy of the compound phase. [J/mol]
        """
        h = self.DHref
        s = self.Sref
        for Tmax in sorted(self._Cp_records.keys()):
            h = h + self._Cp_records[Tmax].H(temperature)
            s = s + self._Cp_records[Tmax].S(temperature)
            if temperature <= Tmax:
                return h - temperature * s
        # Extrapolate beyond the upper limit by using a constant heat capacity.
        Tmax = max(self._Cp_records.keys())
        h = h + self.Cp(Tmax)*(temperature - Tmax)
        s = s + self.Cp(Tmax)*math.log(temperature / Tmax)
        return h - temperature * s
