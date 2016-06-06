#!/usr/bin/env python3
"""
This module provides psd material and material package classes that can do
size distribution calculations.
"""

import os
import sys
import copy

import numpy

from auxi.core.objects import Object
from auxi.core.objects import NamedObject

__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class Material(NamedObject):
    """
    Represents a particulate material consisting of multiple particle size
    classes.

    :param name: The material's name.
    :param file_path: The path of the material definition file.
    :param description: the material's description

    The format of the text file is as follows:

    * The lines are space separated. The values in a line are separated \
        by one or more spaces.
    * The first line is a heading line.
    * All subsequent lines contain a particle size, followed by mass fractions.
    * Particle sizes are indicated in [meter].
    * The first column lists the particle sizes in the material. Each class \
      must be interpreted as "mass fraction retained". In other words if \
      the size class is indicated as 307.2E-3, it means that it is the \
      class of material retained on a 307.2mm screen, and can also be \
      though of as +307.2mm material. The first size class represents the \
      largest particles. The final size class should be zero, as it \
      represents all material that passed through the smallest aperture screen.
    * All subsequent columns describe assays of the material.

    The following is an example of a material text file::

        Compound   FeedA  MillCharge
        307.2E-3   0.20   0.02
        108.6E-3   0.18   0.06
        38.4E-3    0.17   0.04
        13.6E-3    0.07   0.03
        4.8E-3     0.13   0.03
        1.7E-3     0.07   0.04
        600.0E-6   0.06   0.18
        210.0E-6   0.02   0.50
        75.0E-6    0.10   0.10
        0.0E0      0.00   0.00
    """

    def __init__(self, name, file_path, description=None):
        # Initialise the material's properties.
        self.name = name
        self.size_classes = list()

        # Read the material's data from the file and prepare it for use.
        f = open(file_path, "r")
        lines = f.readlines()
        f.close()
        lines = self._prepare_lines(lines)

        # Determine the assay names, and create a dictionary entry for each
        # assay.
        assay_names = lines[0].split(" ")
        del(assay_names[0:1])
        self.assays = dict()
        for assay_name in assay_names:
            self.assays[assay_name] = numpy.array([])

        # Read the size classes and assays.
        for i in range(1, len(lines)):
            strings = lines[i].split(" ")
            if len(strings) < len(assay_names) + 1:  # Not a full line.
                continue
            # Add the new size class.
            self.size_classes.append(float(strings[0]))
            # Add the mass fractions to the assays.
            for j in range(0, len(self.assays)):
                assay_name = assay_names[j]
                self.assays[assay_name] = numpy.append(
                    self.assays[assay_name], float(strings[j+1]))

        # Initialise the remaining properties.
        self.size_class_count = len(self.size_classes)

    def __str__(self):
        """
        Create a string representation of self.
        """

        result = "Material: name='" + self.name + "'\n"

        # Create the header line of the table.
        result = result + "Compound".ljust(20)
        assay_names = sorted(self.assays.keys())
        for assay_name in assay_names:
            result = result + assay_name.ljust(20)
        result = result + "\n"

        # Create the content lines of the table.
        for size_class in self.size_classes:
            result = result + str(size_class).ljust(20)
            compound_index = self.get_size_class_index(size_class)
            for assay_name in assay_names:
                result = result + str(
                    self.assays[assay_name][compound_index]).ljust(20)
            result = result + "\n"
        return result

    def _prepare_lines(self, lines):
        """
        Prepare the lines read from the text file before starting to process
        it.
        """

        result = list()
        for line in lines:
            # Remove all whitespace characters (e.g. spaces, line breaks, etc.)
            # from the start and end of the line.
            line = line.strip()
            # Replace all tabs with spaces.
            line = line.replace("\t", " ")
            # Replace all repeating spaces with a single space.
            while line.find("  ") > -1:
                line = line.replace("  ", " ")
            result.append(line)
        return result

    def get_size_class_index(self, size_class):
        """
        Determine the index of the specified size class.

        :param size_class: The formula and phase of the specified size class,
          e.g. 'Fe2O3[S1]'.

        :returns: The index of the specified size class.
        """

        return self.size_classes.index(size_class)

    def create_empty_assay(self):
        """
        Create an empty array to store an assay. The array's length will be
        equal to the number of size classes in the material.

        :returns: A floating point array.
        """

        return numpy.zeros(self.size_class_count)

    def add_assay(self, name, assay):
        """
        Add an assay to the material.

        :param name: The name of the new assay.
        :param assay: A numpy array containing the size class mass fractions
          for the assay. The sequence of the assay's elements must correspond
          to the sequence of the material's size classes.
        """

        if not type(assay) is numpy.ndarray:
            raise Exception("Invalid assay. It must be a numpy array.")
        elif not assay.shape == (self.size_class_count,):
            raise Exception(
                "Invalid assay: It must have the same number of elements "
                "as the material has size classes.")
        elif name in self.assays.keys():
            raise Exception(
                "Invalid assay: An assay with that name already exists.")
        self.assays[name] = assay

    def get_assay_total(self, name):
        """
        Calculate the total of the specified assay.

        :param name: The name of the assay.

        :returns: The total mass fraction of the specified assay.
        """

        return sum(self.assays[name])

    def create_package(self, assay=None, mass=0.0, normalise=True):
        """
        Create a MaterialPackage based on the specified parameters.

        :param assay: The name of the assay based on which the package must be
          created.
        :param mass: [kg] The mass of the package.
        :param normalise: Indicates whether the assay must be normalised before
          creating the package.

        :returns: The created MaterialPackage.
        """

        if assay is None:
            return MaterialPackage(self, self.create_empty_assay())

        if normalise:
            assay_total = self.get_assay_total(assay)
        else:
            assay_total = 1.0
        return MaterialPackage(self, mass * self.assays[assay] / assay_total)


