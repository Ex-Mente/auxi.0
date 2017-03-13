#!/usr/bin/env python3
"""
This module provides a material class that can do thermochemical calculations.
"""

from auxi.core.objects import NamedObject


__version__ = '0.3.5'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Johan Zietsman'
__credits__ = ['Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class Model(NamedObject):
    """
    A process model.

    :param name: A name for the model.
    :param description: the model's description
    """

    def __init__(self, name, description=None):
        super().__init__(name, description)

        self.parameters = type(self).Parameters()
        self.input_variables = type(self).InputVariables()
        self.output_variables = type(self).OutputVariables()

    def run(self, streams):
        """
        Run the model.

        :param streams: A dictionary of streams in the model.
        :returns: The streams dictionary with the output streams calculated by
        this model.

        If the input streams to required by the model is not found in the
        dictionary, the model will create the streams by itself based on its
        parameters and input variables.
        """
        pass

    class Parameters(object):
        pass

    class InputVariables(object):
        pass

    class OutputVariables(object):
        pass


class SteadyStateModel(Model):
    """
    A steady state process model.

    :param name: A name for the model.
    :param description: the model's description
    """

    def __init__(self, name, description=None):
        super().__init__(name, description)


class DynamicModel(Model):
    """
    A dynamic process model.

    :param name: A name for the model.
    :param description: the model's description
    """

    def __init__(self, name, description=None):
        super().__init__(name, description)


if __name__ == '__main__':
    import unittest
    from core_test import *
    unittest.main()
