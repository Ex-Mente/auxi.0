#!/usr/bin/env python3
"""
This module provides material and material package classes that can do
size distribution and slurry calculations.
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


# TODO: Johan, I replaced 'self.psds' with 'self.assays'
#   to match the psd.py module.


class Material(NamedObject):
    """
    Represents a particulate material consisting of multiple particle size
    classes.

    :param name: The material's name.
    :param file_path: The path of the material definition file.
    :param description: the material's description

    The format of the text file is as follows:

    * The lines are space separated. The values in a line are separated by \
      one or more spaces.
    * The first line is a heading line.
    * The second line contains the density of the solid material.
    * The third line contains the water fraction of the slurry (wet basis).
    * All subsequent lines contain a particle size, followed by mass \
      fractions (dry basis).
    * Particle sizes are indicated in [meter].
    * The first column lists the particle sizes in the material. Each class \
      must be interpreted as "mass fraction retained". In other words if the \
      size class is indicated as 307.2E-3, it means that it is the class of \
      material retained on a 307.2mm screen, and can also be though of as \
      +307.2mm material. The first size class represents the largest \
      particles. The final size class should be zero, as it represents \
      all material that passed through the smallest aperture screen.
    * All subsequent columns describe assays of the material.

    The following is an example of a material text file::

        SizeClass       DryFeedA  DryMillCharge  WetFeedA  WetMillCharge  Water
        solid_density   3.00      3.00           3.00      3.00           1.0.
        H2O             0.00      0.00           0.80      0.60           1.00
        307.2E-3        0.20      0.02           0.20      0.02           0.00
        108.6E-3        0.18      0.06           0.18      0.06           0.00
        38.4E-3         0.17      0.04           0.17      0.04           0.00
        13.6E-3         0.07      0.03           0.07      0.03           0.00
        4.8E-3          0.13      0.03           0.13      0.03           0.00
        1.7E-3          0.07      0.04           0.07      0.04           0.00
        600.0E-6        0.06      0.18           0.06      0.18           0.00
        210.0E-6        0.02      0.50           0.02      0.50           0.00
        75.0E-6         0.10      0.09           0.10      0.09           0.00
        0.0E0           0.00      0.00           0.00      0.00           0.00
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

        # Determine the assay names, and create a dictionary entry
        # for each assay.
        assay_names = lines[0].split(" ")
        del(assay_names[0:1])
        self.assays = dict()
        self.solid_densities = dict()
        self.H2O_fractions = dict()
        for assay_name in assay_names:
            self.assays[assay_name] = numpy.array([])
            self.solid_densities[assay_name] = 1.0
            self.H2O_fractions[assay_name] = 0.0

        # Read the solid densities of the assays.
        strings = lines[1].split(" ")
        if not strings[0] == "solid_density":
            raise Exception(
                "Invalid data file. "
                "The second line of the data file must start with"
                "'solid_density'.")
        # Add the solid densities.
        for j in range(0, len(self.solid_densities)):
            assay_name = assay_names[j]
            self.solid_densities[assay_name] = float(strings[j+1])

        # Read the water fractions of the assays.
        strings = lines[2].split(" ")
        if not strings[0] == "H2O":
            raise Exception(
                "Invalid data file. "
                "The third line of the data file must start with 'H2O'.")
        # Add the water fractions.
        for j in range(0, len(self.H2O_fractions)):
            assay_name = assay_names[j]
            self.H2O_fractions[assay_name] = float(strings[j+1])

        # Read the size classes and mass fractions.
        for i in range(3, len(lines)):
            strings = lines[i].split(" ")
            # Not a full line.
            if len(strings) < len(assay_names) + 1:
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

        # Create the solid density line.
        result = result + "Solid density".ljust(20)
        assay_names = sorted(self.assays.keys())
        for assay_name in assay_names:
            result = result + str(self.solid_densities[assay_name]).ljust(20)
        result = result + "\n"

        # Create the H2O fraction line.
        result = result + "H2O fraction".ljust(20)
        assay_names = sorted(self.assays.keys())
        for assay_name in assay_names:
            result = result + str(self.H2O_fractions[assay_name]).ljust(20)
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

    '''
    # TODO: Johan I replaced this method with the method above.
    def create_empty_psd(self):
        """
        Create an empty array to store a psd. The array's length will be equal
        to the number of size classes in the material.

        :returns: A floating point array.
        """

        return numpy.zeros(self.size_class_count)
    '''

    def add_assay(self, name, solid_density, H2O_fraction, assay):
        """Add an assay to the material.

        :param name: The name of the new assay.
        :param assay: A numpy array containing the size class mass fractions
          for the assay. The sequence of the assay's elements must correspond
          to the sequence of the material's size classes.
        """

        if not type(solid_density) is float:
            raise Exception("Invalid solid density. It must be a float.")
        self.solid_densities[name] = solid_density

        if not type(H2O_fraction) is float:
            raise Exception("Invalid H2O fraction. It must be a float.")
        self.H2O_fractions[name] = H2O_fraction

        if not type(assay) is numpy.ndarray:
            raise Exception("Invalid assay. It must be a numpy array.")
        elif not assay.shape == (self.size_class_count,):
            raise Exception(
                "Invalid assay: It must have the same number of elements as "
                "the material has size classes.")
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

    '''
    # TODO: Johan I replaced this method with the method above.
    def get_psd_total(self, name):
        """Calculate the total of the specified assay's psd.
        :param name: The name of the assay.

        :returns: The total mass fraction of the specified assay.
        """

        return sum(self.assays[name])
    '''

    def create_package(self, assay=None, mass=0.0, normalise=True):
        """
        Create a MaterialPackage based on the specified parameters.

        :param assay: The name of the assay based on which the package
          must be created.
        :param mass: [kg] The mass of the package.
        :param normalise: Indicates whether the assay must be normalised
          before creating the package.

        :returns: The created MaterialPackage.
        """

        if assay is None:
            return MaterialPackage(self, 1.0, 0.0, self.create_empty_assay())

        if normalise:
            assay_total = self.get_assay_total(assay)
            if assay_total == 0.0:
                assay_total = 1.0
        else:
            assay_total = 1.0
        H2O_mass = mass * self.H2O_fractions[assay]
        solid_mass = mass - H2O_mass
        return MaterialPackage(self,
                               self.solid_densities[assay],
                               H2O_mass,
                               solid_mass * self.assays[assay] / assay_total)


