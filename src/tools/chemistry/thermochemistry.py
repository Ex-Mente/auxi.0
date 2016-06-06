#!/usr/bin/env python3
"""
This module provides classes and functions for doing thermochemical
calculations.
"""

import os
import sys
import glob
import math

from auxi.core.objects import Object, NamedObject
from auxi.core.helpers import get_path_relative_to_module as get_path
from auxi.tools.chemistry.stoichiometry import molar_mass as mm


__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class CpRecord(Object):
    """
    A heat capacity (Cp) equation record for a compound phase over a
    specific temperature range.

    :param dictionary: A dictionary containing the data required to initialise
      the phase.
    """

    def __init__(self, dictionary):
        self.Tmin = dictionary['Tmin']
        """[K] The minimum temperature of the range covered by this record."""
        if type(self.Tmin) is not float:
            self.Tmin = float(self.Tmin)

        self.Tmax = dictionary['Tmax']
        """[K] The maximum temperature of the range covered by this record."""
        if type(self.Tmax) is not float:
            self.Tmax = float(self.Tmax)

        self._coefficients = []
        """The coefficiencts of the terms in the Cp equation."""

        self._exponents = []
        """The exponents of the terms in the Cp equation."""

        for t in dictionary['Terms']:
            c = t['Coefficient']
            e = t['Exponent']
            if type(c) is not float:
                c = float(c)
            if type(e) is not float:
                e = float(e)
            self._coefficients.append(c)
            self._exponents.append(e)

    def __str__(self):
        result = '\t\tCp RECORD:' + '\n'
        result += '\t\t\tTmin: ' + str(self.Tmin) + '\n'
        result += '\t\t\tTmax: ' + str(self.Tmax) + '\n'

        for i in range(len(self._coefficients)):
            result += '\t\t\t{:.8e}'.format(self._coefficients[i]) + ' '
            result += str(self._exponents[i]) + '\n'

        return result

    def Cp(self, temperature):
        """
        Calculate the heat capacity of the compound phase.

        :param temperature: [K]

        :returns: [J/mol/K] Heat capacity.
        """

        result = 0.0
        for c, e in zip(self._coefficients, self._exponents):
            result += c * temperature ** e
        return result

    def H(self, temperature):
        """
        Calculate the portion of enthalpy of the compound phase covered by this
        Cp record.

        :param temperature: [K]

        :returns: [J/mol] Enthalpy.
        """

        result = 0.0
        if temperature < self.Tmax:
            T = temperature
        else:
            T = self.Tmax
        Tref = self.Tmin
        for c, e in zip(self._coefficients, self._exponents):
            # Analytically integrate Cp(T).
            if e == -1.0:
                result += c * (math.log(T) - math.log(Tref))
            else:
                result += c * (T ** (e + 1.0) - Tref ** (e + 1.0)) / (e + 1.0)
        return result

    def S(self, temperature):
        """
        Calculate the portion of entropy of the compound phase covered by this
        Cp record.

        :param temperature: [K]

        :returns: Entropy. [J/mol/K]
        """

        result = 0.0
        if temperature < self.Tmax:
            T = temperature
        else:
            T = self.Tmax
        Tref = self.Tmin
        for c, e in zip(self._coefficients, self._exponents):
            # Create a modified exponent to analytically integrate Cp(T)/T
            # instead of Cp(T).
            e_modified = e - 1.0
            if e_modified == -1.0:
                result += c * (math.log(T) - math.log(Tref))
            else:
                e_mod = e_modified + 1.0
                result += c * (T ** (e_mod) - Tref ** (e_mod))  \
                    / (e_mod)
        return result


