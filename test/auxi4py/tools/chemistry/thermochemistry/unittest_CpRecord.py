








import sys
import datetime
from auxi.tools.chemistry.thermochemistry import *
import unittest

test_string_value = "Test"
test_int_value = 3
test_double_value = 5.3
test_datetime_value = datetime.datetime.strptime("2015-02-17 13:37:01", "%Y-%m-%d %H:%M:%S")

#-----------------------------------------------
#//
#//    CpRecord Unit Test
#//
#-----------------------------------------------
class Test_CpRecord(unittest.TestCase):

  def test_CpRecord_default_Tmin_value(self):
    cpRecord = CpRecord()
    self.assertAlmostEqual(cpRecord.tmin, float())
  def test_CpRecord_default_Tmax_value(self):
    cpRecord = CpRecord()
    self.assertAlmostEqual(cpRecord.tmax, float())

  def test_CpRecord_Tmin_property(self):
    cpRecord = CpRecord()
    test_val = test_double_value
    cpRecord.tmin = test_val
    self.assertAlmostEqual(cpRecord.tmin, test_val)
  def test_CpRecord_Tmax_property(self):
    cpRecord = CpRecord()
    test_val = test_double_value
    cpRecord.tmax = test_val
    self.assertAlmostEqual(cpRecord.tmax, test_val)
  def test_CpRecord_CpRecord_fuction(self):
    cpRecord = CpRecord()

    coefficientList = vector<doubleList()
    exponentList = vector<doubleList()

    cpRecord.CpRecord(test_double_value, test_double_value, coefficientList, exponentList)
  def test_CpRecord_to_string_fuction(self):
    cpRecord = CpRecord()


    cpRecord.to_string()
  def test_CpRecord_Cp_fuction(self):
    cpRecord = CpRecord()


    cpRecord.Cp(test_double_value)
  def test_CpRecord_H_fuction(self):
    cpRecord = CpRecord()


    cpRecord.H(test_double_value)
  def test_CpRecord_S_fuction(self):
    cpRecord = CpRecord()


    cpRecord.S(test_double_value)




if __name__ == '__main__':
    unittest.main()
