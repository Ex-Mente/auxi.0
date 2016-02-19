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


def _get_default_data_path():
    module_path = os.path.dirname(sys.modules[__name__].__file__)
    data_path = os.path.join(module_path, r"../data")
    data_path = os.path.abspath(data_path)
    return data_path

DEFAULT_DATA_PATH = _get_default_data_path()
