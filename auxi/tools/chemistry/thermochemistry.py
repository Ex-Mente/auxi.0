#!/usr/bin/env python3
"""
This module provides classes and functions for doing thermochemical
calculations.
"""

import os
import sys
import glob
import math
import warnings
import json

from auxi.core.objects import Object, NamedObject
from auxi.core.helpers import get_path_relative_to_module as get_path
from auxi.tools.chemistry.stoichiometry import molar_mass as mm
from auxi.tools.physicalconstants import R


__version__ = '0.3.1'
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
        """The coefficients of the terms in the Cp equation."""

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

    def Cp(self, T):
        """
        Calculate the heat capacity of the compound phase.

        :param T: [K] temperature

        :returns: [J/mol/K] Heat capacity.
        """

        result = 0.0
        for c, e in zip(self._coefficients, self._exponents):
            result += c*T**e
        return result

    def H(self, T):
        """
        Calculate the portion of enthalpy of the compound phase covered by this
        Cp record.

        :param T: [K] temperature

        :returns: [J/mol] Enthalpy.
        """

        result = 0.0
        if T < self.Tmax:
            lT = T
        else:
            lT = self.Tmax
        Tref = self.Tmin

        for c, e in zip(self._coefficients, self._exponents):
            # Analytically integrate Cp(T).
            if e == -1.0:
                result += c * math.log(lT/Tref)
            else:
                result += c * (lT**(e+1.0) - Tref**(e+1.0)) / (e+1.0)
        return result

    def S(self, T):
        """
        Calculate the portion of entropy of the compound phase covered by this
        Cp record.

        :param T: [K] temperature

        :returns: Entropy. [J/mol/K]
        """

        result = 0.0
        if T < self.Tmax:
            lT = T
        else:
            lT = self.Tmax
        Tref = self.Tmin
        for c, e in zip(self._coefficients, self._exponents):
            # Create a modified exponent to analytically integrate Cp(T)/T
            # instead of Cp(T).
            e_modified = e - 1.0
            if e_modified == -1.0:
                result += c * math.log(lT/Tref)
            else:
                e_mod = e_modified + 1.0
                result += c * (lT**e_mod - Tref**e_mod) / e_mod
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

        if 'magnetic' in dictionary:
            self.Tc_mag = ['magnetic']['Tc']
            """The critical temperature, which is the Curie temperature for
            ferromagnetic materials or the Neel temperature for
            antiferromagnetic materials."""

            self.beta0_mag = ['magnetic']['beta0']
            """The average magnetic moment per atom."""

            self.p_mag = ['magnetic']['p']
            """This value can be thought of as the fraction of the magnetic
            enthalpy absorbed above the critical. It depends on structure."""

        self._Cp_records = {}
        """A dictionary containing the phase's Cp records."""

        for k, v in dictionary['Cp_records'].items():
            tmax = k
            # TODO: Fix string/float conversion issue
            tmax = str(float(tmax))
            self._Cp_records[tmax] = CpRecord(v)

        self._init()

    def _init(self):
        if 'Tc_mag' in dir(self) and 'beta0_mag' in dir(self) and \
           'p_mag' in dir(self):
            self._A_mag = 79/(140*self.p_mag)
            self._B_mag = (474/497)*(1/self.p_mag - 1)
            self._D_mag = (518/1125) + (11692/15975)*(1/self.p_mag - 1)
        else:
            self.Cp_mag = self.Zero_mag
            self.H_mag = self.Zero_mag
            self.S_mag = self.Zero_mag
            self.G_mag = self.Zero_mag

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

    def Zero_mag(self, T):
        """
        Return a zero value for a phase with no magnetic property data.

        :param T: [K] temperature

        :returns: Zero.
        """

        return 0.0

    def Cp(self, T):
        """
        Calculate the heat capacity of the compound phase at the specified
        temperature.

        :param T: [K] temperature

        :returns: [J/mol/K] The heat capacity of the compound phase.
        """

        # TODO: Fix str/float conversion
        for Tmax in sorted([float(TT) for TT in self._Cp_records.keys()]):
            if T < Tmax:
                return self._Cp_records[str(Tmax)].Cp(T) + self.Cp_mag(T)

        Tmax = max([float(TT) for TT in self._Cp_records.keys()])

        return self._Cp_records[str(Tmax)].Cp(Tmax) + self.Cp_mag(T)

    def Cp_mag(self, T):
        """
        Calculate the phase's magnetic contribution to heat capacity at the
        specified temperature.

        :param T: [K] temperature

        :returns: [J/mol/K] The magnetic heat capacity of the compound phase.

        Dinsdale, A. T. (1991). SGTE data for pure elements. Calphad, 15(4),
        317–425. http://doi.org/10.1016/0364-5916(91)90030-N
        """

        tau = T / self.Tc_mag

        if tau <= 1.0:
            c = (self._B_mag*(2*tau**3 + 2*tau**9/3 + 2*tau**15/5))/self._D_mag
        else:
            c = (2*tau**-5 + 2*tau**-15/3 + 2*tau**-25/5)/self._D_mag

        result = R*math.log(self.beta0_mag + 1)*c

        return result

    def H(self, T):
        """
        Calculate the enthalpy of the compound phase at the specified
        temperature.

        :param T: [K] temperature

        :returns: [J/mol] The enthalpy of the compound phase.
        """

        result = self.DHref

        for Tmax in sorted([float(TT) for TT in self._Cp_records.keys()]):
            result += self._Cp_records[str(Tmax)].H(T)
            if T <= Tmax:
                return result + self.H_mag(T)

        # Extrapolate beyond the upper limit by using a constant heat capacity.
        Tmax = max([float(TT) for TT in self._Cp_records.keys()])
        result += self.Cp(Tmax)*(T - Tmax)

        return result + self.H_mag(T)

    def H_mag(self, T):
        """
        Calculate the phase's magnetic contribution to enthalpy at the
        specified temperature.

        :param T: [K] temperature

        :returns: [J/mol] The magnetic enthalpy of the compound phase.

        Dinsdale, A. T. (1991). SGTE data for pure elements. Calphad, 15(4),
        317–425. http://doi.org/10.1016/0364-5916(91)90030-N
        """

        tau = T / self.Tc_mag

        if tau <= 1.0:
            h = (-self._A_mag/tau +
                 self._B_mag*(tau**3/2 + tau**9/15 + tau**15/40))/self._D_mag
        else:
            h = -(tau**-5/2 + tau**-15/21 + tau**-25/60)/self._D_mag

        return R*T*math.log(self.beta0_mag + 1)*h

    def S(self, T):
        """
        Calculate the entropy of the compound phase at the specified
        temperature.

        :param T: [K] temperature

        :returns: [J/mol/K] The entropy of the compound phase.
        """

        result = self.Sref

        for Tmax in sorted([float(TT) for TT in self._Cp_records.keys()]):
            result += self._Cp_records[str(Tmax)].S(T)
            if T <= Tmax:
                return result + self.S_mag(T)

        # Extrapolate beyond the upper limit by using a constant heat capacity.
        Tmax = max([float(TT) for TT in self._Cp_records.keys()])
        result += self.Cp(Tmax)*math.log(T / Tmax)

        return result + self.S_mag(T)

    def S_mag(self, T):
        """
        Calculate the phase's magnetic contribution to entropy at the
        specified temperature.

        :param T: [K] temperature

        :returns: [J/mol/K] The magnetic entropy of the compound phase.

        Dinsdale, A. T. (1991). SGTE data for pure elements. Calphad, 15(4),
        317–425. http://doi.org/10.1016/0364-5916(91)90030-N
        """

        tau = T / self.Tc_mag

        if tau <= 1.0:
            s = 1 - (self._B_mag*(2*tau**3/3 + 2*tau**9/27 + 2*tau**15/75)) / \
                self._D_mag
        else:
            s = (2*tau**-5/5 + 2*tau**-15/45 + 2*tau**-25/125)/self._D_mag

        return -R*math.log(self.beta0_mag + 1)*s

    def G(self, T):
        """Calculate the heat capacity of the compound phase at the specified
        temperature.

        :param T: [K] temperature

        :returns: [J/mol] The Gibbs free energy of the compound phase.
        """

        h = self.DHref
        s = self.Sref

        for Tmax in sorted([float(TT) for TT in self._Cp_records.keys()]):
            h = h + self._Cp_records[str(Tmax)].H(T)
            s = s + self._Cp_records[str(Tmax)].S(T)
            if T <= Tmax:
                return h - T * s + self.G_mag(T)

        # Extrapolate beyond the upper limit by using a constant heat capacity.
        Tmax = max([float(TT) for TT in self._Cp_records.keys()])
        h = h + self.Cp(Tmax)*(T - Tmax)
        s = s + self.Cp(Tmax)*math.log(T / Tmax)

        return h - T * s + self.G_mag(T)

    def G_mag(self, T):
        """
        Calculate the phase's magnetic contribution to Gibbs energy at the
        specified temperature.

        :param T: [K] temperature

        :returns: [J/mol] The magnetic Gibbs energy of the compound phase.

        Dinsdale, A. T. (1991). SGTE data for pure elements. Calphad, 15(4),
        317–425. http://doi.org/10.1016/0364-5916(91)90030-N
        """

        tau = T / self.Tc_mag

        if tau <= 1.0:
            g = 1 - (self._A_mag/tau +
                     self._B_mag*(tau**3/6 + tau**9/135 + tau**15/600)) /\
                    self._D_mag
        else:
            g = -(tau**-5/10 + tau**-15/315 + tau**-25/1500)/self._D_mag

        return R*T*math.log(self.beta0_mag + 1)*g


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
            if not 'Symbol' in v:
                v['Symbol'] = k
            self._phases[k] = Phase(v)