class Phase(NamedObject):
    """
    A phase of a chemical compound.

    :param dictionary: Dictionary containing the data required to initialise
      the phase.
    """

    def __init__(self, dictionary):
        self.name = dictionary['Symbol']
        """The phase's name, e.g. solid, liquid, gas, etc."""

        self.symbol = dictionary['Symbol']
        """The phase's symbol, e.g. S1 = solid 1, L = liquid, etc."""

        self.Tref = 298.15
        """[K] The reference temperature of the phase."""

        self.DHref = dictionary['DHref']
        """[J/mol] The formation enthalpy of the phase at Tref."""

        self.Sref = dictionary['Sref']
        """[J/mol/K] The standard entropy of the phase at Tref."""

        self._Cp_records = {}
        """A dictionary containing the phase's Cp records."""

        for k, v in dictionary['Cp_records'].items():
            tmax = k
            if type(tmax) is not float:
                tmax = float(tmax)
            self._Cp_records[tmax] = CpRecord(v)

    def __str__(self):
        result = '\tPHASE: ' + self.name + '\n'
        result += '\t\tName: ' + self.name + '\n'
        result += '\t\tSymbol: ' + self.symbol + '\n'
        result += '\t\tTref: ' + str(self.Tref) + '\n'
        result += '\t\tDHref: ' + str(self.DHref) + '\n'
        result += '\t\tSref: ' + str(self.Sref) + '\n'
        result += '\t\tCp record count:' + str(len(self._Cp_records)) + '\n'

        for k, v in self._Cp_records.items():
            result += str(v)

        return result

    def Cp(self, temperature):
        """
        Calculate the heat capacity of the compound phase at the specified
        temperature.

        :param temperature: [K]

        :returns: [J/mol/K] The heat capacity of the compound phase.
        """

        for Tmax in sorted(self._Cp_records.keys()):
            if temperature < Tmax:
                return self._Cp_records[Tmax].Cp(temperature)

        Tmax = max(self._Cp_records.keys())

        return self._Cp_records[Tmax].Cp(Tmax)

    def H(self, temperature):
        """
        Calculate the enthalpy of the compound phase at the specified
        temperature.

        :param temperature: [K]

        :returns: [J/mol] The enthalpy of the compound phase.
        """

        result = self.DHref

        for Tmax in sorted(self._Cp_records.keys()):
            result += self._Cp_records[Tmax].H(temperature)
            if temperature <= Tmax:
                return result

        # Extrapolate beyond the upper limit by using a constant heat capacity.
        Tmax = max(self._Cp_records.keys())
        result += self.Cp(Tmax)*(temperature - Tmax)

        return result

    def S(self, temperature):
        """
        Calculate the entropy of the compound phase at the specified
        temperature.

        :param temperature: [K]

        :returns: [J/mol/K] The entropy of the compound phase.
        """

        result = self.Sref

        for Tmax in sorted(self._Cp_records.keys()):
            result += self._Cp_records[Tmax].S(temperature)
            if temperature <= Tmax:
                return result

        # Extrapolate beyond the upper limit by using a constant heat capacity.
        Tmax = max(self._Cp_records.keys())
        result += self.Cp(Tmax)*math.log(temperature / Tmax)

        return result

    def G(self, temperature):
        """Calculate the heat capacity of the compound phase at the specified
        temperature.

        :param temperature: [K]

        :returns: [J/mol] The Gibbs free energy of the compound phase.
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


class Compound(Object):
    """
    Represents a chemical compound.

    :param dictionary: Dictionary containing the data required to initialise
      the compound.
    """

    def __init__(self, dictionary):
        self.formula = dictionary['Formula']
        """Chemical formula, e.g. 'Fe', 'CO2'."""

        self.molar_mass = mm(self.formula) / 1000.0
        """Molar mass. [kg/mol]"""

        self._phases = {}
        """Dictionary containing the compound's phase objects."""

        if 'Reference' in dictionary:
            self.reference = dictionary['Reference']
        else:
            self.reference = ""

        """Reference to the publisher of the thermo data."""

        for k, v in dictionary['Phases'].items():
            self._phases[k] = Phase(v)

