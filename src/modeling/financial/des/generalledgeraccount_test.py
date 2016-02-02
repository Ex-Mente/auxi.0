# -*- coding: utf-8 -*-
"""
This module provides testing code for the auxi.modeling.financial.des.generalledgeraccount module.

@author: Ex Mente Technologies (Pty) Ltd
"""

import unittest
from auxi.modeling.financial.des.generalledgeraccount import AccountType
from auxi.modeling.financial.des.generalledgeraccount import GeneralLedgerAccount

__version__ = "0.2.0"


# =============================================================================
# Types.
# =============================================================================

class TestAllFunctions(unittest.TestCase):
    """
        Tester for the auxi.modeling.financial.des.generalledgeraccount class.
    """

    def setUp(self):
        self.object = GeneralLedgerAccount("NameA",
                                           description="DescriptionA",
                                           number="010",
                                           account_type=AccountType.asset)

    def test_constructor(self):
        self.assertEqual(self.object.name, "NameA")
        self.assertEqual(self.object.description, "DescriptionA")
        self.assertEqual(self.object.number, "010")
        self.assertEqual(self.object.account_type, AccountType.asset)

    def test_create_account(self):
        new_account = self.object.create_account("TestA",
                                                 description="TestA_Desc",
                                                 number="011")
        self.assertEqual(new_account.name, "TestA")
        self.assertEqual(new_account.description, "TestA_Desc")
        self.assertEqual(new_account.number, "011")
        self.assertEqual(new_account.account_type, self.object.account_type)

        self.assertEqual(new_account, self.object.accounts[0])

    def test_remove_account(self):
        self.object.create_account("TestA",
                                   description="TestA_Desc",
                                   number="011")
        self.object.remove_account("TestA")
        self.assertEqual(len(self.object.accounts), 0)

# =============================================================================
# Display documentation and run tests.
# =============================================================================
# os.system("cls")

# help(TransactionTemplate)

if __name__ == '__main__':
    unittest.main()
