







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
#//    BasicActivity Unit Test
#//
#-----------------------------------------------
class Test_BasicActivity(unittest.TestCase):

  def test_BasicActivity_default_Date_value(self):
    basicActivity = BasicActivity()
    self.assertEqual(basicActivity.date, datetime.datetime.strptime("1500-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
  def test_BasicActivity_default_TxTemplate_value(self):
    basicActivity = BasicActivity()
    self.assertEqual(basicActivity.txTemplate, TransactionTemplate())
  def test_BasicActivity_default_Amount_value(self):
    basicActivity = BasicActivity()
    self.assertEqual(basicActivity.amount, 0.0)

  def test_BasicActivity_Date_property(self):
    basicActivity = BasicActivity()
    basicActivity.date = test_datetime_value
    self.assertEqual(basicActivity.date, test_datetime_value)
  def test_BasicActivity_TxTemplate_property(self):
    basicActivity = BasicActivity()
  def test_BasicActivity_Amount_property(self):
    basicActivity = BasicActivity()
    test_val = 0.0 + test_double_value
    basicActivity.amount = test_val
    self.assertAlmostEqual(basicActivity.amount, test_val)
  def test_BasicActivity_BasicActivity_fuction(self):
    basicActivity = BasicActivity()

    tx_template = TransactionTemplate()

    basicActivity.BasicActivity(test_string_value, test_string_value, test_int_value, test_int_value, test_int_value, test_double_value, tx_template)
  def test_BasicActivity_BasicActivity_fuction(self):
    basicActivity = BasicActivity()

    tx_template = TransactionTemplate()

    basicActivity.BasicActivity(test_string_value, test_string_value, test_datetime_value, test_datetime_value, test_int_value, test_double_value, tx_template)
  def test_BasicActivity_BasicActivity_fuction(self):
    basicActivity = BasicActivity()

    tx_template = TransactionTemplate()

    basicActivity.BasicActivity(test_string_value, test_string_value, test_datetime_value, test_int_value, test_int_value, test_double_value, tx_template)
  def test_BasicActivity_initialize_fuction(self):
    basicActivity = BasicActivity()


    basicActivity.initialize()
  def test_BasicActivity_OnExecute_MeetExecutionCriteria_fuction(self):
    basicActivity = BasicActivity()


    basicActivity.OnExecute_MeetExecutionCriteria(test_int_value)
  def test_BasicActivity_prepare_to_run_fuction(self):
    basicActivity = BasicActivity()

    clock = Clock()

    basicActivity.prepare_to_run(clock, test_int_value)
  def test_BasicActivity_run_fuction(self):
    basicActivity = BasicActivity()

    clock = Clock()
    generalLedger = GeneralLedger()

    basicActivity.run(clock, test_int_value, generalLedger)




if __name__ == '__main__':
    unittest.main()
