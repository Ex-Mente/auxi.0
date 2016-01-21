







import sys
import datetime
from auxi.modelling.business import *
import unittest

test_string_value = "Test"
test_int_value = 3
test_double_value = 5.3
test_datetime_value = datetime.datetime.strptime("2015-02-17 13:37:01", "%Y-%m-%d %H:%M:%S")

#-----------------------------------------------
#//
#//    AssetPurchaseActivity Unit Test
#//
#-----------------------------------------------
class Test_AssetPurchaseActivity(unittest.TestCase):

  def test_AssetPurchaseActivity_default_Date_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.date, datetime.datetime.strptime("1500-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
  def test_AssetPurchaseActivity_default_GeneralLedgerExpenseAccount_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.generalLedgerExpenseAccount, GeneralLedgerAccount())
  def test_AssetPurchaseActivity_default_GeneralLedgerAssetAccount_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.generalLedgerAssetAccount, GeneralLedgerAccount())
  def test_AssetPurchaseActivity_default_AssetPurchaseTxTemplate_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.assetPurchaseTxTemplate, TransactionTemplate())
  def test_AssetPurchaseActivity_default_AddDepreciationTxTemplate_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.addDepreciationTxTemplate, TransactionTemplate())
  def test_AssetPurchaseActivity_default_PurchaseAmount_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.purchaseAmount, 0.0)
  def test_AssetPurchaseActivity_default_WriteOffAmount_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.writeOffAmount, 0.0)
  def test_AssetPurchaseActivity_default_MonthsTillWrittenOff_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.monthsTillWrittenOff, 0.0)
  def test_AssetPurchaseActivity_default_PeriodicDepreciationAmount_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.periodicDepreciationAmount, 0.0)
  def test_AssetPurchaseActivity_default_AmountLeft_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.amountLeft, 0.0)
  def test_AssetPurchaseActivity_default_MonthsLeft_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.monthsLeft, 0.0)
  def test_AssetPurchaseActivity_default_CurrentAssetValue_value(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    self.assertEqual(assetPurchaseActivity.currentAssetValue, 0.0)

  def test_AssetPurchaseActivity_Date_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    assetPurchaseActivity.date = test_datetime_value
    self.assertEqual(assetPurchaseActivity.date, test_datetime_value)
  def test_AssetPurchaseActivity_GeneralLedgerExpenseAccount_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
  def test_AssetPurchaseActivity_GeneralLedgerAssetAccount_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
  def test_AssetPurchaseActivity_AssetPurchaseTxTemplate_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
  def test_AssetPurchaseActivity_AddDepreciationTxTemplate_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
  def test_AssetPurchaseActivity_PurchaseAmount_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    test_val = 0.0 + test_double_value
    assetPurchaseActivity.purchaseAmount = test_val
    self.assertAlmostEqual(assetPurchaseActivity.purchaseAmount, test_val)
  def test_AssetPurchaseActivity_WriteOffAmount_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    test_val = 0.0 + test_double_value
    assetPurchaseActivity.writeOffAmount = test_val
    self.assertAlmostEqual(assetPurchaseActivity.writeOffAmount, test_val)
  def test_AssetPurchaseActivity_MonthsTillWrittenOff_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    test_val = 0.0 + test_double_value
    assetPurchaseActivity.monthsTillWrittenOff = test_val
    self.assertAlmostEqual(assetPurchaseActivity.monthsTillWrittenOff, test_val)
  def test_AssetPurchaseActivity_PeriodicDepreciationAmount_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    test_val = 0.0 + test_double_value
    assetPurchaseActivity.periodicDepreciationAmount = test_val
    self.assertAlmostEqual(assetPurchaseActivity.periodicDepreciationAmount, test_val)
  def test_AssetPurchaseActivity_AmountLeft_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    test_val = 0.0 + test_double_value
    assetPurchaseActivity.amountLeft = test_val
    self.assertAlmostEqual(assetPurchaseActivity.amountLeft, test_val)
  def test_AssetPurchaseActivity_MonthsLeft_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    test_val = 0.0 + test_double_value
    assetPurchaseActivity.monthsLeft = test_val
    self.assertAlmostEqual(assetPurchaseActivity.monthsLeft, test_val)
  def test_AssetPurchaseActivity_CurrentAssetValue_property(self):
    assetPurchaseActivity = AssetPurchaseActivity()
    test_val = 0.0 + test_double_value
    assetPurchaseActivity.currentAssetValue = test_val
    self.assertAlmostEqual(assetPurchaseActivity.currentAssetValue, test_val)
  def test_AssetPurchaseActivity_AssetPurchaseActivity_fuction(self):
    assetPurchaseActivity = AssetPurchaseActivity()


    assetPurchaseActivity.AssetPurchaseActivity(test_string_value, test_string_value, test_int_value, test_int_value, test_int_value)
  def test_AssetPurchaseActivity_AssetPurchaseActivity_fuction(self):
    assetPurchaseActivity = AssetPurchaseActivity()


    assetPurchaseActivity.AssetPurchaseActivity(test_string_value, test_string_value, test_datetime_value, test_datetime_value, test_int_value)
  def test_AssetPurchaseActivity_AssetPurchaseActivity_fuction(self):
    assetPurchaseActivity = AssetPurchaseActivity()


    assetPurchaseActivity.AssetPurchaseActivity(test_string_value, test_string_value, test_datetime_value, test_int_value, test_int_value)
  def test_AssetPurchaseActivity_initialize_fuction(self):
    assetPurchaseActivity = AssetPurchaseActivity()


    assetPurchaseActivity.initialize()
  def test_AssetPurchaseActivity_OnExecute_MeetExecutionCriteria_fuction(self):
    assetPurchaseActivity = AssetPurchaseActivity()


    assetPurchaseActivity.OnExecute_MeetExecutionCriteria(test_int_value)
  def test_AssetPurchaseActivity_prepare_to_run_fuction(self):
    assetPurchaseActivity = AssetPurchaseActivity()

    clock = Clock()

    assetPurchaseActivity.prepare_to_run(clock, test_int_value)
  def test_AssetPurchaseActivity_run_fuction(self):
    assetPurchaseActivity = AssetPurchaseActivity()

    clock = Clock()
    generalLedger = GeneralLedger()

    assetPurchaseActivity.run(clock, test_int_value, generalLedger)




if __name__ == '__main__':
    unittest.main()
