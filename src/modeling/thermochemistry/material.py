# -*- coding: utf-8 -*-
"""
This module provides a material class that can do thermochemical calculations.
"""
__version__ = "0.2.0"


import os
import sys
import numpy
from auxi.core.namedobject import NamedObject
from auxi.modeling.thermochemistry.materialpackage import MaterialPackage
from auxi.tools.chemistry import stoichiometry as stoich


class Material(NamedObject):
    """Represents a material consisting of multiple chemical compounds, having
    the ability to do thermochemical calculations.

    :param name: A name for the material.
    :param file_path: The location of the file containing the material's data.

    The format of the text file is as follows:
        * The items in a line are separated by one or more spaces or tabs.
        * The first line is a heading line. It contains the word "Compound" \
        followed by zero or more assay names.
        * Subsequent lines contain a compound formula and phase, followed by \
        a mass fraction for each assay.
        * The list of compounds and mass fractions can be ended off with a \
        "#" character. This indicates that custom material properties follow \
        below in the lines below the hash.
        * If a custom material property is defined, a value must be \
        provided for each assay name. A price custom property is used as an \
        example below.

    The following is an example of a material text file::

        Compound   IlmeniteA  IlmeniteB  IlmeniteC
        Al2O3[S1]  0.01160    0.01550    0.00941
        CaO[S]     0.00022    0.00001    0.00017
        Cr2O3[S]   0.00008    0.00022    0.00011
        Fe2O3[S1]  0.20200    0.47300    0.49674
        Fe3O4[S1]  0.00000    0.00000    0.00000
        FeO[S1]    0.27900    0.19100    0.00000
        K2O[S]     0.00004    0.00001    0.00005
        MgO[S]     0.01040    0.00580    0.01090
        MnO[S]     0.00540    0.00480    0.00525
        Na2O[S1]   0.00007    0.00005    0.00031
        P4O10[S]   0.00001    0.00032    0.00015
        SiO2[S1]   0.00850    0.00490    0.01744
        TiO2[S1]   0.47700    0.29400    0.45949
        V2O5[S]    0.00360    0.00800    0.00000
        #
        Price[USD/kg]  1.2        1.3        1.1
    """

    # -------------------------------------------------------------------------
    # Standard methods.
    # -------------------------------------------------------------------------
    def __init__(self, name, file_path):
        # Initialise the material's properties.
        self.name = name
        """The material's name."""

        self.compounds = list()
        """The material's list of chemical compounds."""

        # Read the material's data from the file and prepare it for use.
        f = open(file_path, "r")
        lines = f.readlines()
        f.close()
        lines = self._prepare_lines(lines)

        # Determine the assay names, and create a dictionary entry for each
        # assay.
        assay_names = lines[0].split(" ")
        del(assay_names[0:1])
        self.raw_assays = {}
        """A dictionary containing raw assays for this material."""
        self.converted_assays = {}
        """A dictionary containing converted assays for this material."""

        for assay_name in assay_names:
            self.raw_assays[assay_name] = numpy.array([])
            self.converted_assays[assay_name] = numpy.array([])

        # Read the compounds and assays.
        must_read_custom_properties = False
        for i in range(1, len(lines)):
            if lines[i].startswith("#"):
                must_read_custom_properties = True
                break
            strings = lines[i].split(" ")
            if len(strings) < len(assay_names) + 1:  # Not a full line.
                continue

            # Add the new compound.
            self.compounds.append(strings[0])

            # Add the mass fractions to the assays.
            for j in range(0, len(self.raw_assays)):
                assay_name = assay_names[j]
                self.raw_assays[assay_name] = numpy.append(self.raw_assays[assay_name],
                                                       float(strings[j+1]))
                self.converted_assays[assay_name] = numpy.append(self.converted_assays[assay_name],
                                                       float(strings[j+1]))

        # Read the custom properties.
        self.assay_custom_properties = dict()
        for j in range(0, len(self.raw_assays)):
            assay_name = assay_names[j]
            self.assay_custom_properties[assay_name] = dict()
        self.custom_properties = []
        if must_read_custom_properties:
            for i in range(i+1, len(lines)):
                strings = lines[i].split(" ")
                for j in range(0, len(self.raw_assays)):
                    assay_name = assay_names[j]
                    property_name = strings[0]
                    self.custom_properties.append(property_name)
                    property_dictionary = self.assay_custom_properties[assay_name]
                    property_dictionary[property_name] = float(strings[j+1])

        # Initialise the remaining properties.
        self.compound_count = len(self.compounds)
        """The number of chemical compounds in the material."""

        self.elements = self._create_element_list()

    def __str__(self):
        if len(self.raw_assays) > 0:
            line_length = 20 + (3 + 14) * len(self.raw_assays) - 2
        else:
            line_length = 20 + len(self.name)
        result = "=" * line_length + "\n"
        result += "Material\n"
        result += "=" * line_length + "\n"
        result += "Name".ljust(20) + self.name + "\n"

        # Create the header line of the table.
        result += "-" * line_length + "\n"
        if len(self.raw_assays) > 0:
            result = result + "Composition Details (mass fractions)\n"
        result += "Compound".ljust(20)
        assay_names = sorted(self.raw_assays.keys())
        pad = ''
        for assay_name in assay_names:
            result += pad + assay_name[0:15].ljust(15)
            pad = '  '
        result += "\n"
        result += "-" * line_length + "\n"

        # Create the content lines of the table.
        for compound in sorted(self.compounds):
            result = result + compound.ljust(20)
            compound_index = self.get_compound_index(compound)
            pad = ''
            for assay_name in assay_names:
                result += pad + '{:.8e}'.format(self.raw_assays[assay_name][compound_index]).rjust(15)
                pad = '  '
            result = result + "\n"

        # Write the total.
        result += "Total".ljust(20)
        pad = ''
        for assay_name in assay_names:
            total = 0.0
            for compound in sorted(self.compounds):
                compound_index = self.get_compound_index(compound)
                total += self.raw_assays[assay_name][compound_index]
            result += pad + '{:.8e}'.format(total).rjust(15)
            pad = '  '
        result = result + "\n"

        # Write the custom properties.
        if len(self.custom_properties) > 0:
            result += "-" * line_length + "\n"
            result += "Custom Properties:\n"
            result += "-" * line_length + "\n"
            first_assay = list(sorted(self.assay_custom_properties.keys()))[0]
            properties = list(sorted(self.assay_custom_properties[first_assay].keys()))
            for prop in properties:
                pad = ''
                result += prop.ljust(20)
                for assay_name in assay_names:
                    result += pad + "{:.8e}".format(self.assay_custom_properties[assay_name][prop]).rjust(15)
                    pad = '  '
                result += "\n"
        result += "=" * line_length + "\n"

        return result

    # -------------------------------------------------------------------------
    # Private methods.
    # -------------------------------------------------------------------------
    def _prepare_lines(self, lines):
        """Prepare the lines read from the text file before starting to
        process it.

        :param lines: The lines to prepare."""

        result = list()

        for line in lines:
            # Remove all whitespace from the start and end of the line.
            line = line.strip()

            # Replace all tabs with spaces.
            line = line.replace("\t", " ")

            # Replace all repeating spaces with a single space.
            while line.find("  ") > -1:
                line = line.replace("  ", " ")

            result.append(line)

        return result

    def _create_element_list(self):
        """Extract an alphabetically sorted list of elements from the
        material's compounds.

        :returns: Alphabetically sorted list of elements."""

        element_set = stoich.elements(self.compounds)
        return sorted(list(element_set))

    # -------------------------------------------------------------------------
    # Public methods.
    # -------------------------------------------------------------------------
    def get_compound_index(self, compound):
        """Determine the specified compound's index.

        :param compound: Formula and phase of a compound, e.g. "Fe2O3[S1]".

        :returns: Compound index."""

        return self.compounds.index(compound)

    def create_empty_assay(self):
        """Create an empty array to store an assay.

        The array's length will be equal to the number of compounds in the
        material.

        :returns: Empty assay array.
        """

        return numpy.zeros(self.compound_count)

    def add_assay(self, name, assay):
        """Add an assay to the material.

        :param name:  Assay name.
        :param assay: Numpy array containing the compound mass fractions for \
        the assay. The sequence of the assay's elements must correspond to \
        the sequence of the material's compounds.
        """

        if not type(assay) is numpy.ndarray:
            raise Exception("Invalid assay. It must be a numpy array.")
        elif not assay.shape == (self.compound_count,):
            raise Exception("Invalid assay: It must have the same number of "
                            "elements as the material has compounds.")
        elif name in self.raw_assays.keys():
            raise Exception("Invalid assay: An assay with that name already "
                            "exists.")
        self.raw_assays[name] = assay

    def get_assay_total(self, name):
        """Calculate the total/sum of the specified assay's mass fractions.

        :param name: Assay name.

        :returns: Total mass fraction."""

        return sum(self.converted_assays[name])

    def create_package(self, assay=None, mass=0.0, P=1.0, T=25.0,
                       normalise=True):
        """Create a MaterialPackage based on the specified parameters.

        :param assay:     Name of the assay to be used to create the package.
        :param mass:      Package mass. [kg]
        :param P:         Package pressure. [atm]
        :param T:         Package temperature. [°C]
        :param normalise: Indicates whether the assay must be normalised \
        before creating the package.

        :returns: MaterialPackage object."""

        if assay is None:
            return MaterialPackage(self, self.create_empty_assay(), P, T)

        if normalise:
            assay_total = self.get_assay_total(assay)
        else:
            assay_total = 1.0

        return MaterialPackage(self, mass * self.converted_assays[assay] / assay_total,
                               P, T)


class AssayConversionAction(object):
    def run(self, material):
        pass


class Normalise(AssayConversionAction):
    def run(self, material):
        pass


def _get_default_data_path():
    module_path = os.path.dirname(sys.modules[__name__].__file__)
    data_path = os.path.join(module_path, r"data")
    data_path = os.path.abspath(data_path)
    return data_path

DEFAULT_DATA_PATH = _get_default_data_path()
