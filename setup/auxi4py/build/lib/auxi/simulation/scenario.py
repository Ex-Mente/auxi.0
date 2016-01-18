# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 16:30:02 2015

@author: Christoff Kok, Thabisani Nigel Phuthi
"""
__version__ = "0.0.0"

from auxi.modelling.business import NamedObject
from auxi.simulation.segment import *


class Scenario(NamedObject):
    """ A scenario container.

    :param name: The name of the scenario
    :param description: The description of the scenario. By default the scenario
        has no description, but one may be set by the user.

    Simulations may have different scenarios to be studied, where some or all
    parameters may need to be changed.
    Within a scenario there are segments. A segment corresponds to a specific submodel.

    To add a segment to a scenario, use the command::
        scenario['Scenario name'].add_segment('Segment name')
    """

    def __init__(self, name, description=""):
        NamedObject.__init__(self)
        self.name = name
        self.description = description
        self.segments = {}
        self._path = ""
        self.model_executionList = []

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def __getitem__(self, key):
        return self.segments[key]

    def add_segment(self, auxi_object, name):
        self.segments[name] = Segment(name)
        self.segments[name].path = self._path + '::' + name
        self.segments[name].auxi_object = auxi_object
        return self.segments[name]

    def apply_parameter_values(self, interval, date,
                               interval_type, interval_size):
        for seg_name, seg in self.segments.items():
            for param_path, param in seg.parameters.items():
                param.apply_value(seg.auxi_object, interval, date,
                                  interval_type, interval_size, self)

    def run(self):
        # Run the scenario steps
        # TODO: Add scenario steps
        for model in self.model_executionList:
            model.run_from_scenario(self)