class MaterialPackage(Object):
    """
    A package of a material consisting of multiple particle size classes.

    Properties defined here:

    :param material: A reference to the Material to which self belongs.
    :param size_class_masses: [kg] [kg] The masses of the size classes in the
          package.
    """

    def __init__(self, material, size_class_masses):
        # Confirm that the parameters are OK.
        if not type(material) is Material:
            raise TypeError(
                "Invalid material type. Must be psdmaterial.Material")
        if not type(size_class_masses) is numpy.ndarray:
            raise TypeError(
                "Invalid size_class_masses type. Must be numpy.ndarray.")

        # Initialise the object's properties.
        self.material = material
        self.size_class_masses = size_class_masses

    def __str__(self):
        """
        Create a string representation of the object.
        """

        result = "MaterialPackage\n"
        result = result + "material".ljust(20) + self.material.name + "\n"
        result = result + "mass".ljust(20) + str(self.get_mass()) + "\n"
        result = result + "Component masses:\n"
        for size_class in self.material.size_classes:
            index = self.material.get_size_class_index(size_class)
            result = result + str(size_class).ljust(20) + str(
                self.size_class_masses[index]) + "\n"
        return result

    # -------------------------------------------------------------------------
    # Operators.
    # -------------------------------------------------------------------------
    def __add__(self, other):
        """
        Addition operator (+).
        Add self and 'other' together, return the result as a new package, and
        leave self unchanged.

        :param other: Can can be one of the following:
          1. MaterialPackage: 'other' is added to self to create a new package.
          2. tuple: (size class, mass): The specified mass of the specified
          size class is added to self.

        :returns: A new Material package that is the sum of self and 'other'.
        """

        # Add another package.
        if type(other) is MaterialPackage:
            # Packages of the same material.
            if self.material == other.material:
                result = MaterialPackage(
                    self.material,
                    self.size_class_masses + other.size_class_masses)
                return result
            else:  # Packages of different materials.
                result = self.clone()
                for size_class in other.material.size_classes:
                    if size_class not in self.material.size_classes:
                        raise Exception(
                            "Packages of '" + other.material.name +
                            "' cannot be added to packages of '" +
                            self.material.name +
                            "'. The size class '" + size_class +
                            "' was not found in '" + self.material.name + "'.")
                    result = result + (
                        size_class,
                        other.get_size_class_mass(size_class))
                return result

        # Add the specified mass of the specified size class.
        elif self._is_size_class_mass_tuple(other):
            # Added material variables.
            size_class = other[0]
            compound_index = self.material.get_size_class_index(size_class)
            mass = other[1]

            # Create the result package.
            result = self.clone()
            result.size_class_masses[compound_index] = \
                result.size_class_masses[compound_index] + mass
            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid addition argument.")

    def __mul__(self, scalar):
        """
        The multiplication operator (*).
        Create a new package by multiplying self with other.

        :param scalar: The result is a new package with its content equal to
          self multiplied by a scalar, leaving self unchanged.

        :returns: A new MaterialPackage equal to self package multiplied by
          other.
        """

        # Multiply with a scalar floating point number.
        if type(scalar) is float or \
           type(scalar) is numpy.float64 or \
           type(scalar) is numpy.float32:
            if scalar < 0.0:
                raise Exception(
                    "Invalid multiplication operation. "
                    "Cannot multiply package with negative number.")
            result = MaterialPackage(
                self.material, self.size_class_masses * scalar)
            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid multiplication argument.")

    def _is_size_class_mass_tuple(self, value):
        """
        Determines whether value is a tuple of the format
        (size class(float), mass(float)).

        :param value: The value to check.

        :returns: Whether the value is a tuple in the required format.
        """

        if not type(value) is tuple:
            return False
        elif not len(value) == 2:
            return False
        elif not type(value[0]) is float:
            return False
        elif not type(value[1]) is float and \
                not type(value[1]) is numpy.float64 and \
                not type(value[1]) is numpy.float32:
            return False
        else:
            return True

    def clone(self):
        """
        Create a complete copy of self.

        :returns: A MaterialPackage that is identical to self.
        """

        result = copy.copy(self)
        result.size_class_masses = copy.deepcopy(self.size_class_masses)
        return result

    # TODO: test
    def clear(self):
        """
        Set all the size class masses in the package to zero.
        """

        self.size_class_masses = self.size_class_masses * 0.0

    def get_assay(self):
        """
        Determine the assay of self.

        :returns: [mass fractions] An array containing the assay of self.
        """

        return self.size_class_masses / self.size_class_masses.sum()

    def get_mass(self):
        """
        Determine the mass of self.

        returns: [kg] The mass of self.
        """

        return self.size_class_masses.sum()

    def get_size_class_mass(self, size_class):
        """
        Determine the mass of the specified size class in self.

        :param size_class: The formula and phase of the size class,
          e.g. 'Fe2O3[S1]'

        :returns: [kg] The mass of the size class in self.
        """

        return self.size_class_masses[self.material.get_size_class_index(
            size_class)]

    # TODO: Test
    def get_size_class_mass_fraction(self, size_class):
        """
        Determine the mass fraction of the specified size class in self.

        :param size_class: The formula and phase of the size class,
          e.g. 'Fe2O3[S1]'

        :returns: The mass fraction of the size class in self.
        """

        return self.get_size_class_mass(size_class) / self.get_mass()

    def extract(self, other):
        """
        Extract 'other' from self, modifying self and returning the extracted
        material as a new package.

        :param other: Can be one of the following:

          * float: A mass equal to other is extracted from self. Self is
            reduced by other and the extracted package is returned as a new
            package.
          * tuple (size class, mass): The other tuple specifies the mass
            of a size class to be extracted. It is extracted from self and
            the extracted mass is returned as a new package.
          * string: The 'other' string specifies the size class to be
            extracted. All of the mass of that size class will be removed
            from self and a new package created with it.


        :returns: A new material package containing the material that was
          extracted from self.
        """

        # Extract the specified mass.
        if type(other) is float or \
                type(other) is numpy.float64 or \
                type(other) is numpy.float32:
            if other > self.get_mass():
                raise Exception(
                    "Invalid extraction operation. "
                    "Cannot extract a mass larger than the package's mass.")
            fraction_to_subtract = other / self.get_mass()
            result = MaterialPackage(
                self.material, self.size_class_masses * fraction_to_subtract)
            self.size_class_masses = self.size_class_masses * (
                1.0 - fraction_to_subtract)
            return result

        # Extract the specified mass of the specified size class.
        elif self._is_size_class_mass_tuple(other):
            index = self.material.get_size_class_index(other[0])
            if other[1] > self.size_class_masses[index]:
                raise Exception(
                    "Invalid extraction operation. "
                    "Cannot extract a size class mass larger than what the "
                    "package contains.")
            self.size_class_masses[index] = \
                self.size_class_masses[index] - other[1]
            resultarray = self.size_class_masses*0.0
            resultarray[index] = other[1]
            result = MaterialPackage(self.material, resultarray)
            return result

        # Extract all of the specified size class.
        elif type(other) is str:
            index = self.material.get_size_class_index(float(other))
            result = self * 0.0
            result.size_class_masses[index] = self.size_class_masses[index]
            self.size_class_masses[index] = 0.0
            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid extraction argument.")

    # TODO: Test
    def add_to(self, other):
        """
        Add another psd material package to this material package.

        :param other: The other material package.
        """

        # Add another package.
        if type(other) is MaterialPackage:
            # Packages of the same material.
            if self.material == other.material:
                self.size_class_masses = \
                        self.size_class_masses + other.size_class_masses
            else:  # Packages of different materials.
                for size_class in other.material.size_classes:
                    if size_class not in self.material.size_classes:
                        raise Exception(
                            "Packages of '" + other.material.name +
                            "' cannot be added to packages of '" +
                            self.material.name +
                            "'. The size class '" + size_class +
                            "' was not found in '" + self.material.name + "'.")
                    self.add_to(
                        (size_class, other.get_size_class_mass(size_class)))

        # Add the specified mass of the specified size class.
        elif self._is_size_class_mass_tuple(other):
            # Added material variables.
            size_class = other[0]
            compound_index = self.material.get_size_class_index(size_class)
            mass = other[1]

            # Create the result package.
            self.size_class_masses[compound_index] = \
                self.size_class_masses[compound_index] + mass

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError("Invalid addition argument.")


def _get_default_data_path():
    module_path = os.path.dirname(sys.modules[__name__].__file__)
    data_path = os.path.join(module_path, r"data")
    data_path = os.path.abspath(data_path)
    return data_path

DEFAULT_DATA_PATH = _get_default_data_path()
