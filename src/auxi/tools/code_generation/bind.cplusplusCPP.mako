#include "${filename}.h"
#include <boost/lexical_cast.hpp>
#include <iostream>
#include <cmath>
#include <limits>

## Helper Functions
<%!
def is_ComplexClass(p, classes, namespace_name):
    isComplexClass = False
    for c in classes:
      if p.type == c.name:
	return True
    for i in c.additional_includes:
      namespaceless_type = p.type.split("::")[-1:][0]
      if i in [p.type, namespaceless_type]:
	return True
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
%>
<%
namespace_decl = ""
namespace_end = ""
isNamespaceCount = 0
for ns in namespace_parts:
    namespace_decl += "namespace " + ns + " { "
    namespace_end += "}"
%>
% for c in classes:
    % if c.isNamespace == 'true':
        <% isNamespaceCount = isNamespaceCount + 1 %>
${namespace_decl}namespace ${c.name[:1].lower() + c.name[1:]} {
##/////////////////// NAMESPACE ${c.name} ///////////////////
//// Properties ////
% for p in c.properties:
  % if not(p.name=="Name") and not(p.name=="Description"):
    % if p.default is None:
${p.type} m_${p.namelower};
    % elif is_Enum(p, enums):
${p.type} m_${p.namelower} = ${p.type}::${p.default};
    % else:
      % if p.type == "boost::posix_time::ptime":
${p.type} m_${p.namelower} = boost::posix_time::time_from_string("${p.default}");
      % elif p.type == "std::string":
${p.type} m_${p.namelower} = "${p.default}";
      % else:
${p.type} m_${p.namelower} = ${p.default};
      % endif
    % endif
    % if p.optional:
bool m_${p.namelower}Specified = false;
    % endif
  % endif
% endfor


% for p in c.properties:
% if p.private == "true":
<% continue %>
% endif
###
% if p.isList and not p.get in ["custom", "false"]:
${p.type}& Get${p.name}() { return m_${p.namelower}; }
% endif
###
% if not p.isList:
  % if is_ComplexClass(p, classes, namespace_name):
    % if not p.get in ["custom", "false"]:
${p.type}& Get${p.name}() { return m_${p.namelower}; }
    % endif
    % if not p.set in ["custom", "false"]:
void Set${p.name}(${p.type}& value) { m_${p.namelower} = value; }
    % endif
  % else:
    % if not p.get in ["custom", "false"]:
${p.type} Get${p.name}() { return m_${p.namelower}; }
    % endif
    % if not p.set in ["custom", "false"]:
void Set${p.name}(${p.type} value) { m_${p.namelower} = value; }
    % endif
  % endif
% endif
###
% if p.optional:
bool Get${p.name}Specified() { return m_${p.namelower}Specified; }
void Set${p.name}Specified(bool value) { m_${p.namelower} = value; }
% endif
###
% endfor
##///////////////////////////////////////////////////////////
${namespace_end}}
    % endif
% endfor
% if isNamespaceCount != len(classes):
using namespace ${namespace_name};

% for c in classes:
% if c.baseClassName != "Object":
${c.name}::${c.name}()
{
    //ctor
    % if c.constructor_init_function not in [None, ""]:
    ${c.constructor_init_function}();
    % endif
}
% endif

${c.name}::${c.name}(const ${c.name}& other)
{
    % for p in getFullPropertyList(c):
      % if not(p.name=="Name") and not(p.name=="Description"):
    m_${p.namelower} = other.m_${p.namelower};
      % endif
    % endfor
}

${c.name}::~${c.name}()
{

    % if c.destructor_clean_function not in [None, ""]:
    ${c.destructor_clean_function}();
    % endif
}

% for p in c.properties:
% if p.private == "true":
<% continue %>
% endif
###
% if p.isList and not p.get in ["custom", "false"]:
${p.type}& ${c.name}::Get${p.name}() { return m_${p.namelower}; }
% endif
###
% if not p.isList:
  % if is_ComplexClass(p, classes, namespace_name):
    % if not p.get in ["custom", "false"]:
${p.type}& ${c.name}::Get${p.name}() { return m_${p.namelower}; }
    % endif
    % if not p.set in ["custom", "false"]:
void ${c.name}::Set${p.name}(${p.type}& value) { m_${p.namelower} = value; }
    % endif
  % else:
    % if not p.get in ["custom", "false"]:
${p.type} ${c.name}::Get${p.name}() const { return m_${p.namelower}; }
    % endif
    % if not p.set in ["custom", "false"]:
void ${c.name}::Set${p.name}(${p.type} value) { m_${p.namelower} = value; }
    % endif
  % endif
% endif
###
% if p.optional:
bool ${c.name}::Get${p.name}Specified() const { return m_${p.namelower}Specified; }
void ${c.name}::Set${p.name}Specified(bool value) { m_${p.namelower} = value; }
% endif
###
% endfor

<%
    namespace_decl = ""
%>
% for ns in namespace_parts:
    <%
        namespace_decl += "namespace " + ns + " { "
    %>
% endfor
${namespace_decl}
    bool operator==(const ${c.name}& lhs, const ${c.name}& rhs)
    {
        return 1 == 1
	% for p in getFullPropertyList(c):
	  % if p.type == "double":
	  && almost_equal(lhs.m_${p.namelower}, rhs.m_${p.namelower}, 5)
	  % elif not(p.name=="Name") and not(p.name=="Description"):
	  && lhs.m_${p.namelower} == rhs.m_${p.namelower}
	  % endif
	% endfor
	  ;
    }

    bool operator!=(const ${c.name}& lhs, const ${c.name}& rhs)
    {
        return 1 != 1
	% for p in getFullPropertyList(c):
	  % if p.type == "double":
	  || !almost_equal(lhs.m_${p.namelower}, rhs.m_${p.namelower}, 5)
	  % elif not(p.name=="Name") and not(p.name=="Description"):
	  || lhs.m_${p.namelower} != rhs.m_${p.namelower}
	  % endif
	% endfor
	;
    }

    std::ostream& operator<<(std::ostream& os, const ${c.name}& obj)
    {

% if c.baseClassName == "Object":
        os << "A ${c.name} instance.";
% else:
        os << obj.GetName();
% endif
        return os;
    }
% for ns in namespace_parts:
}
% endfor
% endfor
% endif