#    def __str__(self):
#        result = 'COMPOUND: ' + '\n'
#        result += '\tFormula: ' + self.formula + '\n'
#
#        for k, v in self._phases.items():
#            result += str(v)
#
#        return result

    def _init(self):
        for p in self._phases:
            self._phases[p]._init()

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

    def Cp(self, phase, T):
        """
        Calculate the heat capacity of a phase of the compound at a specified
        temperature.

        :param phase: A phase of the compound, e.g. 'S', 'L', 'G'.
        :param T: [K] temperature

        :returns: [J/mol/K] Heat capacity.
        """

        if phase not in self._phases:
            raise Exception("The phase '%s' was not found in compound '%s'." %
                            (phase, self.formula))

        return self._phases[phase].Cp(T)

    def H(self, phase, T):
        """
        Calculate the enthalpy of a phase of the compound at a specified
        temperature.

        :param phase: A phase of the compound, e.g. 'S', 'L', 'G'.
        :param T: [K] temperature

        :returns: [J/mol] Enthalpy.
        """

        try:
            return self._phases[phase].H(T)
        except KeyError:
            raise Exception("The phase '{}' was not found in compound '{}'."
                            .format(phase, self.formula))

    def S(self, phase, T):
        """
        Calculate the enthalpy of a phase of the compound at a specified
        temperature.

        :param phase: A phase of the compound, e.g. 'S', 'L', 'G'.
        :param T: [K] temperature

        :returns: [J/mol/K] Entropy.
        """

        try:
            return self._phases[phase].S(T)
        except KeyError:
            raise Exception("The phase '{}' was not found in compound '{}'."
                            .format(phase, self.formula))

    def G(self, phase, T):
        """
        Calculate the Gibbs free energy of a phase of the compound at a
        specified temperature.

        :param phase: A phase of the compound, e.g. 'S', 'L', 'G'.
        :param T: [K] temperature

        :returns: [J/mol] Gibbs free energy.
        """

        try:
            return self._phases[phase].G(T)
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

    compound = {'Formula': lines[0].split(' ')[1]}
    # FIXME: replace with logging
    print(compound['Formula'])
    compound['Phases'] = phs = {}

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
                    t = {'Coefficient': float(strings[4]),
                         'Exponent': float(strings[5])}
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 10:
                        t = {'Coefficient': float(strings[6]),
                             'Exponent': float(strings[7])}
                        cprecs[Tmax]['Terms'].append(t)
                else:  # old record detected
                    t = {'Coefficient': float(strings[2]),
                         'Exponent': float(strings[3])}
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 8:
                        t = {'Coefficient': float(strings[4]),
                             'Exponent': float(strings[5])}
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
                    t = {'Coefficient': float(strings[2]),
                         'Exponent': float(strings[3])}
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 8:
                        t = {'Coefficient': float(strings[4]),
                             'Exponent': float(strings[5])}
                        cprecs[Tmax]['Terms'].append(t)
                else:  # old record detected
                    t = {'Coefficient': float(strings[2]),
                         'Exponent': float(strings[3])}
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 8:
                        t = {'Coefficient': float(strings[4]),
                             'Exponent': float(strings[5])}
                        cprecs[Tmax]['Terms'].append(t)
        if line.startswith('_'):  # line indicating the start of the data
            started = True

    for name, ph in phs.items():
        cprecs = ph['Cp_records']
        first = cprecs[min(cprecs.keys())]
        first['Tmin'] = 298.15

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
        return json.load(f)


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
        warnings.warn('The specified data file path does not exist. (%s)' % path)
        return

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
        warnings.warn('The specified data file path does not exist. (%s)' % path)
        return

    files = glob.glob(os.path.join(path, 'Compound_*.json'))

    for file in files:
        # compound = Compound(_read_compound_from_auxi_file_(file))
        print(file)
        compound = Compound.read(file)
        compounds[compound.formula] = compound


