







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
#//    CapitalLoanActivity Unit Test
#//
#-----------------------------------------------
class Test_CapitalLoanActivity(unittest.TestCase):

  def test_CapitalLoanActivity_default_Date_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertEqual(capitalLoanActivity.date, datetime.datetime.strptime("1500-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
  def test_CapitalLoanActivity_default_GeneralLedgerLiabilityAccount_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertEqual(capitalLoanActivity.generalLedgerLiabilityAccount, GeneralLedgerAccount())
  def test_CapitalLoanActivity_default_GeneralLedgerExpenseAccount_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertEqual(capitalLoanActivity.generalLedgerExpenseAccount, GeneralLedgerAccount())
  def test_CapitalLoanActivity_default_MakeLoanTxTemplate_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertEqual(capitalLoanActivity.makeLoanTxTemplate, TransactionTemplate())
  def test_CapitalLoanActivity_default_ConsiderInterestTxTemplate_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertEqual(capitalLoanActivity.considerInterestTxTemplate, TransactionTemplate())
  def test_CapitalLoanActivity_default_PayMonthlyLoanAmountTxTemplate_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertEqual(capitalLoanActivity.payMonthlyLoanAmountTxTemplate, TransactionTemplate())
  def test_CapitalLoanActivity_default_LoanAmount_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertEqual(capitalLoanActivity.loanAmount, 0.0)
  def test_CapitalLoanActivity_default_InterestRate_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertEqual(capitalLoanActivity.interestRate, 0.0)
  def test_CapitalLoanActivity_default_PeriodInMonths_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertEqual(capitalLoanActivity.periodInMonths, 0.0)
  def test_CapitalLoanActivity_default_AmountLeft_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertEqual(capitalLoanActivity.amountLeft, 0.0)
  def test_CapitalLoanActivity_default_MonthsLeft_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertEqual(capitalLoanActivity.monthsLeft, 0.0)
  def test_CapitalLoanActivity_default_MonthlyPayment_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertAlmostEqual(capitalLoanActivity.monthlyPayment, float())
  def test_CapitalLoanActivity_default_CurrentInterestAmount_value(self):
    capitalLoanActivity = CapitalLoanActivity()
    self.assertAlmostEqual(capitalLoanActivity.currentInterestAmount, float())

  def test_CapitalLoanActivity_Date_property(self):
    capitalLoanActivity = CapitalLoanActivity()
    capitalLoanActivity.date = test_datetime_value
    self.assertEqual(capitalLoanActivity.date, test_datetime_value)
  def test_CapitalLoanActivity_GeneralLedgerLiabilityAccount_property(self):
    capitalLoanActivity = CapitalLoanActivity()
  def test_CapitalLoanActivity_GeneralLedgerExpenseAccount_property(self):
    capitalLoanActivity = CapitalLoanActivity()
  def test_CapitalLoanActivity_MakeLoanTxTemplate_property(self):
    capitalLoanActivity = CapitalLoanActivity()
  def test_CapitalLoanActivity_ConsiderInterestTxTemplate_property(self):
    capitalLoanActivity = CapitalLoanActivity()
  def test_CapitalLoanActivity_PayMonthlyLoanAmountTxTemplate_property(self):
    capitalLoanActivity = CapitalLoanActivity()
  def test_CapitalLoanActivity_LoanAmount_property(self):
    capitalLoanActivity = CapitalLoanActivity()
    test_val = 0.0 + test_double_value
    capitalLoanActivity.loanAmount = test_val
    self.assertAlmostEqual(capitalLoanActivity.loanAmount, test_val)
  def test_CapitalLoanActivity_InterestRate_property(self):
    capitalLoanActivity = CapitalLoanActivity()
    test_val = 0.0 + test_double_value
    capitalLoanActivity.interestRate = test_val
    self.assertAlmostEqual(capitalLoanActivity.interestRate, test_val)
  def test_CapitalLoanActivity_PeriodInMonths_property(self):
    capitalLoanActivity = CapitalLoanActivity()
    test_val = 0.0 + test_double_value
    capitalLoanActivity.periodInMonths = test_val
    self.assertAlmostEqual(capitalLoanActivity.periodInMonths, test_val)
  def test_CapitalLoanActivity_AmountLeft_property(self):
    capitalLoanActivity = CapitalLoanActivity()
    test_val = 0.0 + test_double_value
    capitalLoanActivity.amountLeft = test_val
    self.assertAlmostEqual(capitalLoanActivity.amountLeft, test_val)
  def test_CapitalLoanActivity_MonthsLeft_property(self):
    capitalLoanActivity = CapitalLoanActivity()
    test_val = 0.0 + test_double_value
    capitalLoanActivity.monthsLeft = test_val
    self.assertAlmostEqual(capitalLoanActivity.monthsLeft, test_val)
  def test_CapitalLoanActivity_MonthlyPayment_property(self):
    capitalLoanActivity = CapitalLoanActivity()
    test_val = test_double_value
    capitalLoanActivity.monthlyPayment = test_val
    self.assertAlmostEqual(capitalLoanActivity.monthlyPayment, test_val)
  def test_CapitalLoanActivity_CurrentInterestAmount_property(self):
    capitalLoanActivity = CapitalLoanActivity()
    test_val = test_double_value
    capitalLoanActivity.currentInterestAmount = test_val
    self.assertAlmostEqual(capitalLoanActivity.currentInterestAmount, test_val)
  def test_CapitalLoanActivity_CapitalLoanActivity_fuction(self):
    capitalLoanActivity = CapitalLoanActivity()


    capitalLoanActivity.CapitalLoanActivity(test_string_value, test_string_value, test_int_value, test_int_value, test_int_value)
  def test_CapitalLoanActivity_CapitalLoanActivity_fuction(self):
    capitalLoanActivity = CapitalLoanActivity()


    capitalLoanActivity.CapitalLoanActivity(test_string_value, test_string_value, test_datetime_value, test_datetime_value, test_int_value)
  def test_CapitalLoanActivity_CapitalLoanActivity_fuction(self):
    capitalLoanActivity = CapitalLoanActivity()


    capitalLoanActivity.CapitalLoanActivity(test_string_value, test_string_value, test_datetime_value, test_int_value, test_int_value)
  def test_CapitalLoanActivity_initialize_fuction(self):
    capitalLoanActivity = CapitalLoanActivity()


    capitalLoanActivity.initialize()
  def test_CapitalLoanActivity_OnExecute_MeetExecutionCriteria_fuction(self):
    capitalLoanActivity = CapitalLoanActivity()


    capitalLoanActivity.OnExecute_MeetExecutionCriteria(test_int_value)
  def test_CapitalLoanActivity_prepare_to_run_fuction(self):
    capitalLoanActivity = CapitalLoanActivity()

    clock = Clock()

    capitalLoanActivity.prepare_to_run(clock, test_int_value)
  def test_CapitalLoanActivity_run_fuction(self):
    capitalLoanActivity = CapitalLoanActivity()

    clock = Clock()
    generalLedger = GeneralLedger()

    capitalLoanActivity.run(clock, test_int_value, generalLedger)




if __name__ == '__main__':
    unittest.main()
