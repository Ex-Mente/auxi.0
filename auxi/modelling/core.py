#!/usr/bin/env python3
"""
This module provides a material class that can do thermochemical calculations.
"""

from auxi.core.objects import NamedObject


__version__ = '0.3.4'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Johan Zietsman'
__credits__ = ['Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class Project(NamedObject):
    """
    A modelling project.

    :param name: A name for the project.
    :param description: the project's description
    """

    def __init__(self, name, description=None):
        super().__init__(name, description)


class Variable(NamedObject):
    """
    A variable used in a modelling project.

    :param name: A name for the variable.
    :param description: the variable's description
    """

    def __init__(self, name, value, units=None, category=None,
                 description=None):
        super(Variable, self).__init__(name, description)
        self.category = category
        self.value = value
        self.units = units

    def __call__(self):
        return self.value


class VariableGroup(NamedObject):
    """
    A variable group used in a modelling project.

    :param name: A name for the group.
    :param description: the group's description
    """

    def __init__(self, name, value, units=None, category=None,
                 description=None):
        super(Variable, self).__init__(name, description)

    def __call__(self):
        return self.value


if __name__ == '__main__':
    import unittest
    from core_test import *
    unittest.main()
