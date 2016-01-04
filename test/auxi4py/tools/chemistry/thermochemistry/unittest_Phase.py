








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
#//    Phase Unit Test
#//
#-----------------------------------------------
class Test_Phase(unittest.TestCase):

  def test_Phase_default_Symbol_value(self):
    phase = Phase()
    self.assertEqual(phase.symbol, "")
  def test_Phase_default_Tref_value(self):
    phase = Phase()
    self.assertAlmostEqual(phase.tref, float())
  def test_Phase_default_DHref_value(self):
    phase = Phase()
    self.assertAlmostEqual(phase.dHref, float())
  def test_Phase_default_Sref_value(self):
    phase = Phase()
    self.assertAlmostEqual(phase.sref, float())

  def test_Phase_Symbol_property(self):
    phase = Phase()
    phase.symbol = test_string_value
    self.assertEqual(phase.symbol, test_string_value)
  def test_Phase_Tref_property(self):
    phase = Phase()
    test_val = test_double_value
    phase.tref = test_val
    self.assertAlmostEqual(phase.tref, test_val)
  def test_Phase_DHref_property(self):
    phase = Phase()
    test_val = test_double_value
    phase.dHref = test_val
    self.assertAlmostEqual(phase.dHref, test_val)
  def test_Phase_Sref_property(self):
    phase = Phase()
    test_val = test_double_value
    phase.sref = test_val
    self.assertAlmostEqual(phase.sref, test_val)
  def test_Phase_Phase_fuction(self):
    phase = Phase()

    cpRecordMap = map<double, CpRecord>()

    phase.Phase(test_string_value, test_string_value, test_double_value, test_double_value, cpRecordMap)
  def test_Phase_to_string_fuction(self):
    phase = Phase()


    phase.to_string()
  def test_Phase_Cp_fuction(self):
    phase = Phase()


    phase.Cp(test_double_value)
  def test_Phase_H_fuction(self):
    phase = Phase()


    phase.H(test_double_value)
  def test_Phase_S_fuction(self):
    phase = Phase()


    phase.S(test_double_value)
  def test_Phase_G_fuction(self):
    phase = Phase()


    phase.G(test_double_value)




if __name__ == '__main__':
    unittest.main()
