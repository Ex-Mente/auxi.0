# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:19:02 2015

@author: Christoff Kok, Thabisani Nigel Phuthi
"""
__version__ = "0.0.0"

from auxi.modelling.business import NamedObject
from auxi.simulation.scenario import *
from auxi.simulation.path_engine import *
from datetime import datetime


def create_investigation_from_auxi_object(auxi_object):
    parameter_path_dict = generate_parameter_paths(auxi_object)

    result = Investigation()
    scenario = result.scenarios["default"]

    path_dict = {}
    for p_path, p_prop in parameter_path_dict.items():
        path_dict[p_path[0]] = p_path[1]

    for seg_path, seg_obj in path_dict.items():
        scenario.add_segment(seg_obj, seg_path)

    for p_path, p_prop in parameter_path_dict.items():
        default_val = 0
        if type(p_prop) is str:
            default_val = ""
        elif type(p_prop) is datetime:
            default_val = datetime(2015, 1, 1, 0, 0, 0)
        scenario.segments[p_path[0]].create_parameter(str(p_path[2]), p_prop, "", default_val)
        # TODO: Append Results
        # TODO: Global Variables must be accessible via parameters.
        #       Calculation Engines as well.
    return result


class Investigation(NamedObject):
    """ Acts as a container for scenarios which store all the parameters of the
    techno-economic model.

    Parameters are time based values (can be made to vary according to date or a
    given reference time.
    Results are also time based values (Are stored according to the simulation's
    virtual date.)
    A submodel's parameters and results are stored under the submodel's
    respective 'segment'
    This division of parameters into segements ensure that there is no mix up of
    parameters between models.
    Furthermore, segments are grouped into scenarios, as the parameters can be
    changed according to the investigation scenario.
    The scenarios are the highest level of grouping in an investigation

    To add a scenario to an investigation use the command::
        investigation.add_scenario('Scenario name')
    """
    def __init__(self):
        NamedObject.__init__(self)
        self.scenarios = {}
        self.scenarios["default"] = Scenario("default")
        self.scenarios["default"].path = self.scenarios["default"].name

    def __getitem__(self, key):
        return self.scenarios[key]

    def add_scenario(self, name):
        self.scenarios[name] = Scenario(name)
        self.scenarios[name].path = name
        return self.scenarios[name]

    def get_parameter(self, scenario_name, segment_name, parameter_name):
        if segment_name in self.scenarios[scenario_name].segments.keys():
            segment = self.scenarios[scenario_name][segment_name]
        else:
            segment = self.scenarios["default"][segment_name]

        return segment[parameter_name]

    def get_result(self, scenario_name, segment_name, result_name):
        if segment_name in self.scenarios[scenario_name].segments.keys():
            segment = self.scenarios[scenario_name][segment_name]
        else:
            segment = self.scenarios["default"][segment_name]

        return segment[result_name]

    def _get_name_path(self, parameter_name):
        for scenario in self.scenarios:
            for segment in scenario.segments:
                for parameter in segment.parameters:
                    if parameter.name == parameter_name:
                        name_path = parameter.path
                    else:
                        print("Parameter does not exist")

        return name_path

    def run_scenario(self, io_reader, scenario_name):
        # Set models' parameters to that of the investigation io reader's file.
        io_reader.update_scenario_from_file(self, scenario_name)
        for scenario in self.scenarios:
            if scenario == scenario_name:
                self.scenarios[scenario].run()
                break
