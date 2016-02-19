#!/usr/bin/env python3
from auxi.core.object import Object


__version__ = "0.2.0rc3"
__license__ = "LGPL v3"
__copyright__ = "Copyright 2016, Ex Mente Technologies (Pty) Ltd"
__author__ = "Christoff Kok, Johan Zietsman"
__credits__ = ["Christoff Kok", "Johan Zietsman"]
__maintainer__ = "Christoff Kok"
__email__ = "christoff.kok@ex-mente.co.za"
__status__ = "Planning"


class NamedObject(Object):
    """
    Base class for all auxi classes requiring a name and description.

    :param name: the object's name
    :param description: the object's description
    """

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


if __name__ == "__main__":
    import unittest
    import namedobject_test
    unittest.main()
