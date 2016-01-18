# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 16:30:02 2015

@author: Christoff Kok, Thabisani Nigel Phuthi
"""
__version__ = "0.0.0"

from auxi.modelling.business import NamedObject
from auxi.simulation.parameter import *


class Segment(NamedObject):
    """ A segment in the database corresponding to a submodel

        :param name: The name of the segment.
        :param description: A description of the segment. (Default has no
                            description)

        The segment has containers for parameters (values to be used in
        simulationcalculations by a submodel) and results (values generated
        by submodels)

        To create a parameter with the segment use the command::
            Segment.create_parameter(name, source units, default_value,
                                     description)
        To add a parameter that has been created outside of this segement,
        use the command::
            Segment.add_parameter(parameter)
        To clone a separately created parameter to a segment use the command::
            Segment.clone_parameter(parameter)
        Similar to the parameter's add and create commands, a result may also
        be created or added respectively with the commands::
            Segment.create_result(name, date, units, description)
            Segment.add_result(result)
    """

    def __init__(self, name, description=""):
        NamedObject.__init__(self)
        self.name = name
        self.description = description
        self._path = None
        self.auxi_object = None
        self.parameters = {}
        self.results = {}

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def __getitem__(self, key):
        return self.parameters[key]

    def create_parameter(self, param_path, source, units, default_value=None,
                         description=""):
        parameter = Parameter(param_path, source, units,
                              default_value, description)
        parameter.path = param_path
        self.parameters[param_path] = parameter
        return self.parameters[param_path]

    def add_parameter(self, parameter):
        self.parameters[parameter.path] = parameter
        return parameter

    def clone_parameter(self, parameter):
        return self.parameters.append(parameter(parameter.path, parameter.units,
                                      parameter.default_value,
                                      parameter.description))
