







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
#//    Clock Unit Test
#//
#-----------------------------------------------
class Test_Clock(unittest.TestCase):

  def test_Clock_default_StartDateTime_value(self):
    clock = Clock()
    self.assertEqual(clock.startDateTime, datetime.datetime.strptime("1500-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
  def test_Clock_default_TimeStepPeriodDuration_value(self):
    clock = Clock()
    self.assertEqual(clock.timeStepPeriodDuration, TimePeriod.month)
  def test_Clock_default_TimeStepPeriodCount_value(self):
    clock = Clock()
    self.assertEqual(clock.timeStepPeriodCount, 1)
  def test_Clock_default_TimeStepIndex_value(self):
    clock = Clock()
    self.assertEqual(clock.timeStepIndex, 0)

  def test_Clock_StartDateTime_property(self):
    clock = Clock()
    clock.startDateTime = test_datetime_value
    self.assertEqual(clock.startDateTime, test_datetime_value)
  def test_Clock_TimeStepPeriodDuration_property(self):
    clock = Clock()
    self.assertEqual(clock.timeStepPeriodDuration, TimePeriod.month)
  def test_Clock_TimeStepPeriodCount_property(self):
    clock = Clock()
    test_val = 1 + test_int_value
    clock.timeStepPeriodCount = test_val
    self.assertEqual(clock.timeStepPeriodCount, test_val)
  def test_Clock_TimeStepIndex_property(self):
    clock = Clock()
    test_val = 0 + test_int_value
    clock.timeStepIndex = test_val
    self.assertEqual(clock.timeStepIndex, test_val)
  def test_Clock_tick_fuction(self):
    clock = Clock()


    clock.tick()
  def test_Clock_reset_fuction(self):
    clock = Clock()


    clock.reset()
  def test_Clock_GetDateTime_fuction(self):
    clock = Clock()


    clock.GetDateTime()
  def test_Clock_GetDateTimeAtPeriodIndex_fuction(self):
    clock = Clock()


    clock.GetDateTimeAtPeriodIndex(test_int_value)




if __name__ == '__main__':
    unittest.main()