class MaterialPackage(Object):
    """
    A package of a slurry material consisting of multiple particle size
    classes.

    :param material: A reference to the Material to which self belongs.
    :param size_class_masses: [kg] [kg] The masses of the size classes in the
          package.
    """

    def __init__(self, material, solid_density, H2O_mass, size_class_masses):
        # Confirm that the parameters are OK.
        if not type(material) is Material:
            raise TypeError(
                "Invalid material type. Must be psdslurrymaterial.Material")
        if not type(size_class_masses) is numpy.ndarray:
            raise TypeError(
                "Invalid size_class_masses type. Must be numpy.ndarray.")

        # Initialise the object's properties.
        self.material = material
        self.solid_density = solid_density
        self.H2O_mass = H2O_mass
        self.size_class_masses = size_class_masses

    def __str__(self):
        """
        Create a string representation of the object.
        """

        result = "MaterialPackage\n"
        result = result + "material".ljust(24) + self.material.name + "\n"
        result = result + "mass fraction solids".ljust(24) + \
            str(self.get_mass_fraction_solids()) + "\n"
        result = result + "volume fraction solids".ljust(24) + \
            str(self.get_volume_fraction_solids()) + "\n"
        result = result + "solid density".ljust(24) + \
            str(self.solid_density) + "\n"
        result = result + "slurry density".ljust(24) + \
            str(self.get_density()) + "\n"
        result = result + "mass".ljust(24) + str(self.get_mass()) + "\n"
        result = result + "H2O mass".ljust(24) + str(self.H2O_mass) + "\n"
        result = result + "volume".ljust(24) + str(self.get_volume()) + "\n"
        result = result + "Component masses:\n"
        for size_class in self.material.size_classes:
            index = self.material.get_size_class_index(size_class)
            result = result + str(size_class).ljust(24) + str(
                self.size_class_masses[index]) + "\n"
        return result

    def __add__(self, other):
        """
        Addition operator (+).
        Add self and 'other' together, return the result as a new package,
        and leave self unchanged.

        :param other: Can can be one of the following:
          1. MaterialPackage: 'other' is added to self to create a new package.
          2. tuple: (size class, mass) The specified mass of the specified size
          class is added to self.

        :returns: A new Material package that is the sum of self and 'other'.
        """

        # Add another package.
        if type(other) is MaterialPackage:
            solid_mass = self.get_solid_mass()
            other_solid_mass = other.get_solid_mass()
            solid_density = (solid_mass + other_solid_mass) / \
                (solid_mass / self.solid_density +
                    other_solid_mass / other.solid_density)
            H2O_mass = self.H2O_mass + other.H2O_mass
            # Packages of the same material.
            if self.material == other.material:
                result = MaterialPackage(
                    self.material,
                    solid_density,
                    H2O_mass,
                    self.size_class_masses + other.size_class_masses)
                return result
            else:  # Packages of different materials.
                result = self.clone()
                result.solid_density = solid_density
                result.H2O_mass = H2O_mass
                for size_class in other.material.size_classes:
                    if size_class not in self.material.size_classes:
                        raise Exception(
                            "Packages of '" + other.material.name +
                            "' cannot be added to packages of '" +
                            self.material.name + "'. The size class '" +
                            size_class + "' was not found in '" +
                            self.material.name + "'.")
                    result = result + (
                        size_class, other.get_size_class_mass(size_class))
                return result

        # Add the specified mass of water.
        elif self._is_H2O_mass_tuple(other):
            # Added material variables.
            mass = other[1]

            # Create the result package.
            result = self.clone()
            result.H2O_mass += mass
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
                self.material,
                self.solid_density,
                self.H2O_mass * scalar, self.size_class_masses * scalar)
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

    def _is_H2O_mass_tuple(self, value):
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
        elif not type(value[0]) is str and not value[0] == "H2O":
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

    def clear(self):
        """
        Set all the size class masses and H20_mass in the package to zero
        and the solid_density to 1.0
        """

        self.solid_density = 1.0
        self.H2O_mass = 0.0
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

        :returns: [kg] The mass of self.
        """

        return self.size_class_masses.sum() + self.H2O_mass

    def get_solid_mass(self):
        """
        Determine the solid mass of self.

        :returns: [kg] The solid mass of self.
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
          e.g. Fe2O3[S1]

        :returns: The mass fraction of the size class in self.
        """

        return self.get_size_class_mass(size_class) / self.get_solid_mass()

    def get_density(self):
        """
        Determine the density of self.
        """

        return self.get_mass() / self.get_volume()

    def get_mass_fraction_solids(self):
        """
        Determine the mass fraction of the solids of self.
        """

        return self.get_solid_mass() / self.get_mass()

    def get_volume(self):
        """
        Determine the volume of self.
        """

        return self.H2O_mass / 1.0 + self.get_solid_mass() / self.solid_density

    def get_volume_fraction_solids(self):
        """
        Determine the volume fraction of the solids of self.
        """

        return 1.0 - (self.H2O_mass / 1.0) / self.get_volume()

    def extract(self, other):
        """
        Extract 'other' from self, modifying self and returning the extracted
        material as a new package.

        :param other: Can be one of the following:

          * float: A mass equal to other is extracted from self. Self is
            reduced by other and the extracted package is returned as a new
            package.
          * tuple (size class, mass): The other tuple specifies the mass of a
            size class to be extracted. It is extracted from self and the
            extracted mass is returned as a new package.
          * string: The 'other' string specifies the size class to be
            extracted. All of the mass of that size class will be removed from
            self and a new package created with it.


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
                self.material,
                self.solid_density,
                self.H2O_mass * fraction_to_subtract,
                self.size_class_masses * fraction_to_subtract)
            self.H2O_mass = self.H2O_mass * (1.0 - fraction_to_subtract)
            self.size_class_masses = \
                self.size_class_masses * (1.0 - fraction_to_subtract)
            return result

        # Extract the specified mass of water.
        elif self._is_H2O_mass_tuple(other):
            if other[1] > self.H2O_mass:
                raise Exception(
                    "Invalid extraction operation. "
                    "Cannot extract a water mass larger than what the package "
                    "contains.")
            self.H2O_mass = self.H2O_mass - other[1]
            resultarray = self.size_class_masses * 0.0
            result = MaterialPackage(
                self.material, self.solid_density, other[1], resultarray)
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
            result = MaterialPackage(
                self.material, self.solid_density, 0.0, resultarray)
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
    # TODO: Document
