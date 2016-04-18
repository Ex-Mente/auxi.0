#!/usr/bin/env python3
"""
This module provides testing code for the
auxi.modelling.financial.tax module.
"""

import unittest
from auxi.modelling.financial.tax import Rule
from auxi.modelling.financial.tax import RuleSet
from auxi.modelling.financial.tax import SalesRule
from auxi.modelling.financial.tax import IncomeRule
from auxi.modelling.financial.tax import CapitalGainsRule

__version__ = '0.2.0rc6'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class RuleUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.tax.Rule class.
    """

    def setUp(self):
        self.object = Rule("NameA",
                           description="DescriptionA")

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")


class RuleSetUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.tax.RuleSet class.
    """

    def setUp(self):
        self.object = RuleSet("NameA",
                              description="DescriptionA",
                              code="ZA")

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.code, "ZA")


class SalesRuleUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.tax.SalesRule class.
    """

    def setUp(self):
        self.object = SalesRule("NameA",
                                description="DescriptionA",
                                percentage=1.14)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.percentage, 1.14)


class IncomeRuleUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.tax.IncomeRule class.
    """

    def setUp(self):
        self.object = IncomeRule("NameA",
                                 description="DescriptionA",
                                 percentage=1.14)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.percentage, 1.14)


class CapitalGainsRuleUnitTester(unittest.TestCase):
    """
    Tester for the auxi.modelling.financial.tax.CapitalGainsRule class.
    """

    def setUp(self):
        self.object = CapitalGainsRule("NameA",
                                       description="DescriptionA",
                                       percentage=1.14)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.percentage, 1.14)


# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(Currency)

if __name__ == '__main__':
    unittest.main()
