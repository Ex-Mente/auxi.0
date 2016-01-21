







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
#//    Activity Unit Test
#//
#-----------------------------------------------
class Test_Activity(unittest.TestCase):

  def test_Activity_default_Currency_value(self):
    activity = Activity()
    self.assertEqual(activity.currency, Units())
  def test_Activity_default_StartPeriod_value(self):
    activity = Activity()
    self.assertEqual(activity.startPeriod, -1)
  def test_Activity_default_EndPeriod_value(self):
    activity = Activity()
    self.assertEqual(activity.endPeriod, -1)
  def test_Activity_default_Interval_value(self):
    activity = Activity()
    self.assertEqual(activity.interval, 1)
  def test_Activity_default_PeriodCount_value(self):
    activity = Activity()
    self.assertEqual(activity.periodCount, -1)
  def test_Activity_default_path_value(self):
    activity = Activity()
    self.assertEqual(activity.path, "")

  def test_Activity_Currency_property(self):
    activity = Activity()
  def test_Activity_StartPeriod_property(self):
    activity = Activity()
    test_val = -1 + test_int_value
    activity.startPeriod = test_val
    self.assertEqual(activity.startPeriod, test_val)
  def test_Activity_EndPeriod_property(self):
    activity = Activity()
    test_val = -1 + test_int_value
    activity.endPeriod = test_val
    self.assertEqual(activity.endPeriod, test_val)
  def test_Activity_Interval_property(self):
    activity = Activity()
    test_val = 1 + test_int_value
    activity.interval = test_val
    self.assertEqual(activity.interval, test_val)
  def test_Activity_PeriodCount_property(self):
    activity = Activity()
    test_val = -1 + test_int_value
    activity.periodCount = test_val
    self.assertEqual(activity.periodCount, test_val)
  def test_Activity_path_property(self):
    activity = Activity()
    activity.path = test_string_value
    self.assertEqual(activity.path, test_string_value)
  def test_Activity_Activity_fuction(self):
    activity = Activity()


    activity.Activity(test_string_value, test_string_value, test_int_value, test_int_value, test_int_value)
  def test_Activity_Activity_fuction(self):
    activity = Activity()


    activity.Activity(test_string_value, test_string_value, test_datetime_value, test_datetime_value, test_int_value)
  def test_Activity_Activity_fuction(self):
    activity = Activity()


    activity.Activity(test_string_value, test_string_value, test_datetime_value, test_int_value, test_int_value)
  def test_Activity_OnExecute_MeetExecutionCriteria_fuction(self):
    activity = Activity()


    activity.OnExecute_MeetExecutionCriteria(test_int_value)
  def test_Activity_prepare_to_run_fuction(self):
    activity = Activity()

    clock = Clock()

    activity.prepare_to_run(clock, test_int_value)
  def test_Activity_SetName_fuction(self):
    activity = Activity()


    activity.SetName(test_string_value)
  def test_Activity_set_path_fuction(self):
    activity = Activity()


    activity.set_path(test_string_value)
  def test_Activity_run_fuction(self):
    activity = Activity()

    clock = Clock()
    generalLedger = GeneralLedger()

    activity.run(clock, test_int_value, generalLedger)




if __name__ == '__main__':
    unittest.main()