def list_compounds():
    """
    List all compounds that are currently loaded in the thermo module, and
    their phases.
    """

    print('Compounds currently loaded:')
    for compound in sorted(compounds.keys()):
        phases = compounds[compound].get_phase_list()
        print('%s: %s' % (compound, ', '.join(phases)))
#        for phase in phases:
#            print(compound + '[' + phase + ']')


def get_datafile_references():
    """
    Retrieve all the references used by the datafiles.
    """
    with open(get_path(__file__, "data/references.json")) as f:
        return json.load(f)


def molar_mass(compound):
    """
    Determine the molar mass of a chemical compound.

    :param compound: Formula of a chemical compound, e.g. 'Fe2O3'.

    :returns: [kg/mol] Molar mass.
    """

    return mm(compound) / 1000.0


def Cp(compound_string, T, mass=1.0):
    """
    Calculate the heat capacity of the compound for the specified temperature
    and mass.

    :param compound_string: Formula and phase of chemical compound, e.g.
      'Fe2O3[S1]'.
    :param T: [°C] temperature
    :param mass: [kg]

    :returns: [kWh/K] Heat capacity.
    """

    formula, phase = _split_compound_string_(compound_string)
    TK = T + 273.15
    compound = compounds[formula]
    result = compound.Cp(phase, TK)

    return _finalise_result_(compound, result, mass)


