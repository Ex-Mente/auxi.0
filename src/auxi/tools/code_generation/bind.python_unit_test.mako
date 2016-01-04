## Helper Functions
<%!
import datetime

def is_ComplexClass(p, classes):
    isComplexClass = False
    for c in classes:
      if p.isList or p.type == c.name:
	isComplexClass = True
	break
    return isComplexClass

def is_Enum(p, enums):
    isEnum = False
    for e in enums:
      if p.type == e.name + "::" + e.name:
    	isEnum = True
    	break
    return isEnum

# Retrieves the class properties + its base class' properties
def getFullPropertyList(c):
  propertyList = []
  propertyList.extend(c.properties)
  if not(c.baseClass == None):
    propertyList.extend(c.baseClass.properties)
  return propertyList

def getPythonFriendlyName(name):
    if name == "yield": return "yieldAmount"
    return name

def getPythonTypeName(name):
    result = name.split("::")[-1]
    if result == "double":
        return "float"
    if result[-1] == "*":
        return result[:-1]
    if name[:12] == "std::vector<":
        result = result.replace("*", "").replace(">", "")
        result = result + "List"
    return result
%>
<% namespace_decl = "" %>
% for ns in namespace_parts:
<% namespace_decl += ns + "." %>
% endfor
<% namespace_decl = namespace_decl[:-1] %>


import sys
import datetime
from ${namespace_decl} import *
import unittest

test_string_value = "Test"
test_int_value = 3
test_double_value = 5.3
test_datetime_value = datetime.datetime.strptime("2015-02-17 13:37:01", "%Y-%m-%d %H:%M:%S")

% for c in classes:
#-----------------------------------------------
#//
#//    ${c.name} Unit Test
#//
#-----------------------------------------------
class Test_${c.name}(unittest.TestCase):

  #############################
  ## Test the default values ##
  #############################
  % for p in getFullPropertyList(c):
    % if p.private == "true" or (p.set == "false" and p.get == "false"):
<% continue %>
    % endif
  def test_${c.name}_default_${p.name}_value(self):
    ${c.namelower} = ${c.name}()
    % if p.isList:
    self.assertEqual(len(${c.namelower}.${getPythonFriendlyName(p.namelower)}), 0)
    % elif is_ComplexClass(p, classes) or (p.default == None and not(p.name=="IsValid")):
      % if p.type == "std::string":
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, "")
      % elif p.type == "boost::posix_time::ptime":
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, "${datetime.datetime.min}")
      % elif p.type in ["double", "float"]:
    self.assertAlmostEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, ${getPythonTypeName(p.type)}())
      % else:
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, ${getPythonTypeName(p.type)}())
      % endif
    % elif is_Enum(p, enums):
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, ${p.type[0:p.type.find("::")]}.${p.default})
    % elif not(p.name=="Name") and not(p.name=="Description"):
      % if p.type == "bool":
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, ${p.default[0].upper() + p.default[1:]})
      % elif p.type == "boost::posix_time::ptime":
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, datetime.datetime.strptime("${p.default}", "%Y-%m-%d %H:%M:%S"))
      % else:
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, ${p.default})
      % endif
    % endif
  % endfor

  #############################
  ##   Test the properties   ##
  #############################
  % for p in getFullPropertyList(c):
% if p.private == "true" or (p.set == "false" and p.get == "false"):
<% continue %>
% endif
  def test_${c.name}_${p.name}_property(self):
    ${c.namelower} = ${c.name}()
    ##
    ## List
    ##
    % if p.isList:
    test_val = ${getPythonTypeName(p.listItemType)}()
    ${c.namelower}.${getPythonFriendlyName(p.namelower)}.append(test_val)
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}[0], test_val)
    ##
    ## Complex Class
    ##
    % elif is_ComplexClass(p, classes):
    test_val = ${p.type}()
    ${c.namelower}.${getPythonFriendlyName(p.namelower)} = test_val
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, test_val);
    ##
    ## Enum
    ##
    % elif is_Enum(p, enums):
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, ${p.type[0:p.type.find("::")]}.${p.default})
    ##
    ## Simple Types
    ##
    % else:
      % if p.type == "std::string":
    ${c.namelower}.${getPythonFriendlyName(p.namelower)} = test_string_value
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, test_string_value)
      % elif p.type == "int":
        % if p.default is None:
    test_val = test_int_value
        % else:
    test_val = ${p.default} + test_int_value
        % endif
    ${c.namelower}.${getPythonFriendlyName(p.namelower)} = test_val
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, test_val)
      % elif p.type == "double":
        % if p.default is None:
    test_val = test_double_value
        % else:
    test_val = ${p.default} + test_double_value
        % endif
    ${c.namelower}.${getPythonFriendlyName(p.namelower)} = test_val
    self.assertAlmostEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, test_val)
      % elif p.type == "boost::posix_time::ptime":
    ${c.namelower}.${getPythonFriendlyName(p.namelower)} = test_datetime_value
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, test_datetime_value)
      % elif p.type == "bool":
    test_val = not(${ p.default[0].upper() + p.default[1:]})
    ${c.namelower}.${getPythonFriendlyName(p.namelower)} = test_val
    self.assertEqual(${c.namelower}.${getPythonFriendlyName(p.namelower)}, test_val)
      % endif
    % endif
  % endfor
  #############################
  ##   Test the functions    ##
  #############################
  % for f in c.functions:
    % if f.private == "true":
<% continue %>
    % endif
  def test_${c.name}_${f.name}_fuction(self):
    ${c.namelower} = ${c.name}()
<%
func_test_code = c.namelower + "." + f.name + "("
func_test_vars = ""
if len(f.params) > 0:
  for pm in f.params:
    if pm[1] in ["string","std::string"]:
      func_test_code = func_test_code + "test_string_value, "
    elif pm[1] == "int":
      func_test_code = func_test_code + "test_int_value, "
    elif pm[1] == "double":
      func_test_code = func_test_code + "test_double_value, "
    elif pm[1] == "boost::posix_time::ptime":
      func_test_code = func_test_code + "test_datetime_value, "
    elif pm[1] == "bool":
      func_test_code = func_test_code + "test_bool_value, "
    else:
      func_test_vars = func_test_vars + "    " + pm[0] + " = " + getPythonTypeName(pm[1]) + "()\n"
      func_test_code = func_test_code + pm[0] + ", "
  func_test_code = func_test_code[:-2]
func_test_code = func_test_code + ")"
%>
% if f.name[0:7] == "remove_" and f.name[7].upper() + f.name[8:] + "List" in [p.name for p in getFullPropertyList(c)]:
    ${f.name[7:]} = ${c.namelower}.create_${f.name[7:]}(test_string_value)
    self.assertEqual(${f.name[7:]}.name, ${c.namelower + "." + f.name[7:] + "List[0].name"})
${func_test_vars}
    ${func_test_code}
    self.assertEqual(len(${c.namelower + "." + f.name[7:] + "List"}), 0)
% else:
${func_test_vars}
    ${func_test_code}
% endif
    % endfor

% endfor



if __name__ == '__main__':
    unittest.main()
