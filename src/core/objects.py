#!/usr/bin/env python3
import json

import jsonpickle


__version__ = '0.2.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class Object(object):
    """
    Base class for all auxi classes.
    """

    def __str__(self):
        o = json.loads(jsonpickle.encode(self))
        result = json.dumps(o, sort_keys=True, indent=4,
                            separators=(',', ': '))
        return result

    def __hash__(self):
        return hash(str(self))

    def _validate_params_(self):
        pass


class NamedObject(Object):
    """
    Base class for all auxi classes requiring a name and description.

    :param name: the object's name
    :param description: the object's description
    """

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def _validate_params_(self, name, description):
        # TODO: Enforce name format.
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


if __name__ == "__main__":
    import unittest
    from objects_test import ObjectUnitTester, NamedObjectUnitTester
    unittest.main()
