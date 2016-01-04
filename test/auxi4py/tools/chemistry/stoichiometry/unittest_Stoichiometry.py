







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
#//    Stoichiometry Unit Test
#//
#-----------------------------------------------
class Test_Stoichiometry(unittest.TestCase):


  def test_Stoichiometry_amount_fuction(self):
    stoichiometry = Stoichiometry()


    stoichiometry.amount(test_string_value, test_double_value)
  def test_Stoichiometry_mass_fuction(self):
    stoichiometry = Stoichiometry()


    stoichiometry.mass(test_string_value, test_double_value)
  def test_Stoichiometry_convert_compound_fuction(self):
    stoichiometry = Stoichiometry()


    stoichiometry.convert_compound(test_double_value, test_string_value, test_string_value, test_string_value)
  def test_Stoichiometry_element_mass_fraction_fuction(self):
    stoichiometry = Stoichiometry()


    stoichiometry.element_mass_fraction(test_string_value, test_string_value)
  def test_Stoichiometry_element_mass_fractions_fuction(self):
    stoichiometry = Stoichiometry()

    elements = stringList()

    stoichiometry.element_mass_fractions(test_string_value, elements)
  def test_Stoichiometry_elements_fuction(self):
    stoichiometry = Stoichiometry()

    compounds = stringList()

    stoichiometry.elements(compounds)
  def test_Stoichiometry_molar_mass_fuction(self):
    stoichiometry = Stoichiometry()


    stoichiometry.molar_mass(test_string_value)
  def test_Stoichiometry_stoichiometry_coefficient_fuction(self):
    stoichiometry = Stoichiometry()


    stoichiometry.stoichiometry_coefficient(test_string_value, test_string_value)
  def test_Stoichiometry_stoichiometry_coefficients_fuction(self):
    stoichiometry = Stoichiometry()

    elements = stringList()

    stoichiometry.stoichiometry_coefficients(test_string_value, elements)




if __name__ == '__main__':
    unittest.main()
