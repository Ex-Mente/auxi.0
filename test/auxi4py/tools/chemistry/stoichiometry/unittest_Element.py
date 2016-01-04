







import sys
import datetime
from auxi.tools.chemistry import *
import unittest

test_string_value = "Test"
test_int_value = 3
test_double_value = 5.3
test_datetime_value = datetime.datetime.strptime("2015-02-17 13:37:01", "%Y-%m-%d %H:%M:%S")

#-----------------------------------------------
#//
#//    Element Unit Test
#//
#-----------------------------------------------
class Test_Element(unittest.TestCase):

  def test_Element_default_Period_value(self):
    element = Element()
    self.assertEqual(element.period, int())
  def test_Element_default_Group_value(self):
    element = Element()
    self.assertEqual(element.group, int())
  def test_Element_default_Atomic_number_value(self):
    element = Element()
    self.assertEqual(element.atomic_number, int())
  def test_Element_default_Symbol_value(self):
    element = Element()
    self.assertEqual(element.symbol, "")
  def test_Element_default_Molar_mass_value(self):
    element = Element()
    self.assertAlmostEqual(element.molar_mass, float())

  def test_Element_Period_property(self):
    element = Element()
    test_val = test_int_value
    element.period = test_val
    self.assertEqual(element.period, test_val)
  def test_Element_Group_property(self):
    element = Element()
    test_val = test_int_value
    element.group = test_val
    self.assertEqual(element.group, test_val)
  def test_Element_Atomic_number_property(self):
    element = Element()
    test_val = test_int_value
    element.atomic_number = test_val
    self.assertEqual(element.atomic_number, test_val)
  def test_Element_Symbol_property(self):
    element = Element()
    element.symbol = test_string_value
    self.assertEqual(element.symbol, test_string_value)
  def test_Element_Molar_mass_property(self):
    element = Element()
    test_val = test_double_value
    element.molar_mass = test_val
    self.assertAlmostEqual(element.molar_mass, test_val)
  def test_Element_to_string_fuction(self):
    element = Element()


    element.to_string()




if __name__ == '__main__':
    unittest.main()
