#!/usr/bin/env python3
"""
This module provides classes to work with materials and material packages that
are described with chemical compositions.
"""

import copy
from os.path import isfile

from auxi.core.objects import Object, NamedObject
from auxi.tools.chemistry.stoichiometry import element_mass_fractions as emf
from auxi.tools.chemistry import stoichiometry as stoich


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
    A material consisting of multiple chemical compounds.

    :param name: The material's name.
    :param file_path: The path of the material definition file.
    :param description: the material's description

    The format of the text file is as follows:

    * The lines are space separated. The values in a line are separated by \
      one or more spaces.
    * The first line is a heading line.
    * All subsequent lines contain a compound formula, followed by mass \
        fractions.
    * The first column lists the compounds in the material.
    * All subsequent columns describe assays of the material.

    The following is an example of a material text file::

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

    def __init__(self, name, file_path, description=None):
        self._validate_params_(name, file_path, description)
        super(Material, self).__init__(name, description)
        self._read_configuration_(file_path)

    def __str__(self):
        # TODO: Replace implementation with tabular.
        result = "Material: name='" + self.name + "'\n"

        # Create the header line of the table.
        result += 'Compound'.ljust(20)
        assay_names = sorted(self.assays.keys())
        for assay_name in assay_names:
            result += assay_name.ljust(20)
        result += '\n'

        # Create the content lines of the table.
        for compound in self.compounds:
            result += compound.ljust(20)
            compound_ix = self.get_compound_index(compound)
            for assay_name in assay_names:
                result += str(self.assays[assay_name][compound_ix]).ljust(20)
            result += '\n'
        return result

    def _validate_params_(self, name, file_path, description):
        super(Material, self)._validate_params_(name, description)

        if not isfile(file_path):
            raise ValueError('The specified file ({}) does not exist.'
                             .format(file_path))

    def _read_configuration_(self, file_path):
        self.compounds = []

        # Read the material's data from the file and prepare it for use.
        with open(file_path) as f:
            lines = f.readlines()
        lines = self._prepare_lines_(lines)

        # Determine assay names, and create a dictionary entry per assay.
        assay_names = lines[0].split(' ')
        del(assay_names[0:1])
        self.assays = dict()
        for assay_name in assay_names:
            self.assays[assay_name] = []

        # Read the compounds and assays.
        for i in range(1, len(lines)):
            strings = lines[i].split(' ')
            if len(strings) < len(assay_names) + 1:  # Not a full line.
                continue
            self.compounds.append(strings[0])  # Add the new compound.
            for j in range(0, len(self.assays)):  # Add mass fractions.
                assay_name = assay_names[j]
                self.assays[assay_name].append(float(strings[j+1]))
        self.compound_count = len(self.compounds)

        # Determine the list of elements.
        self.elements = self._create_element_list_()

    def _prepare_lines_(self, lines):
        """
        Prepare the lines read from the text file before starting to process
        it.
        """

        result = []
        for line in lines:
            # Remove all whitespace from the start and end of the line.
            line = line.strip()

            # Replace all tabs with spaces.
            line = line.replace('\t', ' ')

            # Replace all repeating spaces with a single space.
            while line.find('  ') > -1:
                line = line.replace('  ', ' ')

            result.append(line)

        return result

    def _create_element_list_(self):
        """
        Extract an alphabetically sorted list of elements from the compounds of
        the material.

        :returns: An alphabeticall sorted list of elements.
        """

        element_set = stoich.elements(self.compounds)
        return sorted(list(element_set))

    def get_compound_index(self, compound):
        """
        Determine the index of the specified compound.

        :param compound: The formula and phase of the specified compound, e.g.
          'Fe2O3[S1]'.

        :returns: The index of the specified compound.
        """

        return self.compounds.index(compound)

    def create_empty_assay(self):
        """
        Create an empty array to store an assay. The array's length will be
        equal to the number of compounds in the material.

        :returns: A floating point array.
        """

        return [0] * self.compound_count

    def add_assay(self, name, assay):
        """
        Add an assay to the material.

        :param name: The name of the new assay.
        :param assay: A list containing the compound mass fractions for
          the assay. The sequence of the assay's elements must correspond to
          the sequence of the material's compounds.
        """

        if not type(assay) is list:
            raise Exception('Invalid assay. It must be a list.')

        elif not len(assay) == self.compound_count:
            raise Exception('Invalid assay: It must have the same number of '
                            'elements as the material has compounds.')

        elif name in self.assays:
            raise Exception('Invalid assay: An assay with that name already '
                            'exists.')

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
        masses = [(mass * m) / assay_total for m in self.assays[assay]]
        return MaterialPackage(self, masses)


