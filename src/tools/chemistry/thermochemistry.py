# -*- coding: utf-8 -*-
"""
This module provides a number of functions for doing thermochemical
calculations.

compounds: A dictionary of chemical compounds with thermochemical data loaded
from data files.
"""
__version__ = "0.2.0"

import os
import sys
import glob
from auxi.tools.chemistry import stoichiometry as stoich
from auxi.tools.chemistry.compound import Compound


# =============================================================================
# Private functions.
# =============================================================================

def _get_default_data_path():
    """Calculate the default path in which thermochemical data is stored.

    :returns: Default path."""

    module_path = os.path.dirname(sys.modules[__name__].__file__)
    data_path = os.path.join(module_path, r"data/thermo")
    data_path = os.path.abspath(data_path)
    return data_path


def _read_compound_from_factsage_file(file_name):
    """Build a dictionary containing the thermochemical data of a compound by
    reading the data from a file.

    :param file_name: Name of file to read the data from.

    :returns: Dictionary containing compound data."""

    f = open(file_name, "r")
    lines = f.readlines()
    f.close()
    compound = dict()
    compound["Formula"] = lines[0].split(" ")[1]
    compound["Phases"] = dict()
    started = False
    phaseold = "zz"
    recordold = "0"
    for line in lines:
        if started:
            if line.startswith("_"):  # line indicating end of data
                break
            line = line.replace(" 298 ", " 298.15 ")
            line = line.replace(" - ", " ")
            while '  ' in line:
                line = line.replace("  ", " ")
            line = line.replace(" \n", "")
            line = line.replace("\n", "")
            strings = line.split(" ")
            if len(strings) < 2:  # empty line
                continue
            phase = strings[0]
            if phase != phaseold:  # new phase detected
                phaseold = phase
                compound["Phases"][phase] = dict()
                compound["Phases"][phase]["Symbol"] = phase
                compound["Phases"][phase]["DHref"] = float(strings[2])
                compound["Phases"][phase]["Sref"] = float(strings[3])
                compound["Phases"][phase]["Cp_records"] = dict()
                record = strings[1]
                if record != recordold:  # new record detected
                    recordold = record
                    Tmax = float(strings[len(strings) - 1])
                    compound["Phases"][phase]["Cp_records"][Tmax] = dict()
                    compound["Phases"][phase]["Cp_records"][Tmax]["Tmin"] = float(strings[len(strings) - 2])
                    compound["Phases"][phase]["Cp_records"][Tmax]["Tmax"] = float(strings[len(strings) - 1])
                    compound["Phases"][phase]["Cp_records"][Tmax]["Terms"] = list()
                    t = dict()
                    t["Coefficient"] = float(strings[4])
                    t["Exponent"] = float(strings[5])
                    compound["Phases"][phase]["Cp_records"][Tmax]["Terms"].append(t)
                    if len(strings) == 10:
                        t = dict()
                        t["Coefficient"] = float(strings[6])
                        t["Exponent"] = float(strings[7])
                        compound["Phases"][phase]["Cp_records"][Tmax]["Terms"].append(t)
                else:  # old record detected
                    t = dict()
                    t["Coefficient"] = float(strings[2])
                    t["Exponent"] = float(strings[3])
                    compound["Phases"][phase]["Cp_records"][Tmax]["Terms"].append(t)
                    if len(strings) == 8:
                        t = dict()
                        t["Coefficient"] = float(strings[4])
                        t["Exponent"] = float(strings[5])
                        compound["Phases"][phase]["Cp_records"][Tmax]["Terms"].append(t)
            else:  # old phase detected
                record = strings[1]
                if record != recordold:  # new record detected
                    recordold = record
                    Tmax = float(strings[len(strings) - 1])
                    compound["Phases"][phase]["Cp_records"][Tmax] = dict()
                    compound["Phases"][phase]["Cp_records"][Tmax]["Tmin"] = float(strings[len(strings) - 2])
                    compound["Phases"][phase]["Cp_records"][Tmax]["Tmax"] = float(strings[len(strings) - 1])
                    compound["Phases"][phase]["Cp_records"][Tmax]["Terms"] = list()
                    t = dict()
                    t["Coefficient"] = float(strings[2])
                    t["Exponent"] = float(strings[3])
                    compound["Phases"][phase]["Cp_records"][Tmax]["Terms"].append(t)
                    if len(strings) == 8:
                        t = dict()
                        t["Coefficient"] = float(strings[4])
                        t["Exponent"] = float(strings[5])
                        compound["Phases"][phase]["Cp_records"][Tmax]["Terms"].append(t)
                else:  # old record detected
                    t = dict()
                    t["Coefficient"] = float(strings[2])
                    t["Exponent"] = float(strings[3])
                    compound["Phases"][phase]["Cp_records"][Tmax]["Terms"].append(t)
                    if len(strings) == 8:
                        t = dict()
                        t["Coefficient"] = float(strings[4])
                        t["Exponent"] = float(strings[5])
                        compound["Phases"][phase]["Cp_records"][Tmax]["Terms"].append(t)
        if line.startswith("_"):  # line indicating the start of the data
            started = True
    return compound


