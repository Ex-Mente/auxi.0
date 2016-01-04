








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
#//    Compound Unit Test
#//
#-----------------------------------------------
class Test_Compound(unittest.TestCase):

  def test_Compound_default_Formula_value(self):
    compound = Compound()
    self.assertEqual(compound.formula, "")
  def test_Compound_default_molar_mass_value(self):
    compound = Compound()
    self.assertAlmostEqual(compound.molar_mass, float())

  def test_Compound_Formula_property(self):
    compound = Compound()
    compound.formula = test_string_value
    self.assertEqual(compound.formula, test_string_value)
  def test_Compound_molar_mass_property(self):
    compound = Compound()
    test_val = test_double_value
    compound.molar_mass = test_val
    self.assertAlmostEqual(compound.molar_mass, test_val)
  def test_Compound_Compound_fuction(self):
    compound = Compound()

    phaseMap = string,Phase>()

    compound.Compound(test_string_value, phaseMap)
  def test_Compound_to_string_fuction(self):
    compound = Compound()


    compound.to_string()
  def test_Compound_get_phase_list_fuction(self):
    compound = Compound()


    compound.get_phase_list()
  def test_Compound_Cp_fuction(self):
    compound = Compound()


    compound.Cp(test_string_value, test_double_value)
  def test_Compound_H_fuction(self):
    compound = Compound()


    compound.H(test_string_value, test_double_value)
  def test_Compound_S_fuction(self):
    compound = Compound()


    compound.S(test_string_value, test_double_value)
  def test_Compound_G_fuction(self):
    compound = Compound()


    compound.G(test_string_value, test_double_value)




if __name__ == '__main__':
    unittest.main()
