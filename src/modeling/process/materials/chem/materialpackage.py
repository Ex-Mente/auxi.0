# -*- coding: utf-8 -*-
"""
This module provides material and material package classes that can do chemical calculations.\n

@name: chemistry
@author: Ex Mente Technologies (Pty) Ltd
"""

import os
import sys
import numpy
import copy
from auxi.core.object import Object
from auxi.core.namedobject import NamedObject
from auxi.tools.chemistry import stoichiometry as stoich

__version__ = "0.2.0"


class MaterialPackage(Object):

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, material, compound_masses):
        """Initialise the object.\n
        material        :       A reference to the Material to which self belongs.
        compound_masses : [kg]  The masses of the compounds in the package.
        """

        # Confirm that the parameters are OK.
        if not type(material) is Material:
            raise TypeError("Invalid material type. Must be chemistry.material.Material")
        if not type(compound_masses) is numpy.ndarray:
            raise TypeError("Invalid compound_masses type. Must be numpy.ndarray.")

        # Initialise the object's properties.
        self.material = material
        self.compound_masses = compound_masses


    def __str__(self):
        """Create a string representation of the object."""
        result = "MaterialPackage\n"
        result = result + "material".ljust(20) + self.material.name + "\n"
        result = result + "mass".ljust(20) + str(self.get_mass()) + "\n"
        result = result + "Component masses:\n"
        for compound in self.material.compounds:
            index = self.material.get_compound_index(compound)
            result = result + compound.ljust(20) + str(self.compound_masses[index]) + "\n"
        return result


    # -------------------------------------------------------------------------
    # Operators.
    # -------------------------------------------------------------------------
    def __add__(self, other):
        """Addition operator (+).
        Add self and 'other' together, return the result as a new package, and leave self unchanged.\n
        other  : Can can be one of the following:
                 1. MaterialPackage
                    'other' is added to self to create a new package.
                 2. tuple: (compound, mass)
                    The specified mass of the specified compound is added to self.
        return : A new Material package that is the sum of self and 'other'.
        """

        # Add another package.
        if type(other) is MaterialPackage:
            if self.material == other.material: # Packages of the same material.
                result =  MaterialPackage(self.material, self.compound_masses + other.compound_masses)
                return result
            else: # Packages of different materials.
                result = self.clone()
                for compound in other.material.compounds:
                    if compound not in self.material.compounds:
                        raise Exception("Packages of '" + other.material.name + "' cannot be added to packages of '" + self.material.name + "'. The compound '" + compound + "' was not found in '" + self.material.name + "'.")
                    result = result + (compound, other.get_compound_mass(compound))
                return result

        # Add the specified mass of the specified compound.
        elif self._is_compound_mass_tuple(other):
            # Added material varialbes.
            compound = other[0]
            compound_index = self.material.get_compound_index(compound)
            mass = other[1]

            # Create the result package.
            result = self.clone()
            result.compound_masses[compound_index] = result.compound_masses[compound_index] + mass
            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid addition argument.")


    def __mul__(self, scalar):
        """The multiplication operator (*).
        Create a new package by multiplying self with other.\n
        scalar : The result is a new package with its content equal to self multiplied by a scalar, leaving self unchanged.\n
        result : A new MaterialPackage equal to self package multiplied by other.
        """

        # Multiply with a scalar floating point number.
        if type(scalar) is float or type(scalar) is numpy.float64 or type(scalar) is numpy.float32:
            if scalar < 0.0:
                raise Exception("Invalid multiplication operation. Cannot multiply package with negative number.")
            result = MaterialPackage(self.material, self.compound_masses * scalar)
            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid multiplication argument.")


    # -------------------------------------------------------------------------
    # Private methods.
    # -------------------------------------------------------------------------
    def _is_compound_mass_tuple(self, value):
        """Determines whether value is a tuple of the format (compound(str), mass(float))."""

        if not type(value) is tuple:
            return False
        elif not len(value) == 2:
            return False
        elif not type(value[0]) is str:
            return False
        elif not type(value[1]) is float and not type(value[1]) is numpy.float64 and not type(value[1]) is numpy.float32:
            return False
        else:
            return True


    # -------------------------------------------------------------------------
    # Public methods.
    # -------------------------------------------------------------------------
    def clone(self):
        """Create a complete copy of self.\n
        return : A MaterialPackage that is identical to self."""

        result = copy.copy(self)
        result.compound_masses = copy.deepcopy(self.compound_masses)
        return result


    # TODO: document
    # TODO: test
    def clear(self):
        self.compound_masses = self.compound_masses * 0.0

    def get_assay(self):
        """Determine the assay of self.\n
        return : [mass fractions] An array containing the assay of self.
        """

        return self.compound_masses / self.compound_masses.sum()


    def get_mass(self):
        """Determine the mass of self.\n
        return : [kg] The mass of self.
        """

        return self.compound_masses.sum()


    def get_compound_mass(self, compound):
        """Determine the mass of the specified compound in self.\n
        compound :      The formula and phase of the compound, e.g. Fe2O3[S1]\n
        return   : [kg] The mass of the compound in self.
        """

        return self.compound_masses[self.material.get_compound_index(compound)]


    # TODO: Test
    def get_compound_mass_fraction(self, compound):
        """Determine the mass fraction of the specified compound in self.\n
        compound : The formula and phase of the compound, e.g. Fe2O3[S1]\n
        return   : The mass fraction of the compound in self.
        """

        return self.get_compound_mass(compound) / self.get_mass()


    def get_element_masses(self):
        """Determine the masses of elements in the package.\n
        return : [kg] An array of element masses. The sequence of the elements in the result corresponds with the sequence of elements in the element list of the material.
        """

        result = numpy.zeros(len(self.material.elements))
        for compound in self.material.compounds:
            result = result + self.get_compound_mass(compound) * stoich.element_mass_fractions(compound, self.material.elements)
        return result


    def get_element_mass_dictionary(self):
        """Determine the masses of elements in the package and return as a dictionary.\n
        return : [kg] A dictionary of element symbols and masses.
        """

        element_symbols = self.material.elements
        element_masses = self.get_element_masses()
        result = dict()
        for s, m in zip(element_symbols, element_masses):
            result[s] = m
        return result


    def get_element_mass(self, element):
        """Determine the masses of elements in the package.\n
        return : [kg] An array of element masses. The sequence of the elements in the result corresponds with the sequence of elements in the element list of the material.
        """

        result = numpy.zeros(1)
        for compound in self.material.compounds:
            result = result + self.get_compound_mass(compound) * stoich.element_mass_fractions(compound, [element])
        return result[0]

    def extract(self, other):
        """Extract some material from self.
        Extract 'other' from self, modifying self and returning the extracted material as a new package.\n
        other  : Can be one of the following:
                 1. float
                    A mass equal to other is extracted from self. Self is reduced by other and the extracted package is returned as a new package.
                 2. tuple: (compound, mass)
                    The other tuple specifies the mass of a compound to be extracted. It is extracted from self and the extracted mass is returned as a new package.
                 3. string
                    The 'other' string specifies the compound to be extracted. All of the mass of that compound will be removed from self and a new package created with it.\n
        return : A new material package containing the material that was extracted from self.
        """

        # Extract the specified mass.
        if type(other) is float or type(other) is numpy.float64 or type(other) is numpy.float32:
            if other > self.get_mass():
                raise Exception("Invalid extraction operation. Cannot extract a mass larger than the package's mass.")
            fraction_to_subtract = other / self.get_mass()
            result = MaterialPackage(self.material, self.compound_masses * fraction_to_subtract)
            self.compound_masses = self.compound_masses * (1.0 - fraction_to_subtract)
            return result

        # Extract the specified mass of the specified compound.
        elif self._is_compound_mass_tuple(other):
            index = self.material.get_compound_index(other[0])
            if other[1] > self.compound_masses[index]:
                raise Exception("Invalid extraction operation. Cannot extract a compound mass larger than what the package contains.")
            self.compound_masses[index] = self.compound_masses[index] - other[1]
            resultarray = self.compound_masses*0.0
            resultarray[index] = other[1]
            result = MaterialPackage(self.material, resultarray)
            return result

        # Extract all of the specified compound.
        elif type(other) is str:
            index = self.material.get_compound_index(other)
            result = self * 0.0
            result.compound_masses[index] = self.compound_masses[index]
            self.compound_masses[index] = 0.0
            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid extraction argument.")


    # TODO: Test
    # TODO: Document
    def add_to(self, other):
        # Add another package.
        if type(other) is MaterialPackage:
            if self.material == other.material: # Packages of the same material.
                self.compound_masses = self.compound_masses + other.compound_masses
            else: # Packages of different materials.
                for compound in other.material.compounds:
                    if compound not in self.material.compounds:
                        raise Exception("Packages of '" + other.material.name + "' cannot be added to packages of '" + self.material.name + "'. The compound '" + compound + "' was not found in '" + self.material.name + "'.")
                    self.add_to((compound, other.get_compound_mass(compound)))

        # Add the specified mass of the specified compound.
        elif self._is_compound_mass_tuple(other):
            # Added material varialbes.
            compound = other[0]
            compound_index = self.material.get_compound_index(compound)
            mass = other[1]

            # Create the result package.
            self.compound_masses[compound_index] = self.compound_masses[compound_index] + mass

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid addition argument.")


def _get_default_data_path():
    module_path = os.path.dirname(sys.modules[__name__].__file__)
    data_path = os.path.join(module_path, r"../data")
    data_path = os.path.abspath(data_path)
    return data_path

DEFAULT_DATA_PATH = _get_default_data_path()
