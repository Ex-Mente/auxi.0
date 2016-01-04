







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
#//    Thermochemistry Unit Test
#//
#-----------------------------------------------
class Test_Thermochemistry(unittest.TestCase):

  def test_Thermochemistry_default_CompoundDict_value(self):
    thermochemistry = Thermochemistry()
    self.assertEqual(len(thermochemistry.compoundDict), 0)

  def test_Thermochemistry_CompoundDict_property(self):
    thermochemistry = Thermochemistry()
    test_val = string, Compound()
    thermochemistry.compoundDict.append(test_val)
    self.assertEqual(thermochemistry.compoundDict[0], test_val)
  def test_Thermochemistry_get_default_data_path_fuction(self):
    thermochemistry = Thermochemistry()


    thermochemistry.get_default_data_path()
  def test_Thermochemistry_set_default_data_path_fuction(self):
    thermochemistry = Thermochemistry()


    thermochemistry.set_default_data_path(test_string_value)
  def test_Thermochemistry_convert_fact_file_to_auxi_thermo_file_fuction(self):
    thermochemistry = Thermochemistry()


    thermochemistry.convert_fact_file_to_auxi_thermo_file(test_string_value, test_string_value)
  def test_Thermochemistry_load_data_fuction(self):
    thermochemistry = Thermochemistry()


    thermochemistry.load_data(test_string_value)
  def test_Thermochemistry_list_compounds_fuction(self):
    thermochemistry = Thermochemistry()


    thermochemistry.list_compounds()
  def test_Thermochemistry_molar_mass_fuction(self):
    thermochemistry = Thermochemistry()


    thermochemistry.molar_mass(test_string_value)
  def test_Thermochemistry_Cp_fuction(self):
    thermochemistry = Thermochemistry()


    thermochemistry.Cp(test_string_value, test_double_value, test_double_value)
  def test_Thermochemistry_H_fuction(self):
    thermochemistry = Thermochemistry()


    thermochemistry.H(test_string_value, test_double_value, test_double_value)
  def test_Thermochemistry_S_fuction(self):
    thermochemistry = Thermochemistry()


    thermochemistry.S(test_string_value, test_double_value, test_double_value)
  def test_Thermochemistry_G_fuction(self):
    thermochemistry = Thermochemistry()


    thermochemistry.G(test_string_value, test_double_value, test_double_value)




if __name__ == '__main__':
    unittest.main()
