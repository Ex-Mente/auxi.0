#!/usr/bin/env python3
"""
This module provides testing code for the auxi.modelling.financial.des module.
"""

import unittest
from datetime import datetime

from auxi.modelling.financial.reporting import GeneralLedgerStructure

from auxi.modelling.financial.des import GeneralLedgerStructure as Gls

__version__ = '0.2.0rc6'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class GeneralLedgerStructureUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.reporting.GeneralLedgerStructure
    class.
    """

    def setUp(self):
        gls = Gls("NameA")
        self.object = GeneralLedgerStructure(
            data_source=gls, output_path=None)

    def test__generate_table_(self):
        table = self.object._generate_table_()
        self.assertEqual(table[0], ["Type", "Number", "Name", "Description"])
        # The general leger has 27 accounts
        self.assertEqual(len(table), 28)

    def test_latex(self):
        pass


if __name__ == '__main__':
    unittest.main()