class MaterialPackage(Object):
    """
    A package of a material consisting of multiple chemical compounds.

    :param material: A reference to the Material to which self belongs.
    :param compound_masses: [kg] The masses of the compounds in the package.
    """

    def __init__(self, material, compound_masses):
        self._validate_params_(material, compound_masses)

        self.material = material
        self.compound_masses = compound_masses

    def __str__(self):
        result = 'MaterialPackage\n'
        result += 'material'.ljust(20) + self.material.name + '\n'
        result += 'mass'.ljust(20) + str(self.get_mass()) + '\n'
        result += 'Component masses:\n'
        for compound in self.material.compounds:
            index = self.material.get_compound_index(compound)
            result += compound.ljust(20) + str(self.compound_masses[index])
            result += '\n'
        return result

    def __add__(self, other):
        """
        Add self and 'other' together, return the result as a new package, and
        leave self unchanged.

        :param other: Can can be one of the following:
          1. MaterialPackage: 'other' is added to self to create a new package.
          2. tuple: (compound, mass): The specified mass of the specified
          compound is added to self.

        :returns: A new Material package that is the sum of self and 'other'.
        """

        # Add another package.
        if type(other) is MaterialPackage:
            # Packages of the same material.
            if self.material == other.material:
                result = MaterialPackage(
                    self.material,
                    self.compound_masses + other.compound_masses)
                return result
            else:  # Packages of different materials.
                result = self.clone()
                for compound in other.material.compounds:
                    if compound not in self.material.compounds:
                        raise Exception(
                            "Packages of '" + other.material.name +
                            "' cannot be added to packages of '" +
                            self.material.name +
                            "'. The compound '" + compound +
                            "' was not found in '" + self.material.name + "'.")
                    result += (compound, other.get_compound_mass(compound))
                return result

        # Add the specified mass of the specified compound.
        elif self._is_compound_mass_tuple(other):
            # Added material varialbes.
            compound = other[0]
            compound_index = self.material.get_compound_index(compound)
            mass = other[1]

            # Create the result package.
            result = self.clone()
            result.compound_masses[compound_index] += mass
            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError('Invalid addition argument.')

    def __mul__(self, scalar):
        """
        The multiplication operator (*).

        Create a new package by multiplying self with scalar.

        :param scalar: The result is a new package with its content equal to
          self multiplied by a scalar, leaving self unchanged.

        :returns: A new MaterialPackage equal to self package multiplied by
          other.
        """

        # Multiply with a scalar floating point number.
        if type(scalar) is float:
            if scalar < 0.0:
                raise Exception(
                    'Invalid multiplication operation. '
                    'Cannot multiply package with negative number.')
            result = MaterialPackage(
                self.material, [c * scalar for c in self.compound_masses])
            return result

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError('Invalid multiplication argument.')

    def _validate_params_(self, material, compound_masses):
        if not type(material) is Material:
            raise TypeError('Invalid material type. Must be '
                            'chemistry.material.Material')
        if not type(compound_masses) is list:
            raise TypeError('Invalid compound_masses type. Must be '
                            'list.')

    def _is_compound_mass_tuple(self, value):
        """
        Determines whether value is a tuple of the format (compound(str),
        mass(float)).
        """

        if not type(value) is tuple:
            return False
        elif not len(value) == 2:
            return False
        elif not type(value[0]) is str:
            return False
        elif not type(value[1]) is float:
            return False
        else:
            return True

    def clone(self):
        """
        Create a complete copy of self.

        :returns: A MaterialPackage that is identical to self.
        """

        result = copy.copy(self)
        result.compound_masses = copy.deepcopy(self.compound_masses)

        return result

    # TODO: test
    def clear(self):
        """
        Set all the compound masses in the package to zero.
        """

        self.compound_masses *= 0.0

    def get_assay(self):
        """
        Determine the assay of self.

        :returns: [mass fractions] An array containing the assay of self.
        """

        masses_sum = sum(self.compound_masses)
        return [m / masses_sum for m in self.compound_masses]

    def get_mass(self):
        """
        Get the mass of the package.

        :returns: [kg]
        """

        return sum(self.compound_masses)

    def get_compound_mass(self, compound):
        """
        Get the mass of the specified compound in the package.

        :param compound: The formula of the compound, e.g. Fe2O3.

        :returns: [kg]
        """

        return self.compound_masses[self.material.get_compound_index(compound)]

    # TODO: Test
    def get_compound_mass_fraction(self, compound):
        """
        Get the mass fraction of the specified compound in self.

        :param compound: The formula and phase of the compound, e.g. Fe2O3.

        :returns: []
        """

        return self.get_compound_mass(compound) / self.get_mass()

    def get_element_masses(self):
        """
        Get the masses of elements in the package.

        :returns: [kg] An array of element masses. The sequence of the elements
          in the result corresponds with the sequence of elements in the
          element list of the material.
        """

        result = [0] * len(self.material.elements)
        for compound in self.material.compounds:
            c = self.get_compound_mass(compound)
            f = [c * x for x in emf(compound, self.material.elements)]
            result = [v+f[ix] for ix, v in enumerate(result)]

        return result

    def get_element_mass_dictionary(self):
        """
        Determine the masses of elements in the package and return as a
        dictionary.

        :returns: [kg] A dictionary of element symbols and masses.
        """

        element_symbols = self.material.elements
        element_masses = self.get_element_masses()

        result = {}
        for s, m in zip(element_symbols, element_masses):
            result[s] = m

        return result

    def get_element_mass(self, element):
        """
        Determine the masses of elements in the package.

        :returns: [kg] An array of element masses. The sequence of the elements
          in the result corresponds with the sequence of elements in the
          element list of the material.
        """

        result = [0]
        for compound in self.material.compounds:
            c = self.get_compound_mass(compound)
            f = [c * x for x in emf(compound, [element])]
            result = [v+f[ix] for ix, v in enumerate(result)]

        return result[0]

    def extract(self, other):
        """
        Extract 'other' from self, modifying self and returning the extracted
        material as a new package.

        :param other: Can be one of the following:

          * float: A mass equal to other is extracted from self. Self is
            reduced by other and the extracted package is returned as a
            new package.
          * tuple (compound, mass): The other tuple specifies the mass of
            a compound to be extracted. It is extracted from self and the
            extracted mass is returned as a new package.
          * string: The 'other' string specifies the compound to be extracted.
            All of the mass of that compound will be removed from self and a
            new package created with it.


        :returns: A new material package containing the material that was
          extracted from self.
        """

        # Extract the specified mass.
        if type(other) is float:

            if other > self.get_mass():
                raise Exception('Invalid extraction operation. Cannot extract'
                                'a mass larger than the package\'s mass.')

            fraction_to_subtract = other / self.get_mass()
            result = MaterialPackage(
                self.material,
                [m * fraction_to_subtract for m in self.compound_masses])
            self.compound_masses = [m * (1.0 - fraction_to_subtract)
                                    for m in self.compound_masses]

            return result

        # Extract the specified mass of the specified compound.
        elif self._is_compound_mass_tuple(other):
            index = self.material.get_compound_index(other[0])

            if other[1] > self.compound_masses[index]:
                raise Exception('Invalid extraction operation. Cannot extract'
                                'a compound mass larger than what the package'
                                'contains.')

            self.compound_masses[index] -= other[1]
            resultarray = [0.0] * len(self.compound_masses)
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
            raise TypeError('Invalid extraction argument.')

    # TODO: Test
    def add_to(self, other):
        """
        Add another chem material package to this material package.

        :param other: The other material package.
        """

        # Add another package.
        if type(other) is MaterialPackage:

            # Packages of the same material.
            if self.material == other.material:
                self.compound_masses += other.compound_masses

            # Packages of different materials.
            else:
                for compound in other.material.compounds:
                    if compound not in self.material.compounds:
                        raise Exception("Packages of '" + other.material.name +
                                        "' cannot be added to packages of '" +
                                        self.material.name +
                                        "'. The compound '" + compound +
                                        "' was not found in '" +
                                        self.material.name + "'.")
                    self.add_to((compound, other.get_compound_mass(compound)))

        # Add the specified mass of the specified compound.
        elif self._is_compound_mass_tuple(other):
            # Added material varialbes.
            compound = other[0]
            compound_index = self.material.get_compound_index(compound)
            mass = other[1]

            # Create the result package.
            self.compound_masses[compound_index] += mass

        # If not one of the above, it must be an invalid argument.
        else:
            raise TypeError('Invalid addition argument.')

if __name__ == "__main__":
    import unittest
    from auxi.modelling.process.materials.chem_test \
        import ChemMaterialUnitTester, ChemMaterialPackageUnitTester
    unittest.main()
