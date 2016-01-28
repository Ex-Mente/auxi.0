# -*- coding: utf-8 -*-
"""
This module provides material package class that can do thermochemical
calculations.
"""
__version__ = "0.2.0"


import os
import sys
import numpy
import copy
from auxi.core.object import Object
from auxi.tools.chemistry import stoichiometry as stoich
from auxi.tools.chemistry import thermochemistry
from auxi.modeling.thermochemistry.material import Material


class MaterialPackage(Object):
    """Represents a quantity of material consisting of multiple chemical \
    compounds, having a specific mass, pressure, temperature and enthalpy.

    :param material:        A reference to the Material to which self belongs.
    :param compound_masses: Package compound masses. [kg]
    :param P:               Package pressure. [atm]
    :param T:               Package temperature. [°C]"""

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, material, compound_masses, P=1.0, T=25.0):
        # Confirm that the parameters are OK.
        if not type(material) is Material:
            raise TypeError("Invalid material type. Must be "
                            "thermomaterial.Material")
        if not type(compound_masses) is numpy.ndarray:
            raise TypeError("Invalid compound_masses type. Must be "
                            "numpy.ndarray.")

        # Initialise the object's properties.
        self.material = material
        self._P = P
        self._T = T
        self._compound_masses = compound_masses
        if self.get_mass() > 0.0:
            self._H = self._calculate_H(T)
        else:
            self._H = 0.0

        self.custom_properties = dict()


    def __str__(self):
        result = "==================================================================\n"
        result += "MaterialPackage\n"
        result += "==================================================================\n"
        result += "Material".ljust(20) + self.material.name + "\n"
        result = result + "Mass".ljust(20) + '{:.8e}'.format(self.get_mass()).rjust(15) + " kg\n"
        result = result + "Amount".ljust(20) + '{:.8e}'.format(self.get_amount()).rjust(15) + " kmol\n"
        result = result + "Pressure".ljust(20) + '{:.8e}'.format(self.P).rjust(15) + " atm\n"
        result = result + "Temperature".ljust(20) + '{:.8e}'.format(self.T).rjust(15) + " °C\n"
        result = result + "Enthalpy".ljust(20) + '{:.8e}'.format(self.H).rjust(15) + " kWh\n"
        result += "------------------------------------------------------------------\n"
        result = result + "Compound Details\n"
        result = result + "Formula".ljust(20) + "Mass".ljust(16) + \
                          "Mass Fraction".ljust(16) + \
                          "Mole Fraction".ljust(16) + "\n"
        result += "------------------------------------------------------------------\n"
        mass = self.get_mass()
        compound_moles = self.get_compound_amounts()
        total_moles = compound_moles.sum()
        if mass > 0.0:
            for compound in self.material.compounds:
                index = self.material.get_compound_index(compound)
                result += compound.ljust(20) + \
                          '{:.8e}'.format(self._compound_masses[index])
                result += "  " + \
                          '{:.8e}'.format(self._compound_masses[index] / mass)
                result += "  " + \
                          '{:.8e}'.format(compound_moles[index] / total_moles)
                result += "\n"
        else:
            for compound in self.material.compounds:
                index = self.material.get_compound_index(compound)
                result += compound.ljust(20) + '{:.8e}'.format(0.0)
                result += "  " + '{:.8e}'.format(0.0)
                result += "  " + '{:.8e}'.format(0.0)
                result += "\n"

        # Write the custom properties.
        if len(self.custom_properties) > 0:
            result += "------------------------------------------------------------------\n"
            result += "Custom Properties:\n"
            result += "------------------------------------------------------------------\n"
            properties = list(sorted(self.custom_properties.keys()))
            for prop in properties:
                result += prop.ljust(20)
                result += "{:.8e}".format(self.custom_properties[prop])
                result += "\n"

        result += "==================================================================\n"
        return result


    # -------------------------------------------------------------------------
    # Operators.
    # -------------------------------------------------------------------------
    def __add__(self, other):
        """Addition operator (+).

        Add this package (self) and 'other' together, return the result as a
        new package, and leave self unchanged.

        :param other: Can can be one of the following:
                 1. MaterialPackage
                    'other' is added to self to create a new package.
                 2. tuple: (compound, mass)
                    The specified mass of the specified compound is added to \
                    self, assuming the added material has the same \
                    temperature as self.
                 3. tuple: (compound, mass, temperature)
                    The specified mass of the specified compound at the \
                    specified temperature is added to self.

        :returns: A new Material package that is the sum of self and 'other'.
        """

        # Add another package.
        if type(other) is MaterialPackage:
            if self.material == other.material:  # Packages of same material.
                result = MaterialPackage(self.material,
                                         self._compound_masses +
                                         other._compound_masses)
                result._set_H(self._H + other._H)
                result._P = self._P
                return result
            else:  # Packages of different materials.
                H = self._get_H() + other._get_H()
                result = self.clone()
                for compound in other.material.compounds:
                    if compound not in self.material.compounds:
                        raise Exception("Packages of '" + other.material.name +
                                        "' cannot be added to packages of '" +
                                        self.material.name +
                                        "'. The compound '" + compound +
                                        "' was not found in '" +
                                        self.material.name + "'.")
                    result = result + (compound,
                                       other.get_compound_mass(compound))
                result._set_H(H)
                return result

        # Add the specified mass of the specified compound.
        elif self._is_compound_mass_tuple(other):
            # Added material varialbes.
            compound = other[0]
            index = self.material.get_compound_index(compound)
            mass = other[1]
            enthalpy = thermo.H(compound, self._T, mass)

            # Create the result package.
            result = self.clone()
            result._compound_masses[index] = result._compound_masses[index] + \
                                             mass
            result._H = result._H + enthalpy
            result._P = self._P
            return result

        # Add the specified mass of 'compound' at the specified temperature.
        elif self._is_compound_mass_temperature_tuple(other):
            # Added material varialbes.
            compound = other[0]
            index = self.material.get_compound_index(compound)
            mass = other[1]
            temperature = other[2]
            enthalpy = thermo.H(compound, temperature, mass)

            # Create the result package.
            result = self * 1.0
            result._compound_masses[index] = result._compound_masses[index] + \
                                             mass
            result._set_H(self._H + enthalpy)
            result._P = self._P
            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid addition argument.")

    def __mul__(self, scalar):
        """The multiplication operator (*).

        Create a new package by multiplying self with scalar.

        :param scalar: The result is a new package with its content equal to \
        self multiplied by a scalar, leaving self unchanged.

        :returns: New MaterialPackage object."""

        # Multiply with a scalar floating point number.
        if type(scalar) is float or type(scalar) is numpy.float64 or \
           type(scalar) is numpy.float32:
            if scalar < 0.0:
                raise Exception("Invalid multiplication operation. Cannot "
                                "multiply package with negative number.")
            result = MaterialPackage(self.material, self._compound_masses *
                                     scalar, self._P, self._T)
            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid multiplication argument.")


    # -------------------------------------------------------------------------
    # Private methods.
    # -------------------------------------------------------------------------
    def _calculate_H(self, T):
        """Calculate the enthalpy of the package at the specified temperature.

        :param T: Temperature. [°C]

        :returns: Enthalpy. [kWh]"""

        H = 0.0
        for compound in self.material.compounds:
            index = self.material.get_compound_index(compound)
            dH =  thermo.H(compound, T, self._compound_masses[index])
            H = H + dH
        return H

    def _calculate_T(self, H):
        """Calculate the temperature of the package given the specified
        enthalpy using a secant algorithm.

        :param H: Enthalpy. [kWh]

        :returns: Temperature. [°C]"""

        # Create the initial guesses for temperature.
        x = list()
        x.append(self._T)
        x.append(self._T + 10.0)

        # Evaluate the enthalpy for the initial guesses.
        y = list()
        y.append(self._calculate_H(x[0]) - H)
        y.append(self._calculate_H(x[1]) - H)

        # Solve for temperature.
        for i in range(2, 50):
            x.append(x[i-1] - y[i-1]*((x[i-1] - x[i-2])/(y[i-1] - y[i-2])))
            y.append(self._calculate_H(x[i]) - H)
            if abs(y[i-1]) < 1.0e-5:
                break

        return x[len(x) - 1]

    def _is_compound_mass_tuple(self, value):
        """Determines whether value is a tuple of the format
        (compound(str), mass(float)).

        :param value: The value to be tested.

        :returns: True or False"""

        if not type(value) is tuple:
            return False
        elif not len(value) == 2:
            return False
        elif not type(value[0]) is str:
            return False
        elif not type(value[1]) is float and \
             not type(value[1]) is numpy.float64 and \
             not type(value[1]) is numpy.float32:
            return False
        else:
            return True

    def _is_compound_mass_temperature_tuple(self, value):
        """Determines whether value is a tuple of the format
        (compound(str), mass(float), temperature(float)).

        :param value: The value to be tested.

        :returns: True or False"""

        if not type(value) is tuple:
            return False
        elif not len(value) == 3:
            return False
        elif not type(value[0]) is str:
            return False
        elif not type(value[1]) is float and \
             not type(value[1]) is numpy.float64 and \
             not type(value[1]) is numpy.float32:
            return False
        elif not type(value[1]) is float and \
             not type(value[1]) is numpy.float64 and \
             not type(value[1]) is numpy.float32:
            return False
        else:
            return True

    def _set_H(self, H):
        """Set the enthalpy of the package to the specified value, and
        recalculate it's temperature.

        :param H: The new enthalpy value. [kWh]"""

        self._H = H
        self._T = self._calculate_T(H)

    def _get_H(self):
        """Determine the enthalpy of the package.

        :returns: Enthalpy. [kWh]"""

        return self._H

    def _set_T(self, T):
        """Set the temperature of the package to the specified value, and
        recalculate it's enthalpy.

        :param T: Temperature. [°C]"""

        self._T = T
        self._H = self._calculate_H(T)

    def _get_T(self):
        """Determine the temperature of of the package.

        :returns: Temperature. [°C]"""

        return self._T

    def _set_P(self, P):
        """Set the pressure of the package to the specified value.

        :param P: Pressure. [atm]"""

        self._P = P

    def _get_P(self):
        """Determine the pressure of the package.

        :returns: Pressure. [atm]"""

        return self._P

    # -------------------------------------------------------------------------
    # Public methods.
    # -------------------------------------------------------------------------
    def clone(self):
        """Create a complete copy of the package.

        :returns: A new MaterialPackage object."""

        result = copy.copy(self)
        result._compound_masses = copy.deepcopy(self._compound_masses)
        return result

    def clear(self):
        """Clear the package."""

        self._compound_masses = self._compound_masses * 0.0
        self._P = 1.0
        self._T = 25.0
        self._H = 0.0

    def get_assay(self):
        """Determine the assay of the package.

        :returns: Array of mass fractions."""

        return self._compound_masses / self._compound_masses.sum()

    def get_mass(self):
        """Determine the mass of the package.

        :returns: Mass. [kg]"""

        return self._compound_masses.sum()

    def get_compound_mass(self, compound):
        """Determine the mass of the specified compound in the package.

        :param compound: Formula and phase of a compound, e.g. "Fe2O3[S1]".

        :returns: Mass. [kg]"""

        if compound in self.material.compounds:
            return self._compound_masses[self.material.get_compound_index(compound)]
        else:
            return 0.0

    def get_compound_amounts(self):
        """Determine the mole amounts of all the compounds.

        :returns: List of amounts. [mol]"""

        result = self._compound_masses * 1.0
        for compound in self.material.compounds:
            index = self.material.get_compound_index(compound)
            result[index] = stoich.amount(compound, result[index])
        return result

    def get_compound_amount(self, compound):
        """Determine the mole amount of the specified compound.

        :returns: Amount. [mol]"""

        index = self.material.get_compound_index(compound)
        result = self._compound_masses[index]
        result = stoich.amount(compound, result)
        return result

    def get_amount(self):
        """Determine the sum of mole amounts of all the compounds.

        :returns: Amount. [mol]
        """

        result = 0.0
        for compound in self.material.compounds:
            result += self.get_compound_amount(compound)
        return result

    H = property(_get_H, _set_H, None, "Enthalpy. [kWh]")
    T = property(_get_T, _set_T, None, "Temperature. [°C]")
    P = property(_get_P, _set_P, None, "Pressure. [atm]")
    mass = property(get_mass, None, None, "[kg]")
    amount = property(get_amount, None, None, "[kmol]")

    def get_element_masses(self, elements = None):
        """Determine the masses of elements in the package.

        :returns: Array of element masses. [kg]"""

        if elements == None:
            elements = self.material.elements
        result = numpy.zeros(len(elements))
        for compound in self.material.compounds:
            result = result + self.get_compound_mass(compound) * stoich.element_mass_fractions(compound, elements)
        return result

    def get_element_mass_dictionary(self):
        """Determine the masses of elements in the package and return as a
        dictionary.

        :returns: Dictionary of element symbols and masses. [kg]"""

        element_symbols = self.material.elements
        element_masses = self.get_element_masses()
        result = dict()
        for s, m in zip(element_symbols, element_masses):
            result[s] = m
        return result

    def get_element_mass(self, element):
        """Determine the mass of the specified elements in the package.

        :returns: Masses. [kg]"""

        result = numpy.zeros(1)
        for compound in self.material.compounds:
            result = result + self.get_compound_mass(compound) * stoich.element_mass_fractions(compound, [element])
        return result[0]

    def extract(self, other):
        """Extract some material from this package.
        Extract 'other' from this package, modifying this package and
        returning the extracted material as a new package.

        :param other: Can be one of the following:

                 1. float
                    A mass equal to other is extracted from self. Self is
                    reduced by other and the extracted package is returned as
                    a new package.
                 2. tuple: (compound, mass)
                    The other tuple specifies the mass of a compound to be
                    extracted. It is extracted from self and the extracted
                    mass is returned as a new package.
                 3. string
                    The 'other' string specifies the compound to be extracted.
                    All of the mass of that compound will be removed from self
                    and a new package created with it.
                 4. Material
                    The 'other' material specifies the list of compounds to
                    extract.

        :returns: New MaterialPackage object."""

        # Extract the specified mass.
        if type(other) is float or \
           type(other) is numpy.float64 or \
           type(other) is numpy.float32:
            return self._extract_mass(other)

        # Extract the specified mass of the specified compound.
        elif self._is_compound_mass_tuple(other):
            return self._extract_compound_mass(other[0], other[1])

        # Extract all of the specified compound.
        elif type(other) is str:
            return self._extract_compound(other)

        # TODO: Test
        # Extract all of the compounds of the specified material.
        elif type(other) is Material:
            return self._extract_material(other)

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid extraction argument.")

    def _extract_mass(self, mass):
        if mass > self.get_mass():
            raise Exception("Invalid extraction operation. Cannot extract a mass larger than the package's mass.")
        fraction_to_subtract = mass / self.get_mass()
        result = MaterialPackage(self.material, self._compound_masses * fraction_to_subtract, self._P, self._T)

        self._compound_masses = self._compound_masses * (1.0 - fraction_to_subtract)
        self.T = self.T

        return result

    def _extract_compound(self, compound):
        result = self.material.create_package()

        if compound not in self.material.compounds:
            return result

        index = self.material.get_compound_index(compound)
        result._compound_masses[index] = self._compound_masses[index]
        result.T = self.T

        self._compound_masses[index] = 0.0
        self.T = self.T

        return result

    def _extract_compound_mass(self, compound, mass):
        if compound not in self.material.compounds:
            return self.material.create_package()

        index = self.material.get_compound_index(compound)
        if mass > self._compound_masses[index]:
            raise Exception("Invalid extraction operation. Cannot extract a compound mass larger than what the package contains.")
        self._compound_masses[index] = self._compound_masses[index] - mass
        self.T = self.T

        result = self.material.create_package(P=self._P, T=self._T)
        result += (compound, mass)

        return result

    def _extract_material(self, material):
        result = material.create_package()
        for compound in material.compounds:
            mass = self.get_compound_mass(compound)
            result += (compound, mass)
            self.extract(compound)
        result.T = self.T

        return result


def _get_default_data_path():
    module_path = os.path.dirname(sys.modules[__name__].__file__)
    data_path = os.path.join(module_path, r"data")
    data_path = os.path.abspath(data_path)
    return data_path

DEFAULT_DATA_PATH = _get_default_data_path()