#    def add_to(self, other):
#        # Add another package.
#        if type(other) is MaterialPackage:
#            # Packages of the same material.
#            if self.material == other.material:
#                self.size_class_masses = \
#                   self.size_class_masses + other.size_class_masses
#            else: # Packages of different materials.
#                for size_class in other.material.size_classes:
#                    if size_class not in self.material.size_classes:
#                        raise Exception(
#                           "Packages of '" + other.material.name +
#                           "' cannot be added to packages of '" +
#                           self.material.name + "'. The size class '" +
#                           size_class + "' was not found in '" +
#                           self.material.name + "'.")
#                    self.add_to(
#                        (size_class, other.get_size_class_mass(size_class)))
#
#        # Add the specified mass of the specified size class.
#        elif self._is_size_class_mass_tuple(other):
#            # Added material variables.
#            size_class = other[0]
#            compound_index = self.material.get_size_class_index(size_class)
#            mass = other[1]
#
#            # Create the result package.
#            self.size_class_masses[compound_index] = \
#                self.size_class_masses[compound_index] + mass
#
#        # If not one of the above, it must be an invalid argument.
#        else:
#            raise TypeError("Invalid addition argument.")


def _get_default_data_path():
    module_path = os.path.dirname(sys.modules[__name__].__file__)
    data_path = os.path.join(module_path, r"data")
    data_path = os.path.abspath(data_path)
    return data_path

DEFAULT_DATA_PATH = _get_default_data_path()