def H(compound_string, T, mass=1.0):
    """
    Calculate the enthalpy of the compound for the specified temperature and
    mass.

    :param compound_string: Formula and phase of chemical compound, e.g.
      'Fe2O3[S1]'.
    :param T: [°C] temperature
    :param mass: [kg]

    :returns: [kWh] Enthalpy.
    """

    formula, phase = _split_compound_string_(compound_string)
    TK = T + 273.15
    compound = compounds[formula]
    result = compound.H(phase, TK)

    return _finalise_result_(compound, result, mass)


def S(compound_string, T, mass=1.0):
    """
    Calculate the entropy of the compound for the specified temperature and
    mass.

    :param compound_string: Formula and phase of chemical compound, e.g.
      'Fe2O3[S1]'.
    :param T: [°C] temperature
    :param mass: [kg]

    :returns: [kWh/K] Entropy.
    """

    formula, phase = _split_compound_string_(compound_string)
    TK = T + 273.15
    compound = compounds[formula]
    result = compound.S(phase, TK)

    return _finalise_result_(compound, result, mass)


def G(compound_string, T, mass=1.0):
    """
    Calculate the Gibbs free energy of the compound for the specified
    temperature and mass.

    :param compound_string: Formula and phase of chemical compound, e.g.
      'Fe2O3[S1]'.
    :param T: [°C] temperature
    :param mass: [kg]


    :returns: [kWh] Gibbs free energy.
    """

    formula, phase = _split_compound_string_(compound_string)
    TK = T + 273.15
    compound = compounds[formula]
    result = compound.G(phase, TK)

    return _finalise_result_(compound, result, mass)


compounds = {}
default_data_path = _get_default_data_path_()
load_data_auxi()


if __name__ == '__main__':
    import unittest
    from auxi.tools.chemistry.thermochemistry_test import ThermoFunctionTester
    unittest.main()