#    def __str__(self):
#        result = 'COMPOUND: ' + '\n'
#        result += '\tFormula: ' + self.formula + '\n'
#
#        for k, v in self._phases.items():
#            result += str(v)
#
#        return result

    def get_phase_list(self):
        """
        Get a list of the compound's phases.

        :returns: List of phases.
        """

        return sorted(self._phases.keys())

    def get_reference(self):
        if self.reference in [None, ""]:
            return ""
        return get_datafile_references()[self.reference]

    def Cp(self, phase, temperature):
        """
        Calculate the heat capacity of a phase of the compound at a specified
        temperature.

        :param phase: A phase of the compound, e.g. 'S', 'L', 'G'.
        :param temperature: [K]

        :returns: [J/mol/K] Heat capacity.
        """

        try:
            return self._phases[phase].Cp(temperature)
        except KeyError:
            raise Exception("The phase '{}' was not found in compound '{}'."
                            .format(phase, self.formula))

    def H(self, phase, temperature):
        """
        Calculate the enthalpy of a phase of the compound at a specified
        temperature.

        :param phase: A phase of the compound, e.g. 'S', 'L', 'G'.
        :param temperature: [K]

        :returns: [J/mol] Enthalpy.
        """

        try:
            return self._phases[phase].H(temperature)
        except KeyError:
            raise Exception("The phase '{}' was not found in compound '{}'."
                            .format(phase, self.formula))

    def S(self, phase, temperature):
        """
        Calculate the enthalpy of a phase of the compound at a specified
        temperature.

        :param phase: A phase of the compound, e.g. 'S', 'L', 'G'.
        :param temperature: [K]

        :returns: [J/mol/K] Entropy.
        """

        try:
            return self._phases[phase].S(temperature)
        except KeyError:
            raise Exception("The phase '{}' was not found in compound '{}'."
                            .format(phase, self.formula))

    def G(self, phase, temperature):
        """
        Calculate the Gibbs free energy of a phase of the compound at a
        specified temperature.

        :param phase: A phase of the compound, e.g. 'S', 'L', 'G'.
        :param temperature: [K]

        :returns: [J/mol] Gibbs free energy.
        """

        try:
            return self._phases[phase].G(temperature)
        except KeyError:
            raise Exception("The phase '{}' was not found in compound '{}'."
                            .format(phase, self.formula))


def _get_default_data_path_():
    """
    Calculate the default path in which thermochemical data is stored.

    :returns: Default path.
    """

    module_path = os.path.dirname(sys.modules[__name__].__file__)
    data_path = os.path.join(module_path, r'data/rao')
    data_path = os.path.abspath(data_path)
    return data_path


