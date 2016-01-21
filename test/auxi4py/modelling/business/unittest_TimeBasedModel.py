







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
#//    TimeBasedModel Unit Test
#//
#-----------------------------------------------
class Test_TimeBasedModel(unittest.TestCase):

  def test_TimeBasedModel_default_EntityList_value(self):
    timeBasedModel = TimeBasedModel()
    self.assertEqual(len(timeBasedModel.entityList), 0)
  def test_TimeBasedModel_default_Currency_value(self):
    timeBasedModel = TimeBasedModel()
    self.assertEqual(timeBasedModel.currency, Units())
  def test_TimeBasedModel_default_PeriodCount_value(self):
    timeBasedModel = TimeBasedModel()
    self.assertEqual(timeBasedModel.periodCount, 60)
  def test_TimeBasedModel_default_Clock_value(self):
    timeBasedModel = TimeBasedModel()
    self.assertEqual(timeBasedModel.clock, Clock())

  def test_TimeBasedModel_EntityList_property(self):
    timeBasedModel = TimeBasedModel()
    test_val = Entity()
    timeBasedModel.entityList.append(test_val)
    self.assertEqual(timeBasedModel.entityList[0], test_val)
  def test_TimeBasedModel_Currency_property(self):
    timeBasedModel = TimeBasedModel()
  def test_TimeBasedModel_PeriodCount_property(self):
    timeBasedModel = TimeBasedModel()
    test_val = 60 + test_int_value
    timeBasedModel.periodCount = test_val
    self.assertEqual(timeBasedModel.periodCount, test_val)
  def test_TimeBasedModel_Clock_property(self):
    timeBasedModel = TimeBasedModel()
  def test_TimeBasedModel_TimeBasedModel_fuction(self):
    timeBasedModel = TimeBasedModel()

    period_duration = TimePeriod()

    timeBasedModel.TimeBasedModel(test_string_value, test_string_value, test_datetime_value, period_duration, test_int_value)
  def test_TimeBasedModel_initialize_fuction(self):
    timeBasedModel = TimeBasedModel()


    timeBasedModel.initialize()
  def test_TimeBasedModel_create_entity_fuction(self):
    timeBasedModel = TimeBasedModel()


    timeBasedModel.create_entity(test_string_value)
  def test_TimeBasedModel_remove_entity_fuction(self):
    timeBasedModel = TimeBasedModel()

    entity = timeBasedModel.create_entity(test_string_value)
    self.assertEqual(entity.name, timeBasedModel.entityList[0].name)

    timeBasedModel.remove_entity(test_string_value)
    self.assertEqual(len(timeBasedModel.entityList), 0)
  def test_TimeBasedModel_prepare_to_run_fuction(self):
    timeBasedModel = TimeBasedModel()


    timeBasedModel.prepare_to_run()
  def test_TimeBasedModel_run_fuction(self):
    timeBasedModel = TimeBasedModel()


    timeBasedModel.run()




if __name__ == '__main__':
    unittest.main()
