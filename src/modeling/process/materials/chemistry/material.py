# -*- coding: utf-8 -*-
"""
This module provides material and material package classes that can do chemical calculations.\n

@name: chemmaterial
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


# =============================================================================
# Types.
# =============================================================================

class Material(NamedObject):
    """Represents a material consisting of multiple chemical compounds.\n
    Properties defined here:\n
    name           : The material's name.
    compounds      : The material's list of chemical compounds.
    compound_count : The number of chemical compounds in the material.
    assays         : A dictionary containing assays for this material.
    """

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, file_path):
        """Initialise the object from a text file containing compounds and assays.
        The format of the text file is as follows:
        * The lines are space separated. The values in a line are separated by one or more spaces.
        * The first line is a heading line.
        * All subsequent lines contain a compound formula and phase, followed by mass fractions.
        * The first column lists the compounds in the material.
        * All subsequent columns describe assays of the material.
        The following is an example of a material text file:
        Compound   IlmeniteA  IlmeniteB  IlmeniteC
        Al2O3      0.01160    0.01550    0.00941
        CaO        0.00022    0.00001    0.00017
        Cr2O3      0.00008    0.00022    0.00011
        Fe2O3      0.20200    0.47300    0.49674
        Fe3O4      0.00000    0.00000    0.00000
        FeO        0.27900    0.19100    0.00000
        K2O        0.00004    0.00001    0.00005
        MgO        0.01040    0.00580    0.01090
        MnO        0.00540    0.00480    0.00525
        Na2O       0.00007    0.00005    0.00031
        P4O10      0.00001    0.00032    0.00015
        SiO2       0.00850    0.00490    0.01744
        TiO2       0.47700    0.29400    0.45949
        V2O5       0.00360    0.00800    0.00000
        """

        # Initialise the material's properties.
        self.name = name
        self.compounds = list()

        # Read the material's data from the file and prepare it for use.
        f = open(file_path, "r")
        lines = f.readlines()
        f.close()
        lines = self._prepare_lines(lines)

        # Determine the assay names, and create a dictionary entry for each assay.
        assay_names = lines[0].split(" ")
        del(assay_names[0:1])
        self.assays = dict()
        for assay_name in assay_names:
            self.assays[assay_name] = numpy.array([])

        # Read the compounds and assays.
        for i in range(1, len(lines)):
            strings = lines[i].split(" ")
            if len(strings) < len(assay_names) + 1: # Not a full line.
                continue
            self.compounds.append(strings[0])       # Add the new compound.
            for j in range(0, len(self.assays)):    # Add the mass fractions to the assays.
                assay_name = assay_names[j]
                self.assays[assay_name] = numpy.append(self.assays[assay_name], float(strings[j+1]))

        # Initialise the remaining properties.
        self.compound_count = len(self.compounds)
        self.elements = self._create_element_list()


    def __str__(self):
        """Create a string representation of self."""
        result = "Material: name='" + self.name + "'\n"

        # Create the header line of the table.
        result = result + "Compound".ljust(20)
        assay_names = sorted(self.assays.keys())
        for assay_name in assay_names:
            result = result + assay_name.ljust(20)
        result = result + "\n"

        # Create the content lines of the table.
        for compound in self.compounds:
            result = result + compound.ljust(20)
            compound_index = self.get_compound_index(compound)
            for assay_name in assay_names:
                result = result + str(self.assays[assay_name][compound_index]).ljust(20)
            result = result + "\n"
        return result


    # -------------------------------------------------------------------------
    # Private methods.
    # -------------------------------------------------------------------------
    def _prepare_lines(self, lines):
        """Prepare the lines read from the text file before starting to process it."""

        result = list()
        for line in lines:
            line = line.strip()                 # Remove all whitespace characters (e.g. spaces, line breaks, etc.) from the start and end of the line.
            line = line.replace("\t", " ")      # Replace all tabs with spaces.
            while line.find("  ") > -1:         # Replace all repeating spaces with a single space.
                line = line.replace("  ", " ")
            result.append(line)
        return result


    def _create_element_list(self):
        """Extract an alphabetically sorted list of elements from the compounds of the material.\n
        return : An alphabeticall sorted list of elements."""

        element_set = stoich.elements(self.compounds)
        return sorted(list(element_set))


    # -------------------------------------------------------------------------
    # Public methods.
    # -------------------------------------------------------------------------
    def get_compound_index(self, compound):
        """Determine the index of the specified compound.\n
        compound : The formula and phase of the specified compound, e.g. Fe2O3[S1].\n
        return   : The index of the specified compound.
        """

        return self.compounds.index(compound)


    def create_empty_assay(self):
        """Create an empty array to store an assay. The array's length will be equal to the number of compounds in the material.\n
        return : A floating point array.
        """

        return numpy.zeros(self.compound_count)


    def add_assay(self, name, assay):
        """Add an assay to the material.\n
        name  : The name of the new assay.
        assay : A numpy array containing the compound mass fractions for the assay. The sequence of the assay's elements must correspond to the sequence of the material's compounds.
        """

        if not type(assay) is numpy.ndarray:
            raise Exception("Invalid assay. It must be a numpy array.")
        elif not assay.shape == (self.compound_count,):
            raise Exception("Invalid assay: It must have the same number of elements as the material has compounds.")
        elif name in self.assays.keys():
            raise Exception("Invalid assay: An assay with that name already exists.")
        self.assays[name] = assay


    def get_assay_total(self, name):
        """Calculate the total of the specified assay.\n
        name   : The name of the assay.\n
        return : The total mass fraction of the specified assay.
        """

        return sum(self.assays[name])


    def create_package(self, assay = None, mass = 0.0, normalise=True):
        """Create a MaterialPackage based on the specified parameters.\n
        assay     :       The name of the assay based on which the package must be created.
        mass      : [kg]  The mass of the package.
        normalise :       Indicates whether the assay must be normalised before creating the package.\n
        return    :       The created MaterialPackage.
        """

        if assay == None:
            return MaterialPackage(self, self.create_empty_assay())

        if normalise:
            assay_total = self.get_assay_total(assay)
        else:
            assay_total = 1.0
        return MaterialPackage(self, mass * self.assays[assay] / assay_total)



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
            raise TypeError("Invalid material type. Must be chemmaterial.Material")
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
    data_path = os.path.join(module_path, r"data")
    data_path = os.path.abspath(data_path)
    return data_path

DEFAULT_DATA_PATH = _get_default_data_path()
