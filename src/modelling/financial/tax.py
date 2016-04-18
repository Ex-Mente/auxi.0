#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides classes to manage tax.
"""

from auxi.core.objects import NamedObject

__version__ = '0.2.0rc6'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class Rule(NamedObject):
    """
    Represents a tax rule base class.

    :param name: The name.
    :param description: The description.
    """

    def __init__(self, name, description=None):
        """
        """
        super(Rule, self).__init__(name, description)


class RuleSet(NamedObject):
    """
    Represents a tax rule set base class.

    :param name: The name.
    :param description: The description.
    :param code: The code identifying the rule set. E.g. ZA tax rules, or
      US tax rules.
    """

    def __init__(self, name, description=None, code=None):
        """
        """
        super(RuleSet, self).__init__(name, description)
        self.code = code
        self.rules = []


class SalesRule(NamedObject):
    """
    Represents a sales tax rule class.

    :param name: The name.
    :param description: The description.
    :param percentage: The sales tax percentage.
    """

    def __init__(self, name, description=None, percentage=1.0):
        """
        """
        super(SalesRule, self).__init__(name, description)
        self.percentage = percentage


class IncomeRule(NamedObject):
    """
    Represents an income tax rule class.

    :param name: The name.
    :param description: The description.
    :param percentage: The income tax percentage.
    """

    def __init__(self, name, description=None, percentage=1.0):
        """
        """
        super(IncomeRule, self).__init__(name, description)
        self.percentage = percentage


class CapitalGainsRule(NamedObject):
    """
    Represents a capital gains tax rule class.

    :param name: The name.
    :param description: The description.
    :param percentage: The capital gains tax percentage.
    """

    def __init__(self, name, description=None, percentage=1.0):
        """
        """
        super(CapitalGainsRule, self).__init__(name, description)
        self.percentage = percentage


if __name__ == "__main__":
    import unittest
    from auxi.modelling.financial.tax_test import RuleUnitTester
    from auxi.modelling.financial.tax_test import RuleSetUnitTester
    from auxi.modelling.financial.tax_test import SalesRuleUnitTester
    from auxi.modelling.financial.tax_test import IncomeRuleUnitTester
    from auxi.modelling.financial.tax_test import CapitalGainsRuleUnitTester
    unittest.main()
