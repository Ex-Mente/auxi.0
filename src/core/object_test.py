#!/usr/bin/env python3
"""
This module contains all the code used to test the Testee class.
"""

import unittest

import jsonpickle

from auxi.core.object import Object as Testee


__version__ = "0.2.0rc3"
__license__ = "LGPL v3"
__copyright__ = "Copyright 2016, Ex Mente Technologies (Pty) Ltd"
__author__ = "Christoff Kok, Johan Zietsman"
__credits__ = ["Christoff Kok", "Johan Zietsman"]
__maintainer__ = "Christoff Kok"
__email__ = "christoff.kok@ex-mente.co.za"
__status__ = "Planning"


class ObjectUnitTester(unittest.TestCase):
    """
    The unit tester for the class being tested.
    """

    def setUp(self):
        self.o = Testee()

    def tearDown(self):
        del self.o

    def test___str__(self):
        """
        Test whether the __str__ method successfully generates a json string
        representation of the object.
        """

        # Confirm that the string representation of the current object and that
        # of an object decoded from this string representation are equal.
        str_o = str(self.o)
        new_o = jsonpickle.decode(str_o)
        self.assertEqual(str_o, str(new_o))


if __name__ == '__main__':
    unittest.main()
