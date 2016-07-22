#!/usr/bin/env python3
"""
This package provides auxi's bibliography, and tools to interact with it.
"""


import bibtexparser
from os import path


__version__ = '0.3.1'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class Database(object):
    """
    A bibliography database that contains and provides entries in a bibtex
    file.

    :param path: the path to the bibtex file to load into the database
    """

    def __init__(self, path):
        with open(path) as file:
            bibtex_str = file.read()

        bib_database = bibtexparser.loads(bibtex_str)
        self._dict = bib_database.get_entry_dict()

    def __str__(self):
        return str(self._dict)

    def __getitem__(self, key):
        return self._dict[key]

db = Database(path.join(path.dirname(path.realpath(__file__)),
              r'data/bibliography.bib'))


if __name__ == "__main__":
    import unittest
    from bibliography_test import DatabaseTester
    unittest.main()
