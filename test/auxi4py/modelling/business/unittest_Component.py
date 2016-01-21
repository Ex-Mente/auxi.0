







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
#//    Component Unit Test
#//
#-----------------------------------------------
class Test_Component(unittest.TestCase):

  def test_Component_default_VariableGroupList_value(self):
    component = Component()
    self.assertEqual(len(component.variableGroupList), 0)
  def test_Component_default_ComponentList_value(self):
    component = Component()
    self.assertEqual(len(component.componentList), 0)
  def test_Component_default_ActivityList_value(self):
    component = Component()
    self.assertEqual(len(component.activityList), 0)
  def test_Component_default_path_value(self):
    component = Component()
    self.assertEqual(component.path, "")

  def test_Component_VariableGroupList_property(self):
    component = Component()
    test_val = VariableGroup()
    component.variableGroupList.append(test_val)
    self.assertEqual(component.variableGroupList[0], test_val)
  def test_Component_ComponentList_property(self):
    component = Component()
    test_val = Component()
    component.componentList.append(test_val)
    self.assertEqual(component.componentList[0], test_val)
  def test_Component_ActivityList_property(self):
    component = Component()
    test_val = Activity()
    component.activityList.append(test_val)
    self.assertEqual(component.activityList[0], test_val)
  def test_Component_path_property(self):
    component = Component()
    component.path = test_string_value
    self.assertEqual(component.path, test_string_value)
  def test_Component_create_component_fuction(self):
    component = Component()


    component.create_component(test_string_value)
  def test_Component_remove_component_fuction(self):
    component = Component()

    component = component.create_component(test_string_value)
    self.assertEqual(component.name, component.componentList[0].name)

    component.remove_component(test_string_value)
    self.assertEqual(len(component.componentList), 0)
  def test_Component_SetName_fuction(self):
    component = Component()


    component.SetName(test_string_value)
  def test_Component_set_path_fuction(self):
    component = Component()


    component.set_path(test_string_value)
  def test_Component_prepare_to_run_fuction(self):
    component = Component()

    clock = Clock()

    component.prepare_to_run(clock, test_int_value)
  def test_Component_run_fuction(self):
    component = Component()

    clock = Clock()
    generalLedger = GeneralLedger()

    component.run(clock, test_int_value, generalLedger)




if __name__ == '__main__':
    unittest.main()