def _read_compound_from_factsage_file_(file_name):
    """
    Build a dictionary containing the factsage thermochemical data of a
    compound by reading the data from a file.

    :param file_name: Name of file to read the data from.

    :returns: Dictionary containing compound data.
    """

    with open(file_name) as f:
        lines = f.readlines()

    compound = {}
    compound['Formula'] = lines[0].split(' ')[1]
    compound['Phases'] = {}
    phs = compound['Phases']

    started = False
    phaseold = 'zz'
    recordold = '0'

    for line in lines:
        if started:
            if line.startswith('_'):  # line indicating end of data
                break
            line = line.replace(' 298 ', ' 298.15 ')
            line = line.replace(' - ', ' ')
            while '  ' in line:
                line = line.replace('  ', ' ')
            line = line.replace(' \n', '')
            line = line.replace('\n', '')
            strings = line.split(' ')
            if len(strings) < 2:  # empty line
                continue
            phase = strings[0]
            if phase != phaseold:  # new phase detected
                phaseold = phase
                ph = phs[phase] = {}
                ph['Symbol'] = phase
                ph['DHref'] = float(strings[2])
                ph['Sref'] = float(strings[3])
                cprecs = ph['Cp_records'] = {}
                record = strings[1]
                if record != recordold:  # new record detected
                    recordold = record
                    Tmax = float(strings[len(strings) - 1])
                    cprecs[Tmax] = {}
                    cprecs[Tmax]['Tmin'] = float(strings[len(strings) - 2])
                    cprecs[Tmax]['Tmax'] = float(strings[len(strings) - 1])
                    cprecs[Tmax]['Terms'] = []
                    t = {}
                    t['Coefficient'] = float(strings[4])
                    t['Exponent'] = float(strings[5])
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 10:
                        t = {}
                        t['Coefficient'] = float(strings[6])
                        t['Exponent'] = float(strings[7])
                        cprecs[Tmax]['Terms'].append(t)
                else:  # old record detected
                    t = {}
                    t['Coefficient'] = float(strings[2])
                    t['Exponent'] = float(strings[3])
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 8:
                        t = {}
                        t['Coefficient'] = float(strings[4])
                        t['Exponent'] = float(strings[5])
                        cprecs[Tmax]['Terms'].append(t)
            else:  # old phase detected
                ph = phs[phase]
                record = strings[1]
                if record != recordold:  # new record detected
                    recordold = record
                    Tmax = float(strings[len(strings) - 1])
                    cprecs = ph['Cp_records']
                    cprecs[Tmax] = {}
                    cprecs[Tmax]['Tmin'] = float(strings[len(strings) - 2])
                    cprecs[Tmax]['Tmax'] = float(strings[len(strings) - 1])
                    cprecs[Tmax]['Terms'] = []
                    t = {}
                    t['Coefficient'] = float(strings[2])
                    t['Exponent'] = float(strings[3])
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 8:
                        t = {}
                        t['Coefficient'] = float(strings[4])
                        t['Exponent'] = float(strings[5])
                        cprecs[Tmax]['Terms'].append(t)
                else:  # old record detected
                    t = {}
                    t['Coefficient'] = float(strings[2])
                    t['Exponent'] = float(strings[3])
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 8:
                        t = {}
                        t['Coefficient'] = float(strings[4])
                        t['Exponent'] = float(strings[5])
                        cprecs[Tmax]['Terms'].append(t)
        if line.startswith('_'):  # line indicating the start of the data
            started = True

    return compound


def _split_compound_string_(compound_string):
    """
    Split a compound's combined formula and phase into separate strings for
    the formula and phase.

    :param compound_string: Formula and phase of a chemical compound, e.g.
      'SiO2[S1]'.

    :returns: Formula of chemical compound.
    :returns: Phase of chemical compound.
    """

    formula = compound_string.replace(']', '').split('[')[0]
    phase = compound_string.replace(']', '').split('[')[1]

    return formula, phase


def _finalise_result_(compound, value, mass):
    """
    Convert the value to its final form by unit conversions and multiplying
    by mass.

    :param compound: Compound object.
    :param value: [J/mol] Value to be finalised.
    :param mass: [kg] Mass of compound.

    :returns: [kWh] Finalised value.
    """

    result = value / 3.6E6  # J/x -> kWh/x
    result = result / compound.molar_mass  # x/mol -> x/kg
    result = result * mass  # x/kg -> x

    return result


def _read_compound_from_auxi_file_(file_name):
    """
    Build a dictionary containing the auxi thermochemical data of a compound by
    reading the data from a file.

    :param file_name: Name of file to read the data from.

    :returns: Dictionary containing compound data.
    """

    with open(file_name) as f:
        content = eval(f.read())
    return content


def write_compound_to_auxi_file(directory, compound):
    """
    Writes a compound to an auxi file at the specified directory.

    :param dir: The directory.
    :param compound: The compound.
    """

    file_name = "Compound_" + compound.formula + ".json"
    with open(os.path.join(directory, file_name), 'w') as f:
        f.write(str(compound))


def load_data_factsage(path=''):
    """
    Load all the thermochemical data factsage files located at a path.

    :param path: Path at which the data files are located.
    """

    compounds.clear()

    if path == '':
        path = default_data_path
    if not os.path.exists(path):
        raise Exception('The path does not exist.')

    files = glob.glob(os.path.join(path, 'Compound_*.txt'))

    for file in files:
        compound = Compound(_read_compound_from_factsage_file_(file))
        compounds[compound.formula] = compound