def _split_compound_string(compound_string):
    """Split a compound's combined formula and phase into separate strings for
    the formula and phase.

    :param compound_string: Formula and phase of a chemical compound, e.g. \
    "SiO2[S1].

    :returns: Formula of chemical compound.
    :returns: Phase of chemical compound."""

    formula = compound_string.replace("]", "").split("[")[0]
    phase = compound_string.replace("]", "").split("[")[1]
    return formula, phase


def _finalise_result(compound, value, mass):
    """Convert the value to its final form by unit conversions and multiplying \
    by mass.

    :param compound: Compound object.
    :param value:    Value to be finalised. [J/mol]
    :param mass:     Mass of compound. [kg]

    :returns: Finalised value. [kWh]"""

    result = value / 3.6E6  # J/x -> kWh/x
    result = result / compound.molar_mass  # x/mol -> x/kg
    result = result * mass  # x/kg -> x
    return result


# =============================================================================
# Public functions.
# =============================================================================

def load_data(path=""):
    """Load all the thermochemical data files located at a path.

    :param path: Path at which the data files are located."""

    compounds.clear()

    if path == "":
        path = default_data_path
    if not os.path.exists(path):
        raise Exception("The path does not exist.")

    files = glob.glob(os.path.join(path, "Compound_*.txt"))

    for file in files:
        compound = Compound(_read_compound_from_factsage_file(file))
        compounds[compound.formula] = compound


def list_compounds():
    """List all compounds that are currently loaded in the thermo module, and
    their phases."""

    print("Compounds currently loaded in the thermo module:")
    for compound in sorted(compounds.keys()):
        phases = compounds[compound].get_phase_list()
        for phase in phases:
            print(compound + "[" + phase + "]")


def molar_mass(compound):
    """Determine the molar mass of a chemical compound.

    :param compound: Formula of a chemical compound, e.g. "Fe2O3".

    :returns: Molar mass. [kg/mol]"""

    return stoich.molecular_mass(compound) / 1000.0


def Cp(compound_string, temperature, mass=1.0):
    """Calculate the heat capacity of the compound for the specified
    temperature and mass.

    :param compound_string: Formula and phase of chemical compound, e.g. \
    "Fe2O3[S1]".
    :param temperature:     [°C]
    :param mass:            [kg]

    :returns: Heat capacity. [kWh/K]"""

    formula, phase = _split_compound_string(compound_string)
    temperature_K = temperature + 273.15
    compound = compounds[formula]
    result = compound.Cp(phase, temperature_K)
    return _finalise_result(compound, result, mass)


def H(compound_string, temperature, mass=1.0):
    """Calculate the enthalpy of the compound for the specified temperature
    and mass.

    :param compound_string: Formula and phase of chemical compound, e.g. \
    "Fe2O3[S1]".
    :param temperature:     [°C]
    :param mass:            [kg]

    :returns: Enthalpy. [kWh]"""

    formula, phase = _split_compound_string(compound_string)
    temperature_K = temperature + 273.15
    compound = compounds[formula]
    result = compound.H(phase, temperature_K)
    return _finalise_result(compound, result, mass)


def S(compound_string, temperature, mass=1.0):
    """Calculate the entropy of the compound for the specified temperature and
    mass.

    :param compound_string: Formula and phase of chemical compound, e.g. \
    "Fe2O3[S1]".
    :param temperature:     [°C]
    :param mass:            [kg]

    :returns: Entropy. [kWh/K]"""

    formula, phase = _split_compound_string(compound_string)
    temperature_K = temperature + 273.15
    compound = compounds[formula]
    result = compound.S(phase, temperature_K)
    return _finalise_result(compound, result, mass)


def G(compound_string, temperature, mass=1.0):
    """Calculate the Gibbs free energy of the compound for the specified
    temperature and mass.

    :param compound_string: Formula and phase of chemical compound, e.g. \
    "Fe2O3[S1]".
    :param temperature:     [°C]
    :param mass:            [kg]


    :returns: Gibbs free energy. [kWh]"""

    formula, phase = _split_compound_string(compound_string)
    temperature_K = temperature + 273.15
    compound = compounds[formula]
    result = compound.G(phase, temperature_K)
    return _finalise_result(compound, result, mass)


# =============================================================================
# Public variables.
# =============================================================================

compounds = {}
default_data_path = _get_default_data_path()
load_data()
