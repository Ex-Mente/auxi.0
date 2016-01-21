







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
#//    Entity Unit Test
#//
#-----------------------------------------------
class Test_Entity(unittest.TestCase):

  def test_Entity_default_VariableGroupList_value(self):
    entity = Entity()
    self.assertEqual(len(entity.variableGroupList), 0)
  def test_Entity_default_ComponentList_value(self):
    entity = Entity()
    self.assertEqual(len(entity.componentList), 0)
  def test_Entity_default_TaxRuleSet_value(self):
    entity = Entity()
    self.assertEqual(entity.taxRuleSet, RuleSet())
  def test_Entity_default_NegativeIncomeTaxTotal_value(self):
    entity = Entity()
    self.assertAlmostEqual(entity.negativeIncomeTaxTotal, float())
  def test_Entity_default_PeriodCount_value(self):
    entity = Entity()
    self.assertEqual(entity.periodCount, int())
  def test_Entity_default_Gl_value(self):
    entity = Entity()
    self.assertEqual(entity.gl, GeneralLedger())

  def test_Entity_VariableGroupList_property(self):
    entity = Entity()
    test_val = VariableGroup()
    entity.variableGroupList.append(test_val)
    self.assertEqual(entity.variableGroupList[0], test_val)
  def test_Entity_ComponentList_property(self):
    entity = Entity()
    test_val = Component()
    entity.componentList.append(test_val)
    self.assertEqual(entity.componentList[0], test_val)
  def test_Entity_TaxRuleSet_property(self):
    entity = Entity()
  def test_Entity_NegativeIncomeTaxTotal_property(self):
    entity = Entity()
    test_val = test_double_value
    entity.negativeIncomeTaxTotal = test_val
    self.assertAlmostEqual(entity.negativeIncomeTaxTotal, test_val)
  def test_Entity_PeriodCount_property(self):
    entity = Entity()
    test_val = test_int_value
    entity.periodCount = test_val
    self.assertEqual(entity.periodCount, test_val)
  def test_Entity_Gl_property(self):
    entity = Entity()
  def test_Entity_create_component_fuction(self):
    entity = Entity()


    entity.create_component(test_string_value)
  def test_Entity_remove_component_fuction(self):
    entity = Entity()

    component = entity.create_component(test_string_value)
    self.assertEqual(component.name, entity.componentList[0].name)

    entity.remove_component(test_string_value)
    self.assertEqual(len(entity.componentList), 0)
  def test_Entity_prepare_to_run_fuction(self):
    entity = Entity()

    clock = Clock()

    entity.prepare_to_run(clock, test_int_value)
  def test_Entity_run_fuction(self):
    entity = Entity()

    clock = Clock()
    currency = Units()

    entity.run(clock, test_int_value, currency)




if __name__ == '__main__':
    unittest.main()