def load_data_auxi(path=''):
    """
    Load all the thermochemical data auxi files located at a path.

    :param path: Path at which the data files are located.
    """

    compounds.clear()

    if path == '':
        path = default_data_path
    if not os.path.exists(path):
        raise Exception('The path does not exist.')

    files = glob.glob(os.path.join(path, 'Compound_*.json'))

    for file in files:
        compound = Compound(_read_compound_from_auxi_file_(file))
        compounds[compound.formula] = compound


def list_compounds():
    """
    List all compounds that are currently loaded in the thermo module, and
    their phases.
    """

    print('Compounds currently loaded:')
    for compound in sorted(compounds.keys()):
        phases = compounds[compound].get_phase_list()
        for phase in phases:
            print(compound + '[' + phase + ']')


def get_datafile_references():
    """
    Retrieve all the references used by the datafiles.
    """

    with open(get_path(__file__, "data/references.json")) as f:
        content = eval(f.read())

    return content


def molar_mass(compound):
    """
    Determine the molar mass of a chemical compound.

    :param compound: Formula of a chemical compound, e.g. 'Fe2O3'.

    :returns: [kg/mol] Molar mass.
    """

    return mm(compound) / 1000.0


def Cp(compound_string, temperature, mass=1.0):
    """
    Calculate the heat capacity of the compound for the specified temperature
    and mass.

    :param compound_string: Formula and phase of chemical compound, e.g.
      'Fe2O3[S1]'.
    :param temperature: [°C]
    :param mass: [kg]

    :returns: [kWh/K] Heat capacity.
    """

    formula, phase = _split_compound_string_(compound_string)
    temperature_K = temperature + 273.15
    compound = compounds[formula]
    result = compound.Cp(phase, temperature_K)

    return _finalise_result_(compound, result, mass)


def H(compound_string, temperature, mass=1.0):
    """
    Calculate the enthalpy of the compound for the specified temperature and
    mass.

    :param compound_string: Formula and phase of chemical compound, e.g.
      'Fe2O3[S1]'.
    :param temperature: [°C]
    :param mass: [kg]

    :returns: [kWh] Enthalpy.
    """

    formula, phase = _split_compound_string_(compound_string)
    temperature_K = temperature + 273.15
    compound = compounds[formula]
    result = compound.H(phase, temperature_K)

    return _finalise_result_(compound, result, mass)


def S(compound_string, temperature, mass=1.0):
    """
    Calculate the entropy of the compound for the specified temperature and
    mass.

    :param compound_string: Formula and phase of chemical compound, e.g.
      'Fe2O3[S1]'.
    :param temperature: [°C]
    :param mass: [kg]

    :returns: [kWh/K] Entropy.
    """

    formula, phase = _split_compound_string_(compound_string)
    temperature_K = temperature + 273.15
    compound = compounds[formula]
    result = compound.S(phase, temperature_K)

    return _finalise_result_(compound, result, mass)


def G(compound_string, temperature, mass=1.0):
    """
    Calculate the Gibbs free energy of the compound for the specified
    temperature and mass.

    :param compound_string: Formula and phase of chemical compound, e.g.
      'Fe2O3[S1]'.
    :param temperature: [°C]
    :param mass: [kg]


    :returns: [kWh] Gibbs free energy.
    """

    formula, phase = _split_compound_string_(compound_string)
    temperature_K = temperature + 273.15
    compound = compounds[formula]
    result = compound.G(phase, temperature_K)

    return _finalise_result_(compound, result, mass)


compounds = {}
default_data_path = _get_default_data_path_()
load_data_auxi()


if __name__ == '__main__':
    import unittest
    from auxi.tools.chemistry.thermochemistry_test import ThermoFunctionTester
    unittest.main()
