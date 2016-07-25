#!/usr/bin/env python3
"""
This module contains all the code used to test the testee module.
"""


import unittest
from os import path

from auxi.core.bibliography import Database as testee


__version__ = '0.3.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class DatabaseTester(unittest.TestCase):
    """
    The function tester for the bibliography Database class.
    """

    def test_construct(self):
        """
        Test whether an exception is raised when a database object is created
        from a bibtex file.
        """

        testee(path.join(path.dirname(path.realpath(__file__)),
               'data/bibliography.bib'))

    def test_entry(self):
        """
        Test whether an entry is successfully retrieved from the database.
        """

        db = testee(path.join(path.dirname(path.realpath(__file__)),
                    'data/bibliography.bib'))
        entry = db['lienhard2015']
        self.assertEqual(entry['author'],
                         'J.H. Lienhard IV and J.H. Lienhard V')
        self.assertEqual(entry['title'],
                         'A Heat Transfer Textbook')


if __name__ == '__main__':
    unittest.main()
