#!/usr/bin/env python3
"""
This module provides tools for calculating material physical properties.
"""


import csv
import os
import pandas as pd
import webbrowser
from cerberus import Validator, ValidationError
from enum import Enum

from auxi.core.objects import Object


__version__ = '0.3.0'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Marno Grewar, Christoff Kok, Johan Zietsman'
__credits__ = ['Marno Grewar', 'Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Johan Zietsman'
__email__ = 'johan.zietsman@ex-mente.co.za'
__status__ = 'Planning'


class StateOfMatter(Enum):
    unknown = 0
    solid = 1
    liquid = 2
    solid_liquid = solid | liquid
    gas = 4
    solid_gas = solid | gas
    solid_liquid_gas = solid | liquid | gas
    plasma = 8
    solid_plasma = solid | plasma
    solid_liquid_plasma = solid | liquid | plasma
    solid_liquid_gas_plasma = solid | liquid | gas | plasma
    liquid_plasma = liquid | plasma
    liquid_gas_plasma = liquid | gas | plasma
    gas_plasma = gas | plasma


class DataSet(object):
    """
    Contains a data set used to create and/or test a material physical property
    model.

    :param csvfilepath: path to the csv file that contains the data
    """

    def create_template(material, path, show=False):
        """
        Create a template csv file for a data set.

        :param material: the name of the material
        :param path: the path of the directory where the file must be written
        :param show: a boolean indicating whether the created file should be \
        displayed after creation
        """
        file_name = 'dataset-%s.csv' % material.lower()
        file_path = os.path.join(path, file_name)

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Name', material])
            writer.writerow(['Description', '<Add a data set description '
                                            'here.>'])
            writer.writerow(['Reference', '<Add a reference to the source of '
                                          'the data set here.>'])
            writer.writerow(['Temperature', '<parameter 1 name>',
                            '<parameter 2 name>', '<parameter 3 name>'])
            writer.writerow(['T', '<parameter 1 display symbol>',
                             '<parameter 2 display symbol>',
                             '<parameter 3 display symbol>'])
            writer.writerow(['K', '<parameter 1 units>',
                             '<parameter 2 units>', '<parameter 3 units>'])
            writer.writerow(['T', '<parameter 1 symbol>',
                             '<parameter 2 symbol>', '<parameter 3 symbol>'])
            for i in range(10):
                writer.writerow([100.0 + i*50, float(i), 10.0 + i, 100.0 + i])

        if show is True:
            webbrowser.open_new(file_path)

    def __init__(self, csvfilepath):
        self._file_path = csvfilepath
        self._read_header_information()
        self._read_data()

    def __str__(self):
        result = 'Material:         %s\n' % self.material
        result += 'Description:      %s\n' % self.description
        result += 'References:       %s\n' % self.reference
        result += 'Properties:       %s\n' % self.col_names
        result += 'Symbols:          %s\n' % self.col_symbols
        result += 'Display symbols:  %s\n' % self.col_display_symbols
        result += 'Units:            %s\n' % self.col_units
        result += 'Data:\n'
        result += str(self.data)

        return result

    def _read_header_information(self):
        with open(self._file_path, newline='') as file:
            lines = csv.reader(file, delimiter=',', quotechar='"')

            self.name = os.path.basename(self._file_path)
            """The name of the data set."""

            self.material = next(lines)[1]
            """The name of the material represented by the data set."""

            self.description = next(lines)[1]
            """A description of the data set."""

            self.reference = next(lines)[1]
            """A reference to the source of the data set."""

            self.col_names = next(lines)
            """A list of data set column names."""

            self.col_display_symbols = next(lines)
            """A list of data set column display symbols."""

            self.col_units = next(lines)
            """A list of data set column units."""

            self.col_symbols = next(lines)
            """A list of data set column symbols."""

            self.names_dict = dict(zip(self.col_symbols, self.col_names))
            """A dictionary to translate a parameter's symbol to its name."""

            self.display_symbols_dict = dict(zip(self.col_symbols,
                                                 self.col_display_symbols))
            """
            A dictionary to translate a parameter's symbol to its display
            symbol.
            """

            self.units_dict = dict(zip(self.col_symbols, self.col_units))
            """A dictionary to translate a parameter's symbol to its units."""

    def _read_data(self):
        self.data = pd.read_csv(self._file_path, header=6)


class Model(Object):
    """
    Base class of models that describe the variation of a specific material
    physical property.

    :param material: the name of the material being described, e.g. "Air"
    :param proprty: the name of the property being described, e.g. "density"
    :param symbol: the symbol of the property being described, e.g. "rho"
    :param display symbol: the display symbol of the property being described,\
    e.g. "\rho"
    :param units: the units used to express the property, e.g. "kg/m3"
    :param references: a list of literature references on which this model\
    implementation is based, e.g. ['lienhard2015', 'smith2006']
    :param datasets: a list of data sets on which this model implementation is\
    based, e.g. ['dataset-air-lienhard2015.csv']
    """

    def __init__(self, material, proprty, symbol, display_symbol, units,
                 state_schema, references, datasets):
        self.material = material
        self.property = proprty
        self.symbol = symbol
        self.display_symbol = display_symbol
        self.units = units
        self.references = references
        self.datasets = datasets
        self.state_schema = state_schema
        self._create_validator(self.state_schema)

    def __call__(self, **state):
        """
        For details about this method, please refer to the calculate method.
        """
        return self.calculate(**state)

    def _create_validator(self, state_schema):
        self.state_schema = state_schema
        self.state_validator = Validator(self.state_schema)

    def calculate(self, **state):
        """
        Base calculate method for models.
        Validates the material state parameter(s).

        :param **state: The material state
        """
        if not self.state_validator.validate(state):
            msg = 'The state description contains errors:'
            for key, value in self.state_validator.errors.items():
                msg += ' %s: %s;' % (key, value)
            msg = msg[0:-1]+'.'
            raise ValidationError(msg)


if __name__ == "__main__":
    import unittest
    from core_test import *
    unittest.main()
