# -*- coding: utf-8 -*-
"""
This module contains a single class that represents chemical compound.
"""
__version__ = "0.2.0"

from auxi.core.object import Object
from auxi.tools.chemistry import stoichiometry as stoich
from auxi.tools.chemistry.phase import Phase


class Compound(Object):
    """Represents a chemical compound.

    :param dictionary: Dictionary containing the data required to initialise \
    the compound."""

    def __init__(self, dictionary):
        self.formula = dictionary["Formula"]
        """Chemical formula, e.g. "Fe", "CO2"."""

        self.molar_mass = stoich.molar_mass(self.formula) / 1000.0
        """Molar mass. [kg/mol]"""

        self._phases = dict()
        """Dictionary containing the compound's phase objects."""

        for k, v in dictionary["Phases"].items():
            self._phases[k] = Phase(v)

    def __str__(self):
        result = "COMPOUND: " + "\n"
        result = result + "\tFormula: " + self.formula + "\n"
        for k, v in self._phases.items():
            result = result + str(v)
        return result

    def get_phase_list(self):
        """Get a list of the compound's phases.

        :returns: List of phases."""

        return sorted(self._phases.keys())

    def Cp(self, phase, temperature):
        """Calculate the heat capacity of a phase of the compound at a
        specified temperature.

        :param phase:       A phase of the compound, e.g. "S", "L", "G".
        :param temperature: [K]

        :returns: Heat capacity. [J/mol/K]"""

        try:
            return self._phases[phase].Cp(temperature)
        except KeyError:
            raise Exception("The phase '" + phase + "' was not found in compound '" + self.formula + "'.")

    def H(self, phase, temperature):
        """Calculate the enthalpy of a phase of the compound at a specified
        temperature.

        :param phase:       A phase of the compound, e.g. "S", "L", "G".
        :param temperature: [K]

        :returns: Enthalpy. [J/mol]"""

        try:
            return self._phases[phase].H(temperature)
        except KeyError:
            raise Exception("The phase '" + phase + "' was not found in compound '" + self.formula + "'.")

    def S(self, phase, temperature):
        """Calculate the enthalpy of a phase of the compound at a specified
        temperature.

        :param phase:       A phase of the compound, e.g. "S", "L", "G".
        :param temperature: [K]

        :returns: Entropy. [J/mol/K]"""

        try:
            return self._phases[phase].S(temperature)
        except KeyError:
            raise Exception("The phase '" + phase + "' was not found in compound '" + self.formula + "'.")

    def G(self, phase, temperature):
        """Calculate the Gibbs free energy of a phase of the compound at a
        specified temperature.

        :param phase:       A phase of the compound, e.g. "S", "L", "G".
        :param temperature: [K]

        :returns: Gibbs free energy. [J/mol]"""

        try:
            return self._phases[phase].G(temperature)
        except KeyError:
            raise Exception("The phase '" + phase + "' was not found in compound '" + self.formula + "'.")